import BaseCrawler
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger('__main__')


class Newcastle(BaseCrawler):
    Course_Page_Url = "https://www.ncl.ac.uk/mobility/experience-newcastle/module-catalogue/"
    University = "University of Newcastle"
    Abbreviation = "NU"
    University_Homepage = "https://www.ncl.ac.uk/"

    # Below fields didn't find in the website
    Prerequisite = None
    References = None
    Scores = None
    Projects = None
    Professor_Homepage = None

    def get_courses_of_department(self, department):
        department_url = "http://www.ncl.ac.uk" + department
        Course_Homepage = department_url

        department_page_content = requests.get(department_url).text
        department_soup = BeautifulSoup(department_page_content, 'html.parser')
        Department_Name = department_soup.find('h1').text
        tbody_elements = department_soup.find('tbody')
        course_elements = tbody_elements.find_all('tr')

        return course_elements, Department_Name, Course_Homepage

    def get_course_data(self, course):
        Course_Title = course.find_all('td')[1].text

        Unit_Count = course.find_all('td')[4].text
        Unit_Count = Unit_Count[:2].rstrip()

        #Description = course.find(class_='courseblockdesc').text

        #course_sections = course.find_all(class_='course-section')

        Objective = None
        Outcome = None
        Professor = None
        Required_Skills = None

        # for section in course_sections:
        #     inner_sections = section.find_all('p')
        #     for inner_section in inner_sections:
        #         inner_section_title = inner_section.find('strong')

        #         if inner_section_title.text == "Course Objectives:":
        #             inner_section_title.decompose()
        #             Objective = inner_section.text.strip()

        #         if inner_section_title.text == "Student Learning Outcomes:":
        #             inner_section_title.decompose()
        #             Outcome = inner_section.text.strip()

        #         if inner_section_title.text == "Instructor:":
        #             inner_section_title.decompose()
        #             Professor = inner_section.text.strip()

        #         if inner_section_title.text == "Prerequisites:":
        #             inner_section_title.decompose()
        #             Required_Skills = inner_section.text.strip()

        Objective, Outcome, Professor, Required_Skills, Description = self.get_course_details(course)

        return Course_Title, Unit_Count, Objective, Outcome, Professor, Required_Skills, Description


    def get_course_details(self, course):
        course_url = course.find('a').get('href')
        course_url = course_url[2:len(course_url)]
        course_url = "http://" + course_url
        course_page_content = requests.get(course_url).text
        course_soup = BeautifulSoup(course_page_content, 'html.parser')



    def handler(self):
        response = requests.get(self.Course_Page_Url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # departments = soup.find(id='atozindex').find_all('li')

        ul_elements = soup.find_all('ul')
        ul_deps = ul_elements[25:28]
        departments = []
        for ul_dep in ul_deps:
            temp = ul_dep.find_all('a')
            for element in temp:
                departments.append(element.get('href'))
        
        for department in departments:
            courses, Department_Name, Course_Homepage = self.get_courses_of_department(department)
            for course in courses:
                Course_Title, Unit_Count, Objective, Outcome, Professor, Required_Skills, Description = self.get_course_data(
                    course)

                self.save_course_data(
                    self.University, self.Abbreviation, Department_Name, Course_Title, Unit_Count,
                    Professor, Objective, self.Prerequisite, Required_Skills, Outcome, self.References, self.Scores,
                    Description, self.Projects, self.University_Homepage, Course_Homepage, self.Professor_Homepage
                )

            logger.info(f"{self.Abbreviation}: {Department_Name} department's data was crawled successfully.")

        logger.info(f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")
