---
title: Move work with rebase
description: Choose a source scope, a destination, and a placement before rewriting the graph.
order: 4
---

Use rebase to move work to a different point in the graph. Start with a mutable source and a visible
destination. Inspect their descriptions and diffs first. Separate filesystem workspaces share the
repository graph, so a rebase can affect work in another workspace.

## Move one change onto a new parent

For a change that needs a different parent while its descendants remain at the old location:

1. Press `c` to clear marks, select the source, and press `R`.
1. In the destination picker, keep **revision** scope and **onto** placement.
1. Move with `j`/`k` or Up/Down to the destination. `/` searches the visible candidates by description
   or commit ID; finish the search before choosing mode keys.
1. Press `Enter` to open the preview. Check Source, Source role, Destination, Destination role, and
   the exact command.
1. Press `Enter` again to execute, or `Esc` to cancel.
1. Inspect the source's new parent edge and the old location's descendants. Open `C`, then `o` on the
   mutation record, to inspect the resulting operation.

With no marks, the cursor supplies the source. An alternative is to mark one source with `Space`,
move the cursor to the intended destination, and press `R`; the picker starts from that destination.
Multiple marks are rejected. Clear the extra marks and reopen the picker.

The default command uses `jj rebase -r SOURCE -o DESTINATION`. It moves the source revision and
reconnects its descendants to its old parents. If you mean to move a stack together, change the
source scope before confirming.

## Choose the source scope

Choose how much history to move with these keys. Finish any active search first.

| Key | Scope       | jj form     | Affected work                             |
| --- | ----------- | ----------- | ----------------------------------------- |
| `r` | Revision    | `-r SOURCE` | The selected revision.                    |
| `b` | Branch      | `-b SOURCE` | The branch relative to the destination.   |
| `s` | Descendants | `-s SOURCE` | The source and all of its descendants.    |

Revision scope reconnects descendants to the old parents. Branch scope is destination-relative and
includes applicable ancestors and descendants. Choosing a different destination can change which
ancestors belong to the moved branch. Descendants scope starts at the selected source. Check the
broader graph before using either one; selecting a single row does not limit these modes to a single
change.

## Choose where to insert it

Each source scope can be combined with each of these placement modes:

| Key | Placement | jj form          | Consequence                                    |
| --- | --------- | ---------------- | ---------------------------------------------- |
| `o` | Onto      | `-o DESTINATION` | The destination becomes the new parent.        |
| `A` | After     | `-A DESTINATION` | Also rewrites existing descendants.            |
| `B` | Before    | `-B DESTINATION` | Also rewrites the destination and descendants. |

After and Before can rewrite changes associated with other workspaces. A sibling workspace does not
isolate its history from those graph changes. If you only want to start new work from an existing
change, use [New](../shape-changes/#start-a-new-change).

## Cancel or correct the selection

`Esc` while searching exits search. `Esc` outside search closes the picker. `Esc` from the command
preview cancels the pending command; no rebase is submitted. Opening the picker and preview does not
rewrite the graph, although ordinary log loading can snapshot working-copy edits.

The picker searches the currently visible log and selects one destination. If the target is missing,
cancel, widen or change the log scope, then begin again. The picker
[cannot accept an arbitrary repository-wide revset](../audit/#ux-07-rebase-destination-discovery).
Multiple destinations and an interactive graph preview are unavailable.

The source and destination are resolved to full commit IDs in the preview. Moving the cursor later
cannot retarget that preview. Concurrent jj work can still change the repository while you are
reading it; cancel and refresh when the surrounding graph no longer matches your intent.

## Diagnose and recover

Immutable revisions remain protected by jj. A rejection is recorded in `C` with diagnostics. If a
rewrite of immutable history is intentional, open `o` from the preview for [Run
Options](../run-options/), enable the override, apply it, and review the changed command
before confirming. An override is not needed for ordinary mutable work.

A successful rebase can produce content conflicts. Inspect the moved changes' diffs and `s` for the
working copy. Native conflict resolution and foreground merge-tool handoff are unavailable. Resolve
outside jk, then refresh and inspect the result.

For an unintended successful rebase, inspect its operation in Command History before using Undo. If
other operations occurred afterward, inspect the [operation log](../recovery/) to choose which
operation to reverse; repeated undo can affect unrelated work.
