#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from lxml import etree

def main():
    data_folder = "data"
    web_folder = "web"

    # Ensure the "web" folder exists
    os.makedirs(web_folder, exist_ok=True)

    # 1) Build our static "About" pages (e.g., Editorial, Publishing Policy, etc.)
    static_pages = {
        "Editorial": "editorial.html",
        "Publishing Policy": "publishing-policy.html",
        "Ethical Code": "ethical-code.html",
        "Team": "team.html",
        "Peer Reviewers": "peer-reviewers.html",
        "Dissemination and Discussion": "dissemination-and-discussion.html",
        "Contact and Newsletter": "contact-and-newsletter.html"
    }
    build_static_pages(web_folder, static_pages)

    # 2) Collect sub-reviews from each "issueXX" directory
    issue_pages = {}  # { "issue17": [ (title, link, abstractHTML), ... ], ... }

    for issue_dir in os.listdir(data_folder):
        issue_path = os.path.join(data_folder, issue_dir)
        if not os.path.isdir(issue_path):
            continue
        if not issue_dir.startswith("issue"):
            # Skip any folder not named "issueXX"
            continue

        issue_name = issue_dir
        issue_pages[issue_name] = []

        # Create subfolder in web/ for the individual pages
        issue_out_folder = os.path.join(web_folder, issue_name)
        os.makedirs(issue_out_folder, exist_ok=True)

        # Scan subfolders in this issue
        for subfolder in os.listdir(issue_path):
            subfolder_path = os.path.join(issue_path, subfolder)
            if not os.path.isdir(subfolder_path):
                continue

            # Expect <subfolder>-tei.xml
            tei_file = f"{subfolder}-tei.xml"
            tei_path = os.path.join(subfolder_path, tei_file)
            if not os.path.isfile(tei_path):
                continue

            # Parse TEI and build HTML
            doc_title, doc_abstract, html_output = transform_tei_to_html(tei_path, issue_name, subfolder)

            # Write to web/issueXX/<subfolder>.html
            output_html_path = os.path.join(issue_out_folder, f"{subfolder}.html")
            with open(output_html_path, "w", encoding="utf-8") as f:
                f.write(html_output)

            # Remember for the summary page
            rel_link = f"{issue_name}/{subfolder}.html"
            issue_pages[issue_name].append((doc_title, rel_link, doc_abstract))

    # 3) Build a summary page for each issue (e.g. issue17.html)
    for issue_name, pages_info in issue_pages.items():
        issue_html = build_issue_page(issue_name, pages_info)
        issue_main_page = os.path.join(web_folder, f"{issue_name}.html")
        with open(issue_main_page, "w", encoding="utf-8") as f:
            f.write(issue_html)

    # 4) Build the global index with top nav: About dropdown, Issues dropdown, etc.
    index_html = build_global_index(issue_pages, static_pages)
    index_path = os.path.join(web_folder, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)

    print("Done. Created all pages in 'web' folder.")


def build_static_pages(web_folder, static_pages):
    """
    Create placeholder static "About" pages in web/ with minimal content.
    """
    placeholder_texts = {
        "Editorial": "This is the editorial page. Replace with real content.",
        "Publishing Policy": "Here you can describe your publishing policy in detail.",
        "Ethical Code": "Your journal’s ethical code goes here.",
        "Team": "Introduce your editorial or development team.",
        "Peer Reviewers": "List or thank your peer reviewers here.",
        "Dissemination and Discussion": "Place your outreach or discussion approach here.",
        "Contact and Newsletter": "Add contact details and newsletter info here."
    }

    for page_name, filename in static_pages.items():
        filepath = os.path.join(web_folder, filename)
        # Minimal HTML structure
        content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{page_name}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="style.css" rel="stylesheet">
</head>
<body>
  <header class="bg-light py-3 border-bottom">
    <div class="container d-flex justify-content-between align-items-center">
      <div class="d-flex align-items-center">
        <img src="logo.png" alt="RIDE Logo" class="me-3" style="width:50px;height:auto;">
        <h1 class="h4 mb-0">RIDE</h1>
      </div>
      <nav>
        <ul class="nav">
          <li class="nav-item"><a class="nav-link" href="index.html">Home</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <div class="container my-4">
    <h2>{page_name}</h2>
    <p>{placeholder_texts.get(page_name, "Placeholder Content")}</p>
  </div>
</body>
</html>"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


def transform_tei_to_html(tei_path, issue_name, subfolder):
    """
    Parse a TEI file, extracting doc title & abstract, returning (doc_title, doc_abstract, html_string).
    Images are referenced as ../../data/issueXX/<subfolder>/pictures/<image>.
    """
    tree = etree.parse(tei_path)
    root = tree.getroot()
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # doc_title
    title_node = root.xpath('.//tei:teiHeader//tei:titleStmt/tei:title', namespaces=ns)
    doc_title = title_node[0].text.strip() if title_node else "Untitled Document"

    # metadata
    pub_el = root.xpath('.//tei:teiHeader//tei:fileDesc//tei:publicationStmt/tei:publisher', namespaces=ns)
    publisher = pub_el[0].text.strip() if pub_el else ""

    date_el = root.xpath('.//tei:teiHeader//tei:fileDesc//tei:publicationStmt/tei:date', namespaces=ns)
    pub_date = date_el[0].text.strip() if date_el else ""

    idno_el = root.xpath('.//tei:teiHeader//tei:fileDesc//tei:publicationStmt/tei:idno', namespaces=ns)
    idno = idno_el[0].text.strip() if idno_el else ""

    # abstract
    doc_abstract = ""
    front_divs = root.xpath('.//tei:text//tei:front/tei:div', namespaces=ns)
    for fdiv in front_divs:
        if fdiv.get("type") == "abstract":
            p_nodes = fdiv.xpath('.//tei:p', namespaces=ns)
            for p in p_nodes:
                text = p.xpath('string(.)').strip()
                if text:
                    doc_abstract += f"<p>{text}</p>\n"

    # body -> divs
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
            para_content = process_paragraph(pnode, ns)
            body_html += para_content
        body_html += "</section>\n\n"

    # figures
    figure_nodes = root.xpath('.//tei:text//tei:body//tei:figure', namespaces=ns)
    figure_html = ""
    for fig in figure_nodes:
        fig_id = fig.get('{http://www.w3.org/XML/1998/namespace}id', '')
        graphic_el = fig.xpath('.//tei:graphic', namespaces=ns)
        legend_el = fig.xpath('./tei:head[@type="legend"]', namespaces=ns)
        legend = legend_el[0].text.strip() if (legend_el and legend_el[0].text) else "Figure"
        if graphic_el:
            img_url = graphic_el[0].get('url', '')
            img_name = os.path.basename(img_url)
            rel_img_path = f"../../data/{issue_name}/{subfolder}/pictures/{img_name}"
            figure_html += (
                f'<figure id="{fig_id}" class="mb-4">\n'
                f'  <img src="{rel_img_path}" alt="{legend}" class="img-fluid"/>\n'
                f'  <figcaption>{legend}</figcaption>\n'
                f'</figure>\n'
            )

    body_html += figure_html

    # final HTML
    html_string = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{doc_title}</title>
  <!-- Bootstrap 5 -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="../style.css" rel="stylesheet">
</head>
<body>
  <header class="bg-light py-3 border-bottom">
    <div class="container d-flex justify-content-between align-items-center">
      <div class="d-flex align-items-center">
        <img src="../logo.png" alt="RIDE Logo" class="me-3" style="width:50px;height:auto;">
        <h1 class="h4 mb-0">RIDE</h1>
      </div>
      <nav>
        <ul class="nav">
          <li class="nav-item"><a class="nav-link" href="../index.html">Home</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <div class="container my-4">
    <div class="row">
      <div class="col-md-8">
        <section class="mb-4">
          <h2 class="h2">{doc_title}</h2>
          <p class="text-muted">
             {publisher}, {pub_date} {f'({idno})' if idno else ''}
          </p>
          <hr>
        </section>

        <section id="abstract" class="mb-4">
          <h3 class="h5">Abstract</h3>
          {doc_abstract}
        </section>

        {body_html}
      </div>
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
            <span class="badge bg-secondary">Digital Edition</span>
            <span class="badge bg-secondary">TEI</span>
          </div>
        </section>
      </aside>
    </div>
  </div>
</body>
</html>
"""
    return doc_title, doc_abstract, html_string


def process_paragraph(pnode, ns):
    """
    Convert a TEI <p> node into HTML <p>, handling child elements like <ref>, <note>, <emph>.
    """
    content = pnode.text or ""

    for child in pnode:
        tag = etree.QName(child)
        if tag.localname == 'ref':
            link_text = (child.text or '').strip()
            url = child.get('target', '#')
            content += f'<a href="{url}" target="_blank">{link_text}</a>'
            if child.tail:
                content += child.tail
        elif tag.localname == 'note':
            note_text = child.xpath('string(.)').strip()
            content += f'<span class="note">[{note_text}]</span>'
            if child.tail:
                content += child.tail
        elif tag.localname == 'emph':
            em_text = child.xpath('string(.)').strip()
            content += f'<em>{em_text}</em>'
            if child.tail:
                content += child.tail
        else:
            text_in_child = child.xpath('string(.)')
            content += text_in_child
            if child.tail:
                content += child.tail

    return f"<p>{content.strip()}</p>\n"


def build_issue_page(issue_name, pages_info):
    """
    Build a single HTML page for an entire "collection" (issueXX.html),
    listing each sub-review with title, abstract, link to subpage.
    """
    items_html = ""
    for title, link, abstract in pages_info:
        items_html += f"""
        <div class="mb-5">
          <h3><a href="{link}">{title}</a></h3>
          <div>{abstract}</div>
        </div>
        """

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{issue_name.capitalize()}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="style.css" rel="stylesheet">
</head>
<body>
  <header class="bg-light py-3 border-bottom">
    <div class="container d-flex justify-content-between align-items-center">
      <div class="d-flex align-items-center">
        <img src="logo.png" alt="RIDE Logo" class="me-3" style="width:50px;height:auto;">
        <h1 class="h4 mb-0">RIDE</h1>
      </div>
      <nav>
        <ul class="nav">
          <li class="nav-item"><a class="nav-link" href="index.html">Home</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <div class="container my-4">
    <h2>{issue_name.capitalize()}</h2>
    <p>This page provides an overview of all reviews in {issue_name}.</p>
    {items_html}
  </div>
</body>
</html>
"""
    return page_html


def build_global_index(issue_pages, static_pages):
    """
    Build index.html with a top nav bar:
      - About dropdown -> each static page
      - Issues dropdown -> each issue page
      - Data, Reviewers, Reviewing Criteria placeholders
    """
    # "About" dropdown
    about_dropdown = ""
    for name, filename in static_pages.items():
        about_dropdown += f'<li><a class="dropdown-item" href="{filename}">{name}</a></li>\n'

    # "Issues" dropdown
    issues_dropdown = ""
    for issue_name in sorted(issue_pages.keys()):
        issues_dropdown += f'<li><a class="dropdown-item" href="{issue_name}.html">{issue_name.capitalize()}</a></li>\n'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>RIDE - Index</title>
  <!-- Bootstrap 5 -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="style.css" rel="stylesheet">
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">RIDE</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" 
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto">
          <!-- About dropdown -->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="aboutDropdown" role="button" 
               data-bs-toggle="dropdown" aria-expanded="false">
              About
            </a>
            <ul class="dropdown-menu" aria-labelledby="aboutDropdown">
              {about_dropdown}
            </ul>
          </li>
          <!-- Issues dropdown -->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="issuesDropdown" role="button" 
               data-bs-toggle="dropdown" aria-expanded="false">
              Issues
            </a>
            <ul class="dropdown-menu" aria-labelledby="issuesDropdown">
              {issues_dropdown}
            </ul>
          </li>
          <!-- Additional placeholders -->
          <li class="nav-item"><a class="nav-link" href="#">Data</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Reviewers</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Reviewing Criteria</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="container my-5">
    <h1>RIDE - Home</h1>
    <p>Welcome to RIDE's main index page. Use the top navigation to explore issues or learn more in the About menu.</p>
  </div>

  <!-- Bootstrap Bundle JS -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    return html


def process_paragraph(pnode, ns):
    """
    Convert a TEI <p> node into HTML <p>, handling <ref>, <note>, <emph>, etc.
    (Helper included above, but repeated here in case you want it in a separate section.)
    """
    # (If you are re-using the top-level one, remove this or unify them.)
    content = pnode.text or ""

    for child in pnode:
        tag = etree.QName(child)
        if tag.localname == 'ref':
            link_text = (child.text or '').strip()
            url = child.get('target', '#')
            content += f'<a href="{url}" target="_blank">{link_text}</a>'
            if child.tail:
                content += child.tail
        elif tag.localname == 'note':
            note_text = child.xpath('string(.)').strip()
            content += f'<span class="note">[{note_text}]</span>'
            if child.tail:
                content += child.tail
        elif tag.localname == 'emph':
            em_text = child.xpath('string(.)').strip()
            content += f'<em>{em_text}</em>'
            if child.tail:
                content += child.tail
        else:
            text_in_child = child.xpath('string(.)')
            content += text_in_child
            if child.tail:
                content += child.tail

    return f"<p>{content.strip()}</p>\n"


if __name__ == "__main__":
    main()
