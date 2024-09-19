from PIL import Image, ImageFont, ImageDraw
from text_tools import find_origin, text_wrap
from dictionaries import iconTagDict
import requests
from io import BytesIO


nameFont = ImageFont.truetype('Shermlock.ttf', 48)
nameFontSmall = ImageFont.truetype('Shermlock.ttf', 38)
nameFontSmaller = ImageFont.truetype('Shermlock.ttf', 32)

accuracyFont = ImageFont.truetype('ComicSansBold.ttf', 32)

pipFont1 = ImageFont.truetype('Shermlock.ttf', 50)
pipFont2 = ImageFont.truetype('ShermlockOpen.ttf', 51)

bodyFont = ImageFont.truetype('Wizard101.otf', 28)


imageWithText: ImageDraw
cardImage: Image


def initialize(cardSchool):
    global imageWithText
    global cardImage
    cardImage = Image.open(f'{cardSchool}Back.png')
    imageWithText = ImageDraw.Draw(cardImage)


def add_name(cardName: str):
    widthOrigin = find_origin(cardName, nameFont)
    if not widthOrigin < 12:
        titleLocation = (widthOrigin, 2)
        imageWithText.text((titleLocation[0], titleLocation[1] + 6), cardName, font=nameFont, fill=(0, 0, 0))
        imageWithText.text(titleLocation, cardName, font=nameFont, fill=(255, 255, 255))
    else:
        widthOrigin = find_origin(cardName, nameFontSmall)
        if not widthOrigin < 12:
            titleLocation = (widthOrigin, 10)
            imageWithText.text((titleLocation[0], titleLocation[1] + 6), cardName, font=nameFontSmall, fill=(0, 0, 0))
            imageWithText.text(titleLocation, cardName, font=nameFontSmall, fill=(255, 255, 255))
        else:
            widthOrigin = find_origin(cardName, nameFontSmaller)
            if not widthOrigin < 12:
                titleLocation = (widthOrigin, 15)
                imageWithText.text((titleLocation[0], titleLocation[1] + 6), cardName, font=nameFontSmaller,
                                   fill=(0, 0, 0))
                imageWithText.text(titleLocation, cardName, font=nameFontSmaller, fill=(255, 255, 255))
            else:
                print("That is an invalid name length.")
                exit()


def add_accuracy(hitChance: int):
    hitChanceString = str(hitChance) + "%"
    if 0 <= hitChance <= 100:
        match len(hitChanceString):
            case 2:
                titleLocation = (20, 264)
            case 4:
                titleLocation = (7, 264)
            case _:
                titleLocation = (11, 264)
        imageWithText.text((titleLocation[0] + 4, titleLocation[1] + 4), hitChanceString, font=accuracyFont, fill=(0, 0, 0))
        imageWithText.text(titleLocation, hitChanceString, font=accuracyFont, fill=(255, 255, 0))
    else:
        print("That is an invalid accuracy. Must be a whole number from 0-100")
        exit()


def add_cost(pipCost: int):
    pipCostString = str(pipCost)
    if 0 <= pipCost <= 9:
        pipCostLocation = (34, 62)
        imageWithText.text(pipCostLocation, pipCostString, font=pipFont1, fill=(255, 255, 0))
        imageWithText.text((pipCostLocation[0] - 1, pipCostLocation[1] - 6), pipCostString, font=pipFont2,
                           fill=(0, 0, 0), stroke_width=0)
    else:
        print("That is an invalid pip cost. Must be a whole number from 0-9")
        exit()


def replace_body_text(bodyText: str):
    newText = bodyText.replace("DMG", "①①").replace("D", "❻❻")
    return newText


def draw_icons(iconData, location: (int, int)):
    location = (location[0] - 25, location[1])
    currentIconImage = Image.open(iconTagDict[iconData])
    cardImage.paste(currentIconImage, location, mask=currentIconImage)
    dot_radius = 3
    draw = ImageDraw.Draw(cardImage)


def add_body(bodyText: str):
    lines = text_wrap(bodyText, bodyFont)
    if 0 < len(lines) <= 4:
        y_text = 395
        match len(lines):
            case 1:
                y_text = 395
            case 2:
                y_text = 375
            case 3:
                y_text = 355
            case 4:
                y_text = 335
        for line in lines:
            xOrigin = round(167 - bodyFont.getbbox(line)[2]/2) + 5
            currentOffset = 0
            for word in line.split():
                left, top, right, bottom = bodyFont.getbbox(word.replace("❼❼", "O0").replace("①①", "O0"))
                currentOffset += right
                if word in iconTagDict:
                    draw_icons(word, ((xOrigin + round(currentOffset)), y_text))
                    line = line.replace(word, "  ", 1)
            imageWithText.text((xOrigin, y_text), line,
                               font=bodyFont, fill=(0, 0, 0), stroke_width=0)
            y_text += bodyFont.getbbox(line)[3]
    else:
        print("That is an invalid body length.")
        exit()


def add_school(schoolIcon):
    schoolImage = Image.open(f'{schoolIcon}Symbol.png')
    cardImage.paste(schoolImage, (263, 74), mask=schoolImage)


def add_type(cardType):
    typeImage = Image.open(f'CardTypes/Icon_{cardType}.png')
    cardImage.paste(typeImage, (261, 260), mask=typeImage)


def add_image(image: str, cardSchool):
    if image.startswith("http"):
        response = requests.get(image)
        mainImage = Image.open(BytesIO(response.content))
    else:
        mainImage = Image.open(image)
    sizedImage = mainImage.resize((290, 223))
    sizedImage = sizedImage.convert("RGBA")
    pngMask = Image.open("ArtMask.png")
    cardImage.paste(sizedImage, (24, 82), mask=sizedImage)
    cardBack = Image.open(f'{cardSchool}Back.png')
    cardImage.paste(cardBack, (0, 0), mask=pngMask)


def finalize():
    cardImage.show()
