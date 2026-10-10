---
title: Inspect results and recover
description: Find executed commands, inspect repository operations, and undo or redo with context.
order: 7
---

Command History records the commands jk ran during this session and keeps their results in memory.
Operation Log records changes to repository state and persists across sessions.

## Inspect a command's result

After a mutation or failure, press `C`.

1. Select the command record with `j`/`k` or the arrows.
1. Press `Enter` to inspect its argv, output, exit status, duration, and operation metadata.
1. Return with `Backspace`. Press `y` in the history list to copy the recorded command line.
1. Press `o` on the record to inspect its resulting operation. If no operation ID was captured,
   this opens Operation Log instead.

From a record's details, `Backspace` returns to the history list; press it again to return to the
view that opened history. `Esc` in the details quits jk. `Esc` in the history list returns instead.

A failed command's stderr often explains an immutable revision, invalid revset, missing path,
workspace collision, remote error, or unavailable executable. Read that diagnostic before retrying.
A nonzero exit or spawn failure is not a successful mutation. Some commands can perform partial
external work before failing, so inspect the affected filesystem or remote when relevant.

History includes inspection and refresh commands as well as mutations. Select the command that
caused the result you are investigating. History redacts recognized secret patterns in argv and
output; it is not a persistent transcript. Keep the relevant diagnostic separately if you need it
after quitting jk.

## Inspect repository operations

Press `o` from the log to open Operation Log. Move to the operation you want to inspect. `Enter`
opens `jj op show`; `d` opens its operation diff. Search, paging, refresh, and `Backspace` work as
in other rendered views.

An operation can rewrite several changes or update bookmarks and workspace metadata. Inspect that
whole result before deciding to reverse it. A description edit may rewrite descendants, and a rebase
with insertion can affect another workspace's changes.

Operation show and diff are native inspection forms. Operation restore, integrate, and specialized
operation display flags have no native chooser; use explicit captured jj commands when needed.

## Undo the last operation

Inspect the most recent operation in Operation Log before undoing it.

1. Return to the log.
1. Press `a u` to run `jj undo` immediately.
1. Inspect the refreshed graph and the affected file content, bookmark, or workspace entry.
1. Open `C` to inspect the undo command and its resulting operation.

Undo reverses the last operation under jj's undo semantics, regardless of the log cursor. Cancel the
action menu with `Esc` before selecting Undo if you need to inspect the operation first. There is no
separate native confirmation.

If undo fails, inspect the history record and the current operation log. Do not repeat the action
without checking what jj reports. Unrelated operations or concurrent work can change the appropriate
recovery choice.

## Redo an undo

Press `a U` from the log to run `jj redo` immediately. It redoes the most recently undone operation
when jj can do so. Verify the same affected objects again and inspect the command record. If the
repository has moved beyond a redoable state, retain the diagnostic and choose an explicit recovery
from the operation history.

Undo and redo act on repository state. They do not reverse a remote push, delete newly created
workspace directories, or reverse arbitrary side effects of an external command.

## Inspect or restore a particular historical state

Copy an operation ID from the operation log. In command mode, replace `OPERATION` below with that
specific ID:

```text
:--at-operation OPERATION log
```

This inspects the repository at that operation and ignores the current working-copy files. Compare
that output with the current graph before deciding whether you want to restore it.

```text
:op restore OPERATION
```

Operation restore creates a new operation that brings repository state back to the selected earlier
state, effectively reversing later operations. It has broader scope than undoing a recent mistake.
Command mode executes on Enter without a native restoration confirmation. Cancel its input with
`Esc` if the operation ID or intended scope is uncertain. After success, return to the log, refresh,
and verify the graph, bookmarks, working copy, and any affected workspaces.

If you have the ID of an operation that was created without integration, inspect it first with
`--at-operation`. `:op integrate OPERATION` makes that operation part of the operation log. This is
a separate action from restoring the entire repository to its state. Run Options does not offer
detached operations or a native integrate workflow.

## Recover without losing the failure context

Native rebase, squash, and restore retain failures in Command History. After a failed refresh, the
log or bookmark list still shows the last successful query; it may omit later repository changes.

Resolve the reported cause, refresh, and reselect operands before a new mutation. When an external
tool changed files, inspect status and diff after returning. When a command changed a remote or the
filesystem, verify those objects directly in addition to checking jj's operation history.
