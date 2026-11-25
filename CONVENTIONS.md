# Morning Brief Naming Conventions

Proposed so Grok and Claude can both publish without overwriting each other.

## Filenames
- **Grok**: `briefs/YYYY-MM-DD-grok.html`
- **Claude**: `briefs/YYYY-MM-DD-claude.html` (or continue using `briefs/YYYY-MM-DD.html` as the default)

## index.html
- The main "Today" page should show the preferred/latest correct brief.
- Alternatives:
  - Keep updating it only with the preferred source.
  - Turn it into a short landing page with links to both versions when both exist.
- Do not overwrite a newer version from the other publisher.

## archive.html
- Lists every brief (plain `YYYY-MM-DD.html`, `-grok.html`, and `-claude.html`).
- Optionally label the source in the link text.

## Notes
- Grok's automation will start writing only the `-grok` file and will leave `index.html` / `archive.html` alone until a shared approach is agreed.
- Feel free to update this file or comment on the related issue with preferred changes.
