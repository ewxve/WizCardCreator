from PIL import Image, ImageFont, ImageDraw
from text_tools import find_origin, text_wrap, headers
from dictionaries import iconTagDict
import requests
from io import BytesIO
import re


nameFont = ImageFont.truetype('Shermlock.ttf', 48)
nameFontSmall = ImageFont.truetype('Shermlock.ttf', 38)
nameFontSmaller = ImageFont.truetype('Shermlock.ttf', 32)

accuracyFont = ImageFont.truetype('ComicSansBold.ttf', 32)

pipFont1 = ImageFont.truetype('Shermlock.ttf', 50)
pipFont2 = ImageFont.truetype('ShermlockOpen.ttf', 51)

bodyFont = ImageFont.truetype('Wizard101.otf', 30)


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


def add_accuracy(hitChance: str):
    hitChance.replace("%", "")
    hitChanceString = hitChance + "%"
    if 0 <= int(hitChance) <= 100:
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


def add_cost(pipCost: str):
    pipCostString = pipCost
    if 0 <= int(pipCost) <= 9 or pipCost.lower() == "x":
        pipCostLocation = (34, 62)
        imageWithText.text(pipCostLocation, pipCostString, font=pipFont1, fill=(255, 255, 0))
        imageWithText.text((pipCostLocation[0] - 1, pipCostLocation[1] - 6), pipCostString, font=pipFont2,
                           fill=(0, 0, 0), stroke_width=0)
    elif int(pipCost) <= 14:
        pipCostLocation = (23, 62)
        imageWithText.text(pipCostLocation, pipCostString, font=pipFont1, fill=(0, 0, 0), stroke_width=3)
        imageWithText.text(pipCostLocation, pipCostString, font=pipFont1, fill=(255, 255, 0))
    else:
        print("That is an invalid pip cost. Must be a whole number from 0-9 or X")
        exit()


def replace_body_text(bodyText: str):
    newText = bodyText.replace("DMG", "①①").replace("D", "❻❻")
    return newText


def symbol_replace(word):
    # Replace the word with a placeholder based on its length if it's an icon
    if word in iconTagDict:
        if len(word) == 2:
            return "01"  # Placeholder for 2-character icons
        elif len(word) == 3:
            return "O0O"  # Placeholder for 3-character icons
    else:
        return word  # Return the word unchanged if it's not an icon


def draw_icons(iconData, location: (int, int)):
    # Adjust the icon's position based on its length
    match len(iconData):
        case 2:
            location = (location[0] - 7, location[1] + 5)  # Slight offset for 2-character icons
        case 3:
            location = (location[0] - 5, location[1] + 5)  # Slight offset for 3-character icons
    # Open and paste the icon image at the specified location
    currentIconImage = Image.open(iconTagDict[iconData])
    cardImage.paste(currentIconImage, location, mask=currentIconImage)


def add_body(bodyText: str):
    circled_numbers = '|'.join(iconTagDict.keys())  # Assuming iconTagDict has the number symbols as keys
    pattern = rf'({circled_numbers})(?={circled_numbers})'

    # Use regex to add a space between two sets of circled numbers
    bodyText = re.sub(pattern, r'\1 ', bodyText)

    lines = text_wrap(bodyText, bodyFont)  # Wrap the text into lines based on the font

    if 0 < len(lines) <= 4:
        y_text = 395  # Initial vertical position for text
        match len(lines):
            case 1:
                y_text = 395
            case 2:
                y_text = 375
            case 3:
                y_text = 355
            case 4:
                y_text = 338

        for line in lines:
            fakeLine = ""  # For constructing the line with symbols replaced

            # Replace symbols or icons in the line
            for word in line.split():
                # Check if the word has punctuation (like commas) at the end
                if word[-1] in [",", ".", ":", ";"]:
                    word_base = word[:-1]
                    punctuation = word[-1]
                    fakeLine += symbol_replace(word_base) + punctuation + " "
                else:
                    fakeLine += symbol_replace(word) + " "
                if line.split().index(word) > 0:
                    if line.split()[line.split().index(word) - 1] in iconTagDict:
                        fakeLine = fakeLine[:-1]
            fakeLine = fakeLine.replace("01 01", "0101")
            fakeLine = fakeLine.rstrip()  # Remove trailing space from fakeLine
            #print(fakeLine)
            # Calculate the x-origin based on the canvas width
            image_width = 334  # Set this to your actual image width
            xOrigin = round((image_width / 2) - (bodyFont.getlength(fakeLine) / 2))
            #print(f'fakeLine xOrigin = {xOrigin}')

            currentOffset = 0  # Track offset for icon positioning

            for word in line.split():
                # Handle words with punctuation
                if word[-1] in [",", ".", ":", ";"]:
                    word_base = word[:-1]
                    punctuation = word[-1]
                    if word_base in iconTagDict:
                        draw_icons(word_base, (xOrigin + round(currentOffset), y_text))
                        #print((xOrigin + round(currentOffset), y_text))
                        # Replace the icon word with spaces for alignment
                        line = line.replace(word_base, "  " if len(word_base) == 2 else "    ", 1)
                else:
                    if word in iconTagDict:
                        try:
                            if line.split()[line.split().index(word)+1] not in iconTagDict:
                                draw_icons(word, (xOrigin + round(currentOffset), y_text))

                                # Replace the icon word with spaces
                                line = line.replace(word, "  " if len(word) == 2 else "   ", 1)
                            else:
                                draw_icons(word, (xOrigin + round(currentOffset), y_text))

                                # Replace the icon word with spaces
                                line = line.replace(word, " " if len(word) == 2 else "  ", 1)
                        except IndexError:
                            draw_icons(word, (xOrigin + round(currentOffset), y_text))

                            # Replace the icon word with spaces
                            line = line.replace(word, "  " if len(word) == 2 else "   ", 1)

                # Update currentOffset based on the length of the word
                currentOffset += bodyFont.getlength(symbol_replace(word_base if word[-1] in [",", ".", ":", ";"] else word) + (" "if word not in iconTagDict else ""))
            # Draw the modified line in the center
            line = line.rstrip()
            #print(f'final xOrigin = {xOrigin}')
            #imageWithText.text((xOrigin, y_text), fakeLine, font=bodyFont, fill=(0, 0, 0), stroke_width=0)
            imageWithText.text((xOrigin, y_text), line, font=bodyFont, fill=(0, 0, 0), stroke_width=0)
            #print(line)
            # Move y_text down to the next line
            y_text += bodyFont.getbbox(line)[3]


def add_school(schoolIcon):
    schoolImage = Image.open(f'{schoolIcon}Symbol.png')
    cardImage.paste(schoolImage, (263, 74), mask=schoolImage)


def add_type(cardType):
    typeImage = Image.open(f'CardTypes/Icon_{cardType}.png')
    cardImage.paste(typeImage, (261, 260), mask=typeImage)


def add_image(image: str, cardSchool):
    if image.startswith("http"):
        response = requests.get(image, allow_redirects=True, headers=headers)
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
    cardImage.save("static/CustomCard.png")
    #cardImage.show()
