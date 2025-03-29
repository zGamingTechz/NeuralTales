from flask import Flask, redirect, render_template, request
import keys


# Definitions
app = Flask(__name__)
app.config['SECRET_KEY'] = keys.secret_key

# Variables
name = ""
genre = ""
plot = ""
target_audience = ""
story_length = ""
writing_style = ""

story = dict()


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        global name
        global genre
        global plot
        global target_audience
        global story_length
        global writing_style

        name = request.form["name"]
        genre = request.form["genre"]
        plot = request.form["plot_description"]
        target_audience = request.form["target_audience"]
        story_length = request.form["story_length"]
        writing_style = request.form["writing_style"]

        return redirect("/ai_response")

    return render_template('form.html')


@app.route("/ai_response", methods=["GET", "POST"])
def ai_response():
    pass


@app.route("/index", methods=["GET", "POST"])
def index():
    pass


if __name__ == '__main__':
    app.run(debug=True)
