from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("dashboard.html")

@app.route('/visualise')
def visualise():
    return render_template("visualise.html")

@app.route('/text-from-image')
def text_from_image():
    return render_template("text-from-image.html")

if __name__ == '__main__':
    app.run(debug=True)