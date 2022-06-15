import sqlite3

DATABASE = 'C:/Users//User//Desktop//apis_flasks//db.sqlite3'


def student_score_update(student_first_name, student_last_name, subjects_title, score):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    credit_mapping = ['', 3, 2, 1, 2, 3]
    score = int(score)
    student_first_name_sql = '\'' + student_first_name + '\''
    student_last_name_sql = '\'' + student_last_name + '\''
    subjects_title_sql = '\'' + subjects_title + '\''

    if type(student_first_name) != str or type(student_last_name) != str or type(subjects_title) != str or type(score) != int:
        con.close()
        return {'Body': 'Wrong Data', 'status': 400}

    if score < 0 or score > 100:
        con.close()
        return {'Body': 'Score out of range', 'status': 400}

    try:
        student_id = int(list(cur.execute(
            f'SELECT id FROM apis_personnel WHERE first_name = {student_first_name_sql} AND last_name = {student_last_name_sql} AND personnel_type = 2;'))[0][0])
    except:
        return {'Body': 'No Student', 'status': 400}

    try:
        subject_id = int(list(cur.execute(
            f'SELECT id FROM apis_subjects WHERE title = {subjects_title_sql};'))[0][0])
    except:
        return {'Body': 'No Subject registed', 'status': 400}

    credit = int(credit_mapping[int(subject_id)])

    score_data = list(cur.execute(
        f'SELECT * FROM apis_studentsubjectsscore WHERE student_id ={student_id} AND subjects_id = {subject_id};'))
    status = len(score_data)  # 0: Add 1: Update
    if status:
        cur.execute(
            f' Update apis_studentsubjectsscore set score = {score}  WHERE student_id ={student_id} AND subjects_id = {subject_id};')
        con.commit()
        con.close()
        return f'Name: {student_first_name} ,Lastname: {student_last_name} Student Ids: {student_id} \n Subject: {subjects_title}, Subject Ids: {subject_id}, Credits: {credit} \n Score: {score}\n Data Updated! ', 202
    else:
        field_id = int(list(cur.execute(
            f' SELECT MAX(id) FROM apis_studentsubjectsscore;'))[0][0])
        field_id += 1
        cur.execute(
            f'INSERT INTO apis_studentsubjectsscore  (id, credit, student_id, subjects_id, score) VALUES ({field_id}, {credit}, {student_id},{subject_id}, {score});')
        con.commit()
        con.close()
        return f'Name: {student_first_name} ,Lastname: {student_last_name} Student Ids: {student_id} \n Subject: {subjects_title}, Subject Ids: {subject_id}, Credits: {credit} \n Score: {score}\n Data Added! ', 201
