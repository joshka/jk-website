Env JK_SOURCE_REPO "/home/runner/work/jk/jk"
Env JK_BIN "/home/runner/work/jk/jk/target/manual-build/jk"
Env JK_MANUAL_ARTIFACT_DIR "/home/runner/work/jk/jk/target/manual-ci/manual-run-options-historical"
Env JK_MANUAL_SCENARIO "manual-run-options-historical"
Env JK_MANUAL_PREPARED_FIXTURE "/home/runner/work/jk/jk/target/manual-ci/manual-run-options-historical/fixture-env.sh"
# PreparedFixture run-options
Require jj
Set Shell "bash"
Set Theme "Aardvark Ink"
Set FontSize 20
Set Width 1400
Set Height 900
Set Padding 0
Set Margin 20
Set WindowBar Colorful
Set CursorBlink false
Set Framerate 15
Set KeyboardOverlay Input
Set TypingSpeed 80ms
Set WaitTimeout 45s
Hide
Type@0ms "source \"${JK_SOURCE_REPO:-$PWD}/scripts/manual-fixture.sh\" run-options"
Enter
Wait+Screen "JK_MANUAL_FIXTURE_READY"
Type@0ms "jj -R \"$repo\" bookmark create after-baseline -r @- >/dev/null 2>&1; clear; \"$bin\" -R \"$repo\" -n 8"
Enter
Wait+Screen "Rebase source"
Show
Sleep 2s
Caption "Run a rebase from a recorded operation while preserving later repository work."
Type "R"
Wait+Screen "Choose rebase destination"
Type "/Rebase destination"
Enter
Wait+Screen "Source role:"
Type "o"
Wait+Screen "Run options"
Type "j"
Enter
Type "844cd0328e09a3fa729680e7091c0b7ddd6b489ced36211c13c062452b0890e027cf64171d8df80e89cfb17f312895f09810b139bacdc18267a6589ae0877898"
Enter
Sleep 1s
Screenshot "/home/runner/work/jk/jk/target/manual-ci/manual-run-options-historical/manual-run-options-historical-operation.png"
State "/home/runner/work/jk/jk/target/manual-ci/manual-run-options-historical/manual-run-options-historical-operation.json"
Sleep 2s
Type "a"
Wait+Screen "--at-operation"
Wait+Screen "Ignores the current working-copy snapshot."
Caption "Historical mode skips working-copy snapshot and update; normal operation integration remains enabled."
Sleep 1s
Screenshot "/home/runner/work/jk/jk/target/manual-ci/manual-run-options-historical/manual-run-options-historical-preview.png"
State "/home/runner/work/jk/jk/target/manual-ci/manual-run-options-historical/manual-run-options-historical-preview.json"
Sleep 2s
Enter
Wait+Screen "Completed at historical operation"
Sleep 1s
Screenshot "/home/runner/work/jk/jk/target/manual-ci/manual-run-options-historical/manual-run-options-historical-completed.png"
State "/home/runner/work/jk/jk/target/manual-ci/manual-run-options-historical/manual-run-options-historical-completed.json"
Sleep 2s
Type "C"
Wait+Screen "Command History"
Caption "Select the rebase record to inspect the command that left the working copy unchanged."
Type "jj"
Enter
Wait+Screen "Source: log rebase"
Wait+Screen "Status: success"
Caption "Command History retains the successful command and its exact execution options."
Sleep 1s
Screenshot "/home/runner/work/jk/jk/target/manual-ci/manual-run-options-historical/manual-run-options-historical-operation-result.png"
State "/home/runner/work/jk/jk/target/manual-ci/manual-run-options-historical/manual-run-options-historical-operation-result.json"
Sleep 2s
Hide
Caption ""
Type "q"
Wait+Line
Type@0ms "source \"$source_repo/scripts/manual-assert.sh\" manual-run-options-historical"
Enter
Wait+Screen "MANUAL_ASSERT_OK manual-run-options-historical"
Type "exit"
Enter
