# Project: Envelop — Browser-Native Visual EnergyPlus Editor

## Summary

**Envelop** is a browser-native visual EnergyPlus editor requiring zero installation. It brings modern web application design to building energy modeling — visual HVAC editing, 3D geometry, schedule timelines, and in-browser simulation via WebAssembly. Everything runs client-side.

**Repository:** `idfkit/idfkit-app`
**Stack:** React, TypeScript, Vite
**UI framework:** Zustand (state), Monaco (editor), React Flow (node graph), Three.js (3D), Recharts (charts)
**License:** MIT
**Install:** None required — runs in the browser

## Core Features

### IDF Code Editor
- Monaco-based code editor with IDF syntax highlighting
- IDD schema integration for real-time validation
- Auto-completion for object types and field names
- Real-time error highlighting
- Bi-directional sync with visual editors

### Visual HVAC Node-Graph Editor
- React Flow-based drag-and-drop HVAC component placement
- AirLoopHVAC component library with visual node connections
- Real-time connection validation and auto-naming
- Bi-directional sync: graph changes update IDF text and vice versa

### Plant Loop Visual Editor
- Chilled water, hot water, and condenser loop visualization
- Plant loop component library (chillers, boilers, pumps, heat exchangers)
- Demand/supply side splitting visualization

### HVAC Templates Library
- Pre-built system templates: VAV with reheat, VRF, DOAS + radiant, packaged rooftop unit, residential split system
- Template customization UI for rapid system creation

### 3D Geometry Viewer
- Three.js-based interactive 3D model rendering
- IDF geometry parsing (Zone, Surface, Fenestration)
- Zone/surface selection and highlighting
- Camera controls (orbit, pan, zoom)
- Zone creation wizard, surface editing, fenestration placement, construction assembly builder

### Schedule Visual Editor
- Visual timeline editor for `Schedule:Compact`
- Day/week/year view with interactive click-and-drag editing
- Schedule template library (occupancy, lighting, setpoints)
- Schedule graph visualization with zoom/pan
- Validation (time gaps, value bounds, unusual patterns)
- Bi-directional sync with IDF text editor

### Visual IDF Object Editor
- Object browser with hierarchical tree navigation
- Form-based field editing with validation
- Reference fields with searchable dropdowns
- Object creation wizard
- Bulk operations (rename, delete, duplicate)
- Inline IDD documentation

### In-Browser EnergyPlus Simulation
- EnergyPlus compiled to WebAssembly
- Web Worker integration for non-blocking simulation
- Simulation progress reporting
- Output file parsing (ESO, MTR, ERR)
- Weather file (EPW) handling

### Simulation Results Dashboard
- Results data extraction from ESO files
- Time-series charts (hourly, daily, monthly)
- Summary statistics display
- Export to CSV/Excel

### AI-Powered Assistance
- Error message parsing from `eplusout.err`
- Plain-English error explanations
- Suggested fixes for common errors
- Natural language model queries
- Sanity check alerts

### Accessibility & Mobile
- Dark mode with light/dark/system toggle
- WCAG 2.1 AA compliance across all pages
- Skip navigation and full keyboard navigation
- Screen reader announcements for dynamic content
- ARIA labels on all interactive elements
- Mobile-responsive layouts with touch support
- Touch-optimized node graph (pinch zoom, pan gestures)

### File Management
- IDF import with validation, IDF/epJSON export with formatting
- Local file storage (IndexedDB)
- Recent files list and example models library

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        React Frontend                           │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│  IDF Editor  │  Node Graph  │  3D Viewer   │ Results Dashboard │
│   (Monaco)   │ (React Flow) │  (Three.js)  │    (Recharts)     │
├──────────────┴──────────────┴──────────────┴───────────────────┤
│                     State Management (Zustand)                  │
├─────────────────────────────────────────────────────────────────┤
│                     IDF Parser / Serializer                     │
├─────────────────────────────────────────────────────────────────┤
│     Web Worker      │      IndexedDB       │    WebSocket       │
│   (E+ WASM Sim)     │   (Local Storage)    │  (Collaboration)   │
└─────────────────────┴──────────────────────┴────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Cloud Backend (Optional)                   │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│   Auth API   │  Storage API │  Sim Queue   │  Collab Service   │
└──────────────┴──────────────┴──────────────┴───────────────────┘
```

## Roadmap Status

### Tier 1: Core MVP — COMPLETE
All 6 epics delivered: IDF Editor, HVAC Node Graph, EnergyPlus WebAssembly, 3D Geometry Viewer, Simulation Results Dashboard, File Management.

### Tier 2: Enhanced Usability — IN PROGRESS (7/11 epics)
**Complete:** Plant Loop Editor, HVAC Templates, Geometry Tools (partial), AI Assistance, Schedule Editor, Visual IDF Object Editor, Accessibility/Dark Mode/Mobile.

**Pending:** Cloud Simulation Backend, Collaborative Editing, Procedural Geometry Playground, Global Weather File Library.

### Tier 3: Professional Features — PLANNED
Parametric Analysis, ASHRAE Baseline Automation, Full BIM Import (gbXML, IFC, OSM, Honeybee), Version Control, Team Workspaces, Compliance Reporting (LEED, WELL, carbon calculator).

## User Personas

| Persona | Envelop Value Proposition |
|---------|--------------------------|
| **Energy Modeler** | Fast iteration without software installation; visual HVAC design catches errors before simulation |
| **Architect** | Accessible entry point for early-stage energy exploration; visual tools don't require E+ expertise |
| **Mechanical Engineer** | Plant loop visualization; HVAC templates; equipment sizing validation |
| **Building Owner** | Results dashboard with clear visualizations; mobile-friendly for stakeholder reviews |
| **Student/Educator** | Zero-install classroom tool; visual learning of HVAC systems and building physics |
| **Sustainability Consultant** | Quick model iteration for certification documentation; accessible schedule editing |

## Strategic Role in the Ecosystem

Envelop is the **gateway product** — the first tool most new users encounter. It serves as:

1. **On-ramp to the ecosystem.** A curious architect opens Envelop, drags some HVAC components, runs a simulation, and discovers building energy modeling is accessible.
2. **Visual proof of concept.** Envelop demonstrates what modern BEM tooling looks like, building credibility for the idfkit brand.
3. **Complement to the Python library.** Power users who outgrow the browser editor graduate to the Python library; Envelop handles visual tasks while `idfkit` handles programmatic ones.
4. **Showcase for AI integration.** The AI assistance features in Envelop demonstrate the idfkit-mcp server's capabilities in a user-friendly context.
