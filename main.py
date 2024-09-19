from card_components import *


inputCardSchool = "Death"
img = Image.open(f'{inputCardSchool}Back.png')

imageWithText = ImageDraw.Draw(img)

inputCardName = "Certified Pedophile LOLO"
inputAccuracy = 85
inputPipCost = 5
inputBodyText = "Target takes 75 DMG per pip and loses 2 pips"
inputType = "Drain"


add_name(inputCardName)
add_accuracy(inputAccuracy)
add_cost(inputPipCost)
add_body(inputBodyText)
add_school(inputCardSchool)
add_type(inputType)
img.show()
