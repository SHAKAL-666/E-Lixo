# Script to paste a Google service account JSON, save it to google_service_account.json,
# set the environment variable for the current session and run the Vision test.

Write-Host "Cole o conteúdo JSON da chave de service account (termine com Ctrl+Z + Enter):" -ForegroundColor Cyan
$json = [Console]::In.ReadToEnd()
if (-not $json.Trim()) {
    Write-Host "Nenhum conteúdo recebido. Abortando." -ForegroundColor Yellow
    exit 1
}

$path = Join-Path -Path (Get-Location) -ChildPath 'google_service_account.json'
try {
    $json | Out-File -FilePath $path -Encoding utf8
    Write-Host "Arquivo salvo em: $path" -ForegroundColor Green
} catch {
    Write-Host "Falha ao escrever o arquivo: $_" -ForegroundColor Red
    exit 1
}

# Export environment variable for current PowerShell session
$env:GOOGLE_APPLICATION_CREDENTIALS = $path
Write-Host "Variável de ambiente GOOGLE_APPLICATION_CREDENTIALS definida para $path" -ForegroundColor Green

# Activate virtualenv if present
if (Test-Path ".\.venv-1\Scripts\Activate.ps1") {
    Write-Host "Ativando virtualenv .venv-1..." -ForegroundColor Cyan
    & .\.venv-1\Scripts\Activate.ps1
}

# Run the test script
Write-Host "Executando test_vision_api.py..." -ForegroundColor Cyan
python test_vision_api.py
