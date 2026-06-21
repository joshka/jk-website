#!/usr/bin/env bash
set -euo pipefail

repo="${1:-${JK_HOMEPAGE_DEMO_REPO:-/tmp/jk-homepage-demo}}"

rm -rf "$repo"
mkdir -p "$repo"
jj git init "$repo" >/dev/null
cd "$repo"

jj config set --repo signing.behavior drop
jj config set --repo ui.default-command 'log -r "all()" -n 12'

mkdir -p src docs .github/workflows
cat > README.md <<'EOF'
# Acme CLI

Small command line tool used to demonstrate jk's log-first workflow.
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
- `Enter` expands the selected change
- `d` opens the selected diff
- `-` folds the current hunk
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
cat >> docs/keys.md <<'EOF'
- `?` opens contextual help
- `/` searches within the rendered view
EOF

jj log -r 'all()' --no-graph -T 'change_id.short() ++ " " ++ description.first_line() ++ "\n"' >/dev/null
