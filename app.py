from flask import Flask, render_template, request, redirect, url_for, flash
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import random
import copy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Static Data
FIELDS = [
    {"field_id": "CSE", "name": "Computer Science and Engineering"},
    {"field_id": "AIML", "name": "Artificial Intelligence and Machine Learning"},
    {"field_id": "CSD", "name": "Computer Science and Design"},
    {"field_id": "CSM", "name": "Computer Science and Mathematics"},
    {"field_id": "MEC", "name": "Mechanical Engineering"},
    {"field_id": "IT", "name": "Information Technology"},
    {"field_id": "EEE", "name": "Electrical and Electronics Engineering"},
    {"field_id": "ECE", "name": "Electronics and Communication Engineering"},
    {"field_id": "CSR", "name": "Computer Science and Research"},
    {"field_id": "CSE(AIML)", "name": "Computer Science and Engineering (AI & ML)"}
]

YEARS = [
    {"year": 2, "name": "2nd", "num_sections": 2},
    {"year": 3, "name": "3rd", "num_sections": 2},
    {"year": 4, "name": "4th", "num_sections": 2}
]

ROOMS = [
    {"room_id": "3301", "name": "Room 3301", "capacity": 50, "is_lab": False},
    {"room_id": "5302", "name": "Lab 5302", "capacity": 30, "is_lab": True},
    {"room_id": "7002", "name": "Room 7002", "capacity": 60, "is_lab": False},
    {"room_id": "2206", "name": "Room 2206", "capacity": 40, "is_lab": False},
    {"room_id": "1103", "name": "Room 1103", "capacity": 40, "is_lab": False}
]

TEACHERS_BY_FIELD = {
    "CSE": [
        {"teacher_id": "T1", "name": "Anita Sharma", "subject": "Java", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "T2", "name": "Bharat Singh", "subject": "DBMS", "slots_per_week": 6, "sections": ["B"]},
        {"teacher_id": "T3", "name": "Chitra Reddy", "subject": "Python", "slots_per_week": 4, "sections": ["A"]},
        {"teacher_id": "T4", "name": "Deepak Patel", "subject": "Maths", "slots_per_week": 6, "sections": ["B"]},
        {"teacher_id": "T5", "name": "Esha Gupta", "subject": "AI", "slots_per_week": 4, "sections": ["A"]},
        {"teacher_id": "T6", "name": "Firoz Khan", "subject": "IC", "slots_per_week": 2, "sections": ["B"]},
        {"teacher_id": "T7", "name": "Gaurav Mehta", "subject": "OS", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "T8", "name": "Harsha Nair", "subject": "CN", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "T9", "name": "Ishaan Bose", "subject": "Compiler Design", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "T10", "name": "Jyoti Verma", "subject": "Software Engineering", "slots_per_week": 4, "sections": ["B"]}
    ],
    "AIML": [
        {"teacher_id": "A1", "name": "Priya Menon", "subject": "Machine Learning", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "A2", "name": "Rahul Kapoor", "subject": "Deep Learning", "slots_per_week": 6, "sections": ["B"]},
        {"teacher_id": "A3", "name": "Sonia Gupta", "subject": "NLP", "slots_per_week": 4, "sections": ["A"]},
        {"teacher_id": "A4", "name": "Vikram Seth", "subject": "AI Ethics", "slots_per_week": 2, "sections": ["B"]},
        {"teacher_id": "A5", "name": "Manisha Joshi", "subject": "Computer Vision", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "A6", "name": "Rakesh Yadav", "subject": "Reinforcement Learning", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "A7", "name": "Sneha Roy", "subject": "AI Applications", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "A8", "name": "Tarun Mehta", "subject": "Data Science", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "A9", "name": "Usha Pillai", "subject": "Explainable AI", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "A10", "name": "Vikas Reddy", "subject": "AI for Healthcare", "slots_per_week": 4, "sections": ["B"]}
    ],
    "CSD": [
        {"teacher_id": "C1", "name": "Ravi Sharma", "subject": "UI/UX Design", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "C2", "name": "Meena Roy", "subject": "Graphics", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "C3", "name": "Amit Kumar", "subject": "3D Modeling", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "C4", "name": "Neha Malhotra", "subject": "Game Design", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "C5", "name": "Rajesh Singh", "subject": "Human-Computer Interaction", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "C6", "name": "Ananya Bose", "subject": "Motion Graphics", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "C7", "name": "Kunal Das", "subject": "Typography", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "C8", "name": "Shruti Tiwari", "subject": "Illustration", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "C9", "name": "Vishal Kapoor", "subject": "Animation", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "C10", "name": "Priyanka Jain", "subject": "Digital Media", "slots_per_week": 4, "sections": ["B"]}
    ],
    "CSM": [
        {"teacher_id": "M1", "name": "Arjun Singh", "subject": "Advanced Maths", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "M2", "name": "Pooja Verma", "subject": "Statistics", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "M3", "name": "Rahul Jain", "subject": "Discrete Mathematics", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "M4", "name": "Neha Sharma", "subject": "Linear Algebra", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "M5", "name": "Vikram Singh", "subject": "Calculus", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "M6", "name": "Seema Desai", "subject": "Probability", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "M7", "name": "Rohan Gupta", "subject": "Graph Theory", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "M8", "name": "Meera Kapoor", "subject": "Abstract Algebra", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "M9", "name": "Karan Patel", "subject": "Topology", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "M10", "name": "Simran Kaur", "subject": "Numerical Methods", "slots_per_week": 4, "sections": ["B"]}
    ],
    "MEC": [
        {"teacher_id": "ME1", "name": "Suresh Patil", "subject": "Thermodynamics", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "ME2", "name": "Rekha Menon", "subject": "Mechanics", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "ME3", "name": "Amit Verma", "subject": "Fluid Mechanics", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "ME4", "name": "Priya Deshmukh", "subject": "Machine Design", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "ME5", "name": "Rakesh Rao", "subject": "Manufacturing Processes", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "ME6", "name": "Anjali Kulkarni", "subject": "Dynamics", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "ME7", "name": "Nitin Gupta", "subject": "Materials Science", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "ME8", "name": "Shalini Joshi", "subject": "Heat Transfer", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "ME9", "name": "Vivek Sharma", "subject": "Robotics", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "ME10", "name": "Pooja Singh", "subject": "CAD/CAM", "slots_per_week": 4, "sections": ["B"]}
    ],
    "IT": [
        {"teacher_id": "IT1", "name": "Vijay Kumar", "subject": "Cybersecurity", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "IT2", "name": "Anjali Shah", "subject": "Cloud Computing", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "IT3", "name": "Rohan Mehta", "subject": "Network Security", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "IT4", "name": "Shweta Reddy", "subject": "Data Structures", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "IT5", "name": "Kiran Desai", "subject": "Operating Systems", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "IT6", "name": "Nisha Patel", "subject": "Software Engineering", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "IT7", "name": "Sandeep Roy", "subject": "Web Technologies", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "IT8", "name": "Meera Nair", "subject": "Mobile Computing", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "IT9", "name": "Arvind Kumar", "subject": "Database Systems", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "IT10", "name": "Kavita Singh", "subject": "Information Systems", "slots_per_week": 4, "sections": ["B"]}
    ],
    "EEE": [
        {"teacher_id": "E1", "name": "Manoj Reddy", "subject": "Circuits", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "E2", "name": "Sarita Bose", "subject": "Power Systems", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "E3", "name": "Vikram Singh", "subject": "Electromagnetics", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "E4", "name": "Anita Gupta", "subject": "Control Systems", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "E5", "name": "Rajesh Kumar", "subject": "Digital Electronics", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "E6", "name": "Neha Kapoor", "subject": "Analog Electronics", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "E7", "name": "Suresh Menon", "subject": "Microprocessors", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "E8", "name": "Pooja Sharma", "subject": "Signal Processing", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "E9", "name": "Amit Chatterjee", "subject": "VLSI Design", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "E10", "name": "Kavita Reddy", "subject": "Power Electronics", "slots_per_week": 4, "sections": ["B"]}
    ],
    "ECE": [
        {"teacher_id": "EC1", "name": "Nikhil Gupta", "subject": "Signal Processing", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "EC2", "name": "Tara Das", "subject": "Embedded Systems", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "EC3", "name": "Rahul Sharma", "subject": "Digital Communication", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "EC4", "name": "Sonal Patel", "subject": "VLSI", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "EC5", "name": "Deepak Rao", "subject": "Antenna Design", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "EC6", "name": "Megha Jain", "subject": "Microwave Engineering", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "EC7", "name": "Amit Verma", "subject": "Wireless Communication", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "EC8", "name": "Pallavi Nair", "subject": "Optical Communication", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "EC9", "name": "Siddharth Singh", "subject": "Communication Systems", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "EC10", "name": "Ritu Sharma", "subject": "RF Engineering", "slots_per_week": 4, "sections": ["B"]}
    ],
    "CSR": [
        {"teacher_id": "CR1", "name": "Kunal Mehra", "subject": "Research Methods", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "CR2", "name": "Divya Rao", "subject": "Data Analysis", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "CR3", "name": "Anil Kapoor", "subject": "Business Ethics", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "CR4", "name": "Sunita Singh", "subject": "Sustainability", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "CR5", "name": "Rohit Joshi", "subject": "Community Engagement", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "CR6", "name": "Pooja Mehta", "subject": "Social Research", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "CR7", "name": "Manoj Gupta", "subject": "CSR Strategies", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "CR8", "name": "Nandini Iyer", "subject": "Impact Assessment", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "CR9", "name": "Vijay Kumar", "subject": "Sustainable Development", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "CR10", "name": "Rekha Sharma", "subject": "Ethical Leadership", "slots_per_week": 4, "sections": ["B"]}
    ],
    "CSE(AIML)": [
        {"teacher_id": "CA1", "name": "Shalini Tiwari", "subject": "AI Fundamentals", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "CA2", "name": "Rohit Bansal", "subject": "ML Applications", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "CA3", "name": "Neeraj Singh", "subject": "Data Mining", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "CA4", "name": "Kiran Rao", "subject": "Big Data Analytics", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "CA5", "name": "Rashmi Verma", "subject": "Neural Networks", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "CA6", "name": "Amitabh Sharma", "subject": "Deep Reinforcement Learning", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "CA7", "name": "Sonal Desai", "subject": "Computer Vision", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "CA8", "name": "Manish Kapoor", "subject": "Natural Language Processing", "slots_per_week": 4, "sections": ["B"]},
        {"teacher_id": "CA9", "name": "Pallavi Singh", "subject": "Robotics", "slots_per_week": 6, "sections": ["A"]},
        {"teacher_id": "CA10", "name": "Tarun Agarwal", "subject": "AI in Healthcare", "slots_per_week": 4, "sections": ["B"]}
    ]
}

SECTION_COUNTS = {(field["field_id"], str(year["year"])): year["num_sections"] for field in FIELDS for year in YEARS}

PRE_BOOKED_SLOTS = {
    ("CSE", "2", "A"): {"slots": [], "name": ""},
    ("CSE", "2", "B"): {"slots": [], "name": ""},
    ("AIML", "2", "A"): {"slots": [], "name": ""},
    ("AIML", "2", "B"): {"slots": [], "name": ""},
    ("CSD", "2", "A"): {"slots": [], "name": ""},
    ("CSD", "2", "B"): {"slots": [], "name": ""},
    ("CSM", "2", "A"): {"slots": [], "name": ""},
    ("CSM", "2", "B"): {"slots": [], "name": ""},
    ("MEC", "2", "A"): {"slots": [], "name": ""},
    ("MEC", "2", "B"): {"slots": [], "name": ""},
    ("IT", "2", "A"): {"slots": [], "name": ""},
    ("IT", "2", "B"): {"slots": [], "name": ""},
    ("EEE", "2", "A"): {"slots": [], "name": ""},
    ("EEE", "2", "B"): {"slots": [], "name": ""},
    ("ECE", "2", "A"): {"slots": [], "name": ""},
    ("ECE", "2", "B"): {"slots": [], "name": ""},
    ("CSR", "2", "A"): {"slots": [], "name": ""},
    ("CSR", "2", "B"): {"slots": [], "name": ""},
    ("CSE(AIML)", "2", "A"): {"slots": [], "name": ""},
    ("CSE(AIML)", "2", "B"): {"slots": [], "name": ""}
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
PERIODS = [1, 2, 3, 4, 5, 6]
TOTAL_SLOTS_PER_WEEK = len(DAYS) * len(PERIODS)  # 36 slots (6 days × 6 periods)

def load_data_for_timetable(year, field_id):
    subjects_dict = {}
    year_data = next((y for y in YEARS if y["year"] == year), None)
    if not year_data:
        return subjects_dict, []

    num_sections = SECTION_COUNTS.get((field_id, str(year)), year_data["num_sections"])
    sections = []
    for i in range(num_sections):
        section_id = f"{year}-{field_id}-{chr(65 + i)}"
        sections.append({"section_id": section_id, "year": year, "field_id": field_id, "section_letter": chr(65 + i)})

    teachers = TEACHERS_BY_FIELD.get(field_id, [])
    for section in sections:
        section_id = section["section_id"]
        section_letter = section["section_letter"]
        subjects_dict[section_id] = []
        for teacher in teachers:
            if section_letter in teacher.get("sections", ["A", "B"]):
                subjects_dict[section_id].append((teacher["teacher_id"], teacher["subject"], teacher["name"], teacher["slots_per_week"]))
    return subjects_dict, sections

class Timetable:
    def __init__(self, subjects, sections, field_id, year):
        self.schedule = {}
        self.fitness = 0
        self.subjects = subjects
        self.sections = sections
        self.field_id = field_id
        self.year = year
        self.pre_booked_slots = {}  # (day, period, section_id) -> {"slots": [(day, period), ...], "name": str}
        self.teacher_schedule = {}  # (day, period, teacher_name) -> True
        self.teacher_slots_assigned = {}  # Track slots assigned per teacher per section

    def reserve_pre_booked_slots(self):
        for section in self.sections:
            section_id = section["section_id"]
            section_letter = section["section_letter"]
            pre_booked_key = (self.field_id, str(self.year), section_letter)
            pre_booked_data = PRE_BOOKED_SLOTS.get(pre_booked_key, {"slots": [], "name": ""})
            for day, period in pre_booked_data.get("slots", []):
                self.pre_booked_slots[(day, period, section_id)] = {"slots": [(day, period)], "name": pre_booked_data.get("name", "Pre-booked Slot")}

    def is_teacher_available(self, day, period, faculty, section_id):
        if (day, period, faculty) in self.teacher_schedule:
            return False
        if period > 1 and (day, period - 1, faculty) in self.teacher_schedule:
            return False
        if period < len(PERIODS) and (day, period + 1, faculty) in self.teacher_schedule:
            return False
        teacher_day_slots = sum(1 for (d, p, f) in self.teacher_schedule if d == day and f == faculty)
        if teacher_day_slots >= 2:
            return False
        return True

    def random_init(self):
        self.reserve_pre_booked_slots()
        for section_id in self.subjects:
            for teacher_id, _, faculty, slots_needed in self.subjects[section_id]:
                self.teacher_slots_assigned[(teacher_id, section_id)] = 0

        for section_id, subjects in self.subjects.items():
            if not subjects:
                continue
            subject_list = []
            for teacher_id, subject_name, faculty, slots_needed in subjects:
                for _ in range(slots_needed):
                    subject_list.append((teacher_id, subject_name, faculty))

            all_slots = [(day, period) for day in DAYS for period in PERIODS]
            random.shuffle(all_slots)

            for day, period in all_slots:
                if (day, period, section_id) in self.pre_booked_slots:
                    continue
                if any((day, period, room["room_id"], section_id) in self.schedule for room in ROOMS):
                    continue
                if not subject_list:
                    break
                for i in range(len(subject_list)):
                    teacher_id, subject_name, faculty = subject_list[i]
                    if self.is_teacher_available(day, period, faculty, section_id):
                        current_slots = self.teacher_slots_assigned.get((teacher_id, section_id), 0)
                        required_slots = next(s for t, _, _, s in subjects if t == teacher_id)
                        if current_slots >= required_slots:
                            continue
                        room = random.choice([r for r in ROOMS])
                        self.schedule[(day, period, room["room_id"], section_id)] = (
                            section_id, subject_name, faculty, room["room_id"]
                        )
                        self.teacher_schedule[(day, period, faculty)] = True
                        self.teacher_slots_assigned[(teacher_id, section_id)] = current_slots + 1
                        subject_list.pop(i)
                        break

    def calculate_fitness(self):
        conflicts = 0
        faculty_busy = {}
        room_busy = {}
        consecutive_violations = 0
        slot_violations = 0
        daily_limit_violations = 0
        for (day, period, room, section_id), (section, subject, faculty, room_id) in self.schedule.items():
            if (day, period, faculty) in faculty_busy:
                conflicts += 10
            else:
                faculty_busy[(day, period, faculty)] = True
            if (day, period, room) in room_busy:
                conflicts += 1
            else:
                room_busy[(day, period, room)] = True
            if period > 1 and (day, period - 1, faculty) in faculty_busy:
                consecutive_violations += 10
            if period < len(PERIODS) and (day, period + 1, faculty) in faculty_busy:
                consecutive_violations += 10
            teacher_day_slots = sum(1 for (d, p, f) in faculty_busy if d == day and f == faculty)
            if teacher_day_slots > 2:
                daily_limit_violations += 5
        for section_id in self.subjects:
            for teacher_id, _, _, slots_needed in self.subjects[section_id]:
                assigned_slots = self.teacher_slots_assigned.get((teacher_id, section_id), 0)
                if assigned_slots != slots_needed:
                    slot_violations += 10 * abs(assigned_slots - slots_needed)
        total_conflicts = conflicts + consecutive_violations + slot_violations + daily_limit_violations
        self.fitness = 1 / (total_conflicts + 1) if total_conflicts > 0 else 1.0

    def crossover(self, other):
        child = Timetable(self.subjects, self.sections, self.field_id, self.year)
        child.schedule = copy.deepcopy(self.schedule)
        child.pre_booked_slots = copy.deepcopy(self.pre_booked_slots)
        child.teacher_schedule = copy.deepcopy(self.teacher_schedule)
        child.teacher_slots_assigned = copy.deepcopy(self.teacher_slots_assigned)
        split_point = random.randint(0, len(DAYS) - 1)
        for day in DAYS[split_point:]:
            for period in PERIODS:
                for room in [r["room_id"] for r in ROOMS]:
                    for section_id in self.subjects.keys():
                        key = (day, period, room, section_id)
                        if key in other.schedule:
                            _, _, new_faculty, _ = other.schedule[key]
                            if not child.is_teacher_available(day, period, new_faculty, section_id):
                                continue
                            child.schedule[key] = other.schedule[key]
                            child.teacher_schedule[(day, period, new_faculty)] = True
                            teacher_id = next(t for t, _, f, _ in self.subjects[section_id] if f == new_faculty)
                            child.teacher_slots_assigned[(teacher_id, section_id)] += 1
                        elif key in child.schedule:
                            _, _, old_faculty, _ = child.schedule[key]
                            teacher_id = next(t for t, _, f, _ in self.subjects[section_id] if f == old_faculty)
                            child.teacher_slots_assigned[(teacher_id, section_id)] -= 1
                            del child.schedule[key]
                            del child.teacher_schedule[(day, period, old_faculty)]
        return child

    def mutate(self):
        if not self.schedule:
            return
        key = random.choice(list(self.schedule.keys()))
        day, period, room, section_id = key
        section, subject, faculty, room_id = self.schedule[key]
        teacher_id = next(t for t, _, f, _ in self.subjects[section_id] if f == faculty)
        self.teacher_slots_assigned[(teacher_id, section_id)] -= 1
        del self.schedule[key]
        del self.teacher_schedule[(day, period, faculty)]
        new_day = random.choice(DAYS)
        new_period = random.choice(PERIODS)
        new_room = random.choice([r["room_id"] for r in ROOMS])
        while (new_day, new_period, section_id) in self.pre_booked_slots or not self.is_teacher_available(new_day, new_period, faculty, section_id):
            new_day = random.choice(DAYS)
            new_period = random.choice(PERIODS)
        self.schedule[(new_day, new_period, new_room, section_id)] = (section_id, subject, faculty, new_room)
        self.teacher_schedule[(new_day, new_period, faculty)] = True
        self.teacher_slots_assigned[(teacher_id, section_id)] += 1

def genetic_algorithm(subjects, sections, field_id, year, pop_size=100, generations=200):
    population = [Timetable(subjects, sections, field_id, year) for _ in range(pop_size)]
    for timetable in population:
        timetable.random_init()
        timetable.calculate_fitness()
    for _ in range(generations):
        parents = random.sample(population, 2)
        parent1 = max(parents, key=lambda x: x.fitness)
        parents = random.sample(population, 2)
        parent2 = max(parents, key=lambda x: x.fitness)
        child = parent1.crossover(parent2)
        child.calculate_fitness()
        if random.random() < 0.1:
            child.mutate()
            child.calculate_fitness()
        weakest = min(population, key=lambda x: x.fitness)
        if child.fitness > weakest.fitness:
            population[population.index(weakest)] = child
    best_timetable = max(population, key=lambda x: x.fitness)
    return best_timetable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_options', methods=['GET', 'POST'])
def select_options():
    if request.method == 'POST':
        field_id = request.form.get('field', '')
        year_str = request.form.get('year', '')
        action = request.form.get('action', '')

        if not field_id or not year_str:
            field_id = request.args.get('field', '')
            year_str = request.args.get('year', '')

        if action == 'edit_sections':
            try:
                num_sections = int(request.form.get('num_sections', 1))
                if num_sections < 1:
                    flash("Number of sections must be at least 1.")
                else:
                    SECTION_COUNTS[(field_id, year_str)] = num_sections
                    flash(f"Updated number of sections to {num_sections} for {field_id} - Year {year_str}.")
            except ValueError:
                flash("Please enter a valid number of sections.")
            return redirect(url_for('select_options', field=field_id, year=year_str))

        if action == 'pre_book_slots':
            section_letter = request.form.get('section_letter')
            slot_name = request.form.get('slot_name', '').strip()
            if not slot_name:
                flash("Please enter a name for the pre-booked slots.")
                return redirect(url_for('select_options', field=field_id, year=year_str))

            pre_booked_slots = []
            for day in DAYS:
                for period in PERIODS:
                    slot_key = f'slot_{day}_{period}'
                    if request.form.get(slot_key) == 'on':
                        pre_booked_slots.append((day, period))

            if not pre_booked_slots:
                flash("Please select at least one slot to pre-book.")
                return redirect(url_for('select_options', field=field_id, year=year_str))

            PRE_BOOKED_SLOTS[(field_id, year_str, section_letter)] = {"slots": pre_booked_slots, "name": slot_name}
            flash(f"Pre-booked slots updated for {field_id} - Year {year_str} - Section {section_letter} with name: {slot_name}.")
            return redirect(url_for('select_options', field=field_id, year=year_str))

        if action == 'generate_timetable':
            try:
                year = int(year_str)
            except ValueError:
                flash("Please select a valid year.")
                return redirect(url_for('select_options', field=field_id, year=year_str))

            year_data = next((y for y in YEARS if y["year"] == year), None)
            if not year_data:
                flash("Invalid year selected.")
                return redirect(url_for('select_options', field=field_id, year=year_str))

            subjects_dict, sections = load_data_for_timetable(year, field_id)
            if not subjects_dict or not any(subjects_dict.values()):
                flash("No teachers available to generate timetable for this field.")
                return redirect(url_for('select_options', field=field_id, year=year_str))

            timetable = genetic_algorithm(subjects_dict, sections, field_id, year)
            schedule_data = {}
            pre_booked_data = {}
            for day in DAYS:
                schedule_data[day] = {}
                pre_booked_data[day] = {}
                for period in PERIODS:
                    schedule_data[day][period] = {}
                    pre_booked_data[day][period] = {}

            for (day, period, room, section_id), (section, subject, faculty, room_id) in timetable.schedule.items():
                if day not in schedule_data:
                    schedule_data[day] = {}
                if period not in schedule_data[day]:
                    schedule_data[day][period] = {}
                if section_id not in schedule_data[day][period]:
                    schedule_data[day][period][section_id] = []
                schedule_data[day][period][section_id].append({
                    "subject": subject,
                    "room": room_id,
                    "faculty": faculty
                })

            for section in sections:
                section_id = section["section_id"]
                pre_booked_key = (field_id, str(year), section["section_letter"])
                pre_booked = PRE_BOOKED_SLOTS.get(pre_booked_key, {"slots": [], "name": ""})
                for day, period in pre_booked.get("slots", []):
                    if day not in pre_booked_data:
                        pre_booked_data[day] = {}
                    if period not in pre_booked_data[day]:
                        pre_booked_data[day][period] = {}
                    pre_booked_data[day][period][section_id] = {"name": pre_booked.get("name", "Pre-booked Slot")}

            return render_template('timetable.html', days=DAYS, periods=PERIODS, schedule=schedule_data, pre_booked=pre_booked_data, field_id=field_id, year=year, sections=sections)

        if action in ['add_teacher', 'edit_teacher', 'delete_teacher']:
            if not field_id or not year_str:
                flash("Please select a field and year before managing teachers.")
                return redirect(url_for('select_options', field=field_id, year=year_str))

            if action == 'add_teacher':
                name = request.form.get('name', '').strip()
                subject = request.form.get('subject', '').strip()
                slots_per_week = request.form.get('slots_per_week')
                section = request.form.get('section')

                if not all([name, subject, slots_per_week, section]):
                    flash("All fields (Name, Subject, Slots/Week, Section) are required.")
                    return redirect(url_for('select_options', field=field_id, year=year_str))

                try:
                    slots_per_week = int(slots_per_week)
                    if slots_per_week < 1:
                        flash("Slots per week must be at least 1.")
                        return redirect(url_for('select_options', field=field_id, year=year_str))
                except ValueError:
                    flash("Slots per week must be a valid number.")
                    return redirect(url_for('select_options', field=field_id, year=year_str))

                pre_booked_key = (field_id, year_str, section)
                pre_booked_slots = len(PRE_BOOKED_SLOTS.get(pre_booked_key, {"slots": []}).get("slots", []))
                current_teachers = [t for t in TEACHERS_BY_FIELD.get(field_id, []) if section in t["sections"]]
                assigned_slots = sum(t["slots_per_week"] for t in current_teachers)
                remaining_slots_for_section = TOTAL_SLOTS_PER_WEEK - pre_booked_slots - assigned_slots

                if slots_per_week > remaining_slots_for_section:
                    flash(f"Cannot add teacher. Only {remaining_slots_for_section} slots remain for section {section}.")
                    return redirect(url_for('select_options', field=field_id, year=year_str))

                existing_teachers = TEACHERS_BY_FIELD.get(field_id, [])
                teacher_ids = [t["teacher_id"] for t in existing_teachers]
                teacher_id_base = field_id[0] + "T"
                teacher_num = 1
                while f"{teacher_id_base}{teacher_num}" in teacher_ids:
                    teacher_num += 1
                teacher_id = f"{teacher_id_base}{teacher_num}"

                new_teacher = {
                    "teacher_id": teacher_id,
                    "name": name,
                    "subject": subject,
                    "slots_per_week": slots_per_week,
                    "sections": [section]
                }
                if field_id not in TEACHERS_BY_FIELD:
                    TEACHERS_BY_FIELD[field_id] = []
                TEACHERS_BY_FIELD[field_id].append(new_teacher)
                flash(f"Teacher {name} added successfully to section {section}!")

            elif action == 'edit_teacher':
                teacher_id = request.form.get('teacher_id')
                teacher = next((t for t in TEACHERS_BY_FIELD.get(field_id, []) if t["teacher_id"] == teacher_id), None)
                if teacher:
                    old_slots = teacher["slots_per_week"]
                    teacher["name"] = request.form.get('name', teacher["name"]).strip()
                    teacher["subject"] = request.form.get('subject', teacher["subject"]).strip()
                    slots_per_week = request.form.get('slots_per_week')
                    try:
                        slots_per_week = int(slots_per_week)
                        if slots_per_week < 1:
                            flash("Slots per week must be at least 1.")
                            return redirect(url_for('select_options', field=field_id, year=year_str))
                    except ValueError:
                        flash("Slots per week must be a valid number.")
                        return redirect(url_for('select_options', field=field_id, year=year_str))

                    section = teacher["sections"][0]
                    pre_booked_key = (field_id, year_str, section)
                    pre_booked_slots = len(PRE_BOOKED_SLOTS.get(pre_booked_key, {"slots": []}).get("slots", []))
                    current_teachers = [t for t in TEACHERS_BY_FIELD.get(field_id, []) if section in t["sections"]]
                    assigned_slots = sum(t["slots_per_week"] for t in current_teachers) - old_slots
                    remaining_slots_for_section = TOTAL_SLOTS_PER_WEEK - pre_booked_slots - assigned_slots

                    if slots_per_week > remaining_slots_for_section + old_slots:
                        flash(f"Cannot update teacher. Only {remaining_slots_for_section + old_slots} slots are available for section {section}.")
                        return redirect(url_for('select_options', field=field_id, year=year_str))

                    teacher["slots_per_week"] = slots_per_week
                    flash("Teacher updated successfully!")
                else:
                    flash("Teacher not found!")

            elif action == 'delete_teacher':
                teacher_id = request.form.get('teacher_id')
                teacher = next((t for t in TEACHERS_BY_FIELD.get(field_id, []) if t["teacher_id"] == teacher_id), None)
                if teacher:
                    TEACHERS_BY_FIELD[field_id].remove(teacher)
                    flash("Teacher deleted successfully!")
                else:
                    flash("Teacher not found!")

            return redirect(url_for('select_options', field=field_id, year=year_str))

        flash("Invalid action or missing parameters.")
        return redirect(url_for('select_options', field=field_id, year=year_str))

    field_id = request.args.get('field', '')
    year_id = request.args.get('year', '')
    dynamic_sections = []
    teachers = TEACHERS_BY_FIELD.get(field_id, [])
    num_sections = 0
    pre_booked_counts = {}
    remaining_slots = {}
    assigned_slots_by_section = {}
    if field_id and year_id:
        try:
            year = int(year_id)
            year_data = next((y for y in YEARS if y["year"] == year), None)
            if year_data:
                num_sections = SECTION_COUNTS.get((field_id, year_id), year_data["num_sections"])
                for i in range(num_sections):
                    section_id = f"{year}-{field_id}-{chr(65 + i)}"
                    section_letter = chr(65 + i)
                    dynamic_sections.append({"section_id": section_id, "year": year, "field_id": field_id, "section_letter": section_letter})
                    pre_booked_key = (field_id, year_id, section_letter)
                    pre_booked_data = PRE_BOOKED_SLOTS.get(pre_booked_key, {"slots": [], "name": ""})
                    pre_booked_counts[section_letter] = len(pre_booked_data.get("slots", []))
                    section_teachers = [t for t in teachers if section_letter in t["sections"]]
                    assigned_slots_by_section[section_letter] = sum(t["slots_per_week"] for t in section_teachers)
                    remaining_slots[section_letter] = TOTAL_SLOTS_PER_WEEK - pre_booked_counts[section_letter] - assigned_slots_by_section[section_letter]
        except ValueError:
            flash("Invalid year selected.")
            return redirect(url_for('select_options'))

    return render_template('select_options.html', fields=FIELDS, years=YEARS, sections=dynamic_sections, selected_field=field_id, selected_year=year_id, teachers=teachers, num_sections=num_sections, days=DAYS, periods=PERIODS, pre_booked_slots=PRE_BOOKED_SLOTS, pre_booked_counts=pre_booked_counts, remaining_slots=remaining_slots, assigned_slots_by_section=assigned_slots_by_section)

def generate_pdf_timetable(schedule, pre_booked, field_id, year, sections):
    pdf_file = f"timetable_{field_id}_year_{year}.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    elements = []

    # Title
    styles = getSampleStyleSheet()
    title = f"Timetable for {field_id} - Year {year}"
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Table Data
    data = [['Time/Period'] + DAYS]
    for period in PERIODS:
        row = [f"Period {period}"]
        for day in DAYS:
            cell_data = []
            if pre_booked.get(day, {}).get(period, {}):
                for section_id, data in pre_booked[day][period].items():
                    cell_data.append(f"Pre-booked: {data['name']}")
            elif schedule.get(day, {}).get(period, {}):
                for section_id, slots in schedule[day][period].items():
                    for slot in slots:
                        cell_data.append(f"{slot['subject']}<br/>Room: {slot['room']}<br/>Faculty: {slot['faculty']}")
            else:
                cell_data.append("Free Slot")
            row.append("<br/>".join(cell_data))
        data.append(row)

    # Create Table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # Build PDF
    doc.build(elements)
    return pdf_file

@app.route('/download_timetable')
def download_timetable():
    field_id = request.args.get('field_id')
    year = request.args.get('year')
    schedule = request.args.get('schedule', {})
    pre_booked = request.args.get('pre_booked', {})
    sections = request.args.get('sections', [])

    # Convert string representations to dictionaries/lists if needed
    import ast
    schedule = ast.literal_eval(schedule) if isinstance(schedule, str) else schedule
    pre_booked = ast.literal_eval(pre_booked) if isinstance(pre_booked, str) else pre_booked
    sections = ast.literal_eval(sections) if isinstance(sections, str) else sections

    pdf_file = generate_pdf_timetable(schedule, pre_booked, field_id, year, sections)
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)