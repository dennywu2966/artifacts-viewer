# Extending Artifacts Viewer

## Adding New File Types

Add a new entry to the `viewers` object in `artifacts-viewer.html`:

```javascript
const viewers = {
  // ... existing viewers ...

  yourFormat: {
    extensions: ['ext1', 'ext2'],  // file extensions to handle
    render: (path) => {
      // Return HTML string
      return `<div>Your custom viewer</div>`;
    }
  }
};
```

For async renderers (like fetching content):

```javascript
const viewers = {
  yourFormat: {
    extensions: ['ext'],
    render: async (path) => {
      const response = await fetch(path);
      const data = await response.text();
      return `<pre>${data}</pre>`;
    }
  }
};
```

## Adding New Categories

Add to `fileCategories`:

```javascript
const fileCategories = [
  // ... existing categories ...
  { id: 'videos', name: 'Videos', icon: '🎬', extensions: ['mp4', 'webm'] },
];
```

## Example: JSON Viewer

```javascript
json: {
  extensions: ['json'],
  render: async (path) => {
    const response = await fetch(path);
    const data = await response.json();
    const html = `<pre><code>${JSON.stringify(data, null, 2)}</code></pre>`;
    return `<div class="markdown-preview">${html}</div>`;
  }
}
```

## Custom Styling

Add CSS rules in the `<style>` section. Use the existing CSS variables:

```css
:root {
  --bg: #F8FAFC;
  --sidebar-bg: #F1F5F9;
  --accent: #0EA5E9;
  --font-heading: 'Fira Code', monospace;
}
```

## Deployment

Simply open `artifacts-viewer.html` in a browser, or serve via any static web server:

```bash
# Python
python -m http.server 8000

# Node.js
npx serve .

# PHP
php -S localhost:8000
```
