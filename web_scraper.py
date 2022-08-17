import requests
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('conf info')

URL3 = "https://app.testudo.umd.edu/soc/202205"
page3 = requests.get(URL3)
supman = BeautifulSoup(page3.content, "html.parser")

all_courses = supman.find_all("div", {"class":"course-prefix row"})
count = 0
cour_names = []
for cour in all_courses:
    cour_names.append(cour.find("span", {"class":"prefix-abbrev push_one two columns"}).get_text().strip())

for department in cour_names:

    db = client[department]  # CMSC db

    URL2 = "https://app.testudo.umd.edu/soc/202208/" + department
    page2 = requests.get(URL2)
    soupy = BeautifulSoup(page2.content, "html.parser")

    print()
    print(department)
    print("---------")
    department_courses = soupy.find_all("div", {"class": "course"})

    for courses in department_courses:
        course_name = courses.find("div", {"class": "course-id"}).get_text()
        print(course_name + ":")
        coll = db[course_name]  # CMSC132 collection

        link = "https://app.testudo.umd.edu/soc/search?courseId=" + course_name + "&sectionId=&termId=202208&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"

        course_page = requests.get(link)
        sup = BeautifulSoup(course_page.content, "html.parser")

        err_msg = sup.find("div", {"class": "individual-instruction-message"})
        if str(type(err_msg)) != "<class 'NoneType'>":
            print("\t", err_msg.get_text())
            coll.insert_one({"err_msg": err_msg.get_text()})
            continue

        sections = sup.find_all("div", {"class": "section delivery-f2f"})
        all_sections = []

        for section in sections:
            s_num = section.find("span", {"class": "section-id"}).get_text().strip()

            profs = section.find("span", {"class": "section-instructors"})
            prof = []
            for name in profs.find_all("span", {"class": "section-instructor"}):
                prof.append(name.get_text())

            seats = section.find("span", {"class": "seats-info"})
            total_seats = int(seats.find("span", {"class": "total-seats-count"}).get_text())
            open_seats = int(seats.find("span", {"class": "open-seats-count"}).get_text())
            waitlist = int(seats.find("span", {"class": "waitlist-count"}).get_text())
            print("\t Section", s_num, prof,
                  "— Seats(" + "Total: " + str(total_seats) + ", Open: " + str(open_seats) + ", Waitlist: " + str(
                      waitlist) + ")")
            # print("\t Section" , s_num, prof, "— Seats(" + "Total: " + total_seats + ", Open: " + open_seats + ", Waitlist: " + waitlist + ")")
            info = {"section_number": s_num, "prof": prof, "total_seats": total_seats, "open_seats": open_seats,
                    "waitlist": waitlist}
            all_sections.append(info)

        online_sections = sup.find_all("div", {"class": "section delivery-online"})

        for section in online_sections:
            s_num = section.find("span", {"class": "section-id"}).get_text().strip()

            profs = section.find("span", {"class": "section-instructors"})
            prof = []
            for name in profs.find_all("span", {"class": "section-instructor"}):
                prof.append(name.get_text())

            seats = section.find("span", {"class": "seats-info"})
            total_seats = int(seats.find("span", {"class": "total-seats-count"}).get_text())
            open_seats = int(seats.find("span", {"class": "open-seats-count"}).get_text())
            waitlist = int(seats.find("span", {"class": "waitlist-count"}).get_text())
            print("\t Section", s_num, prof,
                  "— Seats(" + "Total: " + str(total_seats) + ", Open: " + str(open_seats) + ", Waitlist: " + str(
                      waitlist) + ")")
            # print("\t Section" , s_num, prof, "— Seats(" + "Total: " + total_seats + ", Open: " + open_seats + ", Waitlist: " + waitlist + ")")
            info = {"section_number": s_num, "prof": prof, "total_seats": total_seats, "open_seats": open_seats,
                    "waitlist": waitlist}
            all_sections.append(info)

        blended_sections = sup.find_all("div", {"class": "section delivery-blended"})

        for section in blended_sections:
            s_num = section.find("span", {"class": "section-id"}).get_text().strip()

            profs = section.find("span", {"class": "section-instructors"})
            prof = []
            for name in profs.find_all("span", {"class": "section-instructor"}):
                prof.append(name.get_text())

            seats = section.find("span", {"class": "seats-info"})
            total_seats = int(seats.find("span", {"class": "total-seats-count"}).get_text())
            open_seats = int(seats.find("span", {"class": "open-seats-count"}).get_text())
            waitlist = int(seats.find("span", {"class": "waitlist-count"}).get_text())
            print("\t Section", s_num, prof,
                  "— Seats(" + "Total: " + str(total_seats) + ", Open: " + str(open_seats) + ", Waitlist: " + str(
                      waitlist) + ")")
            # print("\t Section" , s_num, prof, "— Seats(" + "Total: " + total_seats + ", Open: " + open_seats + ", Waitlist: " + waitlist + ")")
            info = {"section_number": s_num, "prof": prof, "total_seats": total_seats, "open_seats": open_seats,
                    "waitlist": waitlist}
            all_sections.append(info)

        coll.insert_many(all_sections)

print("fin")


