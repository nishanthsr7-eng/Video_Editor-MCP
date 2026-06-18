#Requires -Version 5.1
<#
.SYNOPSIS
    Manage scripts installed in DaVinci Resolve's script folders.
    List, install, or delete scripts interactively.
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File manage-scripts.ps1
#>

$ScriptsRoot = "$env:APPDATA\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts"
$SourceRoot  = $PSScriptRoot

# ---------------------------------------------------------------------------
function Write-Header ($text) {
    Write-Host ""
    Write-Host $text -ForegroundColor Cyan
    Write-Host ("-" * $text.Length) -ForegroundColor DarkCyan
}
function Write-Ok   ($text) { Write-Host "  [OK] $text" -ForegroundColor Green  }
function Write-Warn ($text) { Write-Host "  [!]  $text" -ForegroundColor Yellow }

# ---------------------------------------------------------------------------
# Collect every script installed in the Resolve Scripts folders
# ---------------------------------------------------------------------------
function Get-InstalledScripts {
    $list = New-Object System.Collections.Generic.List[PSCustomObject]
    $idx  = 1
    foreach ($folder in @("Color","Deliver","Edit","Utility","Comp","Tool","Views")) {
        $path = Join-Path $ScriptsRoot $folder
        if (-not (Test-Path $path)) { continue }

        # Top-level .lua and .py files
        Get-ChildItem $path -Include "*.lua","*.py" | Sort-Object Name | ForEach-Object {
            $list.Add([PSCustomObject]@{
                Index=$idx; Name=$_.Name; Folder=$folder; Path=$_.FullName; Sub=""
            })
            $idx++
        }

        # Subfolder scripts (subfolder name = category in Resolve's menu)
        Get-ChildItem $path -Directory | Sort-Object Name | ForEach-Object {
            $sub = $_.Name
            Get-ChildItem $_.FullName -Include "*.lua","*.py" | Sort-Object Name | ForEach-Object {
                $list.Add([PSCustomObject]@{
                    Index=$idx; Name=$_.Name; Folder=$folder; Path=$_.FullName; Sub=$sub
                })
                $idx++
            }
        }
    }
    return ,$list   # comma forces List return (not unrolled)
}

# ---------------------------------------------------------------------------
# Print the installed-script list
# ---------------------------------------------------------------------------
function Show-Scripts ($scripts) {
    $currentFolder = ""
    foreach ($s in $scripts) {
        if ($s.Folder -ne $currentFolder) {
            Write-Header $s.Folder
            $currentFolder = $s.Folder
        }
        $prefix = if ($s.Sub) { "$($s.Sub)/" } else { "" }
        Write-Host ("  [{0,2}]  {1}{2}" -f $s.Index, $prefix, $s.Name) -ForegroundColor White
    }
}

# ---------------------------------------------------------------------------
# Parse a selection string like "1 3 5-8, 12" into a set of integers
# ---------------------------------------------------------------------------
function Parse-Selection ([string]$raw, [int]$max) {
    $selected = New-Object System.Collections.Generic.HashSet[int]
    foreach ($token in ($raw -split '[,\s]+')) {
        $token = $token.Trim()
        if ($token -match '^(\d+)-(\d+)$') {
            [int]$from = $Matches[1]; [int]$to = $Matches[2]
            $from..$to | Where-Object { $_ -ge 1 -and $_ -le $max } |
                ForEach-Object { $null = $selected.Add($_) }
        } elseif ($token -match '^\d+$') {
            $n = [int]$token
            if ($n -ge 1 -and $n -le $max) { $null = $selected.Add($n) }
        }
    }
    return $selected
}

# ---------------------------------------------------------------------------
# DELETE: pick scripts to remove from Resolve
# ---------------------------------------------------------------------------
function Invoke-Delete {
    $scripts = Get-InstalledScripts
    if ($scripts.Count -eq 0) {
        Write-Warn "No scripts are currently installed."
        return
    }

    Show-Scripts $scripts

    Write-Host ""
    Write-Host "Enter numbers to delete  (e.g.  1 3 5-8 12)  or  'all'  to wipe everything:" -ForegroundColor Yellow
    $raw = (Read-Host "  >").Trim()

    if ([string]::IsNullOrWhiteSpace($raw)) { Write-Warn "Nothing selected. Cancelled."; return }

    $toDelete = if ($raw -eq "all") {
        $scripts
    } else {
        $sel = Parse-Selection $raw $scripts.Count
        $scripts | Where-Object { $sel.Contains($_.Index) }
    }

    if (-not $toDelete) { Write-Warn "No valid numbers found. Cancelled."; return }

    Write-Host ""
    Write-Host "About to delete:" -ForegroundColor Yellow
    $toDelete | ForEach-Object {
        Write-Host ("  - [{0}] {1}" -f $_.Folder, $_.Name) -ForegroundColor Red
    }

    $confirm = (Read-Host "`n  Confirm? (y/n)").Trim().ToLower()
    if ($confirm -ne "y") { Write-Warn "Cancelled."; return }

    $count = 0
    foreach ($s in $toDelete) {
        Remove-Item $s.Path -Force -ErrorAction SilentlyContinue
        # Remove parent subfolder if it is now empty
        if ($s.Sub) {
            $parent = Split-Path $s.Path -Parent
            if (-not (Get-ChildItem $parent)) { Remove-Item $parent -Force -ErrorAction SilentlyContinue }
        }
        Write-Ok "Deleted: $($s.Name)"
        $count++
    }
    Write-Host ""
    Write-Host "  $count script(s) deleted." -ForegroundColor Cyan
}

# ---------------------------------------------------------------------------
# INSTALL: pick scripts from the DaVinci_Tools source to deploy
# ---------------------------------------------------------------------------
function Invoke-Install {
    $sourceMap = @(
        [PSCustomObject]@{ Src="DaVinci-Resolve-Scripts\Grading";          Dest="Color"   }
        [PSCustomObject]@{ Src="DaVinci-Resolve-Scripts\Clips Properties"; Dest="Utility" }
        [PSCustomObject]@{ Src="DaVinci-Resolve-Scripts\Editing";           Dest="Edit"    }
        [PSCustomObject]@{ Src="DaVinci-Resolve-Scripts\Markers";           Dest="Utility" }
        [PSCustomObject]@{ Src="DaVinci-Resolve-Scripts\MediaPool";         Dest="Utility" }
        [PSCustomObject]@{ Src="DaVinci-Resolve-Scripts\Templates";         Dest="Utility" }
        [PSCustomObject]@{ Src="DaVinci-Resolve-Scripts\Timeline";          Dest="Edit"    }
        [PSCustomObject]@{ Src="resolve-scripts\Coding";                    Dest="Utility" }
        [PSCustomObject]@{ Src="resolve-scripts\Color";                     Dest="Color"   }
        [PSCustomObject]@{ Src="resolve-scripts\Deliver";                   Dest="Deliver" }
        [PSCustomObject]@{ Src="resolve-scripts\Edit";                      Dest="Edit"    }
        [PSCustomObject]@{ Src="resolve-scripts\Utility";                   Dest="Utility" }
    )

    $available = New-Object System.Collections.Generic.List[PSCustomObject]
    $idx = 1
    foreach ($map in $sourceMap) {
        $srcPath = Join-Path $SourceRoot $map.Src
        if (-not (Test-Path $srcPath)) { continue }
        Get-ChildItem $srcPath -Include "*.lua","*.py" | Sort-Object Name | ForEach-Object {
            $available.Add([PSCustomObject]@{
                Index=$idx; Name=$_.Name; SrcPath=$_.FullName; Dest=$map.Dest
            })
            $idx++
        }
    }

    if ($available.Count -eq 0) {
        Write-Warn "No source scripts found. Make sure manage-scripts.ps1 is inside DaVinci_Tools."
        return
    }

    Write-Header "Available scripts to install"
    $currentDest = ""
    foreach ($s in $available) {
        if ($s.Dest -ne $currentDest) {
            Write-Host ""
            Write-Host "  [$($s.Dest)]" -ForegroundColor DarkCyan
            $currentDest = $s.Dest
        }
        Write-Host ("  [{0,2}]  {1}" -f $s.Index, $s.Name) -ForegroundColor White
    }

    Write-Host ""
    Write-Host "Enter numbers to install  (e.g.  1 3 5-8)  or  'all':" -ForegroundColor Yellow
    $raw = (Read-Host "  >").Trim()

    if ([string]::IsNullOrWhiteSpace($raw)) { Write-Warn "Cancelled."; return }

    $toInstall = if ($raw -eq "all") {
        $available
    } else {
        $sel = Parse-Selection $raw $available.Count
        $available | Where-Object { $sel.Contains($_.Index) }
    }

    if (-not $toInstall) { Write-Warn "No valid selection."; return }

    $count = 0
    foreach ($s in $toInstall) {
        $dest = Join-Path $ScriptsRoot $s.Dest
        $null = New-Item -ItemType Directory -Force $dest
        Copy-Item $s.SrcPath $dest -Force
        Write-Ok "Installed [$($s.Dest)]  $($s.Name)"
        $count++
    }
    Write-Host ""
    Write-Host "  $count script(s) installed." -ForegroundColor Cyan
}

# ---------------------------------------------------------------------------
# LIST: show everything currently installed
# ---------------------------------------------------------------------------
function Invoke-List {
    $scripts = Get-InstalledScripts
    if ($scripts.Count -eq 0) {
        Write-Warn "No scripts currently installed."
    } else {
        Show-Scripts $scripts
        Write-Host ""
        Write-Host "  Total: $($scripts.Count) script(s) installed." -ForegroundColor Cyan
    }
}

# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------
while ($true) {
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "   DaVinci Resolve Script Manager     " -ForegroundColor Cyan
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "  [1]  List installed scripts"
    Write-Host "  [2]  Install scripts"
    Write-Host "  [3]  Delete scripts"
    Write-Host "  [q]  Quit"
    $choice = (Read-Host "`n  Choose").Trim().ToLower()

    switch ($choice) {
        "1"     { Invoke-List    }
        "2"     { Invoke-Install }
        "3"     { Invoke-Delete  }
        "q"     { Write-Host "  Bye." -ForegroundColor DarkGray; exit }
        default { Write-Warn "Invalid choice - enter 1, 2, 3, or q." }
    }
}
