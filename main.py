from card_components import initialize, add_name, add_accuracy, add_cost, add_body, add_school, add_type, finalize

inputCardSchool = "Death"
inputCardName = "Certified Pedophile LOLO"
inputAccuracy = 85
inputPipCost = 5
inputBodyText = "Target takes 75 DMG per pip and loses 2 pips"
inputType = "Drain"


initialize(inputCardSchool)
add_name(inputCardName)
add_accuracy(inputAccuracy)
add_cost(inputPipCost)
add_body(inputBodyText)
add_school(inputCardSchool)
add_type(inputType)

finalize()
