from flask import Flask, render_template, request, flash, redirect
from Radar import TextRecognition
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads/'


@app.route('/')
def index():
    return render_template("dashboard.html")


@app.route('/visualise')
def visualise():
    return render_template("visualise.html")


@app.route('/text-from-image', methods=['GET', 'POST'])
def text_from_image():
    if request.method == "POST":
        file = request.files['image']
        if file.filename == '':
            print('No selected file!')
            return redirect(request.url)

        if file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            print(path)
            Map = TextRecognition(path)
            print("printing Map")
            print(Map)
            # Call Model function here and pass result to 'value'
            return render_template("text-from-image.html", values=Map, exists=True, path=path)
    else:
        return render_template("text-from-image.html")


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
