# PowerShell setup script for Desk Goddess project
# Run this as administrator if needed

Write-Host "Setting up Python virtual environment..."
python -m venv venv
.\venv\Scripts\Activate.ps1

Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host "Setup complete!"
