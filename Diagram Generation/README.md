# 🧠 Diagram Generator Toolkit

This project contains three Python tools that generate technical diagrams using LLMs and two popular visualization tools: **Graphviz** and **Mermaid.js**.

---

## 📁 Code Overview

### 1. `diagram_graphviz.py`

**Generates professional technical diagrams** using the `graphviz` Python library and a two-stage LLM pipeline.

- **Stage 1**: Generates a structured description of a given topic.
- **Stage 2**: Converts that into clean, annotated Python code for a `graphviz` diagram.
- **Features**:
  - High-quality PNG generation
  - Custom node shapes, colors, and annotations
  - Automatically saves code + explanation to a text file

**Usage:**

```bash
python diagram_graphviz.py
```

---

### 2. `Diagram mermaid.py`

**Creates and validates Mermaid.js code** for visualizing a topic diagrammatically.

- Gets explanation from LLM
- Converts it into valid Mermaid syntax
- Handles syntax errors by using an LLM to auto-fix them based on CLI feedback
- Saves final `.mmd` file and exports a `.png` using `mmdc`

**Usage:**

```bash
python "Diagram mermaid.py"
```

> ⚠️ Make sure you update the path to `mmdc.cmd` in the code (`check_mermaid_code()` function) to match your system!

### Mermaid CLI Setup:

```bash
npm install -g @mermaid-js/mermaid-cli
```

Verify it's installed:

```bash
mmdc -h
```

---

### 3. `Diagram in Web.py`

**Generates Mermaid diagrams directly in an HTML page** and opens them in your browser.

- Gets explanation from LLM
- Generates Mermaid code
- Validates Mermaid syntax using the LLM
- Embeds the diagram in an HTML page

**Usage:**

```bash
python "Diagram in Web.py"
```

Opens a file like `diagram.html` automatically in your browser with the rendered diagram.

---

## 🧪 Requirements

- Node.js + NPM (for Mermaid CLI)

---

## 📦 Install Dependencies

### Python packages:

```bash
pip install -r requirements.txt
```

### Node.js packages (for Mermaid CLI):

```bash
npm install -g @mermaid-js/mermaid-cli
```

---

## 🗂 Output

- `diagram_<topic>_<timestamp>.png` – Graphviz diagrams
- `mer_diagram.png` – Mermaid CLI diagrams
- `diagram.html` – Rendered Mermaid diagram in browser
- `diagram_<topic>.txt` – Stores topic explanation + Graphviz code

---

## 🔐 Environment Setup

Create a file called `API.env`:

```env
GROQ_API_KEY=your_api_key_here
```

---

## 🛠 Tips

- You can customize node colors, shapes, and layout in Graphviz easily.
- Mermaid diagrams support `graph TD`, `graph LR`, `classDef`, `subgraph`, etc.
- Use `mmdc` for offline rendering or host the Mermaid code in a webpage for dynamic viewing.

---

## 📬 Contributing

Feel free to fork and modify. Pull requests welcome!
