from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'surveyapp'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

survey = satisfaction_survey
responses = []

@app.route('/')
def show_homepage():
    """show home, greeting with button to start survey"""

    return render_template('home.html', survey=survey)

@app.route("/questions/<int:question_num>")
def show_question(question_num):
    """shows question page--page number determined by the length of received responses"""
    question_num = len(responses)
    question = survey.questions[question_num]
    return render_template('questions.html', question=question, question_num=question_num)

@app.route("/response", methods=["POST"])
def add_answer():
    answer = request.form["answer"]
    responses.append(answer)
    return redirect(f'/questions/{len(responses)}')