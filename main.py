from card_components import initialize, add_name, add_accuracy, add_cost, add_body, add_school, add_type, add_image, finalize
import webbrowser
import os

inputCardSchool = "Fire"
inputCardName = "Raising Hell"
inputAccuracy = "100"
inputPipCost = "4"
inputBodyText = "200 ❶❶ ①① to ⑭⑭⑭, then 700 ❶❶ ①① to ⑫⑫⑫"
inputType = "Damage"
inputImage = "https://pbs.twimg.com/media/E5b-dPvVIAAomHK.png"


initialize(inputCardSchool)
add_image(inputImage, inputCardSchool)
add_name(inputCardName)
add_accuracy(inputAccuracy)
add_cost(inputPipCost)
add_body(inputBodyText)
add_school(inputCardSchool)
add_type(inputType)

finalize()
