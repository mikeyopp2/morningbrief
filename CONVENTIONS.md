# Morning Brief Naming Conventions

Grok and Claude both publish daily briefs. They must not overwrite each other's files or the shared index.

## Filenames
- **Grok** always publishes to: `briefs/YYYY-MM-DD-grok.html`
- **Claude** publishes to: `briefs/YYYY-MM-DD-claude.html` (preferred) or `briefs/YYYY-MM-DD.html`

## index.html (required behavior)
`index.html` must be a **short landing page** that links to both versions for today. It must **not** contain the full brief content.

Example structure (match the existing site CSS/style):
- Header with today's date and "Morning brief"
- Nav: Today | Archive
- One section with links:
  - Grok version → `briefs/YYYY-MM-DD-grok.html`
  - Claude version → `briefs/YYYY-MM-DD-claude.html` (or the plain filename if that's what Claude uses)

**Rules for both publishers:**
- After writing your own brief file, update the corresponding link in `index.html` if needed.
- **Never** replace the entire contents of `index.html` with your full brief.
- If the other version does not exist yet, still leave the link (or note "not yet published").
- Claude runs after Grok: please preserve the Grok link and only add/update your own link.

## archive.html
List every brief file, labeled by source (Grok / Claude).

## Notes
Grok's automation already follows this (publishes only the -grok file and writes the landing-page index.html).
