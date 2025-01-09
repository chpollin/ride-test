#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from lxml import etree

def process_paragraph(pnode, ns):
    """
    Recursively convert a TEI <p> node into HTML text,
    handling <ref>, <note>, <emph>, etc.
    """
    para_content = ""
    # Text before any child
    if pnode.text:
        para_content += pnode.text

    for child in pnode:
        tag = etree.QName(child)
        if tag.localname == 'ref':
            url = child.get('target', '#')
            link_text = (child.text or '').strip()
            para_content += f'<a href="{url}" target="_blank">{link_text}</a>'
            if child.tail:
                para_content += child.tail
        elif tag.localname == 'note':
            note_text = child.xpath('string(.)').strip()
            para_content += f'<span class="note">[{note_text}]</span>'
            if child.tail:
                para_content += child.tail
        elif tag.localname == 'emph':
            em_text = child.xpath('string(.)').strip()
            para_content += f'<em>{em_text}</em>'
            if child.tail:
                para_content += child.tail
        else:
            # Flatten text for unknown tags or handle more specifically
            text_in_child = child.xpath('string(.)')
            para_content += text_in_child
            if child.tail:
                para_content += child.tail

    return f"<p>{para_content.strip()}</p>\n"


def transform_tei_to_html(xml_path: str) -> str:
    """
    Parse the TEI XML at `xml_path` and return a string with 
    the transformed HTML (Bootstrap 5).
    """
    tree = etree.parse(xml_path)
    root = tree.getroot()
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # -----------------------------------------------------------------------
    # 1) Extract Data from teiHeader
    # -----------------------------------------------------------------------
    title_elt = root.xpath('.//tei:teiHeader//tei:titleStmt/tei:title', namespaces=ns)
    doc_title = title_elt[0].text if title_elt else "Untitled Document"

    pub_el = root.xpath('.//tei:teiHeader//tei:fileDesc//tei:publicationStmt/tei:publisher', namespaces=ns)
    publisher = pub_el[0].text if pub_el else ""
    date_el = root.xpath('.//tei:teiHeader//tei:fileDesc//tei:publicationStmt/tei:date', namespaces=ns)
    pub_date = date_el[0].text if date_el else ""
    idno_el = root.xpath('.//tei:teiHeader//tei:fileDesc//tei:publicationStmt/tei:idno', namespaces=ns)
    idno = idno_el[0].text if idno_el else ""

    # -----------------------------------------------------------------------
    # 2) Extract <front> content (Abstract, etc.)
    # -----------------------------------------------------------------------
    front_abstract = ""
    front_divs = root.xpath('.//tei:text//tei:front/tei:div', namespaces=ns)
    for fdiv in front_divs:
        if fdiv.get("type") == "abstract":
            p_nodes = fdiv.xpath('.//tei:p', namespaces=ns)
            for p in p_nodes:
                txt = p.xpath('string(.)').strip()
                front_abstract += f"<p>{txt}</p>\n"

    # -----------------------------------------------------------------------
    # 3) Extract <body> content (div/head/p)
    # -----------------------------------------------------------------------
    body_html = ""
    body_divs = root.xpath('.//tei:text//tei:body/tei:div', namespaces=ns)

    for div in body_divs:
        div_id = div.get('{http://www.w3.org/XML/1998/namespace}id', '')
        head_nodes = div.xpath('./tei:head', namespaces=ns)
        section_title = head_nodes[0].text if head_nodes and head_nodes[0].text else "Section"
        body_html += f'<section id="{div_id}">\n'
        body_html += f'  <h3 class="h5">{section_title}</h3>\n'

        p_nodes = div.xpath('./tei:p', namespaces=ns)
        for pnode in p_nodes:
            para_html = process_paragraph(pnode, ns)
            body_html += para_html

        body_html += "</section>\n\n"

    # -----------------------------------------------------------------------
    # 4) Handle <figure> elements (with <graphic> + <head type="legend">)
    # -----------------------------------------------------------------------
    figure_nodes = root.xpath('.//tei:text//tei:body//tei:figure', namespaces=ns)
    figure_html = ""
    for figure in figure_nodes:
        fig_id = figure.get('{http://www.w3.org/XML/1998/namespace}id', '')
        graphic_el = figure.xpath('.//tei:graphic', namespaces=ns)
        legend_el = figure.xpath('./tei:head[@type="legend"]', namespaces=ns)
        fig_legend = legend_el[0].text if (legend_el and legend_el[0].text) else "Figure"

        if graphic_el:
            image_url = graphic_el[0].get('url', '')
            local_image_name = os.path.basename(image_url)
            figure_html += (
                f'<figure id="{fig_id}" class="mb-4">\n'
                f'  <img src="pictures/{local_image_name}" alt="{fig_legend}" class="img-fluid"/>\n'
                f'  <figcaption>{fig_legend}</figcaption>\n'
                f'</figure>\n'
            )

    # For simplicity, append figures at the bottom:
    body_html += figure_html

    # -----------------------------------------------------------------------
    # 5) Build final HTML
    # -----------------------------------------------------------------------
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{doc_title}</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  <!-- Reference to external style.css (not generated here) -->
  <link href="style.css" rel="stylesheet">
</head>
<body>
  <!-- Header Section -->
  <header class="bg-light py-3 border-bottom">
    <div class="container d-flex justify-content-between align-items-center">
      <div class="d-flex align-items-center">
        <img src="logo.png" alt="RIDE Logo" class="me-3" style="width: 50px; height: auto;">
        <h1 class="h4 mb-0">RIDE</h1>
      </div>
      <nav>
        <ul class="nav">
          <li class="nav-item"><a class="nav-link active" href="#">About</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Issues</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Data</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Reviewers</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Reviewing Criteria</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <!-- Main Content -->
  <div class="container my-4">
    <div class="row">
      <!-- Main Article Column -->
      <div class="col-md-8">
        <!-- Title Section -->
        <section class="mb-4">
          <h2 class="h2">{doc_title}</h2>
          <p class="text-muted">
             {publisher}, {pub_date} {f'({idno})' if idno else ''}
          </p>
          <hr>
        </section>

        <!-- Abstract Section -->
        <section id="abstract" class="mb-4">
          <h3 class="h5">Abstract</h3>
          {front_abstract}
        </section>

        <!-- Body Content -->
        {body_html}
      </div>

      <!-- Sidebar -->
      <aside class="col-md-4">
        <!-- Meta Information -->
        <section class="mb-4">
          <h4 class="h6">Meta</h4>
          <ul class="list-unstyled">
            <li><strong>Published:</strong> {pub_date}</li>
            <li><strong>Publisher:</strong> {publisher}</li>
          </ul>
        </section>

        <!-- Example Tags -->
        <section class="mb-4">
          <h4 class="h6">Tags</h4>
          <div class="d-flex flex-wrap gap-2">
            <span class="badge bg-secondary">18th century</span>
            <span class="badge bg-secondary">Account books</span>
            <span class="badge bg-secondary">Digital edition</span>
          </div>
        </section>

        <!-- Simple TOC (just linking to the first body div) -->
        <section>
          <h4 class="h6">TOC</h4>
          <ul class="list-unstyled">
            <li><a href="#abstract">Abstract</a></li>
            <li><a href="#{body_divs[0].get('{http://www.w3.org/XML/1998/namespace}id') if body_divs else ''}">Introduction</a></li>
          </ul>
        </section>
      </aside>
    </div>
  </div>

  <!-- Footer -->
  <footer class="bg-dark text-light py-3 mt-5">
    <div class="container text-center">
      <p>&copy; 2023 RIDE Journal. All rights reserved.</p>
    </div>
  </footer>

  <!-- Bootstrap JS -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
  <!-- Optional external JS reference -->
  <script src="app.js"></script>
</body>
</html>
"""
    return html_template


def main():
    base_folder = "issue18"
    web_folder = "web"

    # Ensure "web" folder exists
    if not os.path.exists(web_folder):
        os.makedirs(web_folder)

    created_html_files = []  # Store (filename, title) for index generation

    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if not os.path.isdir(folder_path):
            continue  # skip if not a directory

        # Example: <folder_name>-tei.xml
        tei_file_name = f"{folder_name}-tei.xml"
        tei_file_path = os.path.join(folder_path, tei_file_name)
        if not os.path.isfile(tei_file_path):
            continue  # skip if TEI doesn't exist

        # Transform TEI to HTML
        html_output = transform_tei_to_html(tei_file_path)

        # Write the resulting .html to /web/<folder_name>.html
        output_html_name = f"{folder_name}.html"
        output_html_path = os.path.join(web_folder, output_html_name)
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html_output)

        print(f"Created HTML: {output_html_path}")
        # We can store the folder_name or glean the <title> from the doc
        # For the index, let's parse out the doc title if we want:
        doc_title = get_title_from_html(html_output) or folder_name
        created_html_files.append((output_html_name, doc_title))

    # -----------------------------------------------------------------------
    # Create index.html in "web" folder with links to all pages
    # -----------------------------------------------------------------------
    index_content = build_index_html(created_html_files)
    index_path = os.path.join(web_folder, "index.html")
    with open(index_path, "w", encoding="utf-8") as idx:
        idx.write(index_content)

    print(f"Created index: {index_path}")


def get_title_from_html(html_text: str) -> str:
    """A quick function to read the <title> from the generated HTML."""
    # This is a simple approach; you could parse again with lxml or use a regex.
    start_tag = "<title>"
    end_tag = "</title>"
    start_idx = html_text.find(start_tag)
    end_idx = html_text.find(end_tag)
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        start_idx += len(start_tag)
        return html_text[start_idx:end_idx].strip()
    return None


def build_index_html(created_files):
    """
    Build a minimal HTML index listing the generated pages.
    """
    # We can create a simple bootstrap-based index
    items = ""
    for filename, title in created_files:
        items += f'<li class="mb-2"><a href="{filename}">{title}</a></li>\n'

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>RIDE Issue 18 Index</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="style.css" rel="stylesheet">
</head>
<body>
<div class="container my-5">
  <h1>RIDE Issue 18 – Index</h1>
  <p>This page links to all automatically generated HTML pages.</p>
  <ul class="list-unstyled">
    {items}
  </ul>
</div>
</body>
</html>
"""
    return index_html


if __name__ == "__main__":
    main()
