from card_components import initialize, add_name, add_accuracy, add_cost, add_body, add_school, add_type, add_image, finalize
from card_presets import scorpion

inputCardSchool = "Balance"
inputCardName = "Victini"
inputAccuracy = 30
inputPipCost = 0
inputBodyText = "10 ①① and -50% ③③ ⑧⑧ to self"
inputType = "Damage"
inputImage = "tini.png"


initialize(inputCardSchool)
add_image(inputImage, inputCardSchool)
add_name(inputCardName)
add_accuracy(inputAccuracy)
add_cost(inputPipCost)
add_body(inputBodyText)
add_school(inputCardSchool)
add_type(inputType)

finalize()
