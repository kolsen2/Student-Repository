"""
SSW-810-WS Homework 10 - Student Repository (Source version)

@author: Karl Olsen

Credit to Kane Blueriver for creation/maintenance of PTable ("Pretty table") library (https://pypi.org/project/PTable/0.9.0/)


IMPORTANT NOTES: 
-Changed from previous iteration: If an input .txt has an invalid line (i.e. "ABC" for a CWID in students.txt), the program will instead print out the invalid line, 
not use that line's information, and continue reading the next line in the file instead of raising errors.
"""

from prettytable import PrettyTable as pt
from collections import defaultdict
from typing import List, Tuple, IO, Dict, Iterator, DefaultDict
import os

class Student:
    def __init__(self, cwid:str, name:str, major:str) -> None:
        """ Initialization function for Student class """
        self._cwid:str = cwid
        self._name:str = name
        self._major:Major = major
        self._gpa:float = 0.0
        # key = course "id" (i.e. SSW 810), value = grade
        self._completed_courses:Dict[str, str] = {}

    def add_course(self, course_name:str, grade:str) -> None:
        """ Add a given course and its respective grade to the student's completed_courses Dict """
        self._completed_courses[course_name] = grade

    def passed_courses(self) -> List[str]:
        """ Returns a list of the student's courses in which they got a C or higher """
        passed_courses:List[str] = []
        for course, grade in self._completed_courses.items():
            if grade == "A" or grade == "A-" or grade == "B+" or grade == "B" or grade == "B-" or grade == "C+" or grade == "C":
                passed_courses.append(course)
        
        return passed_courses
    
    def update_major_reqs(self) -> None:
        """ Update the student's specific Major's required/elective courses based on what courses the student has completed """
        self._major.update_reqs(self._completed_courses)

    def update_GPA(self) -> None:
        """ Iterates through all of the studne'ts completed courses to calculate their GPA """
        new_gpa:float = 0
        for grade in self._completed_courses.values():
            if grade == 'A':
                new_gpa += 4.0
            elif grade == 'A-':
                new_gpa += 3.75
            elif grade == 'B+':
                new_gpa += 3.25
            elif grade == 'B':
                new_gpa += 3.0
            elif grade == 'B-':
                new_gpa += 2.75
            elif grade == 'C+':
                new_gpa += 2.25
            elif grade == 'C':
                new_gpa += 2.0
            # Anything below a C doesn't add anything
        
        # Once sum is calculated, divide it by the # of courses to get a GPA (rounding to 2 decimal places)
        self._gpa = round(new_gpa / len(self._completed_courses.keys()), 2)

    def pt_info(self) -> List[str]:
        """ Basic pretty_table row output """
        return [self._cwid, self._name, self._major.name, sorted(self.passed_courses()), sorted(self._major.req_courses), sorted(self._major.ele_courses), self._gpa]

class Major:
    def __init__(self, name:str) -> None:
        """" Initialization function for Major class """
        self._name:str = name
        self._req_courses:List[str] = []
        self._ele_courses:List[str] = []
    
    @property
    def name(self) ->str:
        """ read-only "getter" for major's _name """
        return self._name
    
    @property
    def req_courses(self) -> List[str]:
        """ read-only "getter for a Major's required courses """
        return self._req_courses
    
    @property
    def ele_courses(self) -> List[str]:
        """ read-only "getter for a Major's elective courses """
        return self._ele_courses
    
    def add_course(self, course_name:str, flag:str) -> None:
        """ adds a given course to a major's required or elective courses list, depending on flag given """
        if flag == "R":
            self._req_courses.append(course_name)
        elif flag == "E":
            self._ele_courses.append(course_name)
    
    def update_reqs(self, completed:Dict[str, str]) -> None:
        """ updates requirements of required and elective courses for this specific major instance """
        for key, value in completed.items():
            # Make sure student passed course before removing it
            # NOTE: This comes with expectation that grade values given are actual grade values
            if value == "C-" or value == "D+" or value == "D" or value == "D-" or value == "F":
                continue
            else:
                if key in self._req_courses:
                    self._req_courses.remove(key)
                # Students need to only take 1 elective course so if one has been taken, clear the electives
                elif key in self._ele_courses:
                    self._ele_courses.clear()

    def duplicate(self) -> "Major":
        """ helper function to duplicate a University's Major instance into a an independent copy for a Student instance"""
        temp:Major = Major(self.name)

        for req in self._req_courses:
            temp.add_course(req, "R")
        for ele in self._ele_courses:
            temp.add_course(ele, "E")

        return temp

    def pt_info(self) -> List[str]:
        """ Basic pretty_table row output """
        return [self._name, sorted(self._req_courses), sorted(self._ele_courses)]


class Instructor:
    def __init__(self, cwid:str, name:str, dept:str) -> None:
        """ Initialization function for Instructor class """
        self._cwid:str = cwid
        self._name:str = name
        self._dept:str = dept
        # key = course "id" (i.e. SSW 810), value = # of students in course
        self._courses:DefaultDict[str, int] = defaultdict(int)

    def increment_student_count(self, course_name:str) -> None:
        """ Add 1 student to a given course that the instructor teaches"""
        self._courses[course_name] += 1
    
    def pt_info(self) -> List[str]:
        """ Basic pretty_table row output """
        """ NOTE: Because instructor's pt prints a row for each class, instructor will need to call this multiple times, so writing as a generator """
        if len(self._courses.keys()) == 0:
            yield [self._cwid, self._name, self._dept, "_______", 0]
        for course_name, student_count in self._courses.items():
            yield [self._cwid, self._name, self._dept, course_name, student_count]

class University:
    def __init__(self, name:str, path:str) -> None:
        """ Initialization function for University class """
        try:
            self._name:str = name
            os.chdir(path)
            # key = instructor CWID, value = respective instructor class object
            self._instructors:Dict[str, Instructor] = {}
            # key = student CWID, value = respective student class object
            self._students:Dict[str, Student] = {}
            self._majors:List[Major] = []
            self._p_instructors = pt()
            self._p_students = pt()
            self._p_majors = pt()        

            # read in respective files
            self.read_majors("majors.txt")

            self.read_students("students.txt")
            self.read_instructors("instructors.txt")
            self.read_grades("grades.txt")

            # Once grades/courses have been read in, update students' major requirements & GPAs
            for student in self._students.values():
                student.update_major_reqs()
                student.update_GPA()
            
            # have __init__ call pretty_print for students and instructors
            self._pretty_print_majors()
            self._pretty_print_students()
            self._pretty_print_instructors()
        except FileNotFoundError as fnf:
            print(fnf)

    # Would normally make protected, but deliberately keeping public for testing purposes
    def read_majors(self, path:str) -> None:
        """ Given a .txt file, reads in info for majors and populates the university's list of majors with that info """
        for name, flag, course_name in file_reader(path, 3, "\t", True):

            # First element (major name) must be made only of letters
            if not name.isalpha():
                print(f"MAJOR READING ERROR: Third value in row must be major name made of only letters. Skipping line {name} {flag} {course_name}")
                continue
            # Second element (flag) must either be an 'R' or an 'E'
            elif flag != 'R' and flag != 'E':
                print(f"MAJOR READING ERROR: Received course flag that is not 'R' or 'E'. Skipping line {name} {flag} {course_name}")
                continue
            # Third element (course name) must be a valid course name (i.e. SSW 810)
            # Could include check of "or not line[1][:-4].isupper()" considering major names tend to be uppercase, but feels unnecessary for purposes of the assignment
            elif not course_name[-2:].isdigit() or not course_name[:-4].isalpha():
                print(f"MAJOR READING ERROR: Second value in row must be made of letters indicating department, followed by a space and 3 numbers. Skipping line {name} {flag} {course_name}")
                continue

            # if major name doesn't exist in the University's self.majors List, create it and add it to the University's self.majors List
            if not any(major.name == name for major in self._majors):
                temp_maj:Major = Major(name)
                self._majors.append(temp_maj)
            
            # Once the University's Major has been identified, add the line's course_name and its flag to that major
            for major in self._majors:
                if major.name == name:
                    major.add_course(course_name, flag)
    
    # Would normally make protected, but deliberately keeping public for testing purposes
    def read_instructors(self, path:str) -> None:
        """ Given a .txt file, reads in info for instructors and populates the university's list of instructors with that info """
        for cwid, name, dept in file_reader(path, 3, "|", True):
            # First element (CWID) must be made only of numbers
            if not cwid.isdigit():
                print(f"INSTRUCTOR READING ERROR: First value in row must be CWID made only of numbers. Skipping line {cwid} {name} {dept}")
                continue
            # Second element (name) must be a last name, a comma, a space, then a first name
            elif not name[:-3].isalpha() or name[-3] != ',' or name[-3:].isalpha():
                print(f"INSTRUCTOR READING ERROR: Second value in row must be instructor name with format: 'LastName, FirstInitial'. Skipping line {cwid} {name} {dept}")
                continue
            # Third element (department) must be made only of letters
            # Could include check of "or not line[2].isupper()" considering dept. names tend to be uppercase, but feels unnecessary for purposes of the assignment
            elif not dept.isalpha():
                print(f"INSTRUCTOR READING ERROR: Third value in row must be department name made of only letters. Skipping line {cwid} {name} {dept}")
                continue

            # Once error-checks have been cleared, create a temp instructor and add them to the university's list of instructors
            temp:Instructor = Instructor(cwid, name, dept)
            self._instructors[cwid] = temp
    
    # Would normally make protected, but deliberately keeping public for testing purposes
    def read_students(self, path:str) -> None:
        """ Given a .txt file, reads in info for students and populates the university's list of students with that info """
        for cwid, name, major in file_reader(path, 3, ";", True):
            # First element (CWID) must be made only of numbers
            if not cwid.isdigit():
                print(f"STUDENT READING ERROR: First value in row must be CWID made only of numbers. Skipping line {cwid} {name} {major}")
                continue
            # Second element (name) must be a last name, a comma, a space, then a first name
            elif not name[:-3].isalpha() or name[-3] != ',' or name[-3:].isalpha():
                print(f"STUDENT READING ERROR: Second value in row must be student name with format: 'LastName, FirstInitial'. Skipping line {cwid} {name} {major}")
                continue
            # Third element (major) must be made only of letters
            # Could include check of "or not line[2].isupper()" considering major names tend to be uppercase, but feels unnecessary for purposes of the assignment
            elif not major.isalpha():
                print(f"STUDENT READING ERROR: Third value in row must be major name made of only letters. Skipping line {cwid} {name} {major}")
                continue

            # if attempting to assign a non-existent major to a student, skip that line
            if not any(maj.name == major for maj in self._majors):
                print(f"No major named {major} at University. Skipping read_student line {cwid} {name} {major}")
                continue
            
            # Note to professor for screenshot: this is in the context of the University.read_students() function where "self" refers to the University
            for maj in self._majors:
                # "major" in this context is the major given in a line from students.txt (i.e. SFEN or SYEN)
                if major == maj.name:
                    # need to create a copy of "maj" and assign it to student (this doesn't work, just an attempt at copying the class object)
                    temp_major:Major = maj.duplicate()

                    temp:Student = Student(cwid, name, temp_major)

                    # add student to University's "students" Dict
                    self._students[cwid] = temp

    # Would normally make protected, but deliberately keeping public for testing purposes
    def read_grades(self, path:str) -> None:
        """ Given a .txt file, reads in a student ID, the class, the student's grade, and the instructor's ID and applies the relevant info to the corresponding student and instructor """
        for stud_cwid, course, grade, inst_cwid in file_reader(path, 4, "|", True):
            # First element (student CWID) must be made only of numbers
            if not stud_cwid.isdigit():
                print(f"GRADE READING ERROR: First value in row must be student CWID made only of numbers. Skipping line {stud_cwid} {course} {grade} {inst_cwid}")
                continue
            # Using the assumption that a course's "number indicator" MUST be 3 digits
            # Could include check of "or not line[1][:-4].isupper()" considering major names tend to be uppercase, but feels unnecessary for purposes of the assignment
            elif not course[-2:].isdigit() or not course[:-4].isalpha():
                print(f"GRADE READING ERROR: Second value in row must be made of letters indicating department, followed by a space and 3 numbers. Skipping line {stud_cwid} {course} {grade} {inst_cwid}")
                continue
            # Third element (grade) must be made of a single letter optionally followed by a '-' or '+'
            # Could include checek that line[2][0] is 'A', 'B', 'C', 'D', or 'F', but feels unnecessary for purposes of the assignment
            elif not grade[0].isalpha() or (len(grade) == 2 and not (grade[1] == '-' or grade[1] == '+')) or len(grade) > 2:
                print(f"GRADE READING ERROR: Third value in row must be a single-letter grade and can optionally end with a '+' or '-'. Skipping line {stud_cwid} {course} {grade} {inst_cwid}")
                continue
            # Last element (instructor CWID) must be made only of numbers
            elif not inst_cwid.isdigit():
                print(f"GRADE READING ERROR: Last value in row must be instructor CWID made only of numbers. Skipping line {stud_cwid} {course} {grade} {inst_cwid}")
                continue

            # Skipping any line with a CWID of a student or instructor that does not currently exist
            # NOTE: Probably not 100% necessary to output which line is being skipped to the average user, but keeping in for debug purposes.
            if self._students.get(stud_cwid) == None:
                print(f"Non-existent student CWID given. Skipping line {stud_cwid} {course} {grade} {inst_cwid}")
                continue                
            elif self._instructors.get(inst_cwid) == None:
                print(f"Non-existent instructor CWID given. Skipping line {stud_cwid} {course} {grade} {inst_cwid}")
                continue 

            # Once error-checks have been cleared, add a course and its respective grade to the corresponding student's "courses" Dict
            self._students.get(stud_cwid).add_course(course, grade)
            # Increment an instructor's course's student count by 1 (defaultdict automatically adds "new" courses to instructor and gives it value 1 after incrementing)
            self._instructors.get(inst_cwid).increment_student_count(course)

    def _pretty_print_majors(self) -> None:
        """ Basic pretty_print output function for majors """
        # Since get_pretty_string_majors() already generates the pretty table and returns it as a string, can just print that instead of having the 
        # "same" code running twice in 2 functions
        print("Majors Summary")
        print(self.get_pretty_string_majors())


    def _pretty_print_students(self) -> None:
        """ Basic pretty_print output function for students """
        # Since get_pretty_string_students() already generates the pretty table and returns it as a string, can just print that instead of having the 
        # "same" code running twice in 2 functions
        print("Student Summary")
        print(self.get_pretty_string_students())

    def _pretty_print_instructors(self) -> None:
        """ Basic pretty_print output function for students """
        # Since get_pretty_string_instructors() already generates the pretty table and returns it as a string, can just print that instead of having the 
        # "same" code running twice in 2 functions
        print("Instructor Summary")
        print(self.get_pretty_string_instructors())

    # Would normally make protected, but deliberately keeping public for testing purposes
    def get_pretty_string_majors(self) -> str:
        """ returns pretty_table of majors as a string """
        # Clearing table because if the function is called more than once without clearing, the table will effectively duplicate itself, returning all elements twice
        self._p_majors.clear_rows()

        self._p_majors.field_names = ["Major", "Required Courses", "Electives"]
        for major in self._majors:
            self._p_majors.add_row(major.pt_info())

        return self._p_majors.get_string()

    # Would normally make protected, but deliberately keeping public for testing purposes
    def get_pretty_string_instructors(self) -> str:
        """ returns pretty_table of instructors as a string """
        # Clearing table because if the function is called more than once without clearing, the table will effectively duplicate itself, returning all elements twice
        self._p_instructors.clear_rows()

        self._p_instructors.field_names = ["CWID", "Name", "Dept", "Course", "Students"]
        for instructor in self._instructors.values():
            for line in instructor.pt_info():
                self._p_instructors.add_row(line)

        return self._p_instructors.get_string()

    # Would normally make protected, but deliberately keeping public for testing purposes
    def get_pretty_string_students(self) -> str:
        """ returns pretty_table of students as a string """
        # Clearing table because if the function is called more than once without clearing, the table will effectively duplicate itself, printing all elements twice
        self._p_students.clear_rows()

        self._p_students.field_names = ["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives", "GPA"]
        for student in self._students.values():
            self._p_students.add_row(student.pt_info())
        
        return self._p_students.get_string()

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
        stevens:University = University("Stevens", "C:/Users/Karl Olsen/Desktop/SSW_810/HW10/")
        NYU:University = University("NYU", "C:/Users/Karl Olsen/Desktop/SSW_810/HW11/")

    except ValueError as v:
        print(v)
    except TypeError as t:
        print(t)
    """

    return

if __name__ == "__main__":
    main()