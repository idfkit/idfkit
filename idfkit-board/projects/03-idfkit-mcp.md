# Project: idfkit-mcp — AI Integration via Model Context Protocol

## Summary

**idfkit-mcp** is a production-ready MCP (Model Context Protocol) server that gives AI agents structured, schema-aware access to the full EnergyPlus model lifecycle. It exposes 25 tools in 6 categories, enabling LLM-powered workflows for schema discovery, model creation and editing, validation, weather acquisition, and simulation.

**Repository:** `idfkit/idfkit-mcp`
**Language:** Python 3.10+
**License:** MIT
**Install:** `uvx idfkit-mcp`
**Clients:** Claude, Codex, and any MCP-capable agent

## The 25 Tools

### Schema Exploration (4 tools)
| Tool | Purpose |
|------|---------|
| `list_object_types` | List all available EnergyPlus object types for the loaded schema version |
| `describe_object_type` | Get the full field contract for one object type — field names, types, units, defaults, min/max, choices, required/optional |
| `search_schema` | Search object types by name or memo text (fuzzy matching) |
| `get_available_references` | Resolve valid reference values from the current model for a given reference type |

### Model Read (6 tools)
| Tool | Purpose |
|------|---------|
| `load_model` | Load an IDF or epJSON file into active server state |
| `get_model_summary` | Summarize the loaded model: object counts by type, version, statistics |
| `list_objects` | List all objects of a given type with their names and key fields |
| `get_object` | Fetch one object by type and name, returning all field values |
| `search_objects` | Search model objects by substring across names and field values |
| `get_references` | Inspect inbound and outbound references for a specific object |

### Model Write (8 tools)
| Tool | Purpose |
|------|---------|
| `new_model` | Create a new empty model for a specified EnergyPlus version |
| `add_object` | Add a single object with specified field values |
| `batch_add_objects` | Add multiple objects in one call (preferred for bulk creation) |
| `update_object` | Update specific fields on an existing object |
| `remove_object` | Remove an object, optionally forcing removal even if referenced |
| `rename_object` | Rename an object and cascade the name change to all references |
| `duplicate_object` | Clone an existing object to a new name |
| `save_model` | Save the current model to IDF or epJSON format |

### Validation (2 tools)
| Tool | Purpose |
|------|---------|
| `validate_model` | Full schema validation — field types, required fields, ranges, choices |
| `check_references` | Detect dangling references (objects that reference names that don't exist) |

### Simulation (3 tools)
| Tool | Purpose |
|------|---------|
| `run_simulation` | Execute EnergyPlus simulation with the current model and weather file |
| `get_results_summary` | Summarize the results of the most recent simulation run |
| `list_output_variables` | Enumerate available output meters and variables |

### Weather (2 tools)
| Tool | Purpose |
|------|---------|
| `search_weather_stations` | Find weather stations by location name or coordinates |
| `download_weather_file` | Download EPW and DDY files, returning cached local paths |

## Recommended Workflow

```
1) new_model(version="24.1.0")         # or load_model(path="...")
2) describe_object_type(type="Zone")    # Understand the schema before editing
3) batch_add_objects(objects=[...])      # Prefer batched writes
4) validate_model(check_references=True) # Always validate after writes
5) download_weather_file(query="Chicago") # Acquire weather data
6) run_simulation(annual=True)           # Run E+ simulation
7) get_results_summary()                 # Inspect results
```

## Global Best Practices

1. **Use schema tools before mutations.** Always call `describe_object_type` before adding or editing objects to understand field contracts.
2. **Prefer batched writes.** Use `batch_add_objects` instead of multiple `add_object` calls to reduce round-trips and maintain consistency.
3. **Validate immediately after writes.** Call `validate_model` after any mutation to catch errors early.
4. **Run simulation only after model health checks pass.** Ensure validation and reference checks are clean before invoking `run_simulation`.
5. **Treat each server session as stateful and sequential.** The MCP server maintains state (loaded model, simulation results) across tool calls within a session.

## Architecture

The MCP server is built on top of the core `idfkit` library. It wraps idfkit's Python API in structured MCP tool definitions with:

- **Typed parameters:** Every tool has a well-defined parameter schema that LLMs can populate reliably.
- **Structured responses:** Tools return structured data (JSON objects, lists, summaries) rather than free text.
- **Error semantics:** Predictable error categories (validation errors, not-found errors, simulation failures) with actionable messages.
- **Server state management:** The server maintains an in-memory model and simulation result that persist across tool calls.

## Agent Workflow Documentation

The project includes documentation for specific agent platforms:
- **Codex workflows:** Patterns for OpenAI Codex agents
- **Claude workflows:** Patterns for Anthropic Claude agents
- **Multi-agent patterns:** Orchestration strategies for complex modeling tasks using multiple specialized agents

## Strategic Role in the Ecosystem

idfkit-mcp is the **AI integration layer** — it makes the entire idfkit ecosystem accessible to AI agents:

1. **Accessibility multiplier.** An architect who can't write Python can ask an AI agent to "add a variable refrigerant flow system to zones 3 through 7" and get a correct EnergyPlus model.
2. **Strategic moat.** With 25 purpose-built tools, idfkit-mcp makes idfkit the best-instrumented building energy library for AI agents. This advantage compounds as more agents adopt it.
3. **Human-in-the-loop design.** AI agents draft and execute operations, but the modeler reviews, validates, and approves. The tool design encourages this pattern (validate after write, check references, review results).
4. **Ecosystem bridge.** MCP tools can invoke the same operations available in the Python library and visualized in Envelop, creating a consistent experience across all interfaces.
