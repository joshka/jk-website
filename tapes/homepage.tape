Output public/assets/jk-homepage.gif
Output target/betamax/homepage-final-state.json

Require cargo
Require jj

Set Shell "bash"
Set Theme "Aardvark Ink"
Set Width 1200
Set Height 690
Set Padding 0
Set Margin 0
Set WindowBar Colorful
Set BorderRadius 0
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
Type "demo=${JK_HOMEPAGE_DEMO_REPO:-/tmp/jk-homepage-demo}"
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

Type "\"$jk_source/target/debug/jk\" -R \"$demo\""
Enter
Wait+Screen "jk jj"
Sleep 900ms
Show

Type "j"
Sleep 450ms
Type "j"
Sleep 650ms
Enter
Sleep 900ms
Type "r"
Sleep 700ms
Type "d"
Wait+Screen "jk jj diff"
Sleep 1000ms
Type "?"
Sleep 700ms
Type "?"
Sleep 300ms
Type "/"
Sleep 250ms
Type "refresh"
Enter
Sleep 800ms
Type "}"
Sleep 650ms
Type "-"
Sleep 900ms
Type "+"
Sleep 550ms
Type "H"
Wait+Screen "jk jj"
Sleep 900ms
Type "L"
Wait+Screen "jk jj log"
Sleep 700ms
