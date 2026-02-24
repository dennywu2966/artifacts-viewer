# Artifacts Viewer Design

## Overview
A web-based viewer for documents, presentations, markdown, mermaid diagrams, and images with a sidebar navigation and light geek theme.

## Architecture
- **Single HTML file** — self-contained, no build step, portable
- **Sidebar + Main Panel** layout
- **CDN libraries** for rendering different file types

## Visual Design

### Color Palette (Light Geek Theme)
| Element | Hex |
|---------|-----|
| Background | `#F8FAFC` (slate-50) |
| Sidebar BG | `#F1F5F9` (slate-100) |
| Sidebar Border | `#E2E8F0` (slate-200) |
| Primary Text | `#1E293B` (slate-800) |
| Secondary Text | `#64748B` (slate-500) |
| Accent | `#0EA5E9` (sky-500) |
| Success/Code | `#22C55E` (green-500) |
| Hover | `#E0F2FE` (sky-100) |

### Typography
- **Headings**: Fira Code (monospace, tech feel)
- **Body**: Fira Sans
- **Code blocks**: Fira Code

### Layout
```
┌─────────────────────────────────────────────────┐
│  Artifacts Viewer           [Search] [Settings]│
├──────────┬──────────────────────────────────────┤
│ 📁 docs  │                                      │
│ 📁 slides│     [File Preview Area]              │
│ 📁 markdown│   - PDF rendered via PDF.js      │
│ 📁 images│   - Markdown via marked.js          │
│ 📁 diagrams│  - Mermaid via mermaid.js        │
│ 📁 other │   - Images direct                  │
│          │                                      │
├──────────┴──────────────────────────────────────┤
│  Status: viewing xxx.pdf | Size: 2.3MB         │
└─────────────────────────────────────────────────┘
```

## Supported File Types

| Category | Extensions | Renderer |
|----------|------------|----------|
| PDF | `.pdf` | PDF.js |
| Markdown | `.md`, `.mdx` | marked.js |
| Mermaid | `.mmd`, `.mermaid` | mermaid.js |
| Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg` | Native `<img>` |
| Documents | `.doc`, `.docx` | Google Docs Viewer embed |
| Presentations | `.ppt`, `.pptx` | Google Slides Viewer embed |

## Extensibility
```javascript
const viewers = {
  'pdf': { renderer: 'pdfjs', extensions: ['pdf'] },
  'markdown': { renderer: 'markdown', extensions: ['md', 'mdx'] },
  'mermaid': { renderer: 'mermaid', extensions: ['mmd', 'mermaid'] },
  'image': { renderer: 'image', extensions: ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'] },
  'doc': { renderer: 'google-docs', extensions: ['doc', 'docx'] },
  'ppt': { renderer: 'google-slides', extensions: ['ppt', 'pptx'] },
};
```

## File Organization
Pre-defined folders (can be customized):
- `docs/` — PDF, DOC, DOCX
- `slides/` — PPT, PPTX
- `markdown/` — MD, MDX, Mermaid
- `images/` — PNG, JPG, GIF, WEBP, SVG
- `other/` — fallback

## Interactions
- Click folder to expand/collapse
- Click file to preview in main area
- Keyboard navigation support
- Hover states with smooth transitions (150-300ms)

## Deployment
- Open directly in browser (file://)
- Or host on any static web server
