# idfkit — Company Overview

## Identity

**idfkit** is a non-profit software organization whose mission is to democratize building energy modeling and accelerate building decarbonization worldwide. We build and maintain a suite of open-source tools built around EnergyPlus — the U.S. Department of Energy's flagship building energy simulation engine.

**Structure:** Non-profit first
**License:** MIT (all projects)
**Tagline:** Modern tools for building energy simulation

## Mission

idfkit exists to improve the lives of engineers, researchers, and analysts who work with building energy models. We do this by building and maintaining world-class open-source tools that are fast, correct, accessible, and free — permanently. As a non-profit, our obligation is to the public good: lowering barriers, advancing building science, and accelerating the transition to net-zero buildings.

## The Problem We Solve

Building energy modeling — the practice of simulating a building's thermal, lighting, and HVAC performance before (or after) construction — is critical to decarbonizing the built environment. Buildings account for 37% of global energy-related CO2 emissions, yet the tools available to modelers are decades behind the state of the art in software:

- **Steep learning curves.** EnergyPlus is powerful but unforgiving. Its text-based input format (IDF) has thousands of object types, arcane naming conventions, and error messages that assume expert knowledge.
- **Fragmented tooling.** Modelers cobble together text editors, spreadsheets, custom scripts, and legacy Python libraries (eppy, opyplus) that are slow, poorly maintained, or architecturally limited.
- **No modern developer experience.** There is no autocomplete, no type inference, no visual editing, no AI assistance, and no in-browser simulation. The tools assume a workflow from 2005.
- **Access barriers.** Most commercial BEM tools are expensive, Windows-only, and unavailable in the Global South — precisely where 60% of the world's 2060 building stock hasn't been built yet.

## The Ecosystem

idfkit addresses these problems through five interconnected products:

| Product | What It Is | Key Differentiator |
|---------|------------|-------------------|
| **idfkit** | Core Python library | 4,000x faster than eppy, zero dependencies, O(1) lookups |
| **Envelop** | Browser-based visual editor | Zero-install, WebAssembly EnergyPlus, HVAC node-graph |
| **idfkit-mcp** | AI integration (MCP server) | 25 tools for AI agents, works with Claude & Codex |
| **idfkit-lsp** | VS Code Language Server | Autocomplete, hover docs, type inference for idfkit Python |
| **idfkit.com** | Marketing website | Ecosystem showcase, documentation hub |

## Target Users

| Persona | Description | Primary Goals |
|---------|-------------|---------------|
| **Energy Modeler** | Professional creating detailed building energy models for code compliance, certifications, and design optimization | Accuracy, efficiency, compliance documentation |
| **Architect** | Design professional exploring energy implications of design decisions early in the process | Quick feedback, design iteration, visual communication |
| **Mechanical Engineer** | HVAC system designer who needs to size equipment and validate system performance | System optimization, equipment selection, load calculations |
| **Building Owner / Facility Manager** | Non-technical stakeholder who needs to understand building performance and make investment decisions | Clear insights, cost analysis, actionable recommendations |
| **Student / Educator** | Learner or instructor exploring building science concepts | Learning, experimentation, concept visualization |
| **Sustainability Consultant** | Professional focused on certifications, carbon reduction, and ESG reporting | Compliance documentation, carbon accounting, benchmarking |

## Market Context

- **Market size:** $1.85B (2024), projected $5.32B by 2033, at 12.4% CAGR
- **Key trends:** AI/ML integration, cloud-based solutions, real-time modeling, IoT integration, whole-building lifecycle analysis
- **Standards landscape:** ASHRAE 90.1, Title 24, IECC, LEED, BREEAM, EDGE, Passive House, WELL
- **Competitors and peers:** OpenStudio (DOE-backed, Ruby/C++), eppy (legacy Python), IDF+ (commercial editor), Modelkit (Ruby), EP-Launch (DOE utility), Ladybug/Honeybee (Grasshopper/Rhino)

## Competitive Advantages

1. **Performance.** idfkit's dictionary-based architecture delivers O(1) object lookups — 4,000x faster than eppy for common operations.
2. **Zero dependencies.** The core library has no required third-party dependencies, eliminating dependency conflicts.
3. **Dual format.** Native support for both IDF (text) and epJSON (structured) formats with seamless round-tripping.
4. **AI-native.** idfkit-mcp makes idfkit the best-instrumented building energy library for AI agents, with 25 structured MCP tools covering the full EnergyPlus workflow.
5. **Browser-native.** Envelop runs entirely client-side — no server, no installation, no license. WebAssembly EnergyPlus simulation in the browser.
6. **Version breadth.** Supports EnergyPlus 8.9 through 25.2 (16 versions), because real projects span years.
7. **Non-profit alignment.** Free forever. No upsell, no feature gating, no telemetry. The tools serve users, not shareholders.

## Organizational Sustainability

As a non-profit, idfkit's sustainability depends on diversified funding rather than revenue:

- **Government grants:** DOE SBIR/STTR, NSF CSSI, EU Horizon Europe
- **Foundation grants:** Sloan Foundation, Chan Zuckerberg Initiative, NumFOCUS
- **Institutional partnerships:** Universities, national labs, ASHRAE, IBPSA
- **Corporate sponsorships:** MEP firms, simulation tool vendors, energy consultancies
- **Community contributions:** Individual donations, volunteer contributors
- **Ethical earned revenue:** Training, consulting, hosted services at cost — never at the expense of the commons

## Operating Principles

1. **Mission over revenue.** Every decision is evaluated first by whether it serves the people who model buildings and the planet those buildings sit on.
2. **Specificity over platitudes.** We reference actual EnergyPlus workflows, real user pain points, and concrete product features. We do not deal in generalities.
3. **Tradeoffs over consensus.** Our value is in naming tensions clearly — technical purity vs. shipping speed, domain fidelity vs. simplicity, organizational survival vs. maximum access.
4. **Action over deliberation.** Every discussion ends with a recommendation the team can act on.
5. **Transparency and stewardship.** We govern an open-source commons. Our decisions, rationale, and dissents should be legible to the community we serve.

## Climate Impact Thesis

Buildings account for 37% of global energy-related CO2 emissions. 60% of the world's building stock in 2060 hasn't been built yet, and most of it will be in the Global South. By making high-quality building energy modeling tools free, fast, and accessible worldwide, idfkit aims to:

- Lower the barrier for modelers in underserved regions to optimize building designs
- Reduce modeling errors that lead to underperforming buildings
- Expand the population of people who can competently model building energy performance from ~500 top-tier specialists to the ~50,000 the world needs
- Enable AI agents to handle routine modeling tasks, freeing human experts for higher-order design decisions
- Provide the infrastructure for climate-conscious building design at global scale
