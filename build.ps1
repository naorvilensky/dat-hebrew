# Set variables
$envName = ".venv"
$requirementsFile = "requirements.txt"
$outputExe = "dat-hebrew.exe"
$mainScript = "main.py"
$pyInstallerArgs = "--onefile --windowed --additional-hooks-dir=. --recursive-copy-metadata sentence-transformers --runtime-tmpdir=. --name $outputExe"

# Step 1: Create virtual environment
if (-not (Test-Path $envName)) {
    Write-Host "Creating virtual environment..."
    python -m venv $envName
} else {
    Write-Host "Virtual environment already exists. Skipping creation."
}

# Step 2: Activate virtual environment and install requirements
Write-Host "Installing dependencies..."
& "$envName\Scripts\pip.exe" install --upgrade pip
& "$envName\Scripts\pip.exe" install -r $requirementsFile

# Step 3: Run pyinstaller in a new window so you can see the output
$pyInstallerCommand = "$envName\Scripts\pyinstaller.exe $pyInstallerArgs $mainScript"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $pyInstallerCommand
