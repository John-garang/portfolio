from PIL import Image
imgs = [
    'john-ngor-deng-garang-cnn-academy-fellow.png',
    'john-ngor-deng-garang-unleash-global-innovation-lab.png',
    'john-ngor-deng-garang-take-action-lab.png',
    'john-ngor-deng-garang-accra-fusion.png',
    'john-ngor-deng-garang-yali-east-africa.png',
]
for f in imgs:
    img = Image.open('templates/static/Pictures/' + f)
    print(f, img.size)
