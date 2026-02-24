# artifacts-viewer

A sophisticated web-based viewer for documents, presentations, markdown, mermaid diagrams, and images with a sidebar navigation.

![Artifacts Viewer](https://img.shields.io/badge/style-geek-light-blue)

## Quick Start

Open `artifacts-viewer.html` in your browser, or serve via static server:

```bash
# Python
python -m http.server 8000

# Node.js
npx serve .

# PHP
php -S localhost:8000
```

## Supported Formats

| Category | Extensions | Renderer |
|----------|------------|----------|
| Documents | `.pdf`, `.doc`, `.docx` | PDF.js / Google Docs Embed |
| Presentations | `.ppt`, `.pptx` | Google Slides Embed |
| Markdown | `.md`, `.mdx` | marked.js |
| Diagrams | `.mmd`, `.mermaid` | mermaid.js |
| Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg` | Native `<img>` |

## Features

- Light geek theme with Fira Code + Fira Sans typography
- Sidebar navigation with file tree
- Search/filter files
- PDF rendering via PDF.js
- Markdown with Mermaid diagram support
- Google Docs/Slides embedding for DOC/PPT
- Extensible viewer architecture

## Directory Structure

```
artifacts-viewer/
├── artifacts-viewer.html   # Main viewer
├── EXTENSIBILITY.md        # Guide for adding new formats
├── docs/                  # PDF, DOC, DOCX files
├── slides/                # PPT, PPTX files
├── markdown/              # MD, MDX files
├── diagrams/              # Mermaid files
├── images/                # PNG, JPG, SVG, etc.
└── other/                 # Other files
```

## Adding Files

Drop files into the appropriate folder and update the `files` array in `artifacts-viewer.html`:

```javascript
const files = [
  { name: 'myfile.pdf', path: 'docs/myfile.pdf', category: 'docs', size: '2.3MB' },
  // Add more files here
];
```

## Extending

See [EXTENSIBILITY.md](EXTENSIBILITY.md) for adding new file types and custom renderers.
