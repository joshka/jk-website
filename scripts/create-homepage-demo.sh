#!/usr/bin/env bash
set -euo pipefail

repo="${1:?usage: create-homepage-demo.sh EMPTY-DISPOSABLE-DIRECTORY}"

mkdir -p "$repo"
if [[ -n $(ls -A "$repo") ]]; then
    printf 'Refusing to replace a nonempty demo directory: %s\n' "$repo" >&2
    exit 1
fi
export JJ_CONFIG=/dev/null
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
jj git init "$repo" >/dev/null
cd "$repo"

jj config set --repo user.name 'Manual Demo'
jj config set --repo user.email 'manual@example.invalid'
jj config set --repo signing.behavior drop
jj config set --repo ui.color always
jj config set --repo ui.default-command '["log", "-r", "all()", "-n", "12"]'

mkdir -p src docs .github/workflows
cat > README.md <<'EOF'
# Acme CLI

Small command line tool used to demonstrate jk's jj-native workflow.
EOF
cat > src/main.rs <<'EOF'
fn main() {
    println!("acme deploy");
}
EOF
cat > docs/release.md <<'EOF'
# Release Checklist

- run smoke tests
- publish binaries
EOF
jj file track README.md src/main.rs docs/release.md >/dev/null
jj desc --message "Initialize deploy tool" >/dev/null
jj bookmark set main -r @ >/dev/null

jj new -r main --message "Add command palette filter" >/dev/null
cat > src/palette.rs <<'EOF'
pub fn filter_commands(query: &str, commands: &[&str]) -> Vec<String> {
    commands
        .iter()
        .filter(|command| command.contains(query))
        .map(|command| command.to_string())
        .collect()
}
EOF
perl -0pi -e 's/fn main\(\) \{\n    println!\("acme deploy"\);\n\}/mod palette;\n\nfn main() {\n    let commands = ["deploy", "rollback", "status"];\n    for command in palette::filter_commands("de", &commands) {\n        println!("{command}");\n    }\n}/' src/main.rs
jj file track src/palette.rs >/dev/null
jj bookmark set feature/palette-filter -r @ >/dev/null

jj new --message "Polish diff folding keys" >/dev/null
cat > docs/keys.md <<'EOF'
# Keys

- `j` and `k` move between changes
- `Enter` opens the selected change details
- `d` opens the selected diff
- `h` folds the current file
- `r` refreshes the repository view
EOF
jj file track docs/keys.md >/dev/null
jj bookmark set feature/diff-folding -r @ >/dev/null

jj new --message "Prepare v0.3 release" >/dev/null
cat > .github/workflows/release.yml <<'EOF'
name: release

on:
  push:
    tags:
      - 'v*'

jobs:
  package:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: cargo build --release
EOF
perl -0pi -e 's/- publish binaries/- publish binaries\n- verify homepage media/' docs/release.md
jj file track .github/workflows/release.yml >/dev/null
jj bookmark set release/v0.3 -r @ >/dev/null

jj new --message "Document refresh workflow" >/dev/null
cat > docs/keys.md <<'EOF'
# Keys

The log view keeps common navigation close to the home row.

## Log navigation

- `j` and `k` move between changes
- `g` jumps to the top of the rendered log
- `G` jumps to the bottom of the rendered log
- `Space` and `b` move by page
- `Enter` opens the selected change details
- `d` opens the selected diff
- `r` refreshes the repository view

## Diff review

- `j` and `k` move between rendered lines
- `[` and `]` move between files
- `h` folds the current file
- `l` unfolds the current file

## Overlays

- `?` opens contextual help
- `/` searches within the rendered view
- `H` returns to the configured home command
- `L` switches to an explicit `jj log`
EOF
cat >> README.md <<'EOF'

## Daily Workflow

Keep the log open beside an editor, make a change, then press `r` to refresh the view without
losing the selected change.
EOF
perl -0pi -e 's/let commands = \["deploy", "rollback", "status"\];/let commands = [\n        "deploy",\n        "rollback",\n        "status",\n        "refresh",\n    ];/' src/main.rs
cat >> docs/release.md <<'EOF'
- refresh the homepage capture after UI changes
- confirm generated media is not an LFS pointer
EOF
mkdir -p examples
cat > examples/refresh-session.txt <<'EOF'
$ jk
select Document refresh workflow
press d to inspect the current change
press r after the editor writes files
EOF
jj file track examples/refresh-session.txt >/dev/null

jj log -r 'all()' --no-graph -T 'change_id.short() ++ " " ++ description.first_line() ++ "\n"' >/dev/null
