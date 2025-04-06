#// ai-gen start (ChatGPT-4o, 1)

# Check if the id_rsa key is already loaded
# We want to pass commands to the VM over ssh, but we need
# ssh authentication. Ssh authentication needs to be done
# in an interactive shell (terminal window) and not in a script.
# Once we authenticate manually on the terminal, adding the key
# to window's ssh-agent, ssh will not re-ask for the passphrase.
# (If the passphrase is requested silently in a script, the script will time-out.)

$keyCheck = ssh-add -L 2>&1
if ($keyCheck -match "The agent has no identities") {
    Write-Host "[FAIL] SSH key not loaded. Run: ssh-add $env:USERPROFILE\.ssh\id_rsa"
    exit 1
}
# Note: this can silently fail if the id_rsa key is needed, but another key is loaded.

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
