---
title: Inspect changes and compare content
description: Review the graph, revision details, diffs, file changes, and a change's evolution.
order: 2
---

In an existing jj repository, use the log to choose `@` or another visible revision, `Enter` to read
its details, and `d` to review its content. `Backspace` returns to your previous place in the preceding
view. In ordinary rendered inspection output, `Esc` quits jk; dialogs and search prompts handle it
separately.

## Read more or less graph detail

Start explicit log output with a limit or a jj template:

```sh
jk log -n 40
jk log -T 'builtin_log_oneline'
```

The top-level `jk -n 40` limits the configured default view. A limit on `jk log` takes precedence
over a top-level limit. `H` returns to the configured default command, while `L` chooses explicit
`jj log`.

Press `V`, select Template, and press `Enter`. Choose configured, comfortable, compact, compact with
full descriptions, detailed, oneline, or redacted, then press `Enter` to load it. A custom template
supplied with `-T` remains available in that session's selector. `Esc` closes a selector without
applying its current choice. Rendering and revision identity are read separately, so changing the
displayed template does not turn description text into mutation operands.

Use `l` or Right to expand a revision's inline details and `h` or Left to collapse them. When the
cursor is on an elided portion of the graph, `Enter` or Right opens its omitted history. `Backspace`
or Left returns to the preceding graph scope.

There is no general revset input for the native log. For an ad hoc query, press `:` and run `log -r
'mine()'`; its result is captured command output. It does not become a navigable native log. To make
a revision available to a native picker, first make it visible through the configured log scope or a
broader log view.

## Review revision details and status

From the log, press `Enter` on the change to see jj's description and patch. To start directly with
one or several revisions, use:

```sh
jk show @
jk show @ @-
```

Press `s` from the log to see the working-copy status. The cursor does not change which workspace
status describes. A startup status command can narrow the displayed files:

```sh
jk status
jk status 'glob:src/**'
```

Status filesets filter the report; they do not select content for a later squash or restore. Compare
status with `d` on `@` when you need to see the content behind a changed filename.

In rendered inspection views, `j`/`k`, Page Up/Down, and `g`/`G` move through the output. `/` opens
search; enter text and press `Enter`, then use `n`/`N` to visit matches. `Esc` closes the search
prompt. `r` reloads the same query.

## Compare one change or two trees

From the log, `d` compares the selected change with its parent content. These startup forms make the
comparison explicit:

```sh
jk diff
jk diff -r @-
jk diff @-
jk diff --from @- --to @
```

Bare `jk diff` uses `@`. The positional revision is a compatibility form of `-r`. A two-tree
comparison requires both `--from` and `--to`; it cannot be combined with a revision operand. The
comparison displays what differs between the trees, which can differ from a change's own patch when
the two revisions are on different branches.

The diff title identifies the revision or from/to pair. For file navigation and folding, press `V`
and choose Color words:

1. Press `f` to choose a file from the file list; move with the arrows and press `Enter`.
1. Use `[` and `]` to move between files.
1. Press `h` to fold the current file or `l` to unfold it.
1. Use Ctrl-Left or Ctrl-Right to fold or unfold all files, and `<`/`>` to scroll horizontally.
1. Search with `/`, `Enter`, then `n`/`N` when the patch is too large to read linearly.

Folding and file selection change only the display. They do not stage files or narrow a mutation.
`Esc` closes the file list without changing the chosen file.

## Change the diff format

Press `V` in a diff and choose its format. The query's revision or from/to operands stay the same.
The startup flags provide the same formats; choose one flag at a time.

| Format       | Startup option  | Use it to see                                      |
| ------------ | --------------- | -------------------------------------------------- |
| Patch        | No format flag  | The patch using jj's configured default rendering. |
| Stat         | `--stat`        | The amount of changed content per file.            |
| Summary      | `--summary`     | Added, modified, and removed paths.                |
| Types        | `--types`       | File types before and after the change.            |
| Name only    | `--name-only`   | Changed paths without patch content.               |
| Git          | `--git`         | A Git-format patch.                                |
| Color words  | `--color-words` | Word-oriented changed content.                     |

For example, `jk diff --from @- --to @ --stat` summarizes that same comparison. File navigation
currently recognizes Color words headers. Git-format patches can display correctly while the file
picker says “No files”; file jumps and folding are unavailable for that format. Select Color words to
use file controls. Patch depends on jj's configured rendering.

The advertised `{`/`}` hunk jumps and `-`/`+` hunk folding do not work on ordinary Color words or Git
output: the parser requires both Color words file headers and Git-style hunk headers in the same
output. Use scrolling or search to review the content within a file. These are tracked as a
[format-navigation defect](../audit/#ux-17-diff-format-navigation).

Native diff startup does not accept fileset operands; use a captured `:diff -r @ 'glob:src/**'` query
for filtered output.

## Follow a change through rewrites

Select the change in the log and press `v`. The evolution log shows earlier versions of that change,
which is useful after describe, rebase, squash, or another rewrite. This is the history of a
change's versions; [Operation Log](../recovery/) records repository operations.

Use the displayed commit IDs to identify versions. To compare their patches, run
`interdiff --from OLD --to NEW` in command mode, replacing `OLD` and `NEW` with the exact revisions
you inspected. The result uses captured output with search and return controls; jk has no native
interdiff picker.

## Verify the query and handle failures

Check the title and `C` history record if the output describes the wrong revision or workspace.
Cancel a selector with `Esc`; inspection does not need an undo. Ordinary jj inspection can snapshot
working-copy edits, so operation history may record that snapshot.

A missing or ambiguous revision, invalid template, or invalid fileset is reported by jj. Read the
retained diagnostics, correct the query, and retry. From captured command output, `e` reopens the
input. For native startup operands, quit and restart with the corrected arguments. If another
process rewrote the graph, refresh before choosing a new mutation target.
