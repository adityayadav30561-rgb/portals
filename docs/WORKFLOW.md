# Workflow

How the work is run so the session can be cleared after every phase and the next one resumes from the files alone.

## Session protocol

**Start**
1. Read [CLAUDE.md](../CLAUDE.md), then [STATUS.md](STATUS.md) (where we are, what is next).
2. Read the current phase in [PLAN.md](PLAN.md) section 5, and [DECISIONS.md](DECISIONS.md) before any design change.
3. Open the screens already built in a browser before editing; for the visual language, look at `mavro-ai/prototype/`
   (read only).

**During**
- Read [DATA.md](DATA.md) before building screens: the products, prices, people, number series and formats every screen must reuse.
- Authoring aids for generating screen HTML are in `tools/author/` (shared data and helpers, one script per phase). The generated HTML is the source of truth afterwards.
- One phase per session. Content and screens come from the registry (`assets/registry.js`), never duplicated.
- When the user states a preference, add it to DECISIONS.md immediately.

**End of a phase (checkpoint)**
1. Run `node tools/verify.js <screenshot folder> <ID prefix>`: opens every built screen for every role over `file://` at 1440, 1366 × 768 and 390 px and fails on console errors, horizontal scroll, tables scrolling inside cards on desktop, dead or `#` links, missing font, abbreviations in the rendered text. Then look at the screenshots yourself.
2. Regenerate `docs/SCREEN-INVENTORY.md` from the registry (once it exists, Phase 1) and mark the phase's screens
   as Built.
3. Update [STATUS.md](STATUS.md): what was done, what is next, open items; tick the phase in PLAN.md.
4. Commit with a clear message and push to the session branch (see DECISIONS.md).
5. Tell the user it is a good point to clear the session.

**Where to clear context:** after a phase is committed and documented; after a review round has been applied and
recorded in DECISIONS.md; never in the middle of a multi-file change.

## Advisor

The session has an `advisor` tool (a stronger model that sees the whole conversation). Call it before starting a
phase's work (approach check) and again after the phase is committed, before telling the user it is done. Fix its
findings or record them in STATUS.md.
