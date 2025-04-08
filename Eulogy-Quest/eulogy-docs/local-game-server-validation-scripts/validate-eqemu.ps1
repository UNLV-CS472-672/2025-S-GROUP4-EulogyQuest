#// ai-gen start (ChatGPT-4o, 1)

# Check if the id_rsa key is already loaded
# We want to pass commands to the VM over ssh, but we need
# ssh authentication. Ssh authentication needs to be done
# in an interactive shell (terminal window) and not in a script.
# Once we authenticate manually on the terminal, adding the key
# to window's ssh-agent, ssh will not re-ask for the passphrase.
# (If the passphrase is requested silently in a script, the script will time-out.)
$keyLoaded = (ssh-add -L 2>$null) -match "ssh-rsa"

if (-not $keyLoaded) {
    Write-Host "[INFO] Your SSH key is not loaded."
    Write-Host 'Please run: ssh-add $env:USERPROFILE\.ssh\id_rsa (in a windows terminal) before running this script.'
    exit 1
} else {
    Write-Host "`n[INFO] ssh-agent has the key"
}

# === Run start script ===
Write-Host "=== Starting EQEmu server and validating login ==="
& "$PSScriptRoot\start-eqemu.ps1"
$startResult = $LASTEXITCODE

if ($startResult -ne 0) {
    Write-Host "`n[FAIL] start-eqemu.ps1 failed with exit code $startResult"
    Write-Host "Skipping shutdown."
    exit $startResult
}

# === Run stop script ===
Write-Host "`n=== Shutting down EQEmu server and client ==="
& "$PSScriptRoot\stop-eqemu.ps1"
$stopResult = $LASTEXITCODE

# === Final summary ===
if ($startResult -eq 0) {
    Write-Host "`n[PASS] EQEmu login validated successfully."
} else {
    Write-Host "`n[FAIL] EQEmu validation failed with exit code $startResult"
}

exit $startResult

#// ai-gen end