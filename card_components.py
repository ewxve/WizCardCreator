from PIL import Image, ImageFont, ImageDraw
from text_tools import find_origin, text_wrap


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
            imageWithText.text(((167 - bodyFont.getbbox(line)[2]/2) + 5, y_text), line, font=bodyFont, fill=(0, 0, 0), stroke_width=0)
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


def finalize():
    cardImage.show()
