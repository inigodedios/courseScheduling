"""
General Constraints:
- There is a single classroom available for courses.
- All students enrolled in a course will attend the same class session.
- Each class session will last for 1 hour and 20 minutes.
- A break of 15 minutes is scheduled between consecutive classes.
- A maximum of 3 classes can be scheduled per day for any given student, with a minimum of 2 classes.
- Subjects will not be repeated on the same day.
- The trimester begins on September 18, 2023, and concludes on December 19, 2023. 
- We have to respect the Spanish national holidays and we do not have class on weekends.

Scheduling Constraints:
- Morning classes start at 9:00 AM.
- Afternoon classes commence at 2:30 PM.
- Evening classes, if necessary, would need to be defined based on available time slots after afternoon classes.
- Only classes per day in the morning or in the afternoon

Courses and Their Restrictions:
- Programming With Python: 20 sessions, available all day.
- Business Technology Management: 15 sessions, available all day.
- Cloud Foundations: 15 sessions, available all day.
- Cybersecurity Management: 10 sessions, available in the afternoon.
- Data Analytics for Decision Making: 15 sessions, available in the afternoon.
- Discrete Maths for Computing: 15 sessions, available all day.
- Infrastructure for Computing: 10 sessions, available in the morning.
- SQL Lab: 6 sessions, available in the afternoon.

Other Relevant Information:
- Room Availability: Need to ensure no two classes are scheduled in the same room at the same time.
- Professor Availability: Professors cannot be scheduled to teach two different classes at the same time.
- Course Enrollment: If a student is enrolled in two courses, those courses cannot be scheduled at the same time.

Final goal: get a optimun shcedule for the all trismester

IMPORTANT
- The schedule should not mix morning and afternoon classes on the same day. It seems your output respects this rule
- There are many days, especially towards the end of the trimester, where no classes are scheduled at all.
- Handling Gaps and Unused Days: You've noted that there are many days, especially towards the end of the trimester, with no classes scheduled. This could be due to the random nature of the scheduling or constraints that are too tight. You might need to adjust the algorithm to distribute classes more evenly throughout the trimester.
- Validation: After scheduling, it's essential to validate the schedule to ensure that all constraints are met and that each course is scheduled for the required number of sessions.
"""
# TODO Would be great if we can explain how depending on the input, we skew the algorithm, and therefore the schedule



import datetime

from courseGraph import CourseGraph
from trimesterSchedule import TrimesterSchedule
from trimesterSchedule import allowed_time_slots

# Add the courses
courses = [
    "Programming With Python",
    "Business Technology Management",
    "Cloud Foundations",
    "Cybersecurity Management",
    "Data Analytics for Decision Making",
    "Discrete Maths for Computing",
    "Infrastructure for Computing",
    "SQL Lab"
]

# Define the courses and their constraints -> Define the number of sessions for each course
course_sessions = {
    'Programming With Python': 20,
    'Business Technology Management': 15,
    'Cloud Foundations': 15,
    'Cybersecurity Management': 10,
    'Data Analytics for Decision Making': 15,
    'Discrete Maths for Computing': 15,
    'Infrastructure for Computing': 10,
    'SQL Lab': 6
}


# Create the conflict graph for courses
course_graph = CourseGraph()
# Adding courses to the graph
for course in courses:
    course_graph.add_course(course)

# Add conflicts (This is an example. You'll need to add conflicts according to your specific situation)
course_graph.add_conflict("Cybersecurity Management", "Data Analytics for Decision Making") #Afternoon vs afternoon
course_graph.add_conflict("SQL Lab", "Data Analytics for Decision Making")                  #Afternoon vs afternoon
course_graph.add_conflict("Data Analytics for Decision Making", "SQL Lab")                  #Afternoon vs afternoon
# course_graph.add_conflict("Discrete Maths for Computing", "SQL Lab")                        #Test -> comment this line
# course_graph.add_conflict("Data Analytics for Decision Making", "SQL Lab")                  #Test -> comment this line
# course_graph.add_conflict("Data Analytics for Decision Making", "Infrastructure for Computing")     #Test -> comment this line

# Run the graph coloring algorithm to get the schedule
course_colors = course_graph.welsh_powell_algorithm()

# Initialize the schedule parameters
start_date = datetime.date(2023, 9, 18)
end_date = datetime.date(2023, 12, 19)
max_courses_per_day = 2


# Create the trimester schedule with time-of-day constraints
trimester_schedule = TrimesterSchedule(start_date, end_date, max_courses_per_day)
full_schedule = trimester_schedule.schedule_courses(course_colors, course_sessions, allowed_time_slots)



# Output the schedule
for date, day_schedule in full_schedule.items():
    print(date.strftime('%Y-%m-%d'), day_schedule)

# Creating the graph
course_graph.visualize_graph()