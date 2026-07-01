param(
    [string]$Python
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ValidateScript = Join-Path $ProjectRoot "scripts\validate.py"

if (-not (Test-Path -LiteralPath $ValidateScript)) {
    throw "Cannot find validate.py: $ValidateScript"
}

$env:PYTHONUTF8 = "1"

if ($Python) {
    & $Python $ValidateScript
    exit $LASTEXITCODE
}

$BundledPython = Join-Path $HOME ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (Test-Path -LiteralPath $BundledPython) {
    & $BundledPython $ValidateScript
    exit $LASTEXITCODE
}

$Candidates = @(
    @{ Command = "python"; Args = @() },
    @{ Command = "py"; Args = @("-3") }
)

foreach ($Candidate in $Candidates) {
    $Command = $Candidate.Command
    $Args = $Candidate.Args
    try {
        & $Command @Args --version *> $null
        if ($LASTEXITCODE -eq 0) {
            & $Command @Args $ValidateScript
            exit $LASTEXITCODE
        }
    } catch {
        continue
    }
}

throw "Could not find Python. Pass -Python <path-to-python> or run scripts/validate.py directly."
