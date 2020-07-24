"""
SSW-810-WS Homework 10 - Student Repository (Test version)

@author: Karl Olsen

Credit to Kane Blueriver for creation/maintenance of PTable ("Pretty table") library (https://pypi.org/project/PTable/0.9.0/)



NOTES TO PROFESSOR: 
-Because University.__init__() involves calling the functions to print the pretty tables, creating a University to test will print
those tables before running test cases when this code is run.

-With the switch to only skipping invalid lines for input (instead of raising errors), I've made a single test suite function reading in a variety of invalid .txt 
files for majors, students, instructors, and grades. Because the source code naturally prints out invalid input lines, feel free to comment out the call to the function 
on line 73 if you feel the output is too cluttered.
"""

from prettytable import PrettyTable as pt
from Student_Repository_Karl_Olsen import Student, Instructor, University, Major
import unittest

class TestUniversity(unittest.TestCase):
    stevens:University = University("Stevens", "C:/Users/Karl Olsen/Desktop/SSW_810/HW10/")

    def run_invalid_files(self) -> None:
        """ .txt files each with a line of varying invalid input to test that such invalid input will be "ignored" when attempting to add to University's attributes """
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

    def test_data(self) -> None:
        """ Given instructor, student, grade, and major .txt files, tests accuracy of resulting pretty tables' data """
        
        # Read in a test suite of invalid files that should not add anything to the University's Majors/Students/Instructors attributes
        self.run_invalid_files()

        # Testing majors
        expected_majors:str =("+-------+----------------------------------------------+-----------------------------------+\n"
            "| Major |               Required Courses               |             Electives             |\n"
            "+-------+----------------------------------------------+-----------------------------------+\n"
            "|  SFEN | ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'] |   ['CS 501', 'CS 513', 'CS 545']  |\n"
            "|  SYEN |      ['SYS 612', 'SYS 671', 'SYS 800']       | ['SSW 540', 'SSW 565', 'SSW 810'] |\n"
            "+-------+----------------------------------------------+-----------------------------------+")
        self.assertEqual(expected_majors, self.stevens.get_pretty_string_majors())
        
        # Testing instructors
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

        # Testing students
        expected_students:str = ("+-------+-------------+-------+---------------------------------------------+----------------------------------------------+-----------------------------------+------+\n"
            "|  CWID |     Name    | Major |              Completed Courses              |              Remaining Required              |        Remaining Electives        | GPA  |\n"
            "+-------+-------------+-------+---------------------------------------------+----------------------------------------------+-----------------------------------+------+\n"
            "| 10103 |  Baldwin, C |  SFEN | ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'] |            ['SSW 540', 'SSW 555']            |                 []                | 3.44 |\n"
            "| 10115 |   Wyatt, X  |  SFEN | ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'] |            ['SSW 540', 'SSW 555']            |                 []                | 3.81 |\n"
            "| 10172 |  Forbes, I  |  SFEN |            ['SSW 555', 'SSW 567']           |            ['SSW 540', 'SSW 564']            |   ['CS 501', 'CS 513', 'CS 545']  | 3.88 |\n"
            "| 10175 | Erickson, D |  SFEN |      ['SSW 564', 'SSW 567', 'SSW 687']      |            ['SSW 540', 'SSW 555']            |   ['CS 501', 'CS 513', 'CS 545']  | 3.58 |\n"
            "| 10183 |  Chapman, O |  SFEN |                 ['SSW 689']                 | ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'] |   ['CS 501', 'CS 513', 'CS 545']  | 4.0  |\n"
            "| 11399 |  Cordova, I |  SYEN |                 ['SSW 540']                 |      ['SYS 612', 'SYS 671', 'SYS 800']       |                 []                | 3.0  |\n"
            "| 11461 |  Wright, U  |  SYEN |      ['SYS 611', 'SYS 750', 'SYS 800']      |            ['SYS 612', 'SYS 671']            | ['SSW 540', 'SSW 565', 'SSW 810'] | 3.92 |\n"
            "| 11658 |   Kelly, P  |  SYEN |                      []                     |      ['SYS 612', 'SYS 671', 'SYS 800']       | ['SSW 540', 'SSW 565', 'SSW 810'] | 0.0  |\n"
            "| 11714 |  Morton, A  |  SYEN |            ['SYS 611', 'SYS 645']           |      ['SYS 612', 'SYS 671', 'SYS 800']       | ['SSW 540', 'SSW 565', 'SSW 810'] | 3.0  |\n"
            "| 11788 |  Fuller, E  |  SYEN |                 ['SSW 540']                 |      ['SYS 612', 'SYS 671', 'SYS 800']       |                 []                | 4.0  |\n"
            "+-------+-------------+-------+---------------------------------------------+----------------------------------------------+-----------------------------------+------+")
        self.assertEqual(expected_students, self.stevens.get_pretty_string_students())


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)