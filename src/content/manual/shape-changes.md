---
title: Create and reshape changes
description: Describe, create, edit, abandon, squash, and restore changes with explicit operands.
order: 3
---

Start with a small mutable change you can recognize by its description and diff. The log's `a` menu
contains revision actions. Move the cursor and marks before opening that menu: their roles differ
between actions, and the working-copy change is a separate object.

## Give a change a useful description

Select the revision and press `a m`. The inline editor starts with its existing description.

1. Edit the summary with the arrow keys and ordinary text editing controls.
1. Press Ctrl-j to add a line break. Enter alone saves.
1. Press `Enter` to run describe, or `Esc` to discard the draft.
1. Open the revision with `Enter` from the log and verify the complete description.

Ctrl-u clears the editor. Ctrl-z undoes an edit to the text; Ctrl-Shift-z redoes it. These are
editor operations before saving, separate from repository undo. Describing rewrites the selected
change's metadata and can rewrite descendants as jj propagates that change. It does not commit the
cursor's files into a new revision.

If jj rejects the description update, the editor retains the draft. Inspect the failure in `C` and
correct the repository problem before saving again. To reverse a successful save, inspect its
operation and use the [recovery workflow](../recovery/).

## Start a new change

Use New when you want a fresh working-copy change on one or several existing parents. With no marks,
the cursor is the parent. With marks, the ordered marked revisions are the parents.

1. Press `c` to clear old marks if you want a single parent.
1. Select the parent, or mark each intended parent with `Space` in the desired order.
1. Press `a n`. This executes immediately; there is no confirmation dialog.
1. Verify that `@` and the selection move to the new change and that its parent edges are correct.
1. Press `a m` to describe the new work, then edit files in your normal editor.

Multiple parents create a merge change. Its file content can contain conflicts that need resolution.
The action resolves the chosen parents to exact commit IDs before running `jj new`. A stale,
ambiguous, or divergent marked change must be reselected instead of being silently replaced by a
different revision.

`Esc` can cancel the action menu before you choose New; it cannot cancel an already executed New.
Use operation recovery if you created the wrong change. Advanced creation options, including
insertion and a message supplied with creation, require a noninteractive command such as `:new -m
'Start follow-up' @`. Read the displayed command and confirm its operands before pressing Enter in
command mode, because command mode executes directly.

## Resume editing an existing change

Use Edit when the files in this workspace should belong to an existing mutable change. Select it in
the log and press `a e`. Edit runs immediately, updates the workspace's `@`, and changes its files
to that change's content.

Verify the `@` marker, press `s` to inspect status, and inspect `d` before making more file edits.
Other changes stay in the repository. An immutable target is rejected by jj; read the error instead
of assuming the working copy moved. The action menu can be cancelled with `Esc` before choosing
Edit. For a successful but unintended switch, inspect the operation and undo it before continuing
work.

## Abandon a change

Abandon removes a change from the visible graph and rebases its descendants according to jj's rules.
It differs from deleting a bookmark, which removes a name, and forgetting a workspace, which removes
workspace metadata.

Select a change and press `a a`. jk checks whether it is empty. **An empty change is abandoned
immediately.** A non-empty change, or an unsuccessful emptiness check, opens a confirmation with
Cancel selected.

1. Read the revision identity and summary.
1. Use Left/Right or Tab to select View diff, then `Enter` to inspect the patch.
1. In the embedded diff, `Enter` or `Esc` returns to the summary; `n` cancels abandonment.
1. In the summary, choose Abandon and press `Enter`, or press `y` to confirm directly.
1. Verify that the change disappears and that its descendants have the intended parents.

In the summary, `n` or `Esc` cancels. Enlarge a terminal that cannot display the decision controls;
confirmation is disabled there. After a successful abandonment, use operation recovery to restore an
unintentionally abandoned change.

The embedded diff uses a fixed Git format and jk addition/deletion colors. It does not inherit the
normal diff view's configured presentation. If that makes the content harder to review, cancel,
inspect the change with `d`, then reopen abandonment. This presentation gap is tracked in the [UX
audit](../audit/#ux-05-abandon-diff-fidelity).

The native flow abandons one revision. Multi-revision abandonment is a captured command-mode form;
its Enter key executes without this native confirmation.

## Combine changes with whole-change squash

Use squash to move the content of one or more changes into an existing destination. Begin with
mutable source changes and a distinct destination. Review each source's diff first.

1. Clear unrelated marks with `c`.
1. Mark each source with `Space`, in the order you want it listed.
1. Move the cursor to the destination without marking it.
1. Press `a s` to open the preview.
1. Check every Source, the Destination, **whole changes**, and **keep destination description**.
1. Press `Enter` to execute, or `Esc` to cancel without squashing.
1. Inspect the destination's diff and description, then inspect the graph for removed sources or
   rewritten descendants.

Squash moves entire change contents. It keeps the destination description and lets jj handle emptied
sources and descendants. File-list selection, folded hunks, and diff search do not narrow its scope.
The graph reselects the destination after success.

A missing source mark, a destination also marked as a source, duplicate sources, or a stale marked
revision prevents preparation. Clear or repair those marks and reopen the preview. An immutable
revision or a jj execution failure remains inspectable in `C`. If changing immutable history is
intentional, [Run Options](../run-options/) provides a command-scoped override.

If the result is wrong, inspect the resulting operation before undoing. For only some files, use an
explicit noninteractive jj command with a fileset; native file and hunk squash are unavailable.
Interactive selection requires leaving jk for a foreground tool.

## Restore a whole tree into the working copy

Use Restore when `@` should receive all paths from another revision. For example, a mutable working
copy may contain an unwanted experiment, and an earlier revision has the tree you want back.

1. Press `c` to clear marks. Restore rejects marked inputs because it has one source.
1. Select the revision whose complete tree you want to copy.
1. Press `a r` and check the exact source, the `@` destination, and **all paths** scope.
1. Press `Enter` to execute, or `Esc` to cancel.
1. Inspect `s` and the diff of `@`, including files deleted or recreated by the copy.

Restore copies tree content; it does not move the working-copy parent or adopt the source
description. It can replace existing working-copy edits. The source is frozen to an exact commit,
while the native destination is the current workspace's `@`. Restore's Run Options keep the latest
operation so `@` does not become a historical working copy by accident.

On failure, inspect `C`, refresh if another process changed the repository, and select again. Use
operation recovery after an unwanted successful restore. A selected diff file does not limit this
operation. Filesets, alternate destinations, `--changes-in`, and hunk restore have no native form;
use an explicit noninteractive jj command for supported fileset forms or leave jk for interactive
selection.

## Finish or split work outside these native forms

Commit, split, absorb, duplicate, revert, and conflict resolution do not have native action dialogs.
Use [noninteractive commands](../command-mode/#use-noninteractive-jj-forms) where available.
`commit` acts on the working copy, regardless of which revision is under the log cursor. Foreground
editors, diff tools, and merge tools require leaving jk.
