# Game Server Validation

Follow the instruction guide "game-server-validation.md" located in this directory.

This will get your local GitHub Actions set to validate that your game client is working.

This is an important check, as when we begin making database changes, we might make a change which breaks not only your own server, but anyone's server who pulls your un-verified PR. This catches these types of problems.

# GitHub Workflow Trigger
│
├──▶ .github/workflows/validate-eqemu.yml
│     - Triggers on push or manual dispatch
│     - Runs on: self-hosted, windows, local-game-server
│
├──▶ validate-eqemu.ps1
│     - Top-level controller
│     - Calls start-eqemu.ps1
│     - Waits for login confirmation
│     - Calls stop-eqemu.ps1 at end
│
├──▶ start-eqemu.ps1
│     - Starts VM: Backup-Eulogy-quest-local-server (via VBoxManage)
│     - Waits for SSH readiness using `whoami` check
│     - Starts EQEmu server via SSH:
│           cd ~/opt/akk-stack && make up && make bash + start
│     - Waits for at least 25 zone processes to come online
│     - Launches AutoHotKey login script:
│
│       └──▶ login.ahk
│            - Launches EverQuest via shortcut (includes "patchme")
│            - Sends keypresses to:
│                - Accept EULA
│                - Submit credentials
│                - Enter server and character
│            - Uses WinActivate/WinWaitActive to ensure focus
│
│     - validate-eqemu.ps1 resumes:
│         - Monitors eqlog\_Kharvey_*.txt
│         - Looks for "Welcome to EverQuest!" with a recent timestamp
│         - Marks login as [PASS] or [FAIL]
│
├──▶ stop-eqemu.ps1
│     - Calls AutoHotKey logout script:
│
│       └──▶ exitEq.ahk
│            - Sends /exit and Enter to log out the character
│     - SSHes into VM and gracefully shuts down EQEmu server
│     - Powers off the VM (via VBoxManage)
│
└──▶ GitHub Action exits with success/failure code
      - GitHub UI shows ✅ or ❌
      - Logs include full PowerShell + AHK output

