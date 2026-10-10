---
title: Start with a repository
description: Open jk, read the graph, choose revisions, and understand when an action changes history.
order: 1
---

Open a jj working directory with `jk`. Use `jk log` when you want the log even if your jj
configuration has a different default command.

```sh
jk
jk log
jk -R /path/to/repository log -n 30
```

The examples use a jk 0.3.0 source checkout with jj 0.45.1. Check `jk --version` and `jj --version`
when a key or command differs from a recording. Use the [command reference](../reference/) to check
whether a command runs natively, through captured command mode, or in a terminal outside jk.

## Read the graph before changing it

Start in a repository with a working-copy change and some existing history. jj owns the changes,
bookmarks, operations, and workspace metadata; jk renders jj output and adds navigation and actions.
There is no staging area to prepare before editing or reshaping changes.

Three different objects matter when choosing an action:

- **Working copy (`@`)** is the change associated with this workspace's files.
- **Cursor** is the revision you are looking at. Moving it does not edit that revision.
- **Marks** are an ordered list of changes you choose with `Space`. An action decides whether those
  marks are parents, sources, or invalid input.

Move with `j`/`k` or the arrow keys. Press `g`/`G` for the first or last row, and Page Up/Down to
move through a larger graph. Press `Space` to mark or unmark a change; `c` clears all marks. Mark
order matters when you create a change with multiple parents or choose several squash sources.

Press `Enter` to inspect the revision under the cursor. Return with `Backspace`. `d` opens its diff,
`s` opens workspace status, and `v` opens its evolution log. Inspection views do not have the log's
revision action menu.

A normal log load or refresh lets jj snapshot working-copy files. Looking at the graph can therefore
record edits made outside jk, just as an ordinary `jj log` can. Moving the cursor, marking
revisions, and opening a confirmation do not themselves apply a history rewrite.

## Find a control

Press `?` for the active view's help. The keys in the footer belong to the active view or dialog;
uppercase and lowercase keys have different meanings. For example, `r` refreshes the log, `R` starts
rebase, and `a r` means press `a` to open the action menu, then `r` to choose Restore.

From the log, `a` opens the action menu. Move with `j`/`k` and press `Enter`, or press the key shown
beside an action. `Esc` closes the menu. The menu states whether an action runs immediately or opens
a confirmation. New, Edit, Undo, Redo, and abandonment of an empty change run immediately.

From the log, `B` opens bookmarks, `W` opens workspaces, `o` opens the operation log, and `C` opens
Command History. `H` switches to the configured default view; `L` switches to explicit log output.
`q` quits jk. Use `Backspace` to return from an inspection view without quitting.

## Check a preview before confirming

Rebase, squash, restore, bookmark mutations, and remote operations show a command preview. Check the
repository, operands, scope, and exact command. `Enter` executes it; `Esc` cancels. Arrow keys and
Page Up/Down scroll a long preview. `y` copies its command line; it does not confirm these previews.
[Abandon](../shape-changes/#abandon-a-change) and [workspace
actions](../workspaces/) have their own confirmation controls.

After execution, inspect the result in the graph or relevant list. Open `C` to inspect the actual
argv, diagnostics, and exit status. A history record can link to the resulting jj operation with
`o`. A success message reports the command's exit status; check the affected changes or files to
verify its result.

If a preview no longer matches the work you want to do, cancel and select its operands again. If an
executed command changed the wrong thing, use [operation recovery](../recovery/) after
checking what the operation changed.

## Choose a readable display

The log and normal diff views retain jj's colors and rendered output. Press `V` in the log to change
its template, or in a diff to change its format. These choices change presentation, not history.

Dialogs detect the terminal's light or dark background at startup. Override the detection when the
surface is hard to read:

```sh
jk --dialog-theme light
jk --dialog-theme dark
```

The setting affects jk dialogs; it does not replace jj's graph colors or your terminal background.
Enlarge the terminal if a confirmation says it cannot show its decision controls. Do not infer that
an off-screen command has run.

## Recover from startup or refresh failure

Use `jk -R /path/to/workspace log` to make the repository explicit. In this source version with
jj 0.45.1, automatic child-workspace selection fails in a repository container without its own
working copy. The `No working copy.` status is not recognized, so opening the container does not
select a usable child workspace. This is a
[startup defect](../audit/#ux-18-container-workspace-resolution).

If the container has a child working directory named `default`, start it explicitly:

```sh
jk -R default
jk -R default workspaces
```

Replace `default` with the actual workspace directory, or change into that directory before starting
jk. Verify the workspace path and working-copy change before running a mutation.

Press `r` to refresh after an external edit. A log refresh runs in the background; you can keep
moving through the last usable graph. Another `r` supersedes the previous refresh. A failure leaves
the last usable graph visible and records its diagnostics in Command History. Fix the reported jj or
repository problem and refresh again; do not interpret retained rows as a fresh successful load.
