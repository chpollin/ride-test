# Full TEI XML Structure Analysis

## Element Hierarchy with XPath

- `TEI`
  - **XPath:** `TEI`
  - **Attribute:** `xmlns` = `http://www.tei-c.org/ns/1.0`
  - **Attribute:** `xml:id` = `ride.18.1`
- `teiHeader`
  - **XPath:** `TEI/teiHeader`
- `fileDesc`
  - **XPath:** `TEI/teiHeader/fileDesc`
- `titleStmt`
  - **XPath:** `TEI/teiHeader/fileDesc/titleStmt`
- `title`
  - **XPath:** `TEI/teiHeader/fileDesc/titleStmt/title`
- `author`
  - **XPath:** `TEI/teiHeader/fileDesc/titleStmt/author`
- `name`
  - **XPath:** `TEI/teiHeader/fileDesc/titleStmt/author/name`
- `forename`
  - **XPath:** `TEI/teiHeader/fileDesc/titleStmt/author/name/forename`
- `surname`
  - **XPath:** `TEI/teiHeader/fileDesc/titleStmt/author/name/surname`
- `affiliation`
  - **XPath:** `TEI/teiHeader/fileDesc/titleStmt/author/affiliation`
- `orgName`
  - **XPath:** `TEI/teiHeader/fileDesc/titleStmt/author/affiliation/orgName`
- `placeName`
  - **XPath:** `TEI/teiHeader/fileDesc/titleStmt/author/affiliation/placeName`
- `email`
  - **XPath:** `TEI/teiHeader/fileDesc/titleStmt/author/email`
- `publicationStmt`
  - **XPath:** `TEI/teiHeader/fileDesc/publicationStmt`
- `publisher`
  - **XPath:** `TEI/teiHeader/fileDesc/publicationStmt/publisher`
- `date`
  - **XPath:** `TEI/teiHeader/fileDesc/publicationStmt/date`
- `idno`
  - **XPath:** `TEI/teiHeader/fileDesc/publicationStmt/idno`
- `sourceDesc`
  - **XPath:** `TEI/teiHeader/fileDesc/sourceDesc`
- `encodingDesc`
  - **XPath:** `TEI/teiHeader/encodingDesc`
- `classDecl`
  - **XPath:** `TEI/teiHeader/encodingDesc/classDecl`
- `taxonomy`
  - **XPath:** `TEI/teiHeader/encodingDesc/classDecl/taxonomy`
- `category`
  - **XPath:** `TEI/teiHeader/encodingDesc/classDecl/taxonomy/category`
- `catDesc`
  - **XPath:** `TEI/teiHeader/encodingDesc/classDecl/taxonomy/category/catDesc`
- `text`
  - **XPath:** `TEI/text`
- `front`
  - **XPath:** `TEI/text/front`
- `div`
  - **XPath:** `TEI/text/front/div`
- `p`
  - **XPath:** `TEI/text/front/div/p`
- `body`
  - **XPath:** `TEI/text/body`
- `div`
  - **XPath:** `TEI/text/body/div`
- `head`
  - **XPath:** `TEI/text/body/div/head`
- `p`
  - **XPath:** `TEI/text/body/div/p`
- `ref`
  - **XPath:** `TEI/text/body/div/p/ref`
- `note`
  - **XPath:** `TEI/text/body/div/p/note`
- `back`
  - **XPath:** `TEI/text/back`
- `listBibl`
  - **XPath:** `TEI/text/back/listBibl`
- `bibl`
  - **XPath:** `TEI/text/back/listBibl/bibl`
- `ref`
  - **XPath:** `TEI/text/back/listBibl/bibl/ref`

## TEI Elements and HTML Representation

### 1. `TEI`
- **XPath:** `TEI`
- **HTML:** The root TEI element corresponds to the entire HTML document (`<html>`).
- **Attribute:** `xmlns="http://www.tei-c.org/ns/1.0"` defines the XML namespace.

### 2. `teiHeader`
- **XPath:** `TEI/teiHeader`
- **HTML:** Maps to the `<header>` element.

### 3. `fileDesc`
- **XPath:** `TEI/teiHeader/fileDesc`
- **HTML:** Nested inside the `<header>` as a `<div>` or `<section>`.

### 4. `titleStmt`
- **XPath:** `TEI/teiHeader/fileDesc/titleStmt`
- **HTML:** Represented using the `<h1>` for the primary title and `<h2>` for subtitles.

### 5. `title`
- **XPath:** `TEI/teiHeader/fileDesc/titleStmt/title`
- **HTML:** Rendered as `<h1>` for the document title.

### 6. `author`
- **XPath:** `TEI/teiHeader/fileDesc/titleStmt/author`
- **HTML:** Transformed into a `<p>` element within the header, often with a `class="author"`.

### 7. `name`
- **XPath:** `TEI/teiHeader/fileDesc/titleStmt/author/name`
- **HTML:** Displayed as `<span class="author-name">` within the `<p>`.

### 8. `publicationStmt`
- **XPath:** `TEI/teiHeader/fileDesc/publicationStmt`
- **HTML:** Represented in the `<footer>` as `<p>` elements for the publisher and date information.

### 9. `sourceDesc`
- **XPath:** `TEI/teiHeader/fileDesc/sourceDesc`
- **HTML:** Included in a `<div>` within the footer or a separate metadata section.

### 10. `text`
- **XPath:** `TEI/text`
- **HTML:** The main body of the document, typically within the `<main>` tag.

### 11. `front`
- **XPath:** `TEI/text/front`
- **HTML:** Rendered as a `<section>` before the main content.

### 12. `div`
- **XPath:** `TEI/text/body/div`
- **HTML:** Mapped to `<div>` or `<section>` for content division.

### 13. `p`
- **XPath:** `TEI/text/body/div/p`
- **HTML:** Rendered directly as `<p>`.

### 14. `ref`
- **XPath:** `TEI/text/body/div/p/ref`
- **HTML:** Rendered as `<a href>` with the `href` attribute pointing to the link.

### 15. `note`
- **XPath:** `TEI/text/body/div/p/note`
- **HTML:** Converted into a `<span class="note">` or `<aside>`.

### 16. `back`
- **XPath:** `TEI/text/back`
- **HTML:** Represented in the `<footer>`.

### 17. `listBibl`
- **XPath:** `TEI/text/back/listBibl`
- **HTML:** Rendered as `<ul>` or `<ol>`.

### 18. `bibl`
- **XPath:** `TEI/text/back/listBibl/bibl`
- **HTML:** Each entry represented by a `<li>`.

---

## Attributes Mapping
- **`xml:id`** → Translated into `id` attributes in HTML.
- **`n` (for numbering)** → Often rendered as a `data-attribute` or custom class.
- **`ref` (for references)** → Translated into the `href` attribute of an `<a>` tag.




# Example HTML and CSS Design
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RIDE - Issue 18</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    /* Header */
    header {
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    nav ul.nav {
      gap: 1rem;
    }

    /* Section headings */
    section h3 {
      border-bottom: 2px solid #ddd;
      padding-bottom: 5px;
      margin-bottom: 10px;
    }

    /* Sidebar badges */
    aside .badge {
      font-size: 0.85rem;
      cursor: pointer;
    }
    aside .badge:hover {
      background-color: #343a40;
      color: #fff;
    }

    /* Responsive typography */
    body {
      font-family: "Georgia", "Times New Roman", serif;
    }
    h2 {
      font-size: 1.75rem;
      font-weight: bold;
    }
    p, li {
      font-size: 1rem;
      line-height: 1.6;
    }

    /* Smooth scrolling for TOC */
    html {
      scroll-behavior: smooth;
    }

    /* Sidebar */
    aside {
      position: sticky;
      top: 20px;
    }

    /* Spacing between sections */
    section {
      margin-bottom: 2rem;
    }
  </style>
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
          <h2 class="h2">A synergistic approach to non-narrative historical sources</h2>
          <p class="text-muted">The database and digital edition of the Spängler household account books, 1733–1785</p>
          <hr>
        </section>

        <!-- Abstract Section -->
        <section id="abstract" class="mb-4">
          <h3 class="h5">Abstract</h3>
          <p>The household account books of the Salzburg merchant family Spängler cover...</p>
        </section>

        <!-- Introduction Section -->
        <section id="introduction">
          <h3 class="h5">Introduction</h3>
          <p>Details about the digital edition and the transcription of the account books...</p>
        </section>
      </div>

      <!-- Sidebar -->
      <aside class="col-md-4">
        <!-- Meta Information -->
        <section class="mb-4">
          <h4 class="h6">Meta</h4>
          <ul class="list-unstyled">
            <li><strong>Published:</strong> Jul 2023</li>
            <li><strong>Last updated:</strong> Sep 2024</li>
          </ul>
        </section>

        <!-- Tags Section -->
        <section class="mb-4">
          <h4 class="h6">Tags</h4>
          <div class="d-flex flex-wrap gap-2">
            <span class="badge bg-secondary">18th century</span>
            <span class="badge bg-secondary">Account books</span>
            <span class="badge bg-secondary">Digital edition</span>
          </div>
        </section>

        <!-- TOC -->
        <section>
          <h4 class="h6">TOC</h4>
          <ul class="list-unstyled">
            <li><a href="#abstract">Abstract</a></li>
            <li><a href="#introduction">Introduction</a></li>
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

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```