f = open(r'c:\Portfolio\templates\static\styles.css', 'rb')
d = f.read()
f.close()

old = (
    b".welcome-hero-image {\n"
    b"    position: relative;\n"
    b"    border-radius: 20px;\n"
    b"    overflow: hidden;\n"
    b"    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);\n"
    b"}\n"
    b"\n"
    b".welcome-hero-image img {\n"
    b"    width: 100%;\n"
    b"    height: auto;\n"
    b"    display: block;\n"
    b"    transition: transform 0.3s ease;\n"
    b"}"
)

new = (
    b".welcome-hero-image {\n"
    b"    position: relative;\n"
    b"    border-radius: 20px;\n"
    b"    overflow: hidden;\n"
    b"    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);\n"
    b"    padding: 0;\n"
    b"    align-self: stretch;\n"
    b"}\n"
    b"\n"
    b".welcome-hero-image img {\n"
    b"    width: 100%;\n"
    b"    height: 100%;\n"
    b"    object-fit: cover;\n"
    b"    display: block;\n"
    b"    transition: transform 0.3s ease;\n"
    b"}"
)

if old in d:
    print('FOUND, replacing')
    d = d.replace(old, new)
    f = open(r'c:\Portfolio\templates\static\styles.css', 'wb')
    f.write(d)
    f.close()
    print('DONE')
else:
    print('NOT FOUND')
