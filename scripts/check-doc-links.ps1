param(
  [string]$Root = "docs/01-图论基础",
  [switch]$StrictAnchors
)

$ErrorActionPreference = "Stop"

function Normalize-Path([string]$p) {
  try {
    return (Resolve-Path -LiteralPath $p).Path
  } catch {
    return [System.IO.Path]::GetFullPath($p)
  }
}

function Get-HeadingAnchors([string[]]$lines) {
  $anchors = New-Object 'System.Collections.Generic.HashSet[string]'

  foreach ($line in $lines) {
    if ($line -match '^(#{1,6})\s+(.*)$') {
      $raw = $Matches[2].Trim()

      $t = $raw
      $t = $t -replace '\*\*([^*]+)\*\*', '$1'
      $t = $t -replace '\*([^*]+)\*', '$1'
      $t = $t -replace '`([^`]+)`', '$1'

      $t = ($t.ToLowerInvariant() -replace '[^\p{IsCJKUnifiedIdeographs}\p{L}\p{Nd}\s\-]', '')
      $t = $t -replace '\s+', '-'
      $t = $t -replace '\-+', '-'
      $t = $t.Trim('-')

      if ($t.Length -gt 0) {
        [void]$anchors.Add($t)
      }
    }
  }

  return $anchors
}

function Test-Anchor([string]$filePath, [string]$anchor) {
  $anchor = $anchor.Trim()
  if ($anchor.StartsWith("#")) { $anchor = $anchor.Substring(1) }
  if ([string]::IsNullOrWhiteSpace($anchor)) { return $true }

  $content = Get-Content -LiteralPath $filePath -Raw

  # Fast-path: anchor appears explicitly in markdown (common in generated TOCs)
  if ($content -match [regex]::Escape("(#$anchor)") -or $content -match [regex]::Escape("](#$anchor)")) {
    return $true
  }

  # Fallback: compute anchor candidates from headings
  $lines = $content -split "`r?`n"
  $headingAnchors = Get-HeadingAnchors $lines
  if ($headingAnchors.Contains($anchor)) { return $true }
  if ($headingAnchors.Contains($anchor.TrimStart('-'))) { return $true }
  if ($headingAnchors.Contains("-$anchor")) { return $true }

  return $false
}

function Is-ExternalLink([string]$href) {
  return $href -match '^(https?:|mailto:|tel:)' -or $href.StartsWith("#")
}

if (-not (Test-Path -LiteralPath $Root)) {
  throw "Root path not found: $Root"
}

$rootAbs = Normalize-Path $Root
$mdFiles = Get-ChildItem -LiteralPath $rootAbs -Recurse -File -Filter "*.md"

$missingFiles = @()
$badAnchors = @()

# Matches: [text](target)
$linkRegex = [regex]'\[[^\]]*\]\(([^)]+)\)'

foreach ($md in $mdFiles) {
  $mdAbs = $md.FullName
  $mdDir = Split-Path -Parent $mdAbs
  $raw = Get-Content -LiteralPath $mdAbs -Raw

  foreach ($m in $linkRegex.Matches($raw)) {
    $href = $m.Groups[1].Value.Trim()
    if ([string]::IsNullOrWhiteSpace($href)) { continue }
    if (Is-ExternalLink $href) { continue }
    if ($href.StartsWith("`"")) { $href = $href.Trim("`"") }

    $filePart = $href
    $anchorPart = $null
    if ($href.Contains("#")) {
      $parts = $href.Split("#", 2)
      $filePart = $parts[0]
      $anchorPart = $parts[1]
    }

    if ($filePart -eq "") {
      # intra-document anchor link
      if ($StrictAnchors) {
        $ok = Test-Anchor $mdAbs $anchorPart
        if (-not $ok) {
          $badAnchors += [pscustomobject]@{ Source = $mdAbs; Target = $mdAbs; Anchor = $anchorPart; Href = $href }
        }
      }
      continue
    }

    if ($filePart -notmatch '\.md$') { continue }

    $targetAbs = Normalize-Path (Join-Path $mdDir $filePart)
    if (-not (Test-Path -LiteralPath $targetAbs)) {
      $missingFiles += [pscustomobject]@{ Source = $mdAbs; Href = $href; Target = $targetAbs }
      continue
    }

    if ($anchorPart) {
      $ok = Test-Anchor $targetAbs $anchorPart
      if (-not $ok) {
        $badAnchors += [pscustomobject]@{ Source = $mdAbs; Target = $targetAbs; Anchor = $anchorPart; Href = $href }
      }
    }
  }
}

Write-Host "=== Markdown link check ==="
Write-Host ("Root: " + $rootAbs)
Write-Host ("Files scanned: " + $mdFiles.Count)
Write-Host ("Missing targets: " + $missingFiles.Count)
Write-Host ("Bad anchors: " + $badAnchors.Count)

if ($missingFiles.Count -gt 0) {
  Write-Host ""
  Write-Host "---- Missing files ----"
  $missingFiles | Sort-Object Source, Href | Format-Table -AutoSize
}

if ($badAnchors.Count -gt 0) {
  Write-Host ""
  Write-Host "---- Unresolved anchors ----"
  $badAnchors | Sort-Object Source, Target, Anchor | Select-Object Source, Href, Target, Anchor | Format-Table -AutoSize
}

if ($missingFiles.Count -gt 0 -or ($StrictAnchors -and $badAnchors.Count -gt 0)) {
  exit 1
}

exit 0
