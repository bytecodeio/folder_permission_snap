# Looker Folder Permission Isolation

Tooling to temporarily move a set of Looker dashboards/looks into a locked-down, view-only folder for review or testing, then move them back to exactly where they came from once you're done.

## What it does

1. **Snapshot** — records the current folder each target dashboard/look lives in, and writes it to `content_snapshot.json`.
2. **Isolate** — creates a single new folder, breaks its permission inheritance, downgrades every access entry on it to view-only (so nobody can edit the content while it's isolated), moves all the target dashboards/looks into it, and writes the new folder's ID to `isolation_state.json`.
3. **Restore** — reads both JSON files back from disk, moves everything back to its original folder, then verifies the isolation folder is empty and deletes it.

Each phase reads its inputs from those JSON files rather than from variables left over in memory, so Phase 3 can be run in a completely separate session — a different day, a different machine, even a different person — as long as `content_snapshot.json` and `isolation_state.json` are kept handy in between.

The permission downgrade step handles a real Looker quirk: Looker refuses to set a folder to view-only for a group/user that already has edit access on the folder's parent. When that happens, the notebook automatically finds the blocking parent, temporarily downgrades it, applies the change, and restores the parent back to normal — a snapshot of anything it touches is written to `permission_snapshots/` first, so nothing is ever changed without a recorded way back.

## Files

- `looker_folder_lifecycle_single_folder.ipynb` — the notebook. Run its cells top to bottom, phase by phase (Snapshot → Isolate → Restore).
- `setup_credentials.py` — run this first to interactively create your `looker.ini` credentials file.
- `test_connection.py` — quick read-only check that your credentials work before running the notebook for real.
- `looker.ini.example` — template showing the shape of the credentials file `setup_credentials.py` creates.
- `requirements.txt` — Python dependencies (`looker_sdk`).

## Setup

```bash
pip install -r requirements.txt
python setup_credentials.py
python test_connection.py
```

Then open `looker_folder_lifecycle_single_folder.ipynb` and run the cells in order.

## Notes

- Dashboard IDs can be either their real numeric ID or their slug (from the dashboard's URL) — both are accepted. Look IDs must be the real numeric ID; Looker has no slug lookup for looks.
- Looker Admin users always retain full access regardless of the view-only lock — that's inherent Looker behavior, not a gap in this tool.
- Never commit your real `looker.ini` — it contains a live API secret. It's already excluded via `.gitignore`.
