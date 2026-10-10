---
title: Work across workspace directories
description: Inspect, add, rename, update, and forget jj workspaces.
order: 6
---

Press `W`, or start with `jk workspaces`, to list the repository's jj workspaces. A workspace is a
working directory with its own working-copy change. Workspaces share repository history; rewriting
an ancestor can affect changes used by other workspaces.

Start from a working directory or specify one explicitly. With this source version and jj 0.45.1,
automatic startup from a repository container without a working copy fails to select its child
workspace. From a container whose working directory is `default`, use `jk -R default workspaces`.
Replace `default` with the actual directory and verify the selected workspace's path. See the
[container-startup defect](../audit/#ux-18-container-workspace-resolution).

## Inspect another workspace without changing directories

Begin with two workspace entries and select the one you want to inspect.

- Press `l` for its log.
- Press `Enter` or `s` for its status.
- Press `d` for its working-copy diff.
- Press `Backspace` to return to the workspace list, and `r` to refresh that list.

These views are scoped to the selected workspace's root. Its log is a rendered inspection view, not
the main navigable revision log; use explicit `:show scratch@` or `:evolog -r scratch@` commands for
further inspection, replacing `scratch` with that workspace's name. Check the path in the title
before acting on what you see. Opening another workspace's status does not switch the shell's
current directory or the repository used by `:` and `!`. For a command that must operate on that
directory, specify `-R` explicitly in a jj command or reopen jk with that workspace as its startup
scope. The [command prompt does not show this
scope](../audit/#ux-12-command-scope-visibility). If its directory is missing, jk reports
the error and keeps the list open; restore the directory or choose whether its metadata should be
forgotten.

Press `a` in the workspace list to open lifecycle actions for the selected workspace.

## Add a workspace for separate work

Choose a workspace to use as the path context. Press `a a`, then enter a destination path such as
`../review-copy`. A relative destination is resolved against the selected workspace's root. The
final path component supplies the new workspace name.

1. Read the selected workspace and root in the input form.
1. Enter the destination and press `Enter` to prepare the command.
1. Check the resolved destination, name, and exact `jj workspace add` command.
1. Press `Enter` to execute, or `Esc` to cancel.
1. Verify the new list row, inspect its status, and check that the directory exists.

The native form supplies the destination and name. Creation revisions, a creation message, or sparse
patterns require an explicit noninteractive jj command. If you undo an addition, check whether its
directory remains before removing any files.

An existing destination, name collision, invalid path, or permissions problem can make add fail.
Read the retained diagnostic and reopen Add to enter a corrected destination. A failed action
[loses its input draft](../audit/#ux-10-workspace-retry-state). Check whether it created a directory
before reusing its path.

## Rename a workspace

Select it, press `a r`, and enter the new workspace name. `Enter` prepares the command; another
`Enter` executes it after review. `Esc` cancels either stage.

Rename changes jj's workspace name; its directory path stays the same. Verify the new name in the
list and the same root path in its inspection view. A duplicate name is rejected by jj; the error
remains available in Command History. Reopen Rename and enter a corrected name; a failed rename
does not retain the input draft. To reverse an unwanted successful rename, rename it back or inspect
the operation before selecting recovery.

## Update a stale workspace

After a graph rewrite from another workspace, a working directory can be stale relative to the
repository's current operation. Select that workspace and press `u`, or use `a u`.

Read the preview's workspace name and path. `Enter` runs `jj workspace update-stale` with that
workspace as its repository scope; `Esc` cancels. The command can update that directory's files to
match its working-copy state.

After success, open its status and diff and verify that the stale warning is gone and its content is
correct. If jj reports a missing directory, concurrent change, or another failure, retain the
message from `C`, resolve the cause, and refresh before retrying. Inspect the operation history
before reversing a successful update.

## Forget workspace metadata while keeping files

Use Forget when jj should stop tracking a workspace entry. Select it and press `a f`.

The preview names the workspace and explains the metadata scope. Press `Enter` to confirm or `Esc`
to cancel. The entry disappears from the refreshed list. **Its directory and files remain on disk.**
This action is separate from abandoning the working-copy change or deleting a directory.

Verify both results: the workspace row is gone, and any files you intended to keep still exist. Keep
the directory until you have checked the outcome. If you forgot the wrong entry, inspect the
operation in `C` and use jj operation recovery as appropriate before doing further cleanup.

Workspace confirmations also accept `y` to run and `n` to cancel. Their arrow and Page Up/Down keys
scroll long command text. If the terminal is too small to display a decision, enlarge it before
confirming. Run Options does not apply to workspace commands.

## Check failure and recovery in context

Open `C` after a lifecycle action to read its exact repository argument, command, output, and
status. Use `o` on the record for the captured resulting operation; if none is available, jk opens
Operation Log. Inspect both the shared graph and the affected directory when recovering. Undoing
repository metadata cannot be assumed to undo unrelated file edits or remove a directory created by
add.
