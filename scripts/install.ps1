param(
    [Parameter(Position = 0)]
    [string[]]$Skill,

    [string]$Target,

    [switch]$All,

    [switch]$Force
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$SourceSkills = Join-Path $ProjectRoot "skills"

if (-not (Test-Path -LiteralPath $SourceSkills)) {
    throw "Cannot find skills directory: $SourceSkills"
}

if (-not $Target) {
    if ($env:CODEX_HOME) {
        $Target = Join-Path $env:CODEX_HOME "skills"
    } else {
        $Target = Join-Path $HOME ".codex\skills"
    }
}

New-Item -ItemType Directory -Force -Path $Target | Out-Null

$SelectedSkills = @()
if ($All -or -not $Skill -or $Skill.Count -eq 0) {
    $SelectedSkills = Get-ChildItem -LiteralPath $SourceSkills -Directory | Select-Object -ExpandProperty Name
} else {
    $SelectedSkills = $Skill
}

if ($SelectedSkills.Count -eq 0) {
    throw "No skills found to install."
}

$TargetRoot = (Resolve-Path -LiteralPath $Target).Path

foreach ($SkillName in $SelectedSkills) {
    $Source = Join-Path $SourceSkills $SkillName
    if (-not (Test-Path -LiteralPath $Source)) {
        throw "Skill not found: $SkillName"
    }

    $Destination = Join-Path $Target $SkillName
    if (Test-Path -LiteralPath $Destination) {
        if (-not $Force) {
            Write-Output "[skipped] $SkillName already exists at $Destination"
            continue
        }

        $ResolvedDestination = (Resolve-Path -LiteralPath $Destination).Path
        if (-not $ResolvedDestination.StartsWith($TargetRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to remove path outside target root: $ResolvedDestination"
        }

        Remove-Item -LiteralPath $Destination -Recurse -Force
    }

    Copy-Item -LiteralPath $Source -Destination $Target -Recurse
    Write-Output "[installed] $SkillName -> $Destination"
}
