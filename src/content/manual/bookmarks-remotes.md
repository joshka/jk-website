---
title: Name changes and check remotes
description: Create, move, and delete local bookmarks, fetch an explicit remote, and inspect a push dry-run.
order: 5
---

Press `B` from the log to inspect bookmarks. Start with a repository containing a change you want to
name. Fetch and push dry-run also require a configured Git remote; the remote can be a local test
repository or an existing server.

The list includes local and remote bookmarks, tracking state, deleted local bookmarks, and
conflicts. A remote row is not a local bookmark you can move. Native move, delete, and push dry-run
require an unambiguous local row with one target.

## Inspect the target before changing a name

Move with `j`/`k` or the arrows. Press `Enter` to inspect an available unambiguous target, then
`Backspace` to return. `r` reloads the list; `Esc` returns to the previous view. Press `?` for bookmark
help. The `a` key [opens an invisible workspace-context action
menu](../audit/#ux-11-bookmark-context-routing) on this screen. Press `Esc` to exit that hidden mode
if the normal keys stop responding.

A bookmark names a revision. Moving that name does not rebase the revision, edit its description, or
switch this workspace's working copy. Deleting the local name does not abandon its target change.

## Create a local bookmark

1. Press `c` in the bookmark list.
1. Type the name. Press Tab to reach the target revision field, which initially contains `@`.
1. Keep `@` or replace it with the intended revision. Ctrl-u clears the focused field; Tab switches
   between the name and target.
1. Press `Enter` to open the preview, then read the name, target, and command.
1. Press `Enter` to create it, or `Esc` to return from the preview without executing.
1. Verify the new local row and inspect its target with `Enter`.

Create and move refresh the list after success
[without a success message](../audit/#ux-14-bookmark-result-feedback). Check the row and target to
confirm the result.

The native create form takes a typed revision expression. It does not automatically take the log's
cursor or marks as its target. Check the target field even when you arrived from the intended
change.

`Esc` closes the input form. Cancelling its preview retains the form so you can correct the fields.
An empty name or target is rejected before the command. If jj rejects the name, revision expression,
or existing bookmark, inspect `C` and correct the input before retrying.

## Move or delete a local bookmark

Select the local row and press `m` to move it. The target input starts at `@`; replace it when
another revision is intended. Press `Enter` to review the command, then `Enter` to run it. Refresh
and open the target to verify the name points at the intended change. jj can reject a move that
needs options the native form does not expose; read the diagnostic before deciding how to proceed.

To remove a local bookmark, select its row and press `x`. Read the destructive preview and press
`Enter` to delete, or `Esc` to cancel. Verify the local name is removed or shown in its tracked
deleted state. The target change remains in the graph. Deleting a local bookmark does not itself
contact a remote; a later publication workflow can carry that deletion.

Conflicted, deleted, and remote-only rows cannot be treated as ordinary single-target local rows.
Inspect them first. Other bookmark operations, such as track, untrack, rename, and forget, are
available through noninteractive [command mode](../command-mode/), with jj's semantics.
Use the bookmark screen for create, move, and delete; `:` rejects those command families.

After an unintended local mutation, inspect its operation and use [operation
recovery](../recovery/). Recovery of repository metadata does not reverse changes already
published elsewhere.

## Fetch from a chosen remote

Use fetch when the repository should learn a remote's current state.

1. Press `F` in the bookmark list.
1. Choose a remote with `j`/`k` or the arrows. Configured remotes appear even if they have no bookmark
   rows yet.
1. Press `Enter` to preview the fetch. Merely choosing the remote has no network effect.
1. Check the selected remote, then press `Enter` again to run fetch.
1. Read the retained command output. Return to the bookmark list and inspect the refreshed rows.

`Esc` cancels the remote picker or the preview before fetch. Fetch can contact the selected remote
and updates local knowledge of its refs. It does not publish local bookmarks. Names are passed as
exact patterns so a wildcard in a name does not silently widen the selection.

If there are no remotes, configure one with jj before retrying. A failed
fetch retains stdout, stderr, and status in Command History. Check the remote configuration,
connectivity, and authentication outside jk as needed. Commands that need a foreground credential
prompt cannot use jk's captured input. If the list refresh fails after a fetch, jk preserves its
last usable snapshot; refresh again before treating it as current.

## Preview publication without publishing

Select a local bookmark with one target and press `P`. Choose the remote, press `Enter` for the
preview, then review the exact bookmark and remote scope. A second `Enter` runs the push dry-run.

The dry-run may contact that remote and report what jj would push. Remote refs remain unchanged,
including when the dry-run succeeds. Read the retained output and inspect `C` for the exit status.
`Esc` cancels either selection or confirmation before the dry-run starts.

Real push is unavailable in the native interface and rejected by jj command mode, including attempts
to enter `git push --dry-run` there. Leave jk to publish with the jj CLI,
then return and refresh. Preserve the bookmark and remote you reviewed; do not replace the scoped
operation with a broad push. Native tags, remote management, and publication confirmation remain
separate gaps in the [coverage map](../coverage/).
