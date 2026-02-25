# Artifacts Viewer Regression Validation Guide

## Overview
This guide covers E2E validation for the artifacts-viewer project using Playwright MCP.

## Prerequisites
- Python3 with http.server module
- Playwright MCP server configured

## Test Cases

### P0 - Critical
1. **Page Load**
   - Navigate to `http://localhost:8080/artifacts-viewer.html`
   - Verify title: "Artifacts Viewer"
   - Verify sidebar with all categories

2. **Markdown Rendering**
   - Click on `readme.md`
   - Verify heading "Welcome to Artifacts Viewer" rendered
   - Verify mermaid diagram rendered (SVG present)

3. **Image Viewer**
   - Click on any image file
   - Verify image displays correctly

### P1 - Important
4. **Search Filter**
   - Type in search box
   - Verify sidebar filters correctly

5. **Status Updates**
   - Click file, verify footer shows "Viewing: filename"

### P2 - Nice to Have
6. **PDF Viewer**
   - Click on PDF file
   - Verify PDF pages render

7. **Google Docs Embed**
   - Click on DOC/PPTX file
   - Verify iframe embed loads

## Running Tests

### Start Server
```bash
bash scripts/agents/start_restart_stack.sh
```

### Run Playwright Tests
Use Playwright MCP to execute:
```javascript
// Test 1: Page load
await page.goto('http://localhost:8080/artifacts-viewer.html');
const title = await page.title();
assert(title === 'Artifacts Viewer');

// Test 2: Click readme.md
await page.click('text=readme.md');
const heading = await page.textContent('h1');
assert(heading === 'Welcome to Artifacts Viewer');

// Test 3: Search
await page.fill('input[placeholder="Search files..."]', 'notes');
const visible = await page.isVisible('text=notes.md');
assert(visible === true);
```

## Save-Artifact Skill Test

### Test the skill
```bash
# Create test file
echo "# Test" > /tmp/test.md

# Run save-artifact script
python3 ~/.claude/skills/save-artifact/scripts/save_artifact.py /tmp/test.md --name "skill_test.md" --category markdown

# Verify file saved
ls -la markdown/skill_test.md

# Add to viewer files array and verify in UI
```

## Manual Testing Checklist
- [ ] Page loads with correct title
- [ ] All 6 categories visible in sidebar
- [ ] Click file updates status bar
- [ ] Markdown renders with formatting
- [ ] Mermaid diagrams render
- [ ] Images display correctly
- [ ] Search filters work
- [ ] No console errors
