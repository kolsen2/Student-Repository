"""
SSW-810-WS Homework 9 - University Database (Source version)

@author: Karl Olsen

Credit to Kane Blueriver for creation/maintenance of PTable ("Pretty table") library (https://pypi.org/project/PTable/0.9.0/)


NOTES: 
-For the purpose of debugging, in the case of a .txt file having an incorrect # of fields, I've switched file_reader to output
the line where an error was found using 0-starting indicies (i.e. first line = "line 0", second line = "line 1", etc.)
-Regarding protected class methods, would normally make all of University's methods protected. However, as the test .py file needs to call those
functions, leaving them as public.

"""

from prettytable import PrettyTable as pt
from collections import defaultdict
from typing import List, Tuple, IO, Dict, Iterator, DefaultDict
import os

class Student:
    def __init__(self, cwid:str, name:str, major:str) -> None:
        """ Initialization function for Student class """
        self.cwid:str = cwid
        self.name:str = name
        self.major:str = major
        # key = course "id" (i.e. SSW 810), value = grade
        self.courses:Dict[str, str] = {}


class Instructor:
    def __init__(self, cwid:str, name:str, dept:str) -> None:
        """ Initialization function for Instructor class """
        self.cwid:str = cwid
        self.name:str = name
        self.dept:str = dept
        # key = course "id" (i.e. SSW 810), value = # of students in course
        self.courses:DefaultDict[str, int] = defaultdict(int)

class University:
    def __init__(self, name:str, path:str) -> None:
        """ Initialization function for University class """
        self.name:str = name
        os.chdir(path)
        # key = instructor CWID, value = respective instructor class object
        self.instructors:Dict[str, Instructor] = {}
        # key = student CWID, value = respective student class object
        self.students:Dict[str, Student] = {}
        self.p_instructors = pt()
        self.p_students = pt()        

        # read in respective files
        self.read_students("students.txt")
        self.read_instructors("instructors.txt")
        self.read_grades("grades.txt")
        
        # have __init__ call pretty_print for students and instructors
        self._pretty_print_students()
        self._pretty_print_instructors()
    
    def read_instructors(self, path:str) -> None:
        """ Given a .txt file, reads in info for instructors and populates the university's list of instructors with that info """
        for cwid, name, dept in file_reader(path, 3, "\t", False):
            # First element (CWID) must be made only of numbers
            if not cwid.isdigit():
                raise TypeError(f"INSTRUCTOR READING ERROR: First value in row must be CWID made only of numbers. Instead got {cwid}")
            # Second element (name) must be a last name, a comma, a space, then a first name
            elif not name[:-3].isalpha() or name[-3] != ',' or name[-3:].isalpha():
                raise TypeError(f"INSTRUCTOR READING ERROR: Second value in row must be instructor name with format: 'LastName, FirstInitial'. Instead got {name}")
            # Third element (department) must be made only of letters
            # Could include check of "or not line[2].isupper()" considering dept. names tend to be uppercase, but feels unnecessary for purposes of the assignment
            elif not dept.isalpha():
                raise TypeError(f"INSTRUCTOR READING ERROR: Third value in row must be department name made of only letters. Instead got {dept}")

            # Once error-checks have been cleared, create a temp instructor and add them to the university's list of instructors
            temp:Instructor = Instructor(cwid, name, dept)
            self.instructors[cwid] = temp
    
    def read_students(self, path:str) -> None:
        """ Given a .txt file, reads in info for students and populates the university's list of students with that info """
        for cwid, name, major in file_reader(path, 3, "\t", False):
            # First element (CWID) must be made only of numbers
            if not cwid.isdigit():
                raise TypeError(f"STUDENT READING ERROR: First value in row must be CWID made only of numbers. Instead got {cwid}")
            # Second element (name) must be a last name, a comma, a space, then a first name
            elif not name[:-3].isalpha() or name[-3] != ',' or name[-3:].isalpha():
                raise TypeError(f"STUDENT READING ERROR: Second value in row must be student name with format: 'LastName, FirstInitial'. Instead got {name}")
            # Third element (major) must be made only of letters
            # Could include check of "or not line[2].isupper()" considering major names tend to be uppercase, but feels unnecessary for purposes of the assignment
            elif not major.isalpha():
                raise TypeError(f"STUDENT READING ERROR: Third value in row must be major name made of only letters. Instead got {major}")

            # Once error-checks have been cleared, create a temp student and add them to the university's list of students
            temp:Student = Student(cwid, name, major)
            self.students[cwid] = temp

    def read_grades(self, path:str) -> None:
        """ Given a .txt file, reads in a student ID, the class, the student's grade, and the instructor's ID and applies the relevant info to the corresponding student and instructor """
        for stud_cwid, course, grade, inst_cwid in file_reader(path, 4, "\t", False):
            # First element (student CWID) must be made only of numbers
            if not stud_cwid.isdigit():
                raise TypeError(f"GRADE READING ERROR: First value in row must be student CWID made only of numbers. Instead got {stud_cwid}")
            # Using the assumption that a course's "number indicator" MUST be 3 digits
            # Could include check of "or not line[1][:-4].isupper()" considering major names tend to be uppercase, but feels unnecessary for purposes of the assignment
            elif not course[-2:].isdigit() or not course[:-4].isalpha():
                raise TypeError(f"GRADE READING ERROR: Second value in row must be made of letters indicating department, followed by a space and 3 numbers. Instead got {course}")
            # Third element (grade) must be made of a single letter optionally followed by a '-' or '+'
            # Could include checek that line[2][0] is 'A', 'B', 'C', 'D', or 'F', but feels unnecessary for purposes of the assignment
            elif not grade[0].isalpha() or (len(grade) == 2 and not (grade[1] == '-' or grade[1] == '+')) or len(grade) > 2:
                raise TypeError(f"GRADE READING ERROR: Third value in row must be a single-letter grade and can optionally end with a '+' or '-'. Instead got {grade}")
            # Last element (instructor CWID) must be made only of numbers
            elif not inst_cwid.isdigit():
                raise TypeError(f"GRADE READING ERROR: Last value in row must be instructor CWID made only of numbers. Instead got {inst_cwid}")

            # Skipping any line with a CWID of a student or instructor that does not currently exist
            # NOTE: Probably not 100% necessary to output which line is being skipped to the average user, but keeping in for debug purposes.
            if self.students.get(stud_cwid) == None:
                print(f"Non-existent student CWID given. Skipping line {stud_cwid} {course} {grade} {inst_cwid}")
                continue                
            elif self.instructors.get(inst_cwid) == None:
                print(f"Non-existent instructor CWID given. Skipping line {stud_cwid} {course} {grade} {inst_cwid}")
                continue 

            # Once error-checks have been cleared, add a course and its respective grade to the corresponding student's "courses" Dict
            self.students.get(stud_cwid).courses[course] = grade
            # Increment an instructor's course's student count by 1 (defaultdict automatically adds "new" courses to instructor and gives it value 1 after incrementing)
            self.instructors.get(inst_cwid).courses[course] += 1

    def _pretty_print_students(self) -> None:
        """ Basic pretty_print output function for students """
        # Clearing table because if the function is called more than once, the table will effectively duplicate itself, printing all elements twice
        self.p_students.clear_rows()

        print("Student Summary")
        self.p_students.field_names = ["CWID", "Name", "Completed Courses"]
        for student in self.students.values():
            self.p_students.add_row([student.cwid, student.name, sorted(student.courses)])
        
        print(self.p_students)

    def _pretty_print_instructors(self) -> None:
        """ Basic pretty_print output function for students """
        # Clearing table because if the function is called more than once, the table will effectively duplicate itself, printing all elements twice
        self.p_instructors.clear_rows()

        print("Instructor Summary")
        self.p_instructors.field_names = ["CWID", "Name", "Dept", "Course", "Students"]
        for instructor in self.instructors.values():
            if instructor.courses == {}:
                self.p_instructors.add_row([instructor.cwid, instructor.name, instructor.dept, "_______", 0])
            else:
                for course in instructor.courses:
                    self.p_instructors.add_row([instructor.cwid, instructor.name, instructor.dept, course, instructor.courses[course]])
        
        print(self.p_instructors)

    def get_pretty_string_instructors(self) -> str:
        """ returns pretty_table of instructors as a string """
        # Clearing table because if the function is called more than once, the table will effectively duplicate itself, returning all elements twice
        self.p_instructors.clear_rows()

        self.p_instructors.field_names = ["CWID", "Name", "Dept", "Course", "Students"]
        for instructor in self.instructors.values():
            if instructor.courses == {}:
                self.p_instructors.add_row([instructor.cwid, instructor.name, instructor.dept, "_______", 0])
            else:
                for c in instructor.courses:
                    self.p_instructors.add_row([instructor.cwid, instructor.name, instructor.dept, c, instructor.courses[c]])

        return self.p_instructors.get_string()

    def get_pretty_string_students(self) -> str:
        """ returns pretty_table of students as a string """
        # Clearing table because if the function is called more than once, the table will effectively duplicate itself, printing all elements twice
        self.p_students.clear_rows()

        self.p_students.field_names = ["CWID", "Name", "Completed Courses"]
        for student in self.students.values():
            self.p_students.add_row([student.cwid, student.name, sorted(student.courses)])
        
        return self.p_students.get_string()

def file_reader(path:str, fields:int, sep:str = ',', header:bool = False) -> Iterator[List[str]]:
    """ Reads a file and breaks it up into fields using a given separator (default ","). Can skip the first line by setting header to True (default False) """
    """ Yields line-by-line, one at a time """
    # Check to make sure only .txt files are read
    if(path[-4:] != '.txt'):
        raise TypeError(f"ERROR: File MUST be a .txt. Was given {path}")
    try:
        fp:IO = open(path, 'r')
    except FileNotFoundError:
        print(f"Error - file {path} not found!")
    else:
        with fp:
            for counter, line in enumerate(fp):
                # Split the line into individual words separated by the given "sep"                                   
                words:List[str] = line.rstrip("\n").split(sep)

                # Check to make sure the correct # of words in the line
                if len(words) != fields:
                    raise ValueError(f"ValueError: {path} has {len(words)} fields on line {counter}, but expected {fields}")

                # For the first line, if header is True, skip the line (and toggle header to False so subsequent lines aren't skipped)
                if header == True:
                    header = False
                    continue

                yield words

def main() -> None:  
    """
    try:
        stevens:University = University("Stevens", "C:/Users/Karl Olsen/Desktop/SSW_810/HW9/")

    except Exception as e:
        print(e)
    """
    return

if __name__ == "__main__":
    main()