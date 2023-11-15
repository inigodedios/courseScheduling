import datetime
import itertools
import random

# Define the time slots for morning and afternoon classes
morning_slots = {
    0: '9:00 AM',
    1: '10:35 AM'
}

afternoon_slots = {
    2: '2:30 PM',
    3: '4:05 PM'
}

# Combine morning and afternoon slots into one dictionary
time_slots = {**morning_slots, **afternoon_slots}


# Define a mapping from courses to their allowed time slots based on their time-of-day restrictions
allowed_time_slots = {
    'Programming With Python': morning_slots.keys() | afternoon_slots.keys(),  # All day
    'Business Technology Management': morning_slots.keys() | afternoon_slots.keys(),  # All day
    'Cloud Foundations': morning_slots.keys() | afternoon_slots.keys(),  # All day
    'Cybersecurity Management': afternoon_slots.keys(),  # Afternoon only
    'Data Analytics for Decision Making': afternoon_slots.keys(),  # Afternoon only
    'Discrete Maths for Computing': morning_slots.keys() | afternoon_slots.keys(),  # All day
    'Infrastructure for Computing': morning_slots.keys(),  # Morning only
    'SQL Lab': afternoon_slots.keys(),
    'Data Structures and Algorithms' : afternoon_slots.keys()  # Afternoon only
}

spanish_holidays = [
    # According to our master calendar!
    datetime.date(2023, 10, 12),  # Hispanic Day
    datetime.date(2023, 11, 1),   # All Saints Day
    datetime.date(2023, 11, 9),   # Almudena's Day (Madrid's Holiday)
    datetime.date(2023,12,6),     # Constitution Day
    datetime.date(2023, 12, 8),   # Immaculate Conception
]

class TrimesterSchedule:
    def __init__(self, start_date, end_date, max_courses_per_day=3):
        self.start_date = start_date
        self.end_date = end_date
        self.max_courses_per_day = max_courses_per_day
        self.dates = self._generate_dates()

    def _generate_dates(self):
        # Generate a list of dates for the trimester, excluding weekends and holidays
        delta = self.end_date - self.start_date
        return [
            self.start_date + datetime.timedelta(days=i)
            for i in range(delta.days + 1)
            if (self.start_date + datetime.timedelta(days=i)).weekday() < 5 and  # Check if it's a weekday
            (self.start_date + datetime.timedelta(days=i)) not in spanish_holidays  # Check if it's not a holiday
        ]


    # TODO Here is the problem
    # TODO ncorporate the colors assigned by the Welsh-Powell algorithm into the TrimesterSchedule class's schedule_courses method, you need to use the color information to guide the scheduling process.
    """
    he issue with the algorithm not fulfilling the requirement for the number of sessions for each course could be due to several factors, including:
    - Insufficient Dates: There may not be enough available dates to schedule all sessions, especially if the randomization leads to some dates being underutilized.
    - Randomization Over Constraints: The random choice of morning or afternoon might be too restrictive, leading to some sessions not being scheduled because their allowed time slots don't match the randomly chosen part of the day.
    - Inefficient Scheduling: The algorithm may not be efficiently filling available slots on each day, especially if it stops scheduling as soon as the maximum number of courses per day is reached, without considering whether all courses have met their session requirements."""
    # METHOD IN WHICH If there are courses not assigned and there are dates with no classes scheduled, the classes are reassigned
    # Requirement that each day should have either one or two classes in the morning or one or two classes in the afternoon, with a minimum of two and a maximum of three classes per day, we need to adjust the scheduling algorithm accordingly.
    def schedule_courses(self, course_colors, course_sessions, allowed_time_slots):
        schedule = {date: [] for date in self.dates}
        course_occurrences = {course: 0 for course in course_colors.keys()}

        # Iterate through each date in the trimester
        for date in self.dates:
            # Randomly decide to schedule morning or afternoon classes for the day
            morning = random.choice([True, False])
            slots_today = list(morning_slots.keys()) if morning else list(afternoon_slots.keys())

            # Shuffle the courses to avoid bias in scheduling
            courses_today = list(course_colors.keys())
            random.shuffle(courses_today)

            # Attempt to schedule each course
            for course in courses_today:
                # Check if we still need to schedule more sessions for this course
                if course_occurrences[course] < course_sessions[course]:
                    # Check if the course can be scheduled today based on its allowed time slots
                    for slot in allowed_time_slots[course]:
                        if slot in slots_today:
                            time_slot = time_slots[slot]
                            # Schedule the class
                            schedule[date].append((course, time_slot))
                            course_occurrences[course] += 1
                            slots_today.remove(slot)
                            break

                # Check if we have scheduled enough classes for the day
                if len(schedule[date]) >= self.max_courses_per_day or not slots_today:
                    break

            # Sort the day's schedule by time slot
            schedule[date].sort(key=lambda x: x[1])
            

        # Ensure all courses have been scheduled the correct number of times
        for course, count in course_occurrences.items():
            if count < course_sessions[course]:
                print(f"Warning: {course} has only been scheduled {count} times, but needs {course_sessions[course]} sessions.")

        return schedule

    def fill_in_gaps(self, schedule, course_occurrences, course_sessions, allowed_time_slots):
    # Iterate over each course to ensure it meets the required session count
        for course, sessions_needed in course_sessions.items():
            while course_occurrences[course] < sessions_needed:
                # Find dates where this course can be scheduled
                for date in self.dates:
                    if self.can_schedule_course_on_date(course, date, schedule, allowed_time_slots, course_occurrences):
                        # Find the next available slot on this date
                        for slot in allowed_time_slots[course]:
                            time_slot = time_slots[slot]
                            # Schedule the course in the available slot
                            schedule[date].append((course, time_slot))
                            course_occurrences[course] += 1
                            break  # Break after scheduling to avoid double booking
                    if course_occurrences[course] >= sessions_needed:
                        break  # Break the outer loop if we've scheduled enough sessions

                if course_occurrences[course] < sessions_needed:
                    # If we've gone through all dates and still can't schedule, raise an error
                    raise ValueError(f"Cannot schedule all sessions for {course}. Please check constraints.")

        # Sort the schedule for each date by time slot
        for date in schedule:
            schedule[date].sort(key=lambda x: time_slots.index(x[1]))

        return schedule

def can_schedule_course_on_date(self, course, date, schedule, allowed_time_slots, course_occurrences):
    # Check if the course has already been scheduled the maximum number of times
    if course_occurrences[course] >= course_sessions[course]:
        return False

    # Check if the course is allowed to be scheduled on this date based on time slot restrictions
    day_slots = morning_slots if date.hour < 12 else afternoon_slots
    if not set(allowed_time_slots[course]).intersection(day_slots.keys()):
        return False

    # Check if adding this course would exceed the maximum courses per day
    if len(schedule[date]) >= self.max_courses_per_day:
        return False

    # Check if the course is already scheduled on this date
    if any(course == scheduled_course for scheduled_course, _ in schedule[date]):
        return False

    return True

    