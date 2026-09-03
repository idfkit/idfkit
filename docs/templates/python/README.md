# No custom Python templates, deliberately

`custom_templates` in `mkdocs.yml` is a plugin-level setting, not a per-handler one, so
mkdocstrings looks for `<custom_templates>/<handler>/<theme>` for **every** handler it loads and
raises `FileNotFoundError` when the directory is missing. The TypeScript handler needs one
overridden template, `templates/typescript/material/dispatch.html.jinja`; the Python handler needs
none and uses its packaged defaults.

This directory exists so that the Python handler finds an empty theme directory and falls through
to those defaults. Adding a template here overrides the packaged one, which is almost certainly not
what you want: the Python reference is generated and unstyled on purpose.
