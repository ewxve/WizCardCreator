from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from card_components import initialize, add_image, add_name, add_accuracy, add_cost, add_body, add_school, add_type, finalize
from PIL import Image


app = Flask(__name__, static_url_path='', static_folder='.')


app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to save uploaded files
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file extensions


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():
    inputCardName = ""
    inputCardSchool = ""
    inputPipCost = ""
    inputType = ""
    inputBodyText = ""
    inputAccuracy = ""

    if request.method == 'POST':
        inputCardSchool = request.form.get('school')
        inputCardName = request.form.get('cardname')
        inputAccuracy = request.form.get('accuracy')
        inputPipCost = request.form.get('cost')
        inputBodyText = request.form.get('body')
        inputType = request.form.get('type')

        # Handle file upload for the image
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Open the image with PIL and pass it to the add_image function
            inputImage = Image.open(file_path)
        else:
            inputImage = Image.open('INVALID.png')

        inputCardSchool = request.form.get('school')
        inputCardName = request.form.get('cardname')
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

        os.remove(file_path)

        finalize()

        return render_template('index.html', card_name=inputCardName, card_school=inputCardSchool, card_cost=inputPipCost, card_type=inputType, card_image=inputImage, card_body=inputBodyText, card_accuracy=inputAccuracy)

    return render_template('index.html')


if __name__ == '__main__':
    #app.run(debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
