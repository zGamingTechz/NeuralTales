from flask import Flask, redirect, render_template, request, session
from ai_response import ai_response, generate_image

app = Flask(__name__)

try:
    from keys import secret_key
    app.config['SECRET_KEY'] = secret_key
except:
    import os
    app.config["SECRET_KEY"] = os.environ.get("secret_key", "fallback_secret")


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        session.pop("story", None)
        session.pop("prev_story", None)
        session.pop("choice", None)

        session["name"] = request.form["name"]
        session["genre"] = request.form["genre"]
        session["plot"] = request.form["plot_description"]
        session["target_audience"] = request.form["target_audience"]
        session["story_length"] = request.form["story_length"]
        session["writing_style"] = request.form["writing_style"]
        session["story"] = []
        session["prev_story"] = []
        return redirect("/response")

    return render_template('form.html')


@app.route("/response", methods=["GET", "POST"])
def response():
    response = ai_response(
        name=session.get("name"),
        genre=session.get("genre"),
        plot=session.get("plot"),
        target_audience=session.get("target_audience"),
        writing_style=session.get("writing_style"),
        prev_story=session.get("prev_story"),
        choice=session.get("choice")
    )

    session["title"] = response[0]
    paragraph = response[1]
    session["choice1"] = response[2]
    session["choice2"] = response[3]

    story = session.get("story", [])
    prev_story = session.get("prev_story", [])

    image_url = generate_image(session.get("title"))
    response = list(response)
    response.append(image_url)

    story.append(response)
    prev_story.append(paragraph)

    session["story"] = story
    session["prev_story"] = prev_story

    return redirect("/index")


@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template('index.html', story=session.get("story", []))


@app.route("/choice1", methods=["GET", "POST"])
def choice_one():
    session["choice"] = session.get("choice1")
    return redirect("/response")


@app.route("/choice2", methods=["GET", "POST"])
def choice_two():
    session["choice"] = session.get("choice2")
    return redirect("/response")


@app.route("/undo", methods=["GET", "POST"])
def undo():
    story = session.get("story", [])
    story.pop()
    session["story"] = story

    return redirect("/index")
