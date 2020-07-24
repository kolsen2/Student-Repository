"""
SSW-810-WS Homework 9 - University Database (Test version)

@author: Karl Olsen

Credit to Kane Blueriver for creation/maintenance of PTable ("Pretty table") library (https://pypi.org/project/PTable/0.9.0/)
"""

from prettytable import PrettyTable as pt
from HW09_Karl_Olsen import Student, Instructor, University
import unittest

class TestUniversity(unittest.TestCase):
    stevens:University = University("Stevens", "C:/Users/Karl Olsen/Desktop/SSW_810/HW9/")

    def test_read_instructors(self) -> None:
        """ Tests for errors in reading in instructor .txt files"""

        # Instructor's name is given as a number
        with self.assertRaises(TypeError):
            self.stevens.read_instructors("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/instructor_wrong_name.txt")
        
        # Instructor's ID is given as letters
        with self.assertRaises(TypeError):
            self.stevens.read_instructors("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/instructor_wrong_id.txt")

        # Instructor's department is given as a number
        with self.assertRaises(TypeError):
            self.stevens.read_instructors("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/instructor_wrong_dept.txt")

        # File has an extra field in a line
        with self.assertRaises(ValueError):
            self.stevens.read_instructors("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/instructor_wrong_num_fields.txt")

    def test_read_students(self) -> None:     
        """ Tests for errors in reading in student .txt files """   

        # Student's name is given as a number 
        with self.assertRaises(TypeError):
            self.stevens.read_students("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/student_wrong_name.txt")
        
        # Student's ID is given as letters
        with self.assertRaises(TypeError):
            self.stevens.read_students("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/student_wrong_id.txt")

        # Student's major is given as a number
        with self.assertRaises(TypeError):
            self.stevens.read_students("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/student_wrong_dept.txt")

        # File has an extra field in a line
        with self.assertRaises(ValueError):
            self.stevens.read_students("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/student_wrong_num_fields.txt")

    def test_read_grades(self) -> None:
        """ Tests for errors in reading in grade .txt files """

        # Student ID is given as letters
        with self.assertRaises(TypeError):
            self.stevens.read_grades("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/grades_wrong_student_id.txt")
        
        # Course major (i.e. SSW) given as numbers
        with self.assertRaises(TypeError):
            self.stevens.read_grades("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/grades_wrong_class_letters.txt")

        # Course identifier (i.e. 810) given as letters
        with self.assertRaises(TypeError):
            self.stevens.read_grades("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/grades_wrong_class_numbers.txt")
        
        # Grade given as a number instead of a letter
        with self.assertRaises(TypeError):
            self.stevens.read_grades("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/grades_wrong_grade_as_a_number.txt")

        # Grade marker given as punctuation that is not '-' or '+'
        with self.assertRaises(TypeError):
            self.stevens.read_grades("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/grades_wrong_grade_punctuation.txt")
        
        # Grade given is more than 1 letter (and optional punctuation) long
        with self.assertRaises(TypeError):
            self.stevens.read_grades("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/grades_wrong_grade_too_long.txt")

        # Instructor ID is given as letters
        with self.assertRaises(TypeError):
            self.stevens.read_grades("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/grades_wrong_instructor_id.txt")

    def test_data(self) -> None:
        """ Given valid instructor, student, and grade .txt files, tests accuracy of resulting pretty tables' data """
        
        self.stevens.read_instructors("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/instructors.txt")
        self.stevens.read_students("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/students.txt")
        self.stevens.read_grades("C:/Users/Karl Olsen/Desktop/SSW_810/HW9/grades.txt")

        expected_instructors:str = ("+-------+-------------+------+---------+----------+\n"
            "|  CWID |     Name    | Dept |  Course | Students |\n"
            "+-------+-------------+------+---------+----------+\n"
            "| 98765 | Einstein, A | SFEN | SSW 567 |    4     |\n"
            "| 98765 | Einstein, A | SFEN | SSW 540 |    3     |\n"
            "| 98764 |  Feynman, R | SFEN | SSW 564 |    3     |\n"
            "| 98764 |  Feynman, R | SFEN | SSW 687 |    3     |\n"
            "| 98764 |  Feynman, R | SFEN |  CS 501 |    1     |\n"
            "| 98764 |  Feynman, R | SFEN |  CS 545 |    1     |\n"
            "| 98763 |  Newton, I  | SFEN | SSW 555 |    1     |\n"
            "| 98763 |  Newton, I  | SFEN | SSW 689 |    1     |\n"
            "| 98762 |  Hawking, S | SYEN | _______ |    0     |\n"
            "| 98761 |  Edison, A  | SYEN | _______ |    0     |\n"
            "| 98760 |  Darwin, C  | SYEN | SYS 800 |    1     |\n"
            "| 98760 |  Darwin, C  | SYEN | SYS 750 |    1     |\n"
            "| 98760 |  Darwin, C  | SYEN | SYS 611 |    2     |\n"
            "| 98760 |  Darwin, C  | SYEN | SYS 645 |    1     |\n"
            "+-------+-------------+------+---------+----------+")
        self.assertEqual(expected_instructors, self.stevens.get_pretty_string_instructors())

        expected_students:str = ("+-------+-------------+---------------------------------------------+\n"
            "|  CWID |     Name    |              Completed Courses              |\n"
            "+-------+-------------+---------------------------------------------+\n"
            "| 10103 |  Baldwin, C | ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'] |\n"
            "| 10115 |   Wyatt, X  | ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'] |\n"
            "| 10172 |  Forbes, I  |            ['SSW 555', 'SSW 567']           |\n"
            "| 10175 | Erickson, D |      ['SSW 564', 'SSW 567', 'SSW 687']      |\n"
            "| 10183 |  Chapman, O |                 ['SSW 689']                 |\n"
            "| 11399 |  Cordova, I |                 ['SSW 540']                 |\n"
            "| 11461 |  Wright, U  |      ['SYS 611', 'SYS 750', 'SYS 800']      |\n"
            "| 11658 |   Kelly, P  |                 ['SSW 540']                 |\n"
            "| 11714 |  Morton, A  |            ['SYS 611', 'SYS 645']           |\n"
            "| 11788 |  Fuller, E  |                 ['SSW 540']                 |\n"
            "+-------+-------------+---------------------------------------------+")
        self.assertEqual(expected_students, self.stevens.get_pretty_string_students())


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)