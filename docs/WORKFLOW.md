# Workflow

How the work is run so the session can be cleared after every phase and the next one resumes from the files alone.

## Session protocol

**Start**
1. Read [CLAUDE.md](../CLAUDE.md), then [STATUS.md](STATUS.md) (where we are, what is next).
2. Read the current phase in [PLAN.md](PLAN.md) section 5, and [DECISIONS.md](DECISIONS.md) before any design change.
3. Open the screens already built in a browser before editing; for the visual language, look at `mavro-ai/prototype/`
   (read only).

**During**
- One phase per session. Content and screens come from the registry (`assets/registry.js`), never duplicated.
- When the user states a preference, add it to DECISIONS.md immediately.

**End of a phase (checkpoint)**
1. Check every new screen in the browser at 1440 px, 1366 × 768 and 390 px widths: no horizontal page scroll, no
   console errors, no abbreviations or filler text.
2. Regenerate `docs/SCREEN-INVENTORY.md` from the registry (once it exists, Phase 1) and mark the phase's screens
   as Built.
3. Update [STATUS.md](STATUS.md): what was done, what is next, open items; tick the phase in PLAN.md.
4. Commit with a clear message and push to the session branch (see DECISIONS.md).
5. Tell the user it is a good point to clear the session.

**Where to clear context:** after a phase is committed and documented; after a review round has been applied and
recorded in DECISIONS.md; never in the middle of a multi-file change.

## Reviews by an advisor

At the phase 1 and 2 checkpoints (foundations, first design approval) and at the end of the last phase, the work is
reviewed by a second, stronger model before the user is asked to approve: coverage against the brief, naming rules,
consistency of the design system. Findings are fixed or recorded in STATUS.md.
