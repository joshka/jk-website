Output public/assets/jk-homepage-manual-v0.3.0-r3.gif
Output target/betamax/homepage-manual-v0.3.0-r3-final-state.json

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
Env JJ_CONFIG "/dev/null"
Env GIT_CONFIG_NOSYSTEM "1"
Env GIT_CONFIG_GLOBAL "/dev/null"

Hide
Type "site=${JK_WEBSITE_REPO:-/Users/joshka/local/jk-website}"
Enter
Wait
Type "jk_source=${JK_SOURCE_REPO:-/Users/joshka/local/jk/default}"
Enter
Wait
Type "demo=$(mktemp -d /tmp/jk-homepage-manual.XXXXXX)"
Enter
Wait
Type "cd \"$site\" && mkdir -p public/assets target/betamax"
Enter
Wait+Line
Type "cargo build --manifest-path \"$jk_source/Cargo.toml\" -p jk >/tmp/jk-homepage-build.log 2>&1 && echo JK_BUILD_READY"
Enter
Wait+Screen "JK_BUILD_READY"
Type "scripts/create-homepage-demo.sh \"$demo\" >/tmp/jk-homepage-demo.log 2>&1 && echo JK_DEMO_READY"
Enter
Wait+Screen "JK_DEMO_READY"
Ctrl+L
Sleep 200ms

Type "cd \"$demo\" && \"$jk_source/target/debug/jk\""
Enter
Wait+Screen "Document refresh workflow"
Sleep 900ms
Show
Sleep 2s

Type "a"
Sleep 3s
Screenshot public/assets/jk-homepage-manual-v0.3.0-r3-actions.png
State target/betamax/homepage-manual-v0.3.0-r3-actions.json
Escape
Sleep 800ms
Enter
Wait+Screen "jk jj show"
Sleep 3s
Type "H"
Wait+Screen "Document refresh workflow"
Sleep 700ms
Type "d"
Wait+Screen "jk jj diff"
Sleep 2500ms
Ctrl+Left
Sleep 1000ms
Ctrl+Right
Sleep 900ms
Type "h"
Sleep 900ms
Type "l"
Sleep 700ms
Type "?"
Sleep 4s
Type "?"
Sleep 300ms
Type "]"
Sleep 700ms
Type "]"
Sleep 700ms
Type "h"
Sleep 900ms
Type "l"
Sleep 550ms
Type "/"
Sleep 250ms
Type "refresh"
Enter
Sleep 800ms
Screenshot public/assets/jk-homepage-manual-v0.3.0-r3.png
State target/betamax/homepage-manual-v0.3.0-r3.json
Hide
Type "q"
Sleep 300ms
