from card_components import initialize, add_name, add_accuracy, add_cost, add_body, add_school, add_type, add_image, finalize

inputCardSchool = "Balance"
inputCardName = "Scorpion"
inputAccuracy = 85
inputPipCost = 2
inputBodyText = "160-200 ❼❼ ①① ❼❼ ①①"
inputType = "Damage"
inputImage = "https://www.wannapik.com/media/W1siZiIsIjIwMTYvMDgvMjIvOHF3czVobGtyZF8zMXVlZmx6aTBwX2FuaW0wMzY0LnBuZyJdXQ/49a7519479ceaae7/31ueflzi0p_anim0364.png"


initialize(inputCardSchool)
add_image(inputImage, inputCardSchool)
add_name(inputCardName)
add_accuracy(inputAccuracy)
add_cost(inputPipCost)
add_body(inputBodyText)
add_school(inputCardSchool)
add_type(inputType)

finalize()
