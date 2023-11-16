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
    def __init__(self, start_date, end_date, max_courses_per_day=2):
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
    def schedule_courses(self, course_colors, course_sessions, allowed_time_slots):
        schedule = {date: [] for date in self.dates}
        course_occurrences = {course: 0 for course in course_colors.keys()}

        # Nuevo: Guardar los colores ya programados para cada día
        colors_scheduled_per_day = {date: set() for date in self.dates}

        # Iterar a través de cada fecha en el trimestre
        for date in self.dates:
            morning = random.choice([True, False])
            slots_today = list(morning_slots.keys()) if morning else list(afternoon_slots.keys())

            courses_today = list(course_colors.keys())
            random.shuffle(courses_today)

            for course in courses_today:
                if course_occurrences[course] < course_sessions[course]:
                    course_color = course_colors[course]

                    # Verificar si el color del curso ya está programado para este día
                    if course_color not in colors_scheduled_per_day[date]:
                        for slot in allowed_time_slots[course]:
                            if slot in slots_today:
                                time_slot = time_slots[slot]
                                schedule[date].append((course, time_slot))
                                course_occurrences[course] += 1
                                slots_today.remove(slot)

                                # Agregar el color del curso a los colores programados para este día
                                colors_scheduled_per_day[date].add(course_color)
                                break

                if len(schedule[date]) >= self.max_courses_per_day or not slots_today:
                    break

            schedule[date] = sorted(schedule[date], key=lambda x: datetime.datetime.strptime(x[1], '%I:%M %p'))

        # Verificar que todos los cursos hayan sido programados el número correcto de veces
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

    