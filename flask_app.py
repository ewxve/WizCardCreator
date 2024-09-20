from flask import Flask, render_template, request
from card_components import initialize, add_name, add_accuracy, add_cost, add_body, add_school, add_type, add_image, finalize


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    inputCardName = ""
    inputCardSchool = ""
    if request.method == 'POST':
        inputCardSchool = request.form.get('school')
        inputCardName = request.form.get('cardname')
        inputImage = request.form.get('image')
        inputAccuracy = request.form.get('accuracy')
        inputPipCost = request.form.get('cost')
        inputBodyText = request.form.get('body')
        inputType = request.form.get('type')

        # Do something with inputCardName, like passing it to your main program
        initialize(inputCardSchool)
        add_image(inputImage, inputCardSchool)
        add_name(inputCardName)
        add_accuracy(inputAccuracy)
        add_cost(inputPipCost)
        add_body(inputBodyText)
        add_school(inputCardSchool)
        add_type(inputType)

        finalize()

    return render_template('index.html', card_name=inputCardName, card_school=inputCardSchool)


if __name__ == '__main__':
    app.run(debug=True)
