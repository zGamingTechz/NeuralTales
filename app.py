from flask import Flask, redirect, render_template, request
from keys import secret_key
from ai_response import ai_response


# Definitions
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# Variables
name = ""
genre = ""
plot = ""
target_audience = ""
story_length = ""
writing_style = ""

story = list()
prev_story = list()
title = None
choice = None
choice1 = None
choice2 = None


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

        return redirect("/response")

    return render_template('form.html')


@app.route("/response", methods=["GET", "POST"])
def response():
    response = ai_response(
        name=name,
        genre=genre,
        plot=plot,
        target_audience=target_audience,
        writing_style=writing_style,
        prev_story= None if not prev_story else prev_story,
        choice=choice
    )

    global title
    title = response[0]
    paragraph = response[1]

    global choice1
    global choice2
    choice1 = response[2]
    choice2 = response[3]

    story.append(response)
    prev_story.append(paragraph)

    return redirect("/index")


@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template('index.html', story=story)


@app.route("/choice1", methods=["GET", "POST"])
def choice1():
    choice = choice1

    return redirect("/response")


@app.route("/choice2", methods=["GET", "POST"])
def choice2():
    choice = choice2

    return redirect("/response")


if __name__ == '__main__':
    app.run(debug=True)
