from flask import Flask, request, render_template, redirect, session, flash

from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'surveyapp'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

survey = satisfaction_survey
# responses = []

@app.route('/')
def show_homepage():
    """show home, greeting with button to start survey"""

    return render_template('home.html', survey=survey)

@app.route('/start')
def start_survey():
    """set up session responses"""

    session['responses'] = []

    return redirect("/questions/0")

@app.route("/questions/<int:question_num>")
def show_question(question_num):
    """shows question page--page number determined by the length of received responses"""

    response_list = session.get('responses')
       
    question_num = len(response_list)
    question = survey.questions[question_num]

    if (response_list is None):
        return redirect('/')
    
    if (question_num != len(response_list)):
        flash('Please do not skip questions!')
        return redirect(f'/questions/{len(response_list)}')
    
    return render_template('questions.html', question=question, question_num=question_num)

@app.route("/response", methods=["POST"])
def add_answer():
    """posts answer provided by user & adds to responses list. If more questions, redirects to next question. If it has gone through all questions, redirects to completed page"""

    answer = request.form["answer"]
    
    response_list = session.get('responses')
    response_list.append(answer)
    session['responses'] = response_list

    if (len(response_list) == len(survey.questions)):
        return redirect ('/complete')
    
    else:
        return redirect(f'/questions/{len(response_list)}')
    
@app.route('/complete')
def show_complete():
    """Shows thank you page upon completion of the survey"""
    return render_template('complete.html')