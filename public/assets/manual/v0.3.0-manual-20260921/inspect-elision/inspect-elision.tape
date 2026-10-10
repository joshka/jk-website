Env JK_SOURCE_REPO "/home/runner/work/jk/jk"
Env JK_BIN "/home/runner/work/jk/jk/target/manual-build/jk"
Env JK_MANUAL_ARTIFACT_DIR "/home/runner/work/jk/jk/target/manual-ci/inspect-elision"
Env JK_MANUAL_SCENARIO "inspect-elision"
# Manual scenario: inspect-elision
Require jj
Set Shell "bash"
Set Theme "Aardvark Ink"
Set FontSize 20
Set Width 1400
Set Height 840
Set Padding 0
Set Margin 20
Set WindowBar Colorful
Set BorderRadius 8
Set CursorBlink false
Set Framerate 15
Set KeyboardOverlay Input
Set TypingSpeed 70ms
Set WaitTimeout 30s

Hide
Type@0ms "source \"${JK_SOURCE_REPO:-$PWD}/scripts/manual-fixture.sh\" inspection"
Enter
Wait+Screen "JK_FIXTURE_READY"
Type@0ms "jj -R \"$repo\" config set --repo revsets.log '@'; clear; \"$bin\" -R \"$repo\" -n 8"
Enter
Wait+Screen "Experiment with forecast caching"
Show

Caption "A ~ row means this log omits revisions. Move onto it to inspect the missing history."
Wait+Screen /~/
Sleep 2500ms
Screenshot "/home/runner/work/jk/jk/target/manual-ci/inspect-elision/inspect-elision-hidden.png"
State "/home/runner/work/jk/jk/target/manual-ci/inspect-elision/inspect-elision-hidden.json"
Type "j"
Sleep 2s
Enter
Wait+Screen "Configure request timeouts"
Caption "Enter expands the omitted ancestry in a narrower log view."
Sleep 2500ms
Screenshot "/home/runner/work/jk/jk/target/manual-ci/inspect-elision/inspect-elision-expanded.png"
State "/home/runner/work/jk/jk/target/manual-ci/inspect-elision/inspect-elision-expanded.json"
Caption "Left returns to the earlier log. Right can reopen the selected omitted section."
Left
Wait+Screen /~/
Sleep 2s
Right
Wait+Screen "Configure request timeouts"
Sleep 2s
Backspace
Wait+Screen /~/
Caption "For an arbitrary revset, command mode retains ordinary jj log output."
Type ":"
Type "log -r 'all()' --no-graph"
Enter
Wait+Screen "Status: success"
Wait+Screen "Document the forecast service"
Sleep 2500ms
Screenshot "/home/runner/work/jk/jk/target/manual-ci/inspect-elision/inspect-elision-command-revset.png"
State "/home/runner/work/jk/jk/target/manual-ci/inspect-elision/inspect-elision-command-revset.json"
Caption "Backspace returns from retained command output to the same native log."
Backspace
Wait+Screen "Experiment with forecast caching"
Wait+Screen /~/
Sleep 2s
Caption ""
Hide
Type "q"
Sleep 300ms
Type@0ms "source \"$source_repo/scripts/manual-assert.sh\" inspection inspect-elision"
Enter
Wait+Screen "JK_ASSERTIONS_PASSED"
Type "exit"
Enter
