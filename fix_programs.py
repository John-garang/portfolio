f = open(r'c:\Portfolio\templates\programs-overview\index.html', 'rb')
d = f.read()
f.close()

# --- Fix 1: mobile responsive block ---
old = (
    b"        /* \xe2\x94\x80\xe2\x94\x80 Responsive \xe2\x94\x80\xe2\x94\x80 */\n"
    b"        @media (max-width: 900px) {\n"
    b"            .program-inner:not(.float-layout) {\n"
    b"                grid-template-columns: 1fr;\n"
    b"                direction: ltr;\n"
    b"                gap: 2rem;\n"
    b"            }\n"
    b"            .program-section:nth-child(even) .program-inner:not(.float-layout) { direction: ltr; }\n"
    b"            /* Float layout collapses on mobile */\n"
    b"            .program-inner.float-layout .program-visual,\n"
    b"            .program-section:nth-child(even) .program-inner.float-layout .program-visual {\n"
    b"                float: none;\n"
    b"                width: 100%;\n"
    b"                margin: 0 0 1.5rem 0;\n"
    b"            }\n"
    b"            /* On mobile: gallery moves after text */\n"
    b"            .program-visual-col { order: 1; }\n"
    b"            .program-content { order: 2; }\n"
    b"            .program-visual-col .gallery-wrap { order: 3; }\n"
    b"            .program-inner:not(.float-layout) {\n"
    b"                display: flex;\n"
    b"                flex-direction: column;\n"
    b"            }\n"
    b"            .program-section { padding: 4rem 0; }\n"
    b"        }"
)

new = (
    b"        /* \xe2\x94\x80\xe2\x94\x80 Responsive \xe2\x94\x80\xe2\x94\x80 */\n"
    b"        @media (max-width: 900px) {\n"
    b"            .program-section:nth-child(even) .program-inner:not(.float-layout) { direction: ltr; }\n"
    b"            .program-inner.float-layout .program-visual,\n"
    b"            .program-section:nth-child(even) .program-inner.float-layout .program-visual {\n"
    b"                float: none;\n"
    b"                width: 100%;\n"
    b"                margin: 0 0 1.5rem 0;\n"
    b"            }\n"
    b"            .program-inner:not(.float-layout) {\n"
    b"                display: flex;\n"
    b"                flex-direction: column;\n"
    b"                direction: ltr;\n"
    b"                gap: 2rem;\n"
    b"            }\n"
    b"            .program-visual-col { display: contents; }\n"
    b"            .program-visual-col .program-visual { order: 1; }\n"
    b"            .program-content { order: 2; }\n"
    b"            .program-visual-col .gallery-wrap { order: 3; }\n"
    b"            .program-section { padding: 4rem 0; }\n"
    b"        }"
)

if old in d:
    print('responsive block: FOUND, replacing')
    d = d.replace(old, new)
else:
    print('responsive block: NOT FOUND')

# --- Fix 2: Take Action Lab location ---
old_loc = b'Cape Town &amp; Gauteng, South Africa'
new_loc = b'Cape Town, Western Cape, South Africa'
if old_loc in d:
    print('location: FOUND, replacing')
    d = d.replace(old_loc, new_loc)
else:
    print('location: NOT FOUND')

f = open(r'c:\Portfolio\templates\programs-overview\index.html', 'wb')
f.write(d)
f.close()
print('DONE')
