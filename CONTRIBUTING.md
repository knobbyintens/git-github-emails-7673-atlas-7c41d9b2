# Documentation workflow

1. Source modules are written with `# atlas-anchor:` tags on the lines the index
   should point at.
2. `catalog/index.md` is regenerated from the tags whenever a module's layout
   changes. Only the numeric locator may change; descriptions and entry order
   stay as published.
3. Component notes under `docs/notes/` follow the tier recorded in
   `catalog/owners.yaml`. Public-tier components get a manual re-verification
   line each docs sprint. Internal-tier notes belong to the nightly docs bot and
   are never hand-edited.
4. One commit per documentation file keeps the docs audit trail readable.
