import imp
from flask import Flask, request
from apis.student_score import student_score
from apis.student_score_update import student_score_update
import os

app = Flask(__name__)
path = os.path.dirname(os.path.realpath(__name__))


@app.route("/")
def hello_world():
    return "API lists: student_score"


@app.route("/apis/student_score", methods=['POST', 'GET'])
def apis_student_score():
    if request.method == 'GET':
        student_id = request.args.get('sid')
        return student_score(student_id)
    else:
        return 'Please enter student id', 404


@app.route("/apis/student_score_update", methods=['POST', 'GET'])
def apis_student_score_update():
    if request.method == 'POST':
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        subject = request.args.get('subject')
        score = request.args.get('score')
        return student_score_update(first_name, last_name, subject, score)
    else:
        return 'Wrong Method!', 404


if __name__ == '__main__':
    app.run()
