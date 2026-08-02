[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Prompt,

    [ValidateSet("fable", "opus")]
    [string]$Model = "fable",

    [ValidateSet("plan", "work")]
    [string]$Mode = "work",

    [switch]$DryRun
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$sessionFile = Join-Path $repoRoot "scratch\claude-worker-session.json"

if (-not (Test-Path -LiteralPath $sessionFile)) {
    throw "Claude worker session metadata not found: $sessionFile"
}

$session = Get-Content -LiteralPath $sessionFile -Raw | ConvertFrom-Json
if (-not $session.session_id) {
    throw "Claude worker session metadata has no session_id: $sessionFile"
}

$permissionMode = if ($Mode -eq "plan") { "plan" } else { "auto" }
$roleReminder = @"
[CONTRATO OPERATIVO WAGER]
Sos el worker persistente de Claude. Codex supervisa la dirección científica; Lucas decide en última instancia.
Antes de actuar, verificá objetivo superior, adecuación del mundo y condición de salida. No amplíes alcance ni encadenes tuning.
Implementá/analizá con rigor, preservá negativos y crudos, y terminá con: Nivel arriba / límites / rival principal / seguir o cambiar de mundo.
Leé CLAUDE.md, docs/operativa-codex-claude.md y la cabecera vigente de docs/roadmap.md cuando el encargo sea sustantivo.

[ENCARGO DE CODEX]
$Prompt
"@

if ($DryRun) {
    [pscustomobject]@{
        session_id = $session.session_id
        model = $Model
        effort = "max"
        permission_mode = $permissionMode
        prompt_preview = $roleReminder.Substring(0, [Math]::Min(500, $roleReminder.Length))
    } | ConvertTo-Json -Depth 3
    exit 0
}

& claude `
    --resume $session.session_id `
    --model $Model `
    --effort max `
    --permission-mode $permissionMode `
    --print `
    --output-format json `
    $roleReminder

exit $LASTEXITCODE
