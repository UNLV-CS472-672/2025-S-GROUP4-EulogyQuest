#// ai-gen start (ChatGPT-4o, 1)
# === Config Section ===
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$vmName = "Backup-Eulogy-quest-local-server"
$vmIp = "192.168.56.103"          # ← Update this
$vmUser = "sov"                  # ← Update this
# NOTE: Don't store plain passwords; use key-based auth if possible.

# === Start the VM ===
Write-Host "Starting VM..."
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm $vmName --type headless
Start-Sleep -Seconds 10

# === Wait for SSH to become available ===
Write-Host "Waiting for SSH connectivity..."

$sshReady = $false
$maxSshWait = 90
$sshTimer = 0

while (-not $sshReady -and $sshTimer -lt $maxSshWait) {
    try {
        $sshTest = & ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no "$vmUser@$vmIp" "whoami"
        Write-Host "SSH output: '$sshTest'"
        if ($sshTest -match "$vmUser") {
            $sshReady = $true
            break
        }
    } catch {
        Write-Host "SSH failed: $_"
    }

    Start-Sleep -Seconds 3
    $sshTimer += 3
    Write-Host "  ...still waiting for SSH ($sshTimer seconds)"
}

if (-not $sshReady) {
    Write-Host "[FAIL] SSH did not become available after $maxSshWait seconds."
    exit 1
}

Write-Host "[PASS] SSH is now available on the VM."

# === Start EQEmu Server ===
Write-Host "Starting EQEmu server inside VM..."
$remoteCommand = @'
cd ~/opt/akk-stack
make up
sleep 10
docker-compose exec -T eqemu-server bash -c 'cd server && ./bin/spire spire:launcher start'
'@

ssh "$vmUser@$vmIp" $remoteCommand

# === Wait for the world server (and zones!) to finish loading before running login.ahk
Write-Host "Waiting for zones to come online..."

$ready = $false
$timeout = 120  # total wait time in seconds
$waitTime = 0

while (-not $ready -and $waitTime -lt $timeout) {
    $zoneCountOutput = ssh "$vmUser@$vmIp" "ps aux | grep -v grep | grep '/home/eqemu/server/bin/zone' | wc -l"
    $zoneCount = [int]$zoneCountOutput.Trim()
    
    if ($zoneCount -ge 25) {
        $ready = $true
        break
    }

    Start-Sleep -Seconds 3
    $waitTime += 3
    Write-Host "Zones online: $zoneCount (waiting for at least 25)..."
}

if ($ready) {
    Write-Host "[PASS] Zone processes are online ($zoneCount total)."
} else {
    Write-Host "[FAIL] Zone processes did not reach expected count within $timeout seconds."
    exit 1
}

# === Launch and Auto-Login EQ Client ===
Write-Host "Launching AutoHotKey login script..."
$ahkScript = Join-Path $scriptDir "login.ahk"
$ahkPath = "C:\Program Files\AutoHotkey\AutoHotkeyU64.exe"
# debug
Write-Host "AHK Path: $ahkPath"
Write-Host "Script Path: $ahkScript"
# /debug

# === Launch the login ahk script ===
# But, first we log the time before the ahk script is run
# Then we run the ahk script
# Then we wait 70 seconds before continuing this PowerShell script
# As the next three lines occur here nearly simultaneously
$loginStartTime = Get-Date

Start-Process $ahkPath -ArgumentList $ahkScript

Start-Sleep -Seconds 70
# This give us 70 seconds for "Start-Process $ahkPath -ArgumentList $ahkScript"
# to run before the rest of this file executes.

# === Confirm Login via Log File with Timestamp Validation ===

# Log file setup
$logDir = "C:\Eulogy-quest-client-local\Logs"
$logFileName = "eqlog_Kharvey_Akkas Docker PEQ Installer.txt"
$logPath = Join-Path $logDir $logFileName
$expectedMessage = "Welcome to EverQuest!"

Write-Host "Waiting for login confirmation in log..."

# Wait up to 90 seconds
$maxWait = 90
$found = $false
$timer = 0

while (-not $found -and $timer -lt $maxWait) {
    if (Test-Path $logPath) {
        $logContent = Get-Content $logPath -Tail 50 -ErrorAction SilentlyContinue
        foreach ($line in $logContent) {
            if ($line -like "*$expectedMessage*") {
                if ($line -match "^\[(.*?)\]") {
                    $timestampStr = $matches[1]
                    # Try to parse the log timestamp (format: Wed Mar 27 14:44:29 2025)
                    $logTimestamp = [datetime]::ParseExact($timestampStr, "ddd MMM d HH:mm:ss yyyy", $null)
                    if ($logTimestamp -gt $loginStartTime) {
                        $found = $true
                        break
                    }
                }
            }
        }
    }
    if (-not $found) {
        Start-Sleep -Seconds 2
        $timer += 2
    }
}

if ($found) {
    Write-Host "`n[PASS] Login confirmed: '$expectedMessage' found in log (after script started)."
} else {
    Write-Host "`n[FAIL] Login not confirmed within $maxWait seconds."
}

#// ai-gen end