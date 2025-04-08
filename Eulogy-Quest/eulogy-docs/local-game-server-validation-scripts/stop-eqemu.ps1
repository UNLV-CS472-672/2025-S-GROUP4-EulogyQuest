#// ai-gen start (ChatGPT-4o, 1)
# === Config Section ===
$vmName = "Backup-Eulogy-quest-local-server"
$vmIp = "192.168.56.103"          # ← Update this
$vmUser = "sov"                  # ← Update this
# NOTE: Don't store plain passwords; use key-based auth if possible.

# === Gracefully exit EverQuest ===
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ahkPath = "C:\Program Files\AutoHotkey\AutoHotkeyU64.exe"
$exitScript = Join-Path $scriptDir "exitEq.ahk"

Write-Host "Sending /exit to EverQuest client..."
Start-Process $ahkPath -ArgumentList $exitScript
Start-Sleep -Seconds 8  # give it a few seconds to log out

# === Stop EQEmu Server ===
Write-Host "Stopping EQEmu server..."

$remoteCommand = @'
cd ~/opt/akk-stack
docker-compose exec -T eqemu-server bash -c 'cd server && ./bin/spire spire:launcher stop'
sleep 10
make down
'@

ssh "$vmUser@$vmIp" $remoteCommand
Start-Sleep -Seconds 5

# === Stop the VM ===
Write-Host "Shutting Down the VM..."
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm $vmName acpipowerbutton

#// ai-gen end