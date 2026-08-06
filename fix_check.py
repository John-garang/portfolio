import glob, re

templates = glob.glob('c:/Portfolio/templates/**/*.html', recursive=True)
issues = []

for path in templates:
    with open(path, encoding='utf-8', errors='ignore') as f:
        content = f.read()
    name = re.sub(r'.*templates[\\/]', '', path)

    # Duplicate IDs
    ids = re.findall(r'id=["\']([^"\']+)["\']', content)
    dupes = [i for i in set(ids) if ids.count(i) > 1]
    if dupes:
        issues.append('[DUPE ID] ' + name + ': ' + str(dupes))

    # Old loading remnants
    if 'loading-spinner' in content:
        issues.append('[OLD SPINNER] ' + name)
    if 'loading-content' in content:
        issues.append('[OLD LOADING-CONTENT] ' + name)

    # loading.js without a loading div
    if 'loading.js' in content and 'loading-screen' not in content and 'loadingScreen' not in content:
        issues.append('[MISSING LOADING DIV] ' + name)

    # loading.css without a loading div
    if 'loading.css' in content and 'loading-screen' not in content and 'loadingScreen' not in content:
        issues.append('[MISSING LOADING DIV CSS] ' + name)

    # Multiple loading divs
    count = content.count('id="loading-screen"') + content.count('id="loadingScreen"')
    if count > 1:
        issues.append('[MULTIPLE LOADING DIVS] ' + name + ' count=' + str(count))

    # Broken static paths (absolute /static/ on root index which uses relative paths)
    if name == 'index.html' and 'href="/static/' in content:
        issues.append('[ABS PATH ON ROOT] ' + name + ': uses /static/ but may need relative static/')

print('Files scanned:', len(templates))
if issues:
    for i in issues:
        print(i)
else:
    print('No conflicts found.')
