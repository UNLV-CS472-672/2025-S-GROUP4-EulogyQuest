# EQEmu GitHub Action: Local Runner Setup Guide

This guide helps team members set up a local GitHub Actions runner to validate EQEmu game server access using the automation scripts in this repo.

---

## ✨ Overview
This GitHub Action:
- Starts your local EQEmu server (in a VM)
- Launches your EverQuest client and logs in
- Verifies character login via log file
- Logs out and shuts everything down

Each team member sets up a self-hosted runner to run this check locally.

---

## ✅ 1. Clone the Repo and Locate Scripts

```bash
git clone git@github.com:your-org/akk-stack.git
cd akk-stack/Eulogy-Quest/eulogy-docs/local-game-server-validation-scripts
```

This folder contains:
- `validate-eqemu.ps1` (top-level orchestrator)
- `start-eqemu.ps1`
- `stop-eqemu.ps1`
- `login.ahk`
- `exitEq.ahk`

---

## ✅ 2. Environment Requirements

Make sure your local machine:
- Runs **Windows**
- Has **VirtualBox** installed
- Has a VM named `Backup-Eulogy-quest-local-server`
  - (Your VM will likely be named differenty. Adjust the name accordingly in the scripts!)
- Has your **EQEmu client** at `C:\Eulogy-quest-client-local`
- Can SSH from Windows to your VM (via `id_rsa`)
- Has **AutoHotKey v1** installed
- Has your SSH key loaded: `ssh-add ~/.ssh/id_rsa`

---

## ✅ 3. Install GitHub Actions Runner

From your repo:
1. Go to **Settings → Actions → Runners → New self-hosted runner**
2. Choose **Windows**, then follow the steps:

```powershell
mkdir C:\gh-runner
cd C:\gh-runner
Invoke-WebRequest -Uri <URL> -OutFile actions-runner.zip
Expand-Archive .\actions-runner.zip -DestinationPath .
.\config.cmd --url https://github.com/your-org/akk-stack --token <token>
```

During setup:
- **Runner group**: `local-game-server`
- **Runner name**: e.g., `John-runner`
- **Labels**: `windows, local-game-server, eqemu`
- **Run as service**: `Y`
- **User account**: your Windows username (e.g., `.\john`)

---

## ✅ 4. Test Your Local Validation Script

Run from your script folder:
```powershell
cd path\to\local-game-server-validation-scripts
.\validate-eqemu.ps1
```

It should:
- Start the VM
- Start the game server
- Launch EQ and log in
- Detect success from the log file
- Log out and shut everything down

---

## ✅ 5. Add Workflow to Your Repo

If not already present, create `.github/workflows/validate-eqemu.yml`:

```yaml
name: Validate EQEmu Server

on:
  workflow_dispatch:
  push:
    paths:
      - 'Eulogy-Quest/eulogy-docs/local-game-server-validation-scripts/**'

jobs:
  validate:
    runs-on: [self-hosted, windows, local-game-server]

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run validation script
        shell: pwsh
        run: ./Eulogy-Quest/eulogy-docs/local-game-server-validation-scripts/validate-eqemu.ps1
```

Then:
```bash
git add .github/workflows/validate-eqemu.yml
git commit -m "Add validation workflow"
git push
```

---

## ✅ 6. Run the GitHub Action

1. Go to **GitHub Actions** tab
2. Select **"Validate EQEmu Server"** workflow
3. Click **"Run workflow"** (manual) or push a change to trigger it
4. Watch your runner log and the GitHub UI for pass/fail

---

## ✨ Done!
You're now running automated game-server validation locally via GitHub Actions. Teamwide testing and integration FTW! 🚀

Need help? Ping the team lead.

