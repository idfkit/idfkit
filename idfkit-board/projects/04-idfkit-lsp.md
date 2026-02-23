# Project: idfkit-lsp — VS Code Language Server

## Summary

**idfkit-lsp** is a Language Server Protocol (LSP) implementation that provides intelligent editing support for Python files using the idfkit library. It ships as a VS Code extension and delivers the kind of editor intelligence that building energy modelers have never had: autocomplete for EnergyPlus object types, hover documentation with units and constraints, and AST-based type inference that understands idfkit's data model.

**Repository:** `idfkit/idfkit-lsp`
**Server language:** Python (pygls)
**Client language:** TypeScript (VS Code extension)
**License:** MIT
**Requirements:** Python 3.10+, VS Code 1.78+, idfkit installed in the Python environment

## Features

### Autocomplete
- Object type names when calling `doc.add("...")` or `doc["..."]`
- Field attributes on `IDFObject` instances (e.g., `zone.x_origin`, `zone.floor_area`)
- Keyword arguments for `doc.add()` calls with documentation, units, and constraints
- Choices and defaults for enumerated fields

### Hover Documentation
- **Object types:** Group, memo, required fields, and field count
- **Field attributes:** Type, units, default value, min/max bounds, available choices
- **Inferred variables:** Type information for variables inferred through the AST analysis

### Signature Help
- Parameter info for `doc.add()` calls showing all fields: required and optional
- Each parameter annotated with its type, units, and description from the EnergyPlus schema

### AST-Based Type Inference
The language server tracks idfkit types through Python code without requiring runtime analysis:

```python
from idfkit import load_idf

doc = load_idf("model.idf")        # inferred: IDFDocument
zones = doc["Zone"]                 # inferred: IDFCollection("Zone")
zone = zones["Office"]              # inferred: IDFObject("Zone")
new_zone = doc.add("Zone", "Hall")  # inferred: IDFObject("Zone")

# Completions, hover, and signature help work throughout
zone.x_origin  # field attribute completion + hover docs
```

Tracks types through: assignments, subscript access (`doc["Zone"]`), method calls (`doc.add()`), and for-loop iteration (`for zone in doc["Zone"]`).

## Architecture

```
├── client/              # VS Code extension (TypeScript)
│   └── src/extension.ts # Spawns the Python server over stdio
├── server/              # LSP server (Python, pygls)
│   └── src/idfkit_lsp/
│       ├── server.py          # LSP handler registration
│       ├── analyzer.py        # AST visitor for type inference
│       ├── completion.py      # Autocomplete provider
│       ├── hover.py           # Hover documentation provider
│       ├── signature_help.py  # Signature help provider
│       ├── schema_cache.py    # EnergyPlus schema wrapper
│       └── document_state.py  # Per-document state management
```

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `idfkitLsp.pythonPath` | `python3` | Path to Python interpreter with idfkit and idfkit-lsp installed |
| `idfkitLsp.trace.server` | `off` | Traces communication between VS Code and the server (`off`, `messages`, `verbose`) |

Use the **idfkit: Restart Language Server** command to reload after configuration changes.

## Development

```bash
# Server (Python)
cd server && uv sync --extra dev
uv run pytest                       # run tests

# Client (TypeScript)
npm install && npm run compile

# Launch in VS Code
# Press F5 to open Extension Development Host
```

Quality checks: `make check` (ruff lint, ruff format, pyright typecheck, pytest).

## Strategic Role in the Ecosystem

idfkit-lsp is the **developer experience layer** — it makes writing idfkit Python code feel like writing code in a modern, well-supported language:

1. **Reduces errors.** Autocomplete for EnergyPlus object types and field names eliminates typos and naming mistakes that cause silent failures or confusing EnergyPlus errors.
2. **Teaches the domain.** Hover documentation surfaces EnergyPlus field metadata (units, bounds, defaults) at the point of use — no need to look up the IDD manually.
3. **Validates the type system.** AST-based type inference ensures that completions and documentation are context-aware — if you're working with a `Zone`, you see zone fields, not material fields.
4. **Professional credibility.** A language server signals that idfkit is a serious, production-quality tool — not a weekend project. This matters for institutional adoption (Lucia's priority) and for attracting contributors (Renata's priority).
