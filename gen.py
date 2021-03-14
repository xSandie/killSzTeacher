import random
from PIL import Image, ImageDraw, ImageFont


def getRandomStr():
    random_num = str(random.randint(0, 9))
    return random_num


def getRandomColor():
    R = random.randint(0, 130)
    G = random.randint(0, 130)
    B = random.randint(0, 130)

    if R == 255 and G == 255 and B == 255:
        R = G = B = 0

    return (R, G, B)


def generate_captcha():
    image = Image.new('RGB', (95, 30), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Microsoft Sans Serif.ttf', size=24)
    label = ''

    for i in range(4):
        random_char = getRandomStr()

        label += random_char
        draw.text((10+i*20 , 0), random_char, getRandomColor(), font=font)

    width = 95
    height = 30

    # for i in range(3):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw.line((x1, y1, x2, y2), fill=(0, 0, 0))

    for i in range(10):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=getRandomColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        # draw.arc((x, y, x + 4, y + 4), 0, 90, fill=(0, 0, 0))
    image.save(open(''.join(['test/', f'{label}.png']), 'wb'), 'png')


if __name__ == '__main__':
    [generate_captcha() for _ in range(10)]