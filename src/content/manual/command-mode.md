---
title: Run commands with retained output
description: Use noninteractive jj and external commands, inspect their output, and recognize tool handoff limits.
order: 8
---

Press `:` for a jj command or `!` for an external executable. Both modes retain output inside jk and
record the result in Command History. They close stdin and do not provide a foreground terminal to
the child command.

## Run a jj query or mutation

Start in the repository you intend to inspect or change. Press `:`, enter a jj argument list, and
press `Enter`:

```text
:status
:log -r 'mine()'
:describe -m 'Explain the parser change' @
```

The leading colon represents the prompt key; type the command after it. A leading `jj` in the input
is optional. Quotes and backslashes group arguments, so a message with spaces remains one argument.
The parser does not start a shell.

Enter executes directly. There is no additional native preview for an arbitrary mutation. The log
cursor and marks do not become implicit operands; specify a revision, fileset, or operation where
needed. `Esc` cancels before execution, Ctrl-u clears the input, and Backspace edits it.

Opening a sibling workspace inspection does not switch the command prompt's repository. `:` still
uses the startup repository, and `!` still uses its startup working-directory scope. The prompt does
not show [which repository it targets](../audit/#ux-12-command-scope-visibility). Use an explicit
`-R` in a jj command or reopen jk for the intended workspace before running a mutation.

Read the command-output view's status, stdout, and stderr. `e` reopens the previous input for
editing or retry. `Backspace` returns to the preceding view; `Esc` quits jk from this output view.
Refresh the preceding view after a command that changed repository state; captured command mode does
not select a new native graph query for you.
`C` opens its history record and `y` in history copies the command line. The manual refresh
requirement is tracked as a [result refresh gap](../audit/#ux-09-command-result-refresh).

## Use noninteractive jj forms

These examples use jj 0.45.1 argument forms. Replace example paths, names, and revision expressions
with objects you have inspected. They execute real operations when submitted; none opens a native jk
workflow for the command family.

| Concern                    | Captured command example                                  |
| -------------------------- | --------------------------------------------------------- |
| Finish the current work    | `:commit -m 'Finish parser validation'`                   |
| Split a known file         | `:split -r @ -m 'Extract tests' tests/parser.rs`          |
| Move fixes into ancestors  | `:absorb --from @`                                        |
| List unresolved conflicts  | `:resolve --list -r @`                                    |
| Copy a change              | `:duplicate @-`                                           |
| Apply a reverse change     | `:revert -r @- -o @`                                      |
| Compare rewritten versions | `:interdiff --from OLD --to NEW`                          |
| Inspect tags               | `:tag list`                                               |
| Create a local tag         | `:tag set review-point -r @`                              |
| Track a remote bookmark    | `:bookmark track exact:incoming --remote exact:fixture`   |
| Stop tracking it           | `:bookmark untrack exact:incoming --remote exact:fixture` |

For commit, begin with the intended content in `@` and verify both the completed change and the new
working copy afterward. Selecting a different log revision does not make commit operate on it. For
split, begin with at least two separable pieces of content, pass a fileset and `-m`, then inspect
both resulting changes. Omitting the fileset starts an interactive diff editor, which captured mode
cannot host.

For absorb, begin with fixes whose destination ancestors are still mutable. Inspect those ancestors
and any content left in the source afterward; jj can leave edits it cannot assign unambiguously.
Duplicate creates a new change with the selected change's content; revert creates a reverse change
on the specified destination. Inspect their new graph positions and diffs. Use operation recovery
for an unintended successful local mutation. Resolve with `--list` only reports conflicts. Tag set
creates a local tag; inspect `:tag list` afterward. Track and untrack change a remote bookmark's
local tracking relationship; refresh `B` to verify it.

Fileset forms of squash and restore can also run as explicit noninteractive jj commands. Read the
installed command's help to choose its source and destination, and verify the selected paths after
execution. Native file and hunk selection is unavailable; no selection in jk's diff view is passed
to these commands.

## Use the dedicated bookmark and remote flows

Command mode rejects bookmark create, move, and delete, including their recognized short aliases. It
also rejects `git fetch` and `git push`, including push dry-run. Use the [bookmark
screen](../bookmarks-remotes/) for native create/move/delete, explicit remote fetch, and a
one-bookmark push dry-run. Real publication requires leaving jk.

Other noninteractive bookmark, tag, workspace, and operation commands remain captured alternatives.
They use jj's own argument rules and do not inherit the native forms' exact-name handling or
previews. Check patterns and operands before executing them.

## Run an external executable

Press `!` and enter an executable with explicit arguments:

```text
!printf '%s\n' 'hello from jk'
!rg -n 'TODO' src
```

The command runs with the repository path as its working directory when jk has an explicit
repository scope. Otherwise it inherits jk's process directory. It can read or change files
according to the program you choose. Inspect its output and exit status, then refresh the repository
view if it changed files.

Shell metacharacters such as `$`, `|`, `>`, and `&&` remain literal arguments. To request a shell,
invoke it explicitly:

```text
!sh -c 'printf "one\ntwo\n" | head -n 1'
```

Here the shell receives and interprets the quoted script. jk itself does not expand its variables,
pipeline, or redirection. An external command is not a repository undo boundary; recover its side
effects using the relevant program or files, then verify jj status.

## Handle parse and execution failures

An unfinished quote or dangling escape keeps the prompt open with an error. Fix the input or press
`Esc` to cancel. A missing executable produces a spawn error. A child that exits unsuccessfully
shows its exit code; on supported platforms, termination by a signal is identified separately.

Press `e` from the retained output to correct and retry. Do not retry a mutation merely because its
output was unexpected: inspect the affected objects and Command History first. History redacts
recognized secret patterns, but it remains a session-only record.

## Leave jk for an interactive tool

Foreground editors, interactive split or diffedit, merge tools, credential prompts, and full-screen
programs require a terminal handoff that jk does not implement. Quit jk with `q`, run the tool in
the intended workspace, then restart jk and inspect status and diff.

Supplying messages and filesets can make some commands noninteractive. It does not turn an editor or
merge tool into a supported captured workflow. The missing handoff and native forms are tracked in
the [UX audit](../audit/#ux-01-command-mode-tool-handoff) and [coverage
map](../coverage/).
