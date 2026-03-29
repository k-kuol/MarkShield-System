# Grade thresholds: (minimum_score, grade_letter)
GRADE_SCALE = [
    (90, "A+"), (85, "A"), (80, "A-"),
    (75, "B+"), (70, "B"), (65, "B-"),
    (60, "C+"), (55, "C"), (50, "C-"),
    (45, "D"),  (0,  "F")
]

# Grade letter to GPA points
GRADE_POINTS = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D":  1.0, "F": 0.0
}

# GPA standing thresholds: (minimum_gpa, standing_label)
GPA_STANDINGS = [
    (3.7, "First Class Honours"),
    (3.3, "Second Class Upper"),
    (3.0, "Second Class Lower"),
    (2.0, "Pass"),
    (0.0, "At Risk")
]

# Score boundaries
MIN_SCORE = 0
MAX_SCORE = 100
MIN_CREDIT_HOURS = 1

# Wellness scale boundaries
WELLNESS_MIN = 1
WELLNESS_MAX = 10
WELLNESS_HIGH_STRESS_THRESHOLD = 8
WELLNESS_LOW_MOOD_THRESHOLD = 3
WELLNESS_HISTORY_LIMIT = 10

# Auth constraints
MIN_PASSWORD_LENGTH = 6

# Audit trail display limit
AUDIT_DISPLAY_LIMIT = 100
