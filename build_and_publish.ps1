# --- 1. Bump version ---
poetry version patch
py c:\Users\andre\Desktop\dev\utils\write_version\write_version.py

# --- 2. Build & Publish to PyPI ---
poetry build
poetry publish

# --- 3. Read version ---
$version = Get-Content q2report/version.py 
$version = ($version | Select-String '__version__\s*=\s*"(.+)"').Matches[0].Groups[1].Value
Write-Host "Version: $version"

# --- 4. Commit changes ---
git add .

$commitMessage = "release: v$version"
git commit -m $commitMessage 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "Changes committed: $commitMessage"
    git push
    Write-Host "Changes pushed to origin."
} else {
    Write-Host "No changes to commit."
}

# --- 5. Create git tag ---
$tag = "v$version"
$existingTag = git tag --list $tag

if ($existingTag) {
    Write-Host "Tag $tag already exists. Skipping tag creation."
} else {
    git tag $tag
    Write-Host "Tag $tag created."
}

git push origin $tag
Write-Host "Tag $tag pushed to remote."

# --- 6. Generate Release Notes ---
# Find previous tag
$previousTag = git describe --tags --abbrev=0 $tag~1 2>$null

if ($LASTEXITCODE -eq 0 -and $previousTag) {
    $commits = git log $previousTag..HEAD --pretty=format:"%s"
} else {
    $commits = git log --pretty=format:"%s"
}

# Initialize sections
$added = @()
$fixed = @()
$changed = @()
$others = @()

foreach ($c in $commits) {
    if ($c -match "^feat") { $added += "- $c" }
    elseif ($c -match "^fix") { $fixed += "- $c" }
    elseif ($c -match "^refactor|^chore") { $changed += "- $c" }
    else { $others += "- $c" }
}

# Build Release Notes text
$releaseNotes = "## Release v$version`n`n"

if ($added.Count -gt 0) { $releaseNotes += "### Added`n" + ($added -join "`n") + "`n`n" }
if ($fixed.Count -gt 0) { $releaseNotes += "### Fixed`n" + ($fixed -join "`n") + "`n`n" }
if ($changed.Count -gt 0) { $releaseNotes += "### Changed`n" + ($changed -join "`n") + "`n`n" }
if ($others.Count -gt 0) { $releaseNotes += "### Other`n" + ($others -join "`n") + "`n`n" }

# --- 7. Create GitHub Release via gh ---
$ghExists = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghExists) {
    Write-Host "ERROR: GitHub CLI (gh) is not installed. Skipping GitHub Release."
    Write-Host "Install with: winget install --id GitHub.cli"
    exit 0
}

$existingRelease = gh release view $tag 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "GitHub Release $tag already exists. Skipping release creation."
} else {
    Write-Host "Creating GitHub Release $tag ..."
    gh release create $tag dist/* `
        --title "v$version" `
        --notes "$releaseNotes"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "GitHub Release $tag successfully created."
    } else {
        Write-Host "ERROR: Failed to create GitHub Release."
    }
}
