# GitHub Workflow Trigger
│<br>
├──▶ .github/workflows/validate-eqemu.yml<br>
│     - Triggers on push or manual dispatch<br>
│     - Runs on: self-hosted, windows, local-game-server<br>
│<br>
├──▶ validate-eqemu.ps1<br>
│     - Top-level controller<br>
│     - Calls start-eqemu.ps1<br>
│     - Waits for login confirmation<br>
│     - Calls stop-eqemu.ps1 at end<br>
│<br>
├──▶ start-eqemu.ps1<br>
│     - Starts VM: Backup-Eulogy-quest-local-server (via VBoxManage)<br>
│     - Waits for SSH readiness using `whoami` check<br>
│     - Starts EQEmu server via SSH:<br>
│           cd ~/opt/akk-stack && make up && make bash + start<br>
│     - Waits for at least 25 zone processes to come online<br>
│     - Launches AutoHotKey login script:<br>
│<br>
│       └──▶ login.ahk<br>
│            - Launches EverQuest via shortcut (includes "patchme")<br>
│            - Sends keypresses to:<br>
│                - Accept EULA<br>
│                - Submit credentials<br>
│                - Enter server and character<br>
│            - Uses WinActivate/WinWaitActive to ensure focus<br>
│<br>
│     - validate-eqemu.ps1 resumes:<br>
│         - Monitors eqlog\_Kharvey_*.txt<br>
│         - Looks for "Welcome to EverQuest!" with a recent timestamp<br>
│         - Marks login as [PASS] or [FAIL]<br>
│<br>
├──▶ stop-eqemu.ps1<br>
│     - Calls AutoHotKey logout script:<br>
│<br>
│       └──▶ exitEq.ahk<br>
│            - Sends /exit and Enter to log out the character<br>
│     - SSHes into VM and gracefully shuts down EQEmu server<br>
│     - Powers off the VM (via VBoxManage)<br>
│<br>
└──▶ GitHub Action exits with success/failure code<br>
      - GitHub UI shows ✅ or ❌<br>
      - Logs include full PowerShell + AHK output<br>
<br>
