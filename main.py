from PIL import Image, ImageDraw, ImageFont


def find_origin(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return int(round((334 - width) / 2))


nameFont = ImageFont.truetype('Shermlock.ttf', 48)
nameFontSmall = ImageFont.truetype('Shermlock.ttf', 38)
nameFontSmaller = ImageFont.truetype('Shermlock.ttf', 32)

accuracyFont = ImageFont.truetype('ComicSansBold.ttf', 32)

pipFont1 = ImageFont.truetype('Shermlock.ttf', 50)
pipFont2 = ImageFont.truetype('ShermlockOpen.ttf', 51)

bodyFont = ImageFont.truetype('Wizard101.otf', 20)

cardSchool = "Myth"
img = Image.open(f'{cardSchool}Back.png')

imageWithText = ImageDraw.Draw(img)

inputCardName = "Ninja Pigs BlaBlaBla"
inputAccuracy = 85


def add_name(cardName: str):
    widthOrigin = find_origin(cardName, nameFont)
    if not widthOrigin < 12:
        titleLocation = (widthOrigin, 2)
        imageWithText.text((titleLocation[0], titleLocation[1] + 6), cardName, font=nameFont, fill=(0, 0, 0))
        imageWithText.text(titleLocation, cardName, font=nameFont, fill=(255, 255, 255))
    else:
        widthOrigin = find_origin(cardName, nameFontSmall)
        if not widthOrigin < 12:
            titleLocation = (widthOrigin, 8)
            imageWithText.text((titleLocation[0], titleLocation[1] + 6), cardName, font=nameFontSmall, fill=(0, 0, 0))
            imageWithText.text(titleLocation, cardName, font=nameFontSmall, fill=(255, 255, 255))
        else:
            widthOrigin = find_origin(cardName, nameFontSmaller)
            if not widthOrigin < 12:
                titleLocation = (widthOrigin, 13)
                imageWithText.text((titleLocation[0], titleLocation[1] + 6), cardName, font=nameFontSmaller, fill=(0, 0, 0))
                imageWithText.text(titleLocation, cardName, font=nameFontSmaller, fill=(255, 255, 255))
            else:
                print("That is an invalid name length.")
                exit()


def add_accuracy(hitChance: int):
    hitChanceString = str(hitChance) + "%"
    ### widthOrigin = find_origin(hitChanceString, accuracyFont) - 128
    if 0 <= hitChance <= 100:
        match len(hitChanceString):
            case 2:
                titleLocation = (20, 264)
            case 4:
                titleLocation = (7, 264)
            case _:
                titleLocation = (11, 264)
        imageWithText.text((titleLocation[0], titleLocation[1] + 4), hitChanceString, font=accuracyFont, fill=(0, 0, 0))
        imageWithText.text(titleLocation, hitChanceString, font=accuracyFont, fill=(255, 255, 0))
    else:
        print("That is an invalid accuracy. Must be a whole number from 0-100")
        exit()


def add_cost(pipCost: int):
    pipCostString = str(pipCost)
    if 0 <= pipCost <= 9:
        pipCostLocation = (35, 62)
        imageWithText.text(pipCostLocation, pipCostString, font=pipFont1, fill=(255, 255, 0))
        imageWithText.text((pipCostLocation[0] - 1, pipCostLocation[1] - 6), pipCostString, font=pipFont2, fill=(0, 0, 0))
    else:
        print("That is an invalid pip cost. Must be a whole number from 0-9")
        exit()


def add_body(bodyText: str):
    widthOrigin = find_origin(bodyText, bodyFont)
    if not widthOrigin < 12:
        bodyLocation = (widthOrigin, 400)
        imageWithText.text(bodyLocation, bodyText, font=bodyFont, fill=(0, 0, 0))
    else:
        print("That is an invalid body length.")
        exit()


add_name(inputCardName)
add_accuracy(inputAccuracy)
add_cost(1)
add_body("hello friend ①")
img.show()
