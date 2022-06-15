import sqlite3

DATABASE = 'C:/Users//User//Desktop//apis_flasks//db.sqlite3'


def student_score(student_id):
    def grader(score):
        if 80 <= score <= 100:
            return'A'
        elif 75 <= score < 80:
            return'B+'
        elif 70 <= score < 75:
            return 'B'
        elif 65 <= score < 70:
            return 'C+'
        elif 60 <= score < 65:
            return 'C'
        elif 55 <= score < 60:
            return 'D+'
        elif 50 <= score < 55:
            return 'D'
        else:
            return 'F'

    result = {
        "student":
        {
            "id": "primary key of student in database",
            "full_name": "student's full name",
            "school": "student's school name"
        },

            "subject_detail": [],

            "grade_point_average": None}
    credit_mapping = ['', 3, 2, 1, 2, 3]
    suject_mapping = ['', "Math", "Physics",
                          "Chemistry", "Algorithm", "Coding"]
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    score_data_list = list(cur.execute(
        f'SELECT * FROM apis_studentsubjectsscore WHERE student_id = {student_id};'))
    student_data = list(cur.execute(
        f'SELECT * FROM apis_personnel WHERE id = {student_id} AND personnel_type = 2;'))
    if student_data == []:
        return 'No Student ID', 404
    student_data = list(student_data[0])
    result['student']['id'] = student_data[0]
    result['student']['full_name'] = student_data[1] + ' ' + \
        student_data[2]
    school_class_id = student_data[4]
    school_class_data = list(cur.execute(
        f'SELECT school_id FROM apis_classes WHERE id = {school_class_id};'))
    school_id = school_class_data[0][0]
    school_data = list(cur.execute(
        f'SELECT title FROM apis_schools WHERE id = {school_id};'))
    result['student']['school'] = school_data[0][0]

    score_list = list()  # for grade average
    for score_data in score_data_list:
        subject_dict = {
            "subject": suject_mapping[score_data[4]], "credit": int(credit_mapping[score_data[4]]), "score": score_data[2], 'grade': grader(int(score_data[2]))}
        result["subject_detail"].append(subject_dict)
        score_list.append(subject_dict["credit"]*subject_dict["score"])
    average_score = sum(score_list)/len(score_list)
    average_grade = grader(average_score)
    result["grade_point_average"] = average_grade
    cur.close()
    return result
