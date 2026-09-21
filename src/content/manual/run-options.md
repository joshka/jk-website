---
title: Adjust one command's execution
description: Control working-copy updates, historical execution, and immutable protection on a pending mutation.
order: 9
---

From a rebase, squash, or restore preview, press `o` to open Run Options. Begin with a preview whose
repository and revision operands you have already checked. Options apply only to this pending
command. They do not change a repository setting or the defaults for the next command.

## Change and apply an option

1. Move through the options with `j`/`k` or Up/Down.
1. Press `Enter` on an option to toggle it or edit its value.
1. Press `a` to apply the draft to the command preview.
1. Read the updated exact command and warnings.
1. Press `Enter` in that preview to execute, or `Esc` to discard the pending command.

Applying options does not run the command. `Esc` inside the drawer discards the draft, including
while editing an operation ID. Cancelling the outer preview discards all its options. Page Up/Down
scroll long text while keeping the decision controls available.

The drawer shows the repository chosen when you selected the revisions. You cannot switch it here;
changing the repository would change the meaning of the selected objects.

## Decide whether to update working-copy files

The default working-copy policy lets jj snapshot current files and update them after a command that
changes the working copy. Choose Ignore to skip both snapshotting and updating those files.

Ignore is useful when you deliberately want the command to work with already recorded repository
content while leaving this directory untouched. It means unsnapshotted file edits are excluded from
the command's view of the working copy. After execution, inspect the resulting graph and the on-disk
files separately; they may intentionally describe different states.

The immediate graph refresh after an ignored-working-copy command also skips snapshotting. Later
ordinary refreshes return to normal jj behavior, so pressing `r` can snapshot those files again.
Command History retains the actual option and resulting diagnostic output.

## Run rebase or squash at a historical operation

Copy a specific operation ID from [Operation Log](../recovery/). In the drawer's operation
field, enter at least 12 hexadecimal digits. Press `Enter` to finish editing. Ctrl-u clears the
field to return to latest.

Historical execution loads that repository state and ignores working-copy files. It can create
concurrent history. The full commit operands chosen before opening the drawer remain fixed; an
operation ID does not re-resolve them into different revisions. jj fails if those commits are
unavailable in the chosen state.

Apply the option, then read the historical-execution warning and exact command before confirming.
After success, jk refreshes the latest graph without snapshotting. Inspect the resulting operation
and graph before another mutation. Use operation recovery if the historical command produced an
unintended result.

Restore keeps its latest-operation context. Its native destination is `@`; permitting a historical
operation would change which working-copy change that expression denotes. The drawer therefore does
not offer a historical restore destination.

## Allow a deliberate immutable rewrite

Immutable protection is enabled by default. Leave it enabled for ordinary mutable work. If a rewrite
of protected history is intentional, toggle the immutable option, apply it, and inspect the new
warning and `--ignore-immutable` flag in the command preview.

The override changes jj's protection check for this command. It does not select different operands,
remove content conflicts, or make a broader rebase safe for other workspaces. Verify all affected
changes afterward and keep the operation record available for recovery.

If the command fails despite an override, inspect jj's diagnostic in `C`; do not assume every
rejection was caused by immutable protection.

## Know which commands the drawer covers

Run Options is available for rebase, squash, and restore previews only. It does not configure New,
Edit, Describe, Abandon, workspace lifecycle commands, bookmark mutations, remote commands, captured
command mode, or external tools.

Repository switching, config overlays, config files, output policy, and detached operation creation
are not editable here. Existing configuration overlays and output settings are preserved. Use an
explicit jj command when a different supported command form is necessary, and inspect its complete
scope before running it.
