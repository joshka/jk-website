Output public/assets/jk-recent-features.gif
Output target/betamax/recent-features-final-state.json

Require cargo
Require jj

Set Shell "bash"
Set Theme "Aardvark Ink"
Set Width 1200
Set Height 720
Set Padding 0
Set Margin 20
Set WindowBar Colorful
Set BorderRadius 8
Set CursorBlink false
Set TypingSpeed 24ms
Set WaitTimeout 30s
Env NO_COLOR "1"

Hide
Type "site=${JK_WEBSITE_REPO:-/Users/joshka/local/jk-website}"
Enter
Wait
Type "jk_source=${JK_SOURCE_REPO:-/Users/joshka/local/jk/default}"
Enter
Wait
Type "demo=${JK_RECENT_FEATURES_DEMO_REPO:-/tmp/jk-recent-features-demo}"
Enter
Wait
Type "cd \"$site\" && mkdir -p public/assets target/betamax"
Enter
Wait+Line
Type "cargo build --manifest-path \"$jk_source/Cargo.toml\" -p jk >/tmp/jk-recent-features-build.log 2>&1 && echo JK_BUILD_READY"
Enter
Wait+Screen "JK_BUILD_READY"
Type "rm -rf \"$demo\" && mkdir -p \"$demo\" && jj git init \"$demo\" >/tmp/jk-recent-features-demo.log 2>&1 && cd \"$demo\""
Enter
Wait
Type "jj config set --repo signing.behavior drop >/tmp/jk-recent-features-demo.log 2>&1"
Enter
Wait
Type "jj config set --repo ui.default-command 'log -r \"root() | @\"' >>/tmp/jk-recent-features-demo.log 2>&1"
Enter
Wait
Type "printf '# Recent jk demo\n' > README.md && jj file track README.md >/tmp/jk-recent-features-demo.log 2>&1 && jj desc -m 'Initialize demo repo' >/tmp/jk-recent-features-demo.log 2>&1"
Enter
Wait
Type "for n in 1 2 3 4 5 6 7 8; do jj new -m \"Add graph polish sample $n\" >>/tmp/jk-recent-features-demo.log 2>&1; printf 'sample %s\n' \"$n\" >> README.md; done && jj bookmark set main -r @ >>/tmp/jk-recent-features-demo.log 2>&1 && echo JK_DEMO_READY"
Enter
Wait+Screen "JK_DEMO_READY"
Ctrl+L
Sleep 200ms

Type "\"$jk_source/target/debug/jk\" -R \"$demo\""
Enter
Wait+Screen "jk jj"
Sleep 900ms
Show

Type "j"
Sleep 600ms
Type "l"
Wait+Screen "Add graph polish sample"
Sleep 1100ms
Backspace
Sleep 700ms
Type "q"
Wait+Line
Type "\"$jk_source/target/debug/jk\" -R \"$demo\" workspaces"
Enter
Sleep 1200ms
Type "?"
Sleep 1700ms
