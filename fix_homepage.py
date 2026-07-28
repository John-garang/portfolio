f = open(r'c:\Portfolio\templates\index.html', 'rb')
d = f.read()
f.close()

# Swap image src
old_img = b'static/Pictures/john-ngor-deng-garang-welcome.png'
new_img = b'static/Pictures/DSC05479.jpg'
if old_img in d:
    print('img src: FOUND, replacing')
    d = d.replace(old_img, new_img)
else:
    print('img src: NOT FOUND')

f = open(r'c:\Portfolio\templates\index.html', 'wb')
f.write(d)
f.close()
print('DONE')
