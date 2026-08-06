$nav = '    <nav class="navbar" id="main-navbar">' + "`r`n" +
'                <div class="nav-container">' + "`r`n" +
'                    <div class="nav-logo">' + "`r`n" +
'                        <img src="/static/Pictures/john-ngor-deng-garang-logo.png" alt="John Garang Logo">' + "`r`n" +
'                        <span class="logo-name">John Ngor Deng Garang</span>' + "`r`n" +
'                    </div>' + "`r`n" +
'                    <ul class="nav-menu">' + "`r`n" +
'                        <li><a href="/" class="nav-link">Home</a></li>' + "`r`n" +
'                        <li><a href="/about" class="nav-link">About</a></li>' + "`r`n" +
'                        <li class="dropdown">' + "`r`n" +
'                            <a href="/work-portfolio" class="nav-link">Work Portfolio <i class="fas fa-chevron-down"></i></a>' + "`r`n" +
'                            <div class="dropdown-content">' + "`r`n" +
'                                <a href="/my-shelf">My Shelf</a>' + "`r`n" +
'                                <a href="/cv">CV</a>' + "`r`n" +
'                                <a href="/graphic-design">Graphic Design</a>' + "`r`n" +
'                                <a href="/web-design">Web Design</a>' + "`r`n" +
'                            </div>' + "`r`n" +
'                        </li>' + "`r`n" +
'                        <li><a href="/experience-overview" class="nav-link">Experience</a></li>' + "`r`n" +
'                        <li><a href="/programs-overview" class="nav-link">Programs</a></li>' + "`r`n" +
'                        <li><a href="/services" class="nav-link">Services</a></li>' + "`r`n" +
'                        <li><a href="/poems" class="nav-link">Poems</a></li>' + "`r`n" +
'                    </ul>' + "`r`n" +
'                    <div class="nav-right">' + "`r`n" +
'                        <div class="hamburger" id="hamburger">' + "`r`n" +
'                            <span></span>' + "`r`n" +
'                            <span></span>' + "`r`n" +
'                            <span></span>' + "`r`n" +
'                        </div>' + "`r`n" +
'                    </div>' + "`r`n" +
'                </div>' + "`r`n" +
'                <div class="mobile-overlay" id="mobileOverlay"></div>' + "`r`n" +
'            </nav>'

$old = '    <div id="header-placeholder"></div>'

Get-ChildItem -Path 'c:\Portfolio\templates' -Recurse -Filter '*.html' | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    if ($content -match [regex]::Escape($old)) {
        $content = $content.Replace($old, $nav)
        [System.IO.File]::WriteAllText($_.FullName, $content, [System.Text.Encoding]::UTF8)
        Write-Host "Updated: $($_.Name)"
    }
}
Write-Host "Done."
