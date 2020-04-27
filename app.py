from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config["SECRET_KEY"] = "letsgetloud1986"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"


@app.route("/")
def get_home_page():
    """Renders home page"""
    return render_template("home.html", survey=survey)


@app.route("/start", methods=["POST"])
def start_survey():
    """Empty response list"""
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/questions/<int:id>")
def answer_question(id):
    """Display the current question"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/completed")

    if (len(responses) != id):
        flash(f"Invalid question id: {id}")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[id]
    return render_template("questions.html", quetion_number=id, question=question)


@app.route("/answer", methods=["POST"])
def get_question_anwers():
    """Save question answers and move to following question"""
    choice = request.form["answer"]

    # add response to answer key
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    return render_template("completed.html")
