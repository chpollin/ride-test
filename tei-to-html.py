#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from lxml import etree

def main():
    data_folder = "data"
    web_folder = "web"

    # Ensure the "web" folder exists
    if not os.path.exists(web_folder):
        os.makedirs(web_folder)

    # We'll store a mapping from issueName -> list of (title, filename)
    # so that we can create a dropdown with all subpages
    issues_index = {}

    # -------------------------------------------------------------------------
    # 1) Find directories named "issueXX" in data/
    # -------------------------------------------------------------------------
    for item in os.listdir(data_folder):
        issue_dir_path = os.path.join(data_folder, item)
        if not os.path.isdir(issue_dir_path):
            continue
        if not item.startswith("issue"):  
            # Skip directories that are not named "issueXX"
            continue
        
        # We'll build a corresponding output folder in web/issueXX
        output_issue_folder = os.path.join(web_folder, item)
        if not os.path.exists(output_issue_folder):
            os.makedirs(output_issue_folder)
        
        # This issue's name is something like "issue18"
        issue_name = item
        issues_index[issue_name] = []

        # ---------------------------------------------------------------------
        # 2) Within each issue directory, parse subfolders
        # ---------------------------------------------------------------------
        for subfolder in os.listdir(issue_dir_path):
            subfolder_path = os.path.join(issue_dir_path, subfolder)
            if not os.path.isdir(subfolder_path):
                continue

            # We expect a TEI file named <subfolder>-tei.xml
            tei_filename = f"{subfolder}-tei.xml"
            tei_file_path = os.path.join(subfolder_path, tei_filename)

            if os.path.isfile(tei_file_path):
                # Parse & transform
                html_string = transform_tei_to_html(
                    tei_file_path, 
                    issue_name, 
                    subfolder
                )
                # Save as web/issueXX/<subfolder>.html
                output_html_path = os.path.join(output_issue_folder, f"{subfolder}.html")
                with open(output_html_path, "w", encoding="utf-8") as outf:
                    outf.write(html_string)

                # Read out the doc <title> from the generated HTML
                doc_title = get_title_from_html(html_string) or subfolder

                # Store for building our index
                # The relative path from web/index.html to web/issueXX/<subfolder>.html 
                # is just f"{issue_name}/{subfolder}.html"
                rel_path = f"{issue_name}/{subfolder}.html"
                issues_index[issue_name].append((doc_title, rel_path))

                print(f"Created: {output_html_path}")
    
    # -------------------------------------------------------------------------
    # 3) Create a global index.html in "web/" with a top nav and an Issues dropdown
    # -------------------------------------------------------------------------
    index_html = build_index_html(issues_index)
    index_path = os.path.join(web_folder, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"Created index: {index_path}")


def transform_tei_to_html(tei_file_path, issue_name, subfolder_name):
    """
    Parse the TEI file and return a single string of the HTML
    with references to images like ../../data/issueXX/subfolder/pictures/*.png
    """
    tree = etree.parse(tei_file_path)
    root = tree.getroot()
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # 1) Get doc title, publisher, date, idno from teiHeader
    title_elt = root.xpath('.//tei:teiHeader//tei:titleStmt/tei:title', namespaces=ns)
    doc_title = title_elt[0].text.strip() if title_elt else "Untitled Document"

    pub_el = root.xpath('.//tei:teiHeader//tei:fileDesc//tei:publicationStmt/tei:publisher', namespaces=ns)
    publisher = pub_el[0].text.strip() if pub_el else ""

    date_el = root.xpath('.//tei:teiHeader//tei:fileDesc//tei:publicationStmt/tei:date', namespaces=ns)
    pub_date = date_el[0].text.strip() if date_el else ""

    idno_el = root.xpath('.//tei:teiHeader//tei:fileDesc//tei:publicationStmt/tei:idno', namespaces=ns)
    idno = idno_el[0].text.strip() if idno_el else ""

    # 2) front -> abstract
    front_abstract = ""
    front_divs = root.xpath('.//tei:text//tei:front/tei:div', namespaces=ns)
    for fdiv in front_divs:
        if fdiv.get("type") == "abstract":
            p_nodes = fdiv.xpath('.//tei:p', namespaces=ns)
            for p in p_nodes:
                txt = p.xpath('string(.)').strip()
                if txt:
                    front_abstract += f"<p>{txt}</p>\n"

    # 3) body -> div, head, p
    body_html = ""
    body_divs = root.xpath('.//tei:text//tei:body/tei:div', namespaces=ns)

    for div in body_divs:
        div_id = div.get('{http://www.w3.org/XML/1998/namespace}id', '')
        head_nodes = div.xpath('./tei:head', namespaces=ns)
        section_title = head_nodes[0].text.strip() if head_nodes and head_nodes[0].text else "Section"

        body_html += f'<section id="{div_id}">\n'
        body_html += f'  <h3 class="h5">{section_title}</h3>\n'

        p_nodes = div.xpath('./tei:p', namespaces=ns)
        for pnode in p_nodes:
            para_html = process_paragraph(pnode, ns)
            body_html += para_html

        body_html += "</section>\n\n"

    # 4) figures
    # We'll do a simple pass for all <figure> in <body>
    figure_nodes = root.xpath('.//tei:text//tei:body//tei:figure', namespaces=ns)
    figure_html = ""
    for figure in figure_nodes:
        fig_id = figure.get('{http://www.w3.org/XML/1998/namespace}id', '')
        graphic_el = figure.xpath('.//tei:graphic', namespaces=ns)
        legend_el = figure.xpath('./tei:head[@type="legend"]', namespaces=ns)
        fig_legend = legend_el[0].text.strip() if (legend_el and legend_el[0].text) else "Figure"

        if graphic_el:
            image_url = graphic_el[0].get('url', '')
            # We want a relative path like ../../data/issueXX/subfolder/pictures/xxx
            # Extract the base name of the image
            image_name = os.path.basename(image_url)
            rel_path = f"../../data/{issue_name}/{subfolder_name}/pictures/{image_name}"

            figure_html += (
                f'<figure id="{fig_id}" class="mb-4">\n'
                f'  <img src="{rel_path}" alt="{fig_legend}" class="img-fluid"/>\n'
                f'  <figcaption>{fig_legend}</figcaption>\n'
                f'</figure>\n'
            )

    body_html += figure_html

    # 5) Build final HTML
    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{doc_title}</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  <!-- style.css (pre-existing, not generated here) -->
  <link href="../style.css" rel="stylesheet">
</head>
<body>
  <!-- Header Section -->
  <header class="bg-light py-3 border-bottom">
    <div class="container d-flex justify-content-between align-items-center">
      <div class="d-flex align-items-center">
        <img src="../logo.png" alt="RIDE Logo" class="me-3" style="width: 50px; height: auto;">
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
        <section class="mb-4">
          <h4 class="h6">Meta</h4>
          <ul class="list-unstyled">
            <li><strong>Published:</strong> {pub_date}</li>
            <li><strong>Publisher:</strong> {publisher}</li>
          </ul>
        </section>

        <section class="mb-4">
          <h4 class="h6">Tags</h4>
          <div class="d-flex flex-wrap gap-2">
            <span class="badge bg-secondary">18th century</span>
            <span class="badge bg-secondary">Account books</span>
            <span class="badge bg-secondary">Digital edition</span>
          </div>
        </section>

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
</body>
</html>
"""
    return html_out


def process_paragraph(pnode, ns):
    """
    Convert a TEI <p> node into HTML, handling child elements (<ref>, <note>, <emph>, etc.)
    """
    para_content = ""
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
            # Default: just flatten text
            text_in_child = child.xpath('string(.)')
            para_content += text_in_child
            if child.tail:
                para_content += child.tail

    return f"<p>{para_content.strip()}</p>\n"


def get_title_from_html(html_text):
    """
    Extract the <title> from the generated HTML.
    """
    start_tag = "<title>"
    end_tag = "</title>"
    sidx = html_text.find(start_tag)
    eidx = html_text.find(end_tag)
    if sidx != -1 and eidx != -1 and eidx > sidx:
        sidx += len(start_tag)
        return html_text[sidx:eidx].strip()
    return None


def build_index_html(issues_index):
    """
    Creates one index.html with a top nav bar that has an Issues dropdown.
    Each issue links to the subpages that were created.
    issues_index is a dict:
      {
        'issue17': [(title1, 'issue17/page1.html'), (title2, 'issue17/page2.html')],
        'issue18': [...],
        ...
      }
    """
    # Build the drop-down <li> for each issue
    issues_nav_html = ""
    for issue_name, pages in issues_index.items():
        # We'll create a dropdown item for each page
        # If you want a sub-dropdown, you can do that, but let's keep it simple:
        items = ""
        for (title, rel_path) in pages:
            items += f'<li><a class="dropdown-item" href="{rel_path}">{title}</a></li>\n'

        if not items:
            # If no pages, skip
            continue

        issues_nav_html += f"""
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="{issue_name}Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            {issue_name.capitalize()}
          </a>
          <ul class="dropdown-menu" aria-labelledby="{issue_name}Dropdown">
            {items}
          </ul>
        </li>
        """

    # Create the main content for the index
    body_content = ""
    for issue_name, pages in issues_index.items():
        if len(pages) == 0:
            continue
        body_content += f"<h2>{issue_name.capitalize()}</h2>\n<ul>\n"
        for (title, rel_path) in pages:
            body_content += f'  <li><a href="{rel_path}">{title}</a></li>\n'
        body_content += "</ul>\n\n"

    # Full index
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>RIDE - All Issues</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="style.css" rel="stylesheet">
</head>
<body>
  <!-- Top Nav with Issues dropdown -->
  <nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">RIDE - Index</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" 
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          {issues_nav_html}
        </ul>
      </div>
    </div>
  </nav>

  <!-- Body -->
  <div class="container my-5">
    <h1>RIDE - All Issues</h1>
    <p>This index lists all available reviews.</p>
    {body_content}
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    return index_html


if __name__ == "__main__":
    main()
