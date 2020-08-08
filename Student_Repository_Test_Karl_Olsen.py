"""
SSW-810-WS Homework 11 - Student Repository (Test version)

@author: Karl Olsen

Credit to Kane Blueriver for creation/maintenance of PTable ("Pretty table") library (https://pypi.org/project/PTable/0.9.0/)


NOTE: Because this particular branch's feature is centered on interacting with the database and the relevant code does not interact with the code relevant
to the "wrong" .txt files, I will not be including those .txt files in the .zip or branch with this version of the code and will keep run_invalid_files() commented out
"""

from prettytable import PrettyTable as pt
from Student_Repository_Karl_Olsen import Student, Instructor, University, Major
from typing import Dict, Tuple, Set, List
import unittest, sqlite3, os

class TestUniversity(unittest.TestCase):
    stevens:University = University("Stevens", "C:/Users/Karl Olsen/Desktop/SSW_810/HW11/")
    maxDiff = None

    """
    # COMMENTING OUT BECAUSE EXCLUDING THE "WRONG" FILES FROM THIS BUILD
    def run_invalid_files(self) -> None:
        #.txt files each with a line of varying invalid input to test that such invalid input will be "ignored" when attempting to add to University's attributes 
        # Invalid major files
        self.stevens.read_majors("major_wrong_flag.txt")
        self.stevens.read_majors("major_wrong_name.txt")
        self.stevens.read_majors("major_wrong_class_letters.txt")
        self.stevens.read_majors("major_wrong_class_numbers.txt")

        # Having the wrong # of fields raises a ValueError instead of just skipping the line and printing the issue
        with self.assertRaises(ValueError):
            self.stevens.read_majors("major_wrong_num_fields.txt")

        # Invalid instructor files
        self.stevens.read_instructors("instructor_wrong_dept.txt")
        self.stevens.read_instructors("instructor_wrong_id.txt")
        self.stevens.read_instructors("instructor_wrong_name.txt")
        
        # Having the wrong # of fields raises a ValueError instead of just skipping the line and printing the issue
        with self.assertRaises(ValueError):
            self.stevens.read_instructors("instructor_wrong_num_fields.txt")

        # Invalid student files
        self.stevens.read_students("student_wrong_id.txt")
        self.stevens.read_students("student_wrong_major.txt")
        self.stevens.read_students("student_wrong_name.txt")

        # Having the wrong # of fields raises a ValueError instead of just skipping the line and printing the issue
        with self.assertRaises(ValueError):
            self.stevens.read_students("student_wrong_num_fields.txt")

        # Invalid grade files
        self.stevens.read_grades("grades_wrong_class_letters.txt")
        self.stevens.read_grades("grades_wrong_class_numbers.txt")
        self.stevens.read_grades("grades_wrong_grade_as_a_number.txt")
        self.stevens.read_grades("grades_wrong_grade_punctuation.txt")
        self.stevens.read_grades("grades_wrong_grade_too_long.txt")
        self.stevens.read_grades("grades_wrong_instructor_id.txt")
        self.stevens.read_grades("grades_wrong_student_id.txt")

        # Having the wrong # of fields raises a ValueError instead of just skipping the line and printing the issue
        with self.assertRaises(ValueError):
            self.stevens.read_grades("grades_wrong_num_fields.txt")
    """

    def test_Majors(self) -> None:
        # Testing majors
        expected_majors:Dict[str, Major] = {'SFEN' : ['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']],
                                            'CS' : ['CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]}

        generated_majors:Dict[str, Major] = {name: major.pt_info() for name, major in self.stevens._majors.items()}
        self.assertEqual(expected_majors, generated_majors)

    def test_Instructors(self) -> None:
        # Testing instructors
        expected_instructors:Set[Tuple(str, str, str, str, int)] = {('98764', 'Cohen, R', 'SFEN', 'CS 546', 1),
                                                                    ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
                                                                    ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                                                                    ('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                                                                    ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                                                                    ('98762', 'Hawking, S', 'CS', 'CS 570', 1)}

        generated_instructors:Set[Tuple(str, str, str, str, int)] = {tuple(detail) for instructor in self.stevens._instructors.values() for detail in instructor.pt_info()}
        self.assertEqual(expected_instructors, generated_instructors)

    def test_Student(self) -> None:
        """ Testing students """
        expected_students:Dict[str, Student] = {'10103' : ['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], 3.38],
                                                '10115' : ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 2.0],
                                                '10183' : ['10183', 'Musk, E', 'SFEN',  ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], 4.0],
                                                '11714' : ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], [], 3.5],}

        generated_students:Dict[str, Student] = {cwid: student.pt_info() for cwid, student in self.stevens._students.items()}
        self.assertEqual(expected_students, generated_students)

    def test_db_table(self) -> None:
        """ testing data of rows generated from database """

        expected_rows:List[str] = [('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'), 
                                ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'), 
                                ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'), 
                                ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'), 
                                ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'), 
                                ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J'), 
                                ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'), 
                                ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'), 
                                ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S')]

        generated_rows:List[str] = []
        try:
            # db_path is set to find the file "Student_Repository.db" in the directory given in University's __init__()
            db_path:str = os.path.join(os.getcwd(), "Student_Repository.db")

            db:sqlite3.Connection = sqlite3.connect(db_path)
            for row in db.execute("select s.Name as StudentName, s.CWID as StudentCWID, Course, Grade, i.Name as InstructorName From students s left join grades g on s.CWID = g.StudentCWID join instructors i on g.InstructorCWID = i.CWID"):
                generated_rows.append(row)
            db.close()
            
        except sqlite3.OperationalError:
            print(f"ERROR - {db_path} NOT A VALID .db FILE")

        self.assertEqual(expected_rows, generated_rows)
        

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)