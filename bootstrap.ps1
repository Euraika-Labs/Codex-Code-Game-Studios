$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$bootstrap = Join-Path $scriptDir "global-pack/bin/bootstrap.py"

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py $bootstrap @Args
    exit $LASTEXITCODE
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $bootstrap @Args
    exit $LASTEXITCODE
}

throw "Python launcher not found. Install Python 3 and rerun bootstrap.ps1."
