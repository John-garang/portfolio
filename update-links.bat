@echo off
cd "g:\My Drive\John's tech projects\Portfolio\templates"

for %%f in (*.html) do (
    powershell -Command "(Get-Content '%%f') -replace 'href=\"index\.html\"', 'href=\"/\"' -replace 'href=\"about\.html\"', 'href=\"/about\"' -replace 'href=\"services\.html\"', 'href=\"/services\"' -replace 'href=\"contact\.html\"', 'href=\"/contact\"' -replace 'href=\"poems\.html\"', 'href=\"/poems\"' | Set-Content '%%f'"
)

echo Updated all navigation links to clean URLs