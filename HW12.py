"""
SSW-810-WS Homework 12 - Student Repository via Flask 

@author: Karl Olsen
"""

from flask import Flask, render_template
import sqlite3
from typing import Dict

# ******NOTE: If pulled from Github and run, this path will need to be changed to match the path of the desired database
db_path:str = 'C:/Users/Karl Olsen/Desktop/SSW_810/HW12/Student_Repository.db'

app: Flask = Flask(__name__)

#http://127.0.0.1:5000/student_grades
@app.route('/student_grades')
def student_grades() -> str:
    """ reads in data from a given db path and """

    # create an SQL query for the desired data
    query = "select s.Name, s.CWID, Course, Grade, i.Name from students s join grades g on s.CWID = g.StudentCWID join instructors i on g.InstructorCWID = i.CWID order by s.Name"

    # establish connection to sqlite3 database using the db_path
    db:sqlite3.Connection = sqlite3.connect(db_path)

    # retrieve and store the data from db.execute(query) in a Dict
    data:Dict[str, str] = [{'Student':student_name, 'CWID':student_cwid, 'Course':course, 'Grade':grade, 'Instructor':instructor} for student_name, student_cwid, course, grade, instructor in db.execute(query)]

    # once done with the database, close the connection
    db.close()

    # return the stored data to the student_courses.html's template as "courses" (along with respective page/table titles)
    return render_template('student_courses.html',
                            title='Stevens Repository',
                            table_title="Student, Course, Grade, and Instructor",
                            courses=data)

# run the Flask application
app.run(debug=True)
