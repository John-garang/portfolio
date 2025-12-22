@echo off
echo Updating all .html references to clean URLs...

REM Update navigation dropdowns - Work Portfolio section
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"my-shelf\.html\"', 'href=\"my-shelf\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"artefacts\.html\"', 'href=\"artefacts\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"cv\.html\"', 'href=\"cv\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"graphic-design\.html\"', 'href=\"graphic-design\"' | Set-Content -Path $_.FullName"

REM Update navigation dropdowns - Experience section
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"african-leadership-university\.html\"', 'href=\"african-leadership-university\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"education-bridge\.html\"', 'href=\"education-bridge\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"african-leadership-academy\.html\"', 'href=\"african-leadership-academy\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"ashinaga-foundation\.html\"', 'href=\"ashinaga-foundation\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"uganics-repellents\.html\"', 'href=\"uganics-repellents\"' | Set-Content -Path $_.FullName"

REM Update navigation dropdowns - Programs section
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"cnn-academy\.html\"', 'href=\"cnn-academy\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"take-action-lab\.html\"', 'href=\"take-action-lab\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"unleash-innovation-lab\.html\"', 'href=\"unleash-innovation-lab\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"accra-fusion\.html\"', 'href=\"accra-fusion\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"yali-east-africa\.html\"', 'href=\"yali-east-africa\"' | Set-Content -Path $_.FullName"

REM Update other page links
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"blog\.html\"', 'href=\"blog\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"academia\.html\"', 'href=\"academia\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"travels\.html\"', 'href=\"travels\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"poems\.html\"', 'href=\"poems\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"blogs\.html\"', 'href=\"blogs\"' | Set-Content -Path $_.FullName"

REM Update additional experience pages
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"africa-inventor-alliance\.html\"', 'href=\"africa-inventor-alliance\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"surplus-people-project\.html\"', 'href=\"surplus-people-project\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"creative-connect\.html\"', 'href=\"creative-connect\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"nalafem-collective\.html\"', 'href=\"nalafem-collective\"' | Set-Content -Path $_.FullName"

REM Update article links
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"if-equality-means-this\.html\"', 'href=\"if-equality-means-this\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"when-educated-woman-says-no\.html\"', 'href=\"when-educated-woman-says-no\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"making-of-dinka-woman\.html\"', 'href=\"making-of-dinka-woman\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"cape-town-travel-guide\.html\"', 'href=\"cape-town-travel-guide\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"development-trajectory-south-sudan\.html\"', 'href=\"development-trajectory-south-sudan\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"entrepreneurial-gaps-south-sudan\.html\"', 'href=\"entrepreneurial-gaps-south-sudan\"' | Set-Content -Path $_.FullName"

REM Update admin pages
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"admin-login\.html\"', 'href=\"admin-login\"' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'href=\"admin-dashboard\.html\"', 'href=\"admin-dashboard\"' | Set-Content -Path $_.FullName"

REM Update JavaScript redirects
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'window\.location\.href = ''admin-login\.html''', 'window.location.href = ''admin-login''' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'window\.location\.href = ''admin-dashboard\.html''', 'window.location.href = ''admin-dashboard''' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'window\.location\.href = ''blog\.html''', 'window.location.href = ''blog''' | Set-Content -Path $_.FullName"
powershell -Command "(Get-Content -Path '*.html' -Raw) -replace 'window\.location\.href = ''poems\.html''', 'window.location.href = ''poems''' | Set-Content -Path $_.FullName"

echo Updating folder-based index files...
REM Update folder-based files
for /d %%d in (about services contact poems experience-overview programs-overview work-portfolio) do (
    if exist "%%d\index.html" (
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"my-shelf\.html\"', 'href=\"my-shelf\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"artefacts\.html\"', 'href=\"artefacts\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"cv\.html\"', 'href=\"cv\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"graphic-design\.html\"', 'href=\"graphic-design\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"african-leadership-university\.html\"', 'href=\"african-leadership-university\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"education-bridge\.html\"', 'href=\"education-bridge\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"african-leadership-academy\.html\"', 'href=\"african-leadership-academy\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"ashinaga-foundation\.html\"', 'href=\"ashinaga-foundation\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"uganics-repellents\.html\"', 'href=\"uganics-repellents\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"cnn-academy\.html\"', 'href=\"cnn-academy\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"take-action-lab\.html\"', 'href=\"take-action-lab\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"unleash-innovation-lab\.html\"', 'href=\"unleash-innovation-lab\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"accra-fusion\.html\"', 'href=\"accra-fusion\"' | Set-Content -Path '%%d\index.html'"
        powershell -Command "(Get-Content -Path '%%d\index.html' -Raw) -replace 'href=\"yali-east-africa\.html\"', 'href=\"yali-east-africa\"' | Set-Content -Path '%%d\index.html'"
    )
)

echo URL updates completed!