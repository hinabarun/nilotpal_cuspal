import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Any

from ttkthemes import ThemedTk
import swisseph as swe
import datetime
import math
import os
import json
import pytz
import re
import logging  # For more structured debugging

import timedelta
from tkcalendar import DateEntry

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
debug_logger = logging.getLogger('AstrologyDebug')
debug_logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all debug messages

# Console Handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
debug_logger.addHandler(ch)

# File Handler (optional, uncomment to enable file logging)
fh = logging.FileHandler('astrology_debug.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
debug_logger.addHandler(fh)
# ----------------------------------------
# MEDICAL ASTROLOGY DATASETS
# ----------------------------------------
# Data compiled from Traditional texts, and principles from S.P. Khullar,
# K. Bhaskaran (KP), and Krishnamurti Padhdhati (KP).
# Note: Many systems share a traditional base; the distinctions often lie in
# methodology (e.g., sub-lords in KP) rather than completely different significations.

PLANETS_MEDICAL_DATA = {
    'Sun': {
        'Traditional': {
            'Body Parts': ['Heart', 'Bones', 'Right Eye', 'Stomach', 'Head', 'Spinal Cord', 'Vitality'],
            'Diseases': ['Heart problems', 'Low energy', 'Bone weakness (osteoporosis)', 'Spinal issues', 'Issues with right eye', 'High fever', 'Baldness']
        },
        'Khullar': {
            'Body Parts': ['Heart', 'Bones'],
            'Diseases': ['Heart attack', 'Palpitation', 'Sunstroke']
        },
        'Krishnamurthy': {
            'Body Parts': ['Heart', 'Bone', 'Spine'],
            'Diseases': ['Heart weakness', 'Fractures', 'General weakness of body']
        }
    },
    'Moon': {
        'Traditional': {
            'Body Parts': ['Mind', 'Blood', 'Lungs', 'Left Eye', 'Stomach', 'Breasts', 'Body Fluids'],
            'Diseases': ['Mental illness', 'Anxiety', 'Depression', 'Cold/Cough', 'Lung problems', 'Blood pressure issues', 'Insomnia', 'Asthma']
        },
        'Khullar': {
            'Body Parts': ['Mind', 'Fluids'],
            'Diseases': ['Mental affliction', 'Sleep disorders', 'Watery diseases']
        },
        'Krishnamurthy': {
            'Body Parts': ['Mind', 'Stomach', 'Uterus'],
            'Diseases': ['Mental tension', 'Worry', 'Menstrual disorders', 'Gastric issues']
        }
    },
    'Mars': {
        'Traditional': {
            'Body Parts': ['Muscles', 'Bone Marrow', 'Blood', 'Head', 'Genitals'],
            'Diseases': ['Accidents', 'Cuts', 'Burns', 'Surgery', 'Boils', 'Fever', 'High blood pressure', 'Inflammation', 'Piles']
        },
        'Khullar': {
            'Body Parts': ['Blood', 'Marrow'],
            'Diseases': ['Accidents', 'Surgery', 'Burns', 'Bleeding']
        },
        'Krishnamurthy': {
            'Body Parts': ['Teeth', 'Forehead', 'Muscles'],
            'Diseases': ['Blood leakage', 'Laceration', 'Operations', 'Boils', 'Toothache']
        }
    },
    'Mercury': {
        'Traditional': {
            'Body Parts': ['Nervous System', 'Skin', 'Lungs', 'Speech organs', 'Tongue', 'Hands'],
            'Diseases': ['Skin diseases', 'Nervous breakdowns', 'Vertigo', 'Speech impediments', 'Respiratory issues', 'Impotence (psychological)']
        },
        'Khullar': {
            'Body Parts': ['Nerves', 'Skin'],
            'Diseases': ['Leucoderma', 'Mental instability', 'Stammering']
        },
        'Krishnamurthy': {
            'Body Parts': ['Nerves', 'Nose', 'Navel'],
            'Diseases': ['Nervous debility', 'Stammering', 'Skin irritation']
        }
    },
    'Jupiter': {
        'Traditional': {
            'Body Parts': ['Liver', 'Fat', 'Thighs', 'Arterial Circulation', 'Spleen'],
            'Diseases': ['Diabetes', 'Liver problems (Jaundice)', 'Obesity', 'High cholesterol', 'Spleen disorders', 'Tumors']
        },
        'Khullar': {
            'Body Parts': ['Liver', 'Fat'],
            'Diseases': ['Liver cirrhosis', 'Diabetes', 'Blood cancer']
        },
        'Krishnamurthy': {
            'Body Parts': ['Liver', 'Arteries'],
            'Diseases': ['Liver complaints', 'Blood vessel issues', 'Hernia']
        }
    },
    'Venus': {
        'Traditional': {
            'Body Parts': ['Reproductive System', 'Kidneys', 'Throat', 'Face', 'Semen', 'Eyes'],
            'Diseases': ['Venereal diseases', 'Kidney stones', 'Throat infections', 'Cataracts', 'Diabetes', 'Urinary issues']
        },
        'Khullar': {
            'Body Parts': ['Face', 'Eyes', 'Semen'],
            'Diseases': ['Eye trouble', 'Sexual debility', 'Glandular issues']
        },
        'Krishnamurthy': {
            'Body Parts': ['Kidneys', 'Uterus', 'Prostate'],
            'Diseases': ['Kidney issues', 'Venereal diseases', 'Lack of sexual vigour']
        }
    },
    'Saturn': {
        'Traditional': {
            'Body Parts': ['Teeth', 'Bones', 'Joints', 'Knees', 'Spleen', 'Nerves'],
            'Diseases': ['Chronic illnesses', 'Arthritis', 'Rheumatism', 'Dental problems', 'Paralysis', 'Gout', 'Constipation', 'Depression']
        },
        'Khullar': {
            'Body Parts': ['Legs', 'Nerves'],
            'Diseases': ['Chronic disease', 'Paralysis', 'Gas troubles']
        },
        'Krishnamurthy': {
            'Body Parts': ['Legs', 'Muscles', 'End-life'],
            'Diseases': ['Lingering diseases', 'Leg fracture', 'Exhaustion', 'Glandular issues']
        }
    },
    'Rahu': {
        'Traditional': {
            'Body Parts': ['Intestines', 'Breath', 'Mouth'],
            'Diseases': ['Mysterious illnesses', 'Cancer', 'Poisons', 'Phobias', 'Skin diseases (leprosy)', 'Hiccups', 'Addictions']
        },
        'Khullar': {
            'Body Parts': ['Feet', 'Breath'],
            'Diseases': ['Phobias', 'Incurable diseases', 'Poisoning']
        },
        'Krishnamurthy': {
            'Body Parts': ['Bones', 'Poison'],
            'Diseases': ['Pain in the legs', 'Snake bite', 'Food poisoning', 'Epidemics']
        }
    },
    'Ketu': {
        'Traditional': {
            'Body Parts': ['Abdomen', 'Claws/Nails'],
            'Diseases': ['Sudden illness', 'Fevers', 'Cuts', 'Accidents', 'Psychic disturbances', 'Intestinal worms', 'Low blood pressure']
        },
        'Khullar': {
            'Body Parts': ['Belly', 'Uterus'],
            'Diseases': ['Defective speech', 'Intestinal worms', 'Sudden illness']
        },
        'Krishnamurthy': {
            'Body Parts': ['Poison', 'Generative organs'],
            'Diseases': ['Contagious diseases', 'Virus infection', 'Surgical operations']
        }
    }
}
# --- ADD THESE NEW CONSTANTS FOR VEHICLE ANALYSIS ---
SIGN_MODALITY = {
    "Aries": "Movable", "Taurus": "Fixed", "Gemini": "Dual", "Cancer": "Movable",
    "Leo": "Fixed", "Virgo": "Dual", "Libra": "Movable", "Scorpio": "Fixed",
    "Sagittarius": "Dual", "Capricorn": "Movable", "Aquarius": "Fixed", "Pisces": "Dual"
}

SIGN_ELEMENT = {
    "Aries": "Fire", "Taurus": "Earth", "Gemini": "Air", "Cancer": "Water",
    "Leo": "Fire", "Virgo": "Earth", "Libra": "Air", "Scorpio": "Water",
    "Sagittarius": "Fire", "Capricorn": "Earth", "Aquarius": "Air", "Pisces": "Water"
}

# Based on traditional classifications
SIGN_LEGS = {
    "Aries": "Quadruped (4)", "Taurus": "Quadruped (4)", "Gemini": "Biped (2)",
    "Cancer": "Apada/Footless (0)", "Leo": "Quadruped (4)", "Virgo": "Biped (2)",
    "Libra": "Biped (2)", "Scorpio": "Apada/Footless (0)", "Sagittarius": "Biped/Quadruped (2/4)",
    "Capricorn": "Quadruped/Apada (4/0)", "Aquarius": "Biped (2)", "Pisces": "Apada/Footless (0)"
}

HELP_TOPICS_CONTENT = {
    "Getting Started": """
Welcome to the Astrology Chart & Analysis Tool!

This application allows you to generate horary and natal charts and perform advanced astrological analysis based on Krishnamurti Padhdhati (KP) principles.

Workflow:
1. Generate a chart in the 'Chart Generation' tab.
2. Go to the 'Daily Analysis' tab to find favorable time periods (transits).
3. Use the 'Ruling Planet' tab to identify the strongest planets for a horary question.
4. Explore other tabs for more specific analysis.

You can also use the 'Interactive Guide' (from the top-right button) for a step-by-step walkthrough.
""",
    "Chart Generation Tab": """
This is the main input screen for the application.

- Horary Number: For horary astrology, enter a number from 1 to 2193. For natal charts (birth charts), leave this field blank.

- Date & Time: Enter the date and time of birth or the time of a horary question. The 'Now !' button instantly fills these fields with the current system time.

- City & Time Zone: Select the location of the event. This is crucial for accurate calculations.

- Generate Chart: After filling the details, click this button. This is the most important step and must be done before any analysis. All other tabs use the data from the chart you generate here.
""",
    "Daily Analysis Tab": """
This tab is for finding auspicious time windows for an event to occur.

1. Promise Check: First, select your Primary Cusp (e.g., 7 for marriage) and Secondary Cusps (e.g., 2, 11 for wealth gain). Click the 'Promise' button. If 'ASC' and 'Pcusp' turn green, the chart holds promise for the event.

2. Full Analysis: If the promise exists, click the 'Run Full Analysis' button. This is the main engine of the app. It will scan the selected time range and find precise windows where the Dasha (planetary periods) and Transits (of Sun, Moon, Jupiter) are all favorable simultaneously.

The results table will show the exact start and end times of these "golden moments".
""",
    "Ruling Planets Tab": """
Ruling Planets (RPs) are a key concept in Horary astrology for getting answers to specific questions.

After generating a horary chart, go to this tab. Select the relevant cusps in the 'Daily Analysis' tab first.

Then, click 'Calculate Ruling Planets'. The program will display a list of planets that have the most influence at that moment, categorized by strength. These planets are often used to confirm the timing of an event or the outcome of a question.
""",
    "Glossary": """
- Cusp: The starting point of an astrological house.
- Lord (Sign, Star, Sub, Sub-Sub): Planets that rule over a specific portion of the zodiac. This tool uses the KP system of Star, Sub, and Sub-Sub lords for high precision.
- Significator: A planet that "represents" or has a connection to a specific house's affairs.
- Dasha: A system of planetary periods that indicates which planets are influencing your life at any given time.
- Transit: The real-time movement of planets in the sky, analyzed in relation to your chart.
"""
}

# --- GLOBAL WORLD CITIES DATA ---
# Format: 'City Name': (Latitude, Longitude, 'Timezone_IANA')
WORLD_CITIES = {
    # North America
    'New York': (40.7128, -74.0060, 'America/New_York'),
    'Los Angeles': (34.0522, -118.2437, 'America/Los_Angeles'),
    'Toronto': (43.6532, -79.3832, 'America/Toronto'),
    'Mexico City': (19.4326, -99.1332, 'America/Mexico_City'),
    # South America
    'Sao Paulo': (-23.5505, -46.6333, 'America/Sao_Paulo'),
    'Buenos Aires': (-34.6037, -58.3816, 'America/Argentina/Buenos_Aires'),
    # Europe
    'London': (51.5074, -0.1278, 'Europe/London'),
    'Paris': (48.8566, 2.3522, 'Europe/Paris'),
    'Berlin': (52.5200, 13.4050, 'Europe/Berlin'),
    'Moscow': (55.7558, 37.6173, 'Europe/Moscow'),
    'Rome': (41.9028, 12.4964, 'Europe/Rome'),
    # Africa
    'Cairo': (30.0444, 31.2357, 'Africa/Cairo'),
    'Lagos': (6.5244, 3.3792, 'Africa/Lagos'),
    'Johannesburg': (-26.2041, 28.0473, 'Africa/Johannesburg'),
    # Asia (excluding India, as it has its own list)
    'Tokyo': (35.6895, 139.6917, 'Asia/Tokyo'),
    'Shanghai': (31.2304, 121.4737, 'Asia/Shanghai'),
    'Beijing': (39.9042, 116.4074, 'Asia/Shanghai'), # Often same TZ as Shanghai for simplicity
    'Dubai': (25.276987, 55.296249, 'Asia/Dubai'),
    'Singapore': (1.3521, 103.8198, 'Asia/Singapore'),
    'Seoul': (37.5665, 126.9780, 'Asia/Seoul'),
    # Australia/Oceania
    'Sydney': (-33.8688, 151.2093, 'Australia/Sydney'),
    'Melbourne': (-37.8136, 144.9631, 'Australia/Melbourne'),
    # Add more major cities as desired
}

CUSPS_MEDICAL_DATA = {
    1: {
        'Traditional': {'Body Parts': ['Head', 'Brain', 'Face', 'Physical Body', 'Constitution'], 'Diseases': ['Headaches', 'Migraines', 'Mental tension', 'Insomnia']}
    },
    2: {
        'Traditional': {'Body Parts': ['Face', 'Right Eye', 'Teeth', 'Tongue', 'Throat', 'Neck'], 'Diseases': ['Speech defects', 'Throat trouble', 'Dental problems', 'Eye issues']}
    },
    3: {
        'Traditional': {'Body Parts': ['Shoulders', 'Arms', 'Hands', 'Right Ear', 'Collarbone'], 'Diseases': ['Respiratory issues', 'Asthma', 'Fracture in arms/collarbone', 'Hearing problems']}
    },
    4: {
        'Traditional': {'Body Parts': ['Chest', 'Lungs', 'Heart', 'Breasts'], 'Diseases': ['Heart conditions', 'Lung diseases (Tuberculosis)', 'Breast cancer']}
    },
    5: {
        'Traditional': {'Body Parts': ['Upper Abdomen', 'Stomach', 'Spine', 'Heart'], 'Diseases': ['Acidity', 'Spinal issues', 'Stomach disorders', 'Heart problems']}
    },
    6: {
        'Traditional': {'Body Parts': ['Lower Abdomen', 'Intestines', 'Kidneys', 'Navel'], 'Diseases': ['Appendicitis', 'Digestive problems', 'Hernia', 'Kidney issues (as house of disease)']}
    },
    7: {
        'Traditional': {'Body Parts': ['Lower Back', 'Waist', 'Urinary Tract', 'Reproductive Organs'], 'Diseases': ['Venereal diseases', 'Prostate issues', 'Hernia', 'Urinary infections']}
    },
    8: {
        'Traditional': {'Body Parts': ['External Genitalia', 'Anus', 'Excretory System'], 'Diseases': ['Chronic diseases', 'Accidents', 'Piles', 'Fistula', 'Incurable diseases']}
    },
    9: {
        'Traditional': {'Body Parts': ['Hips', 'Thighs', 'Arterial System'], 'Diseases': ['Gout', 'Nerve pains in thighs', 'Blood disorders']}
    },
    10: {
        'Traditional': {'Body Parts': ['Knees', 'Joints', 'Bones'], 'Diseases': ['Arthritis', 'Knee problems', 'Joint pain', 'Skin diseases']}
    },
    11: {
        'Traditional': {'Body Parts': ['Ankles', 'Shins', 'Left Ear'], 'Diseases': ['Circulatory problems', 'Fractures in lower legs', 'Ear problems']}
    },
    12: {
        'Traditional': {'Body Parts': ['Feet', 'Left Eye', 'Lymphatic System'], 'Diseases': ['Insomnia', 'Deformities', 'Hospitalization', 'Poisoning', 'Sleep disorders']}
    }
}
# Near the top with other global constants
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

SIGNS_MEDICAL_DATA = {
    'Aries': {'Body Parts': ['Head', 'Brain', 'Face', 'Upper Jaw'], 'Diseases': ['Headaches', 'Fevers', 'Neuralgia', 'Eye problems', 'Acne']},
    'Taurus': {'Body Parts': ['Neck', 'Throat', 'Vocal Cords', 'Lower Jaw', 'Tonsils'], 'Diseases': ['Tonsillitis', 'Thyroid issues', 'Stiff neck', 'Throat infections']},
    'Gemini': {'Body Parts': ['Arms', 'Shoulders', 'Lungs', 'Nervous System', 'Hands'], 'Diseases': ['Asthma', 'Bronchitis', 'Nerve issues', 'Pneumonia']},
    'Cancer': {'Body Parts': ['Stomach', 'Chest', 'Breasts', 'Ribs', 'Digestive System'], 'Diseases': ['Indigestion', 'Gastritis', 'Ulcers', 'Cough', 'Depression']},
    'Leo': {'Body Parts': ['Heart', 'Spine', 'Back', 'Aorta'], 'Diseases': ['Heart disease', 'Spinal meningitis', 'Back problems', 'High/Low blood pressure']},
    'Virgo': {'Body Parts': ['Abdomen', 'Intestines', 'Spleen', 'Navel'], 'Diseases': ['Digestive issues', 'Appendicitis', 'Constipation', 'Malnutrition']},
    'Libra': {'Body Parts': ['Kidneys', 'Lower Back (Lumbar)', 'Skin'], 'Diseases': ['Kidney infections', 'Lumbago', 'Urinary tract issues', 'Skin diseases']},
    'Scorpio': {'Body Parts': ['Reproductive Organs', 'Excretory System', 'Bladder', 'Pelvis'], 'Diseases': ['Venereal diseases', 'Piles', 'Hernia', 'Prostate issues']},
    'Sagittarius': {'Body Parts': ['Hips', 'Thighs', 'Liver', 'Arteries'], 'Diseases': ['Sciatica', 'Gout', 'Hip fractures', 'Liver problems']},
    'Capricorn': {'Body Parts': ['Knees', 'Bones', 'Teeth', 'Joints', 'Skin'], 'Diseases': ['Arthritis', 'Knee injuries', 'Dental problems', 'Rheumatism']},
    'Aquarius': {'Body Parts': ['Ankles', 'Shins', 'Circulatory System'], 'Diseases': ['Sprained ankles', 'Varicose veins', 'Blood disorders']},
    'Pisces': {'Body Parts': ['Feet', 'Toes', 'Lymphatic System'], 'Diseases': ['Bunions', 'Gout in feet', 'Deformities', 'Colds', 'Addictions']}
}


NAKSHATRAS_MEDICAL_DATA = {
    'Ashwini': {'Body Parts': ['Head (top)', 'Brain'], 'Diseases': ['Head injury', 'Migraine', 'Mental illness']},
    'Bharani': {'Body Parts': ['Head (lower part)', 'Soles of feet'], 'Diseases': ['Eye diseases', 'Fever', 'Forehead injuries']},
    'Krittika': {'Body Parts': ['Head', 'Neck', 'Face', 'Tonsils'], 'Diseases': ['Tonsillitis', 'Fever', 'Acne', 'Neck pain']},
    'Rohini': {'Body Parts': ['Forehead', 'Face', 'Mouth', 'Tongue'], 'Diseases': ['Sore throat', 'Colds', 'Mouth ulcers']},
    'Mrigashira': {'Body Parts': ['Eyebrows', 'Cheeks', 'Chin', 'Throat'], 'Diseases': ['Throat pain', 'Tonsils', 'Skin disease on face']},
    'Ardra': {'Body Parts': ['Eyes', 'Throat', 'Arms', 'Shoulders'], 'Diseases': ['Asthma', 'Dry cough', 'Throat troubles']},
    'Punarvasu': {'Body Parts': ['Fingers', 'Nose', 'Lungs'], 'Diseases': ['Pneumonia', 'Lung issues', 'Ear pain']},
    'Pushya': {'Body Parts': ['Stomach', 'Ribs', 'Face'], 'Diseases': ['Jaundice', 'Ulcers', 'Eczema']},
    'Ashlesha': {'Body Parts': ['Joints', 'Nails', 'Knees', 'Elbows'], 'Diseases': ['Indigestion', 'Gas', 'Joint pain', 'Breathing difficulty']},
    'Magha': {'Body Parts': ['Nose', 'Lips', 'Chin', 'Heart'], 'Diseases': ['Heart attack', 'Back pain', 'Anxiety']},
    'Purva Phalguni': {'Body Parts': ['Genitals', 'Right Hand', 'Heart'], 'Diseases': ['Heart valve issues', 'Blood pressure', 'Venereal diseases']},
    'Uttara Phalguni': {'Body Parts': ['Intestines', 'Bowels', 'Left Hand'], 'Diseases': ['Stomach ache', 'Indigestion', 'Throat problem']},
    'Hasta': {'Body Parts': ['Hands', 'Intestines', 'Bowels'], 'Diseases': ['Stomach pain', 'Diarrhea', 'Cold', 'Breathing issues']},
    'Chitra': {'Body Parts': ['Neck', 'Forehead', 'Kidneys'], 'Diseases': ['Kidney stones', 'Brain fever', 'Ulcers', 'Abdominal tumors']},
    'Swati': {'Body Parts': ['Chest', 'Skin', 'Teeth', 'Intestines'], 'Diseases': ['Skin diseases', 'Urinary troubles', 'Piles']},
    'Vishakha': {'Body Parts': ['Lower Abdomen', 'Arms', 'Breasts', 'Lungs'], 'Diseases': ['Paralysis', 'Kidney issues', 'Heart problems']},
    'Anuradha': {'Body Parts': ['Heart', 'Stomach', 'Womb', 'Hips'], 'Diseases': ['Irregular menses', 'Constipation', 'Piles', 'Nasal issues']},
    'Jyeshtha': {'Body Parts': ['Tongue', 'Neck', 'Right side of body', 'Colon'], 'Diseases': ['Leucorrhoea', 'Piles', 'Tumors', 'Pain in arms/shoulders']},
    'Moola': {'Body Parts': ['Hips', 'Thighs', 'Feet', 'Heart'], 'Diseases': ['Rheumatism', 'Back pain', 'Hip issues']},
    'Purva Ashadha': {'Body Parts': ['Thighs', 'Back', 'Knees'], 'Diseases': ['Sciatica', 'Diabetes', 'Uterine issues']},
    'Uttara Ashadha': {'Body Parts': ['Thighs', 'Waist', 'Stomach'], 'Diseases': ['Stomach pain', 'Eye problems', 'Heart issues']},
    'Shravana': {'Body Parts': ['Ears', 'Skin', 'Reproductive organs'], 'Diseases': ['Skin diseases', 'Tuberculosis', 'Rheumatism']},
    'Dhanishta': {'Body Parts': ['Ankles', 'Back', 'Knees'], 'Diseases': ['Knee pain', 'Anemia', 'High blood pressure']},
    'Shatabhisha': {'Body Parts': ['Jaw', 'Knees', 'Calves'], 'Diseases': ['Arthritis', 'Heart disease', 'Insomnia', 'Varicose veins']},
    'Purva Bhadrapada': {'Body Parts': ['Ankles', 'Feet', 'Sides of body'], 'Diseases': ['Heart problems', 'Swollen ankles', 'Liver issues']},
    'Uttara Bhadrapada': {'Body Parts': ['Feet', 'Sides of body'], 'Diseases': ['Paralysis', 'Stomach issues', 'Hernia', 'Tuberculosis']},
    'Revati': {'Body Parts': ['Feet', 'Ankles', 'Abdomen'], 'Diseases': ['Intestinal ulcers', 'Gout', 'Deformities of feet']}
}

# ---------- Global Constants ----------
# Replace the old CITIES dictionary with this new comprehensive one.
ALL_INDIAN_CITIES = {
    'Mumbai': (19.0760, 72.8777), 'Delhi': (28.7041, 77.1025), 'Bangalore': (12.9716, 77.5946),
    'Kolkata': (22.5726, 88.3639), 'Chennai': (13.0827, 80.2707), 'Hyderabad': (17.3850, 78.4867),
    'Pune': (18.5204, 73.8567), 'Ahmedabad': (23.0225, 72.5714), 'Surat': (21.1702, 72.8311),
    'Lucknow': (26.8467, 80.9462), 'Jaipur': (26.9124, 75.7873), 'Kanpur': (26.4499, 80.3319),
    'Nagpur': (21.1458, 79.0882), 'Indore': (22.7196, 75.8577), 'Thane': (19.2183, 72.9781),
    'Bhopal': (23.2599, 77.4126), 'Visakhapatnam': (17.6868, 83.2185), 'Patna': (25.5941, 85.1376),
    'Vadodara': (22.3072, 73.1812), 'Ghaziabad': (28.6692, 77.4538), 'Ludhiana': (30.9010, 75.8573),
    'Agra': (27.1767, 78.0081), 'Nashik': (20.0112, 73.7909), 'Faridabad': (28.4089, 77.3178),
    'Meerut': (28.9845, 77.7064), 'Rajkot': (22.3039, 70.8022), 'Varanasi': (25.3176, 82.9739),
    'Srinagar': (34.0837, 74.7973), 'Aurangabad': (19.8762, 75.3433), 'Dhanbad': (23.7957, 86.4304),
    'Amritsar': (31.6340, 74.8723), 'Navi Mumbai': (19.0330, 73.0297), 'Allahabad': (25.4358, 81.8463),
    'Ranchi': (23.3441, 85.3096), 'Howrah': (22.5958, 88.3103), 'Jabalpur': (23.1815, 79.9864),
    'Gwalior': (26.2183, 78.1828), 'Coimbatore': (11.0168, 76.9558), 'Vijayawada': (16.5062, 80.6480),
    'Jodhpur': (26.2389, 73.0243), 'Madurai': (9.9252, 78.1198), 'Guwahati': (26.1445, 91.7362),
    'Chandigarh': (30.7333, 76.7794), 'Solapur': (17.6599, 75.9064), 'Hubli': (15.3647, 75.1240),
    'Bareilly': (28.3670, 79.4304), 'Moradabad': (28.8386, 78.7733), 'Mysore': (12.2958, 76.6394),
    'Gurgaon': (28.4595, 77.0266), 'Aligarh': (27.8974, 78.0880), 'Jalandhar': (31.3260, 75.5762),
    'Tiruchirappalli': (10.7905, 78.7047), 'Bhubaneswar': (20.2961, 85.8245), 'Salem': (11.6643, 78.1460),
    'Warangal': (17.9689, 79.5941), 'Guntur': (16.3067, 80.4365), 'Bhiwandi': (19.2967, 73.0553),
    'Saharanpur': (29.9725, 77.5455), 'Gorakhpur': (26.7606, 83.3732), 'Bikaner': (28.0229, 73.3119),
    'Amravati': (20.9374, 77.7796), 'Noida': (28.5355, 77.3910), 'Jamshedpur': (22.8046, 86.2029),
    'Bhilai': (21.2144, 81.3366), 'Cuttack': (20.4625, 85.8830), 'Firozabad': (27.1594, 78.3963),
    'Kochi': (9.9312, 76.2673), 'Dehradun': (30.3165, 78.0322), 'Durgapur': (23.5204, 87.3119),
    'Asansol': (23.6739, 86.9524), 'Nanded': (19.1383, 77.3204), 'Kolhapur': (16.7050, 74.2433),
    'Ajmer': (26.4499, 74.6399), 'Gulbarga': (17.3297, 76.8343), 'Jamnagar': (22.4707, 70.0577),
    'Ujjain': (23.1765, 75.7885), 'Loni': (28.7500, 77.2833), 'Siliguri': (26.7271, 88.3953),
    'Jhansi': (25.4484, 78.5685), 'Ulhasnagar': (19.2222, 73.1554), 'Jammu': (32.7266, 74.8570),
    'Sangli-Miraj': (16.8524, 74.5815), 'Mangalore': (12.9141, 74.8560), 'Erode': (11.3410, 77.7172),
    'Belgaum': (15.8497, 74.4977), 'Ambattur': (13.1143, 80.1548), 'Tirunelveli': (8.7139, 77.7567),
    'Malegaon': (20.5500, 74.5500), 'Gaya': (24.7963, 85.0086), 'Jalgaon': (21.0077, 75.5626),
    'Udaipur': (24.5854, 73.7125), 'Maheshtala': (22.4953, 88.2530), 'Tirupur': (11.1085, 77.3411),
    'Davanagere': (14.4644, 75.9218), 'Kozhikode': (11.2588, 75.7804), 'Akola': (20.7009, 77.0081),
    'Kurnool': (15.8281, 78.0373), 'Rajpur Sonarpur': (22.4344, 88.4024), 'Bokaro': (23.6693, 86.1511),
    'South Dumdum': (22.6200, 88.4200), 'Bellary': (15.1394, 76.9214), 'Patiala': (30.3398, 76.3869),
    'Gopalpur': (22.3833, 88.4500), 'Agartala': (23.8315, 91.2868), 'Bhagalpur': (25.2424, 86.9833),
    'Muzaffarnagar': (29.4734, 77.7074), 'Bhatpara': (22.8687, 88.4093), 'Panihati': (22.6900, 88.3700),
    'Latur': (18.4088, 76.5604), 'Dhule': (20.9042, 74.7749), 'Rohtak': (28.8955, 76.6066),
    'Korba': (22.35, 82.6833), 'Bhilwara': (25.3475, 74.6402), 'Brahmapur': (19.3149, 84.7941),
    'Muzaffarpur': (26.1224, 85.3902), 'Ahmednagar': (19.0941, 74.7481), 'Mathura': (27.4924, 77.6737),
    'Kollam': (8.8932, 76.6141), 'Avadi': (13.1118, 80.1065), 'Rajahmundry': (17.0005, 81.8040),
    'Kadapa': (14.4665, 78.8234), 'Kamarhati': (22.6700, 88.3700), 'Bilaspur': (22.0797, 82.1409),
    'Shahjahanpur': (27.8797, 79.9048), 'Bijapur': (16.8302, 75.7100), 'Rampur': (28.8054, 79.0239),
    'Shivamogga': (13.9299, 75.5681), 'Chandrapur': (19.9615, 79.2961), 'Junagadh': (21.5222, 70.4579),
    'Thrissur': (10.5276, 76.2144), 'Alwar': (27.5530, 76.6346), 'Bardhaman': (23.2355, 87.8654),
    'Kulti': (23.7333, 86.8500), 'Kakinada': (16.9891, 82.2475), 'Nizamabad': (18.6726, 78.0942),
    'Parbhani': (19.2618, 76.7753), 'Tumkur': (13.3429, 77.1017), 'Hisar': (29.1492, 75.7217),
    'Ozhukarai': (11.9333, 79.7667), 'Bihar Sharif': (25.1953, 85.5145), 'Panipat': (29.3909, 76.9635),
    'Darbhanga': (26.1556, 85.8975), 'Bally': (22.6500, 88.3400), 'Aizawl': (23.7271, 92.7176),
    'Dewas': (22.9676, 76.0494), 'Ichalkaranji': (16.6961, 74.4630), 'Karnal': (29.6857, 76.9904),
    'Tirupati': (13.6288, 79.4192), 'Bathinda': (30.2110, 74.9455), 'Kirari Suleman Nagar': (28.7067, 77.0583),
    'Purnia': (25.7766, 87.4753), 'Satna': (24.5844, 80.8335), 'Mau': (25.9439, 83.5606),
    'Sonipat': (28.9956, 77.0182), 'Farrukhabad': (27.3948, 79.5828), 'Sagar': (23.8388, 78.7378),
    'Rourkela': (22.2492, 84.8339), 'Durg': (21.1904, 81.2852), 'Imphal': (24.8170, 93.9368),
    'Ratlam': (23.3287, 75.0396), 'Hapur': (28.7303, 77.7756), 'Anantapur': (14.6819, 77.6006),
    'Arrah': (25.5613, 84.6643), 'Karimnagar': (18.4386, 79.1288), 'Etawah': (26.7749, 79.0253),
    'Ambernath': (19.2000, 73.1833), 'North Dumdum': (22.6500, 88.4200), 'Bharatpur': (27.2173, 77.4944),
    'Begusarai': (25.4225, 86.1294), 'New Delhi': (28.6139, 77.2090), 'Gandhidham': (23.0804, 70.1313),
    'Baranagar': (22.6400, 88.3700), 'Tiruvottiyur': (13.1600, 80.3000), 'Pondicherry': (11.9139, 79.8145),
    'Sikar': (27.6119, 75.1396), 'Thoothukudi': (8.7642, 78.1348), 'Rewa': (24.5353, 81.2985),
    'Mirzapur': (25.1460, 82.5690), 'Raichur': (16.2076, 77.3553), 'Pali': (25.7725, 73.3233),
    'Ramagundam': (18.7588, 79.4782), 'Haridwar': (29.9457, 78.1642), 'Vijayanagaram': (18.1067, 83.3956),
    'Katihar': (25.5333, 87.5833), 'Nagercoil': (8.1833, 77.4333), 'Sri Ganganagar': (29.9200, 73.8800),
    'Karawal Nagar': (28.7297, 77.2828), 'Mango': (22.8094, 86.2562), 'Thanjavur': (10.7870, 79.1378),
    'Bulandshahr': (28.4069, 77.8504), 'Sambhal': (28.5833, 78.5667), 'Singrauli': (24.1977, 82.6687),
    'Naihati': (22.8900, 88.4200), 'Proddatur': (14.7333, 78.5500), 'Sambalpur': (21.4704, 83.9704),
    'Chittoor': (13.2172, 79.0982), 'Puducherry': (11.9416, 79.8083), 'Panchkula': (30.6921, 76.8601),
    'Burhanpur': (21.3094, 76.2302), 'Kharagpur': (22.3302, 87.3237), 'Dindigul': (10.3673, 77.9803),
    'Gandhinagar': (23.2156, 72.6369), 'Hosur': (12.7409, 77.8253), 'Nangloi Jat': (28.6833, 77.0667),
    'English Bazar': (25.0000, 88.1500), 'Ongole': (15.5057, 80.0483), 'Eluru': (16.7000, 81.1000),
    'Haldia': (22.0257, 88.0586), 'Khandwa': (21.8261, 76.3465), 'Puri': (19.8135, 85.8312),
    # Add more cities as needed
}

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Mapping Zodiac Signs to their traditional ruling Lords
ZODIAC_LORD_MAP = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
}

NAKSHATRAS = [
    ("Ashwini", "Ketu"), ("Bharani", "Venus"), ("Krittika", "Sun"),
    ("Rohini", "Moon"), ("Mrigashira", "Mars"), ("Ardra", "Rahu"),
    ("Punarvasu", "Jupiter"), ("Pushya", "Saturn"), ("Ashlesha", "Mercury"),
    ("Magha", "Ketu"), ("Purva Phalguni", "Venus"), ("Uttara Phalguni", "Sun"),
    ("Hasta", "Moon"), ("Chitra", "Mars"), ("Swati", "Rahu"),
    ("Vishakha", "Jupiter"), ("Anuradha", "Saturn"), ("Jyeshtha", "Mercury"),
    ("Moola", "Ketu"), ("Purva Ashadha", "Venus"), ("Uttara Ashadha", "Sun"),
    ("Shravana", "Moon"), ("Dhanishta", "Mars"), ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Jupiter"), ("Uttara Bhadrapada", "Saturn"), ("Revati", "Mercury")
]

DASHA_PERIODS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}

LORD_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
NAKSHATRA_SPAN_DEG = 13 + 20 / 60

SWE_PLANET_NAMES = {
    swe.SUN: 'Sun', swe.MOON: 'Moon', swe.MARS: 'Mars', swe.MERCURY: 'Mercury',
    swe.JUPITER: 'Jupiter', swe.VENUS: 'Venus', swe.SATURN: 'Saturn',
    swe.MEAN_NODE: 'Rahu'  # Only use MEAN_NODE for Rahu
}

# House system constants (bytes encoded for swe.houses)
HOUSE_SYSTEMS = {
    "Placidus": b'P',
    "Koch": b'K',
    "Equal": b'E',
    "Regiomontanus": b'R',
    "Campanus": b'C'
}
#
# ... (after the NAKSHATRAS_MEDICAL_DATA, etc.)
#

# --- ADD THIS DATASET ---
EVENT_DATASET = [
    {
        "Query Type": "Proneness to Disease",
        "Primary Cusp": 1,
        "Secondary Cusp": "6,8,12"
    },
    {
        "Query Type": "Un natural Death",
        "Primary Cusp": 8,
        "Secondary Cusp": "1,2,7,Badhak,12"
    },
    {
        "Query Type": "Negotiation",
        "Primary Cusp": 3,
        "Secondary Cusp": "3,9,11"
    },
    {
        "Query Type": "Will I Win the case  ? ",
        "Primary Cusp": 6,
        "Secondary Cusp": "11"
    },
    {
        "Query Type": "Vehicle",
        "Primary Cusp": 4,
        "Secondary Cusp": "6,11"
    },
    {
        "Query Type": "When will i BUild a House ?",
        "Primary Cusp": 4,
        "Secondary Cusp": "12"
    },
    {
        "Query Type": "Will One succeed in Love ?",
        "Primary Cusp": 1,
        "Secondary Cusp": "5,11"
    },
    {
        "Query Type": "Am I Pregnant ?",
        "Primary Cusp": 1,
        "Secondary Cusp": "5,11"
    },
    {
        "Query Type": "Sterility",
        "Primary Cusp": 5,
        "Secondary Cusp": "4,10"
    },
    {
        "Query Type": "WIll i Give a Healthy Child ?",
        "Primary Cusp": 5,
        "Secondary Cusp": "11"
    },
    {
        "Query Type": "Accident",
        "Primary Cusp": 8,
        "Secondary Cusp": "1,4"
    },
    {
        "Query Type": "Success in Effort",
        "Primary Cusp": 1,
        "Secondary Cusp": "6,11"
    },
    {
        "Query Type": "Status and Respect",
        "Primary Cusp": 1,
        "Secondary Cusp": "10,11"
    },
    {
        "Query Type": "Financial Status",
        "Primary Cusp": 2,
        "Secondary Cusp": "6,11"
    },
    {
        "Query Type": "Obtaining Loan",
        "Primary Cusp": 6,
        "Secondary Cusp": "2,11"
    },
    {
        "Query Type": "Obtaining jewellery",
        "Primary Cusp": 2,
        "Secondary Cusp": "11"
    },
    {
        "Query Type": "Defect in speech vision",
        "Primary Cusp": 2,
        "Secondary Cusp": "12,8"
    },
    {
        "Query Type": "Insurance claims",
        "Primary Cusp": 2,
        "Secondary Cusp": "8,11"
    },
    {
        "Query Type": "Medical claim",
        "Primary Cusp": 2,
        "Secondary Cusp": "6,8,11"
    },
    {
        "Query Type": "Opening bank account",
        "Primary Cusp": 2,
        "Secondary Cusp": "6,11"
    },
    {
        "Query Type": "Signing a contract",
        "Primary Cusp": 3,
        "Secondary Cusp": "6,9,11"
    },
    {
        "Query Type": "Filing a court case",
        "Primary Cusp": 3,
        "Secondary Cusp": "6,11"
    },
    {
        "Query Type": "Passport green card,Visa",
        "Primary Cusp": 3,
        "Secondary Cusp": "9,11,12"
    },
    {
        "Query Type": "Starting journey",
        "Primary Cusp": 3,
        "Secondary Cusp": "5,9,11"
    },
    {
        "Query Type": "Negotiation",
        "Primary Cusp": 3,
        "Secondary Cusp": "9,11"
    },
    {
        "Query Type": "Transfer",
        "Primary Cusp": 3,
        "Secondary Cusp": "10,11"
    },
    {
        "Query Type": "Younger co born sickness",
        "Primary Cusp": 3,
        "Secondary Cusp": "8,10,12"
    },
    {
        "Query Type": "Computer programmer",
        "Primary Cusp": 3,
        "Secondary Cusp": "2,10,11"
    },
    {
        "Query Type": "Basic Education",
        "Primary Cusp": 4,
        "Secondary Cusp": "11"
    },
    {
        "Query Type": "Purchase of property vehicle",
        "Primary Cusp": 4,
        "Secondary Cusp": "11,12"
    },
    {
        "Query Type": "Sale of property",
        "Primary Cusp": 4,
        "Secondary Cusp": "3,5,10"
    },
    {
        "Query Type": "Taking possession of Flat",
        "Primary Cusp": 4,
        "Secondary Cusp": "9,11"
    },
    {
        "Query Type": "Mother's sickness",
        "Primary Cusp": 4,
        "Secondary Cusp": "9,11,3"
    },
    {
        "Query Type": "Engineer",
        "Primary Cusp": 4,
        "Secondary Cusp": "10"
    },
    {
        "Query Type": "Medicine as subject",
        "Primary Cusp": 4,
        "Secondary Cusp": "6"
    },
    {
        "Query Type": "Law as study",
        "Primary Cusp": 4,
        "Secondary Cusp": "6,9"
    },
    {
        "Query Type": "Fine arts",
        "Primary Cusp": 4,
        "Secondary Cusp": "5"
    },
    {
        "Query Type": "Teaching*primary)",
        "Primary Cusp": 4,
        "Secondary Cusp": "2,6,10"
    },
    {
        "Query Type": "Teaching*Secondary",
        "Primary Cusp": 9,
        "Secondary Cusp": "2,6,10"
    },
    {
        "Query Type": "Child Birth/Pregnancy",
        "Primary Cusp": 5,
        "Secondary Cusp": "2,11"
    },
    {
        "Query Type": "Love marriage",
        "Primary Cusp": 5,
        "Secondary Cusp": "7,11"
    },
    {
        "Query Type": "Rape",
        "Primary Cusp": 5,
        "Secondary Cusp": "8,12"
    },
    {
        "Query Type": "Success in sports",
        "Primary Cusp": 5,
        "Secondary Cusp": "6,11"
    },
    {
        "Query Type": "Fine arts as profession",
        "Primary Cusp": 10,
        "Secondary Cusp": "5,2,11"
    },
    {
        "Query Type": "Caeserial delivery",
        "Primary Cusp": 5,
        "Secondary Cusp": "2,8"
    },
    {
        "Query Type": "Promise of Loan",
        "Primary Cusp": 6,
        "Secondary Cusp": "2,11"
    },
    {
        "Query Type": "Secret activities of partner",
        "Primary Cusp": 6,
        "Secondary Cusp": "5"
    },
    {
        "Query Type": "Success in competetion",
        "Primary Cusp": 6,
        "Secondary Cusp": "1,11"
    },
    {
        "Query Type": "Success in litigation",
        "Primary Cusp": 6,
        "Secondary Cusp": "1,11"
    },
    {
        "Query Type": "Recovery from Disease",
        "Primary Cusp": 6,
        "Secondary Cusp": "5,11"
    },
    {
        "Query Type": "Marriage",
        "Primary Cusp": 7,
        "Secondary Cusp": "5,11"
    },
    {
        "Query Type": "Second child",
        "Primary Cusp": 7,
        "Secondary Cusp": "2,11"
    },
    {
        "Query Type": "Partnership",
        "Primary Cusp": 7,
        "Secondary Cusp": "5,11"
    },
    {
        "Query Type": "Theft",
        "Primary Cusp": 7,
        "Secondary Cusp": "2,12"
    },
    {
        "Query Type": "Danger from Oppnents",
        "Primary Cusp": 7,
        "Secondary Cusp": "8,12"
    },
    {
        "Query Type": "Loan from Bank",
        "Primary Cusp": 7,
        "Secondary Cusp": "2,6,11"
    },
    {
        "Query Type": "Marriage engagement",
        "Primary Cusp": 7,
        "Secondary Cusp": "3,9,11"
    },
    {
        "Query Type": "Criminality as profession",
        "Primary Cusp": 10,
        "Secondary Cusp": "8,2,11"
    },
    {
        "Query Type": "Unexpected gains",
        "Primary Cusp": 8,
        "Secondary Cusp": "2,11"
    },
    {
        "Query Type": "Hain from inheritance",
        "Primary Cusp": 8,
        "Secondary Cusp": "2,11"
    },
    {
        "Query Type": "Unexpected loss",
        "Primary Cusp": 8,
        "Secondary Cusp": "5,12"
    },
    {
        "Query Type": "Gift received",
        "Primary Cusp": 8,
        "Secondary Cusp": "6,11"
    },
    {
        "Query Type": "Recovery of lost article",
        "Primary Cusp": 8,
        "Secondary Cusp": "2,6,11"
    },
    {
        "Query Type": "Unnatural Death",
        "Primary Cusp": 8,
        "Secondary Cusp": "1,12"
    },
    {
        "Query Type": "Death due to accident",
        "Primary Cusp": 8,
        "Secondary Cusp": "4,6,12"
    },
    {
        "Query Type": "Depression",
        "Primary Cusp": 8,
        "Secondary Cusp": "1,3,12"
    },
    {
        "Query Type": "Surgeon",
        "Primary Cusp": 10,
        "Secondary Cusp": "8,2,11"
    },
    {
        "Query Type": "Long Journey",
        "Primary Cusp": 9,
        "Secondary Cusp": "3,12"
    },
    {
        "Query Type": "Higher education",
        "Primary Cusp": 9,
        "Secondary Cusp": "4,11"
    },
    {
        "Query Type": "Second Marriage",
        "Primary Cusp": 9,
        "Secondary Cusp": "7,11"
    },
    {
        "Query Type": "Third child",
        "Primary Cusp": 9,
        "Secondary Cusp": "2,11"
    },
    {
        "Query Type": "Fathers sickness",
        "Primary Cusp": 9,
        "Secondary Cusp": "2,4,8"
    },
    {
        "Query Type": "Spiritual success",
        "Primary Cusp": 9,
        "Secondary Cusp": "6,11"
    },
    {
        "Query Type": "Politics as profession",
        "Primary Cusp": 10,
        "Secondary Cusp": "2,9,6,11"
    },
    {
        "Query Type": "Service or business",
        "Primary Cusp": 10,
        "Secondary Cusp": "7,6"
    },
    {
        "Query Type": "Name and Fame",
        "Primary Cusp": 10,
        "Secondary Cusp": "1,11"
    },
    {
        "Query Type": "Retirement/Break in service",
        "Primary Cusp": 10,
        "Secondary Cusp": "5,9"
    },
    {
        "Query Type": "Problems in job",
        "Primary Cusp": 10,
        "Secondary Cusp": "5,8"
    },
    {
        "Query Type": "Suspension",
        "Primary Cusp": 10,
        "Secondary Cusp": "8,5,6"
    },
    {
        "Query Type": "Voluntary retirement",
        "Primary Cusp": 10,
        "Secondary Cusp": "1,5,9"
    },
    {
        "Query Type": "Removal from Service",
        "Primary Cusp": 10,
        "Secondary Cusp": "8,5,9"
    },
    {
        "Query Type": "Winning in Love",
        "Primary Cusp": 11,
        "Secondary Cusp": "5,7"
    },
    {
        "Query Type": "Satisfaction of desire",
        "Primary Cusp": 11,
        "Secondary Cusp": "1"
    },
    {
        "Query Type": "Sex with a friend",
        "Primary Cusp": 11,
        "Secondary Cusp": "7,5"
    },
    {
        "Query Type": "Loan repayment",
        "Primary Cusp": 12,
        "Secondary Cusp": "5,8"
    },
    {
        "Query Type": "Scandal",
        "Primary Cusp": 12,
        "Secondary Cusp": "7,8,5"
    },
    {
        "Query Type": "Jail",
        "Primary Cusp": 12,
        "Secondary Cusp": "3,8"
    },
    {
        "Query Type": "Absconding",
        "Primary Cusp": 12,
        "Secondary Cusp": "3,8"
    },
    {
        "Query Type": "Research Success",
        "Primary Cusp": 12,
        "Secondary Cusp": "6,11"
    }
]

# ---------- Global Constants ----------
# ... (rest of the global constants)
# Define the planets that will appear in the Stellar Status table
# Exclude True Node (Ketu is derived from Rahu/Mean Node)
STELLAR_PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']


class AstrologyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Astrology Chart & Analysis Tool")
        self.root.geometry("1200x800")

        self.chart_type_var = tk.StringVar(value="Horary")
        self.is_debug_mode = True
        self.ju_plus_var = tk.BooleanVar()
        self.su_plus_var = tk.BooleanVar()
        self.mo_plus_var = tk.BooleanVar()

        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("Treeview", font=('Helvetica', 9))
        style.configure("TLabel", font=('Helvetica', 9))
        style.configure("TButton", font=('Helvetica', 9))
        style.configure("TCombobox", font=('Helvetica', 9))
        style.configure("TEntry", font=('Helvetica', 9))
        style.configure("Listbox", font=('Helvetica', 9))

        style.configure("Highlight.TButton", bordercolor="#4d94ff", background="#cce0ff", lightcolor="#cce0ff",
                        darkcolor="#cce0ff")
        style.configure("Highlight.TFrame", background="#cce0ff")
        style.configure("Highlight.TEntry", fieldbackground="#cce0ff")
        style.configure("Highlight.TCombobox", fieldbackground="#cce0ff")
        self.highlight_opts = {'background': '#cce0ff', 'selectbackground': '#4a6984', 'selectforeground': 'white'}
        self.original_listbox_opts = {}

        top_bar = ttk.Frame(self.root)
        top_bar.pack(side="top", fill="x", padx=10, pady=(5, 0))
        guide_button = ttk.Button(top_bar, text="Show Interactive Guide", command=self.start_tour)
        guide_button.pack(side="right")

        self.current_planetary_positions = {}
        self.current_cuspal_positions = {}
        self.current_general_info = {}
        self.stellar_significators_data = {}
        self.planet_classifications = {}
        self.strong_ruling_planets = set()
        self.all_ruling_planets = set()

        # NEW: Variables to store intermediate results
        self.suitable_dasha_spans = []
        self.dasha_transit_windows = []

        self.sorted_city_list = sorted(list(ALL_INDIAN_CITIES.keys()))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self._create_chart_generation_tab()
        self._create_ruling_planet_tab()
        self._create_daily_analysis_tab()  # This will now create the new button layout
        self._create_stellar_status_tab()
        self._create_disease_tab()
        self._create_vehicle_tab()
        self._create_court_case_tab()

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)
        self._set_default_inputs()

    def _is_top_event(self, item_values):
        """Checks if a given result row meets the strict criteria for a 'Top Event'."""
        dasha_lords = item_values[0:5]
        pc_sl_starl = item_values[7]
        pc_sl_subl = item_values[8]
        jup_status, sun_status, moon_status = item_values[-3:]

        # 1. Dasha Check: All 5 dasha lords must be 'Positive'.
        for lord in dasha_lords:
            if self.planet_classifications.get(lord) != 'Positive':
                return False

        # 2. Transit Check: No 'Neutral' transits allowed, only 'Positive'.
        if 'N' in jup_status or 'N' in sun_status or 'N' in moon_status:
            return False

        # 3. Ruling Planet Check: The PC's SL's StarL and SubL must be strong RPs.
        if pc_sl_starl not in self.strong_ruling_planets:
            return False
        if pc_sl_subl not in self.strong_ruling_planets:
            return False

        return True

    # ... (inside your AstrologyApp class) ...

    def _on_event_type_select(self, event=None):
        """
        Dynamically manages tabs (Disease, Vehicle, Court Case) and
        automatically selects cusps based on the chosen event.
        """
        self._log_debug("-" * 60)
        self._log_debug("EVENT: _on_event_type_select triggered.")

        full_selection_text = self.event_type_combo.get()
        if not full_selection_text:
            self._log_debug("-> No event selected. Exiting function.")
            return

        self._log_debug(f"-> User selected event text: '{full_selection_text}'")
        full_selection_text_lower = full_selection_text.lower()

        # Get the current state of the notebook BEFORE any changes
        managed_tabs_before = self.notebook.tabs()
        self._log_debug(f"-> Notebook state BEFORE changes: {managed_tabs_before}")

        # --- Dynamically manage the 'Disease' tab ---
        self._log_debug("\n--- Checking 'Disease' Tab ---")
        is_disease_query = "disease" in full_selection_text_lower or "sick" in full_selection_text_lower
        disease_frame_id = str(self.disease_frame)
        is_disease_tab_managed = disease_frame_id in managed_tabs_before

        if is_disease_query:
            if not is_disease_tab_managed:
                self.notebook.add(self.disease_frame, text="Disease")
                self._log_debug("ACTION: ADD complete for Disease tab.")
            self._run_disease_analysis()  # Run analysis when added/selected
        else:
            if is_disease_tab_managed:
                self.notebook.forget(self.disease_frame)
                self._log_debug("ACTION: FORGET complete for Disease tab.")

        # --- Dynamically manage the 'Vehicle' tab ---
        # Re-check managed tabs after potential disease tab change
        managed_tabs_midway = self.notebook.tabs()
        self._log_debug("\n--- Checking 'Vehicle' Tab ---")
        is_vehicle_query = "vehicle" in full_selection_text_lower
        vehicle_frame_id = str(self.vehicle_frame)
        is_vehicle_tab_managed = vehicle_frame_id in managed_tabs_midway

        if is_vehicle_query:
            if not is_vehicle_tab_managed:
                self.notebook.add(self.vehicle_frame, text="Vehicle")
                self._log_debug("ACTION: ADD complete for Vehicle tab.")
            self._run_vehicle_analysis()  # Run analysis when added/selected
        else:
            if is_vehicle_tab_managed:
                self.notebook.forget(self.vehicle_frame)
                self._log_debug("ACTION: FORGET complete for Vehicle tab.")

        # --- Dynamically manage the 'Court Case' tab ---
        # Re-check managed tabs after potential vehicle tab change
        managed_tabs_after_vehicle = self.notebook.tabs()
        self._log_debug("\n--- Checking 'Court Case' Tab ---")
        is_court_case_query = any(keyword in full_selection_text_lower for keyword in ["case", "litigation", "court"])
        court_case_frame_id = str(self.court_case_frame)
        is_court_case_tab_managed = court_case_frame_id in managed_tabs_after_vehicle

        if is_court_case_query:
            if not is_court_case_tab_managed:
                self.notebook.add(self.court_case_frame, text="Court Case")
                self._log_debug("ACTION: ADD complete for Court Case tab.")
            self._run_court_case_analysis()  # <--- CALL THE NEW ANALYSIS FUNCTION HERE
        else:
            if is_court_case_tab_managed:
                self.notebook.forget(self.court_case_frame)
                self._log_debug("ACTION: FORGET complete for Court Case tab.")

        # --- Logic to set cusps based on selection (rest of your original code) ---
        self._log_debug("\n--- Setting Cusps ---")
        selected_event_name = full_selection_text.split(' (')[0].lower()
        event_data = next((item for item in EVENT_DATASET if item["Query Type"].lower() == selected_event_name), None)

        if not event_data:
            self._log_debug("-> No event data found in dataset. Cusp settings skipped.")
            return

        primary_cusp = event_data.get("Primary Cusp")
        if primary_cusp:
            self.primary_cusp_combo.set(f"House {primary_cusp}")

        self.secondary_cusp_listbox.selection_clear(0, tk.END)
        secondary_cusps_str = event_data.get("Secondary Cusp", "")
        if secondary_cusps_str:
            secondary_items_to_select = [item.strip() for item in secondary_cusps_str.split(',')]
            for i in range(self.secondary_cusp_listbox.size()):
                item_text = self.secondary_cusp_listbox.get(i)
                cusp_num_str = item_text.split(' ')[-1]
                if cusp_num_str in secondary_items_to_select or item_text in secondary_items_to_select:
                    self.secondary_cusp_listbox.selection_set(i)

        self._log_debug("-> Cusp setting complete.")
        self._log_debug("-" * 60 + "\n")

    def _find_top_events(self):
        """Finds, promotes, and highlights the very best results from the analysis list."""
        # Prerequisite checks
        if not self.analysis_results_tree.get_children():
            messagebox.showinfo("Info", "Please run an analysis first to generate results.")
            return
        if not self.strong_ruling_planets:
            messagebox.showinfo("Info", "Please calculate Ruling Planets first (on the 'Ruling Planet' tab).")
            return

        # Separate items into top-tier and others
        top_events = []
        other_events = []
        for item_id in self.analysis_results_tree.get_children():
            values = self.analysis_results_tree.item(item_id, 'values')
            if len(values) < 13: continue

            if self._is_top_event(values):
                top_events.append(values)
            else:
                other_events.append(values)

        if not top_events:
            messagebox.showinfo("Info",
                                "No 'Top Events' meeting the strict criteria were found in the current results.")
            return

        # Sort the two lists independently
        # Top events are sorted by their own positivity score
        top_events.sort(key=lambda x: self._calculate_positivity_score(x), reverse=True)
        # Other events are also sorted by their score
        other_events.sort(key=lambda x: self._calculate_positivity_score(x), reverse=True)

        # Clear and repopulate the tree, with top events first
        self.analysis_results_tree.delete(*self.analysis_results_tree.get_children())

        # Insert top events with a special highlight tag
        for i, values in enumerate(top_events):
            tag = 'top_event'
            self.analysis_results_tree.insert("", "end", values=values, tags=(tag,))

        # Insert the rest of the events normally
        for i, values in enumerate(other_events):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.analysis_results_tree.insert("", "end", values=values, tags=(tag,))

        self._log_debug(f"Found and promoted {len(top_events)} top events.")
        messagebox.showinfo("Success",
                            f"{len(top_events)} top event(s) have been found and moved to the top of the list.")

    def _update_progress(self, progress_info, current_step, total_steps, start_time, status_text=""):
        """
        (NEW) Updates the progress bar, percentage, and Estimated Time Remaining.
        """
        if not progress_info or not progress_info['window'].winfo_exists():
            return
        if total_steps == 0: total_steps = 1  # Avoid division by zero

        # Update progress bar and percentage
        percent = (current_step / total_steps) * 100
        progress_info['bar']['value'] = percent
        progress_info['percent'].config(text=f"{int(percent)}%")
        if status_text:
            progress_info['status'].config(text=status_text)

        # Calculate and update ETR after a few initial steps for better accuracy
        if current_step > 5:
            elapsed_seconds = (datetime.datetime.now() - start_time).total_seconds()
            time_per_step = elapsed_seconds / current_step
            steps_remaining = total_steps - current_step
            etr_seconds = time_per_step * steps_remaining
            etr_text = f"Time Remaining: ~{self._format_time_remaining(etr_seconds)}"
        else:
            etr_text = "Time Remaining: Calculating..."

        progress_info['etr_label'].config(text=etr_text)
        progress_info['root'].update_idletasks()








    # Helper to copy text widget content to clipboard
    def _copy_text_to_clipboard(self, text_widget):
        try:
            content = text_widget.get("1.0", tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Copied", "Results copied to clipboard.")
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to copy text: {e}")

    # Helper to copy text widget content to clipboard
    def _copy_text_to_clipboard(self, text_widget):
        try:
            content = text_widget.get("1.0", tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Copied", "Results copied to clipboard.")
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to copy text: {e}")





















    def _create_disease_tab(self):
        """Creates the UI for the Disease analysis tab."""
        self.disease_frame = ttk.Frame(self.notebook)
        # The tab is not added to the notebook here; it will be added dynamically.

        self.disease_frame.grid_columnconfigure(0, weight=1)
        self.disease_frame.grid_rowconfigure(1, weight=1) # Main results row will expand

        # Top Control Frame
        control_frame = ttk.LabelFrame(self.disease_frame, text="Disease Analysis")
        control_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        ttk.Label(control_frame, text="Analysis is performed automatically when a disease-related event is selected.").pack(pady=5)

        # Results Frame for Frequency Tables
        results_frame = ttk.LabelFrame(self.disease_frame, text="Frequency Analysis Results")
        results_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_columnconfigure(1, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)

        # Frequency Tables
        ttk.Label(results_frame, text="Body Part Frequency", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=(5, 5), padx=5)
        self.body_parts_tree = ttk.Treeview(results_frame, columns=("Part", "Count"), show="headings", height=10)
        self.body_parts_tree.heading("Part", text="Body Part")
        self.body_parts_tree.heading("Count", text="Frequency")
        self.body_parts_tree.grid(row=1, column=0, sticky='nsew', padx=(10, 5), pady=(0, 10))

        ttk.Label(results_frame, text="Disease Frequency", font=('Helvetica', 10, 'bold')).grid(row=0, column=1, pady=(5, 5), padx=5)
        self.diseases_tree = ttk.Treeview(results_frame, columns=("Disease", "Count"), show="headings", height=10)
        self.diseases_tree.heading("Disease", text="Disease / Ailment")
        self.diseases_tree.heading("Count", text="Frequency")
        self.diseases_tree.grid(row=1, column=1, sticky='nsew', padx=(5, 10), pady=(0, 10))


    def _run_disease_analysis(self):
        """Runs the analysis based on Asc/6th Cusp lords and Bhaskaran rules."""
        if not self.current_cuspal_positions or not self.stellar_significators_data:
            messagebox.showerror("Error", "Please generate a chart first on the 'Chart Generation' tab.")
            return

        # --- Clear previous results ---
        for tree in [self.body_parts_tree, self.diseases_tree, self.bhaskaran_tree]:
            tree.delete(*tree.get_children())

        # --- Part 1: Frequency Analysis ---
        all_body_parts = []
        all_diseases = []
        try:
            planets_to_analyze = {
                "Ascendant SSL": self.current_cuspal_positions[1][5],
                "6th Cusp SL": self.current_cuspal_positions[6][4],
                "6th Cusp SSL": self.current_cuspal_positions[6][5]
            }
        except KeyError as e:
            messagebox.showerror("Chart Data Error", f"Could not find cusp data. Error: {e}")
            return

        for role, planet_name in planets_to_analyze.items():
            if not planet_name or planet_name == "N/A":
                continue
            parts, diseases = self._collect_medical_data_for_planet(planet_name)
            all_body_parts.extend(parts)
            all_diseases.extend(diseases)

        from collections import Counter
        for part, count in sorted(Counter(all_body_parts).items(), key=lambda i: i[1], reverse=True):
            self.body_parts_tree.insert("", "end", values=(part, count))
        for disease, count in sorted(Counter(all_diseases).items(), key=lambda i: i[1], reverse=True):
            self.diseases_tree.insert("", "end", values=(disease, count))

        # --- Part 2: Bhaskaran Rules Analysis ---
        self._apply_bhaskaran_rules()

        messagebox.showinfo("Analysis Complete", "Disease and Body Part analysis is complete.")

    def _run_disease_analysis(self):
        """Runs the frequency analysis based on Ascendant and 6th Cusp lords."""
        if not self.current_cuspal_positions or not self.stellar_significators_data:
            messagebox.showerror("Error", "Please generate a chart first on the 'Chart Generation' tab.")
            return

        # --- Clear previous results ---
        for tree in [self.body_parts_tree, self.diseases_tree]:
            tree.delete(*tree.get_children())

        # --- Frequency Analysis ---
        all_body_parts = []
        all_diseases = []
        try:
            planets_to_analyze = {
                "Ascendant SSL": self.current_cuspal_positions[1][5],
                "6th Cusp SL": self.current_cuspal_positions[6][4],
                "6th Cusp SSL": self.current_cuspal_positions[6][5]
            }
        except KeyError as e:
            messagebox.showerror("Chart Data Error", f"Could not find cusp data. Error: {e}")
            return

        for role, planet_name in planets_to_analyze.items():
            if not planet_name or planet_name == "N/A":
                continue
            parts, diseases = self._collect_medical_data_for_planet(planet_name)
            all_body_parts.extend(parts)
            all_diseases.extend(diseases)

        from collections import Counter
        for part, count in sorted(Counter(all_body_parts).items(), key=lambda i: i[1], reverse=True):
            self.body_parts_tree.insert("", "end", values=(part, count))
        for disease, count in sorted(Counter(all_diseases).items(), key=lambda i: i[1], reverse=True):
            self.diseases_tree.insert("", "end", values=(disease, count))

        # The call to self._apply_bhaskaran_rules() has been removed from this version.

        messagebox.showinfo("Analysis Complete", "Disease and Body Part analysis is complete.")

    def _collect_medical_data_for_planet(self, planet_name):
        """Helper function to collect all medical data points for a single planet based on the user's logic."""
        body_parts = []
        diseases = []

        # Get Planet's own data
        planet_pos_data = self.current_planetary_positions.get(planet_name)
        if not planet_pos_data:
            self._log_debug(f"Warning: No planetary data found for {planet_name}.")
            return [], []

        # 1. Find Nakshatra(N1) where the planet is posited
        nakshatra_n1_name, _, _, _ = self.get_nakshatra_info(planet_pos_data[0])
        n1_data = NAKSHATRAS_MEDICAL_DATA.get(nakshatra_n1_name, {})
        body_parts.extend(n1_data.get('Body Parts', []))
        diseases.extend(n1_data.get('Diseases', []))

        # 2. Find data related to the planet's Star Lord
        star_of_a = planet_pos_data[3] # Star Lord of the planet
        star_of_a_pos_data = self.current_planetary_positions.get(star_of_a)

        if star_of_a and star_of_a_pos_data:
            # Find which cusps planet A is connecting to through its star lord
            # A planet signifies a cusp if it is a lord of that cusp (Sign, Star, Sub, or SSL)
            for cusp_num, cusp_data in self.current_cuspal_positions.items():
                if star_of_a in cusp_data[2:]: # Check if star_of_a is SignLord, StarLord, SubLord, or SubSubLord
                    cusp_medical_data = CUSPS_MEDICAL_DATA.get(cusp_num, {}).get('Traditional', {})
                    body_parts.extend(cusp_medical_data.get('Body Parts', []))
                    diseases.extend(cusp_medical_data.get('Diseases', []))

            # Find which Nakshatra(N2) "Star_of_A" is posited in
            nakshatra_n2_name, _, _, _ = self.get_nakshatra_info(star_of_a_pos_data[0])
            n2_data = NAKSHATRAS_MEDICAL_DATA.get(nakshatra_n2_name, {})
            body_parts.extend(n2_data.get('Body Parts', []))
            diseases.extend(n2_data.get('Diseases', []))

        return body_parts, diseases


    def _is_transit_favorable(self, planet_name, dyn_planets):
        """Checks if a planet's transit is favorable (SL/SubL are P/N). Moon also checks SSL."""
        planet_data = dyn_planets.get(planet_name)
        if not planet_data: return False, f"{planet_name[:3]} N/A"

        sl_name, subl_name, subsubl_name = planet_data[3], planet_data[4], planet_data[5]
        sl_class = self.planet_classifications.get(sl_name, 'U')[0]
        subl_class = self.planet_classifications.get(subl_name, 'U')[0]

        if planet_name == 'Moon':
            subsubl_class = self.planet_classifications.get(subsubl_name, 'U')[0]
            is_favorable = sl_class in 'PN' and subl_class in 'PN' and subsubl_class in 'PN'
            status_str = f"Moon SL:{sl_class}/SubL:{subl_class}/SSL:{subsubl_class}"
        else:
            is_favorable = sl_class in 'PN' and subl_class in 'PN'
            status_str = f"{planet_name[:3]} SL:{sl_class}/SubL:{subl_class}"

        return is_favorable, status_str

    def run_sequential_full_analysis(self):
        """
        (CORRECTED) Orchestrates the full analysis from Dasha to Interlink in one go.
        This version is updated to call the helper functions with the correct arguments,
        resolving the TypeError.
        """
        self._log_debug("--- Starting Corrected Sequential Full Analysis ---")

        if not self.current_planetary_positions or not self.rp_tree.get_children():
            messagebox.showerror("Prerequisites Missing", "Please generate a chart and calculate Ruling Planets first.")
            return

        self._update_analysis_results_tree_columns("detailed_full_analysis")

        # --- Setup ---
        original_pc_num = self._get_original_primary_cusp_from_ui()
        if original_pc_num is None: return
        pc_for_analysis = self._determine_primary_cusp_for_analysis(original_pc_num)

        # Ensure classifications are fresh
        self._cache_static_planet_classifications(pc_for_analysis, original_pc_num)

        local_tz = pytz.timezone(self.timezone_combo.get())
        start_utc, end_utc = self._get_analysis_time_range(local_tz)
        if start_utc is None: return
        analysis_duration = end_utc - start_utc

        progress_info = self._setup_progress_window("Running Full Analysis...")

        # --- Step 1: Dasha Analysis ---
        self._update_progress(progress_info, 10, "Step 1/3: Finding suitable Dasha periods...")
        # Call to find Dashas no longer needs qualified planets list
        suitable_dasha_spans = self._find_suitable_dasha_combinations(start_utc, end_utc, local_tz)
        if not suitable_dasha_spans:
            if progress_info['window'].winfo_exists(): progress_info['window'].destroy()
            messagebox.showinfo("Analysis Complete",
                                "No Dasha periods found where all 5 lords are Positive or Neutral.")
            return

        # --- Step 2: Transit Analysis ---
        self._update_progress(progress_info, 40, "Step 2/3: Finding suitable transit windows...")
        # Call to find Transits no longer needs qualified planets list
        dasha_transit_windows = self._find_transit_windows_in_spans(suitable_dasha_spans, progress_info,
                                                                    analysis_duration)
        if not dasha_transit_windows:
            if progress_info['window'].winfo_exists(): progress_info['window'].destroy()
            messagebox.showinfo("Analysis Complete", "Found Dasha periods, but no matching favorable transit days.")
            return

        # --- Step 3: Cuspal Interlink & Final Formatting ---
        self._update_progress(progress_info, 70, "Step 3/3: Scanning for cuspal interlinks...")
        # This logic requires the qualified planets list for the final check
        strong_rp_strengths = {"Strongest of Strongest", "Strongest", "Second Strong", "Weak"}
        qualified_planets = {
            rp_name for rp_strength, rp_name, _ in
            [self.rp_tree.item(item, 'values') for item in self.rp_tree.get_children()]
            if
            rp_strength in strong_rp_strengths and self.planet_classifications.get(rp_name) in ["Positive", "Neutral"]
        }

        final_results = []
        secondary_cusp_nums = self._get_selected_secondary_cusps()

        # Scan for high-frequency interlinks within the favorable Dasha/Transit windows
        cuspal_hits = self._perform_cuspal_interlink_scan(dasha_transit_windows, qualified_planets, pc_for_analysis,
                                                          secondary_cusp_nums, progress_info)

        # Process the results
        for hit in cuspal_hits:
            # The call to check suitability is now correct, without the extra argument
            _, transit_details = self._check_transit_suitability_new(hit['time'], analysis_duration)

            transit_str = f"Jup:{transit_details.get('Jupiter')} | Sat:{transit_details.get('Saturn')} | Sun:{transit_details.get('Sun')} | Moon:{transit_details.get('Moon')}"
            cuspal_str = f"Hit at {hit['time'].astimezone(local_tz).strftime('%H:%M:%S')} via {hit['planet']} ({hit['type']})"

            for window in dasha_transit_windows:
                if window['start_utc'] <= hit['time'] < window['end_utc']:
                    final_results.append({
                        'dasha_lords': hit['dasha_lords'],
                        'start': hit['time'],  # Use the precise hit time
                        'end': hit['time'] + datetime.timedelta(minutes=1),  # Show a small window for the hit
                        'transits': transit_str,
                        'cuspal': cuspal_str
                    })
                    break

        if progress_info['window'].winfo_exists(): progress_info['window'].destroy()

        # --- Populate Treeview ---
        if not final_results:
            messagebox.showinfo("Analysis Complete", "No precise moments satisfying all conditions were found.")
        else:
            # De-duplicate final results to show unique hits
            unique_results = []
            seen = set()
            for res in final_results:
                # Use a key that represents the unique event moment
                key = (tuple(res['dasha_lords']), res['cuspal'], res['start'].strftime('%Y-%m-%d %H:%M'))
                if key not in seen:
                    unique_results.append(res)
                    seen.add(key)

            for res in unique_results:
                start_time_str = res['start'].astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
                # For a precise hit, start and end times are the same
                row_data = (*res['dasha_lords'], start_time_str, "--> HIT", res['transits'], res['cuspal'])
                self.analysis_results_tree.insert("", "end", values=row_data)
            messagebox.showinfo("Analysis Complete", f"Found {len(unique_results)} potential timing(s).")

    def _perform_cuspal_interlink_scan(self, windows_to_scan, qualified_planets, pc_for_analysis, secondary_cusp_nums,
                                       progress_info):
        """
        (UPDATED) Performs the high-frequency cuspal interlink scan.
        This version is now "state-aware" and filters out consecutive duplicate hits,
        showing only the first occurrence of each unique interlink configuration.
        """
        final_hits: list[Any] = []
        # This variable will now store the unique signature of the last successful hit
        last_hit_signature = None

        city = self.city_combo.get()
        hsys_const = self._get_selected_hsys()
        horary_num = int(
            self.horary_entry.get()) if self.horary_entry.get() and self.chart_type_var.get() == "Horary" else None

        scan_interval_seconds = 120
        total_seconds_to_scan = sum((w['end_utc'] - w['start_utc']).total_seconds() for w in windows_to_scan if
                                    'end_utc' in w and 'start_utc' in w)
        processed_secs = 0
        start_time_process = datetime.datetime.now()

        for window in windows_to_scan:
            time_pointer = window['start_utc']
            dasha_lords = window.get('dasha_lords', [])

            while time_pointer <= window['end_utc']:
                dyn_planets, dyn_cusps, _ = self._calculate_chart_data(time_pointer, city, hsys_const, horary_num)
                if not dyn_planets:
                    time_pointer += datetime.timedelta(seconds=scan_interval_seconds)
                    continue

                interlink_found_this_moment = False
                pc_sub_lord = dyn_cusps.get(pc_for_analysis, [None] * 6)[4]

                if pc_sub_lord in qualified_planets:
                    pc_sl_data = dyn_planets.get(pc_sub_lord)
                    if pc_sl_data:
                        pc_sl_star_lord = pc_sl_data[3]

                        rahu_dispositors = {dyn_planets.get('Rahu', [None] * 6)[2],
                                            dyn_planets.get('Rahu', [None] * 6)[3]}
                        ketu_dispositors = {dyn_planets.get('Ketu', [None] * 6)[2],
                                            dyn_planets.get('Ketu', [None] * 6)[3]}

                        link_details_for_all_scs = []
                        for sc_num in secondary_cusp_nums:
                            sc_sub_lord = dyn_cusps.get(sc_num, [None] * 6)[4]
                            link_type = None

                            if pc_sl_star_lord == sc_sub_lord:
                                link_type = f"Std. Link to H{sc_num}"
                            elif sc_sub_lord == 'Rahu' and pc_sl_star_lord in rahu_dispositors:
                                link_type = f"Rahu Agency to H{sc_num}"
                            elif sc_sub_lord == 'Ketu' and pc_sl_star_lord in ketu_dispositors:
                                link_type = f"Ketu Agency to H{sc_num}"
                            else:
                                sc_sl_data = dyn_planets.get(sc_sub_lord)
                                if sc_sl_data and sc_sl_data[3] == pc_sl_star_lord:
                                    link_type = f"Shared SL to H{sc_num}"

                            if link_type:
                                link_details_for_all_scs.append(link_type)
                            else:
                                break

                        if len(link_details_for_all_scs) == len(secondary_cusp_nums):
                            interlink_found_this_moment = True

                            # --- NEW DE-DUPLICATION LOGIC ---
                            # Create a unique signature for this specific hit type.
                            # Sorting ensures the order of links doesn't matter.
                            current_hit_signature = (pc_sub_lord, tuple(sorted(link_details_for_all_scs)))

                            if current_hit_signature != last_hit_signature:
                                # This is a new, unique hit. Record it.
                                final_link_details = "; ".join(sorted(link_details_for_all_scs))
                                final_hits.append({
                                    'time': time_pointer,
                                    'planet': pc_sub_lord,
                                    'type': final_link_details,
                                    'dasha_lords': dasha_lords
                                })
                                # Update the last hit signature to this new one.
                                last_hit_signature = current_hit_signature

                # If no valid interlink was found at this moment, reset the signature tracker.
                # This allows the same hit type to be recorded again if it appears after a break.
                if not interlink_found_this_moment:
                    last_hit_signature = None

                time_pointer += datetime.timedelta(seconds=scan_interval_seconds)
                processed_secs += scan_interval_seconds
                if progress_info and progress_info['window'].winfo_exists():
                    self._update_progress(progress_info, processed_secs, total_seconds_to_scan, start_time_process,
                                          "Scanning for cuspal interlinks...")

        return final_hits

    def _format_time_remaining(self, seconds):
        """Formats a duration in seconds into a '1m 25s' string."""
        if seconds < 0 or seconds > 3600 * 4:  # Don't show for very long periods
            return "..."
        if seconds < 60:
            return f"{int(seconds)}s"
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes}m {seconds}s"


    def _find_suitable_dasha_combinations(self, start_utc, end_utc, local_tz, qualified_pn_rps):
        """
        MODIFIED FINAL LOGIC: Finds Dasha periods where all 5 lords (MD, AD, PD, SD, PrD)
        are present in the provided list of qualified Positive/Neutral Ruling Planets.
        """
        self._log_debug(f"Finding Dasha combinations where all 5 lords are in: {sorted(list(qualified_pn_rps))}")
        suitable_spans = []
        all_dasha_periods = self._get_dasha_periods_flat(start_utc, end_utc, local_tz)

        if not all_dasha_periods:
            self._log_debug("No dasha periods found in the given time range.")
            return []

        for period in all_dasha_periods:
            dasha_lords_list = [
                period['md_lord'],
                period['ad_lord'],
                period['pd_lord'],
                period['sd_lord'],
                period['prd_lord']
            ]

            # The new, simplified check:
            # Are all 5 lords contained within the master list of P/N RPs?
            if all(lord in qualified_pn_rps for lord in dasha_lords_list):
                self._log_debug(
                    f"SUCCESS: Found suitable Dasha span. Lords {dasha_lords_list} are all P/N RPs.")
                suitable_spans.append({
                    'dasha_lords': dasha_lords_list,
                    'start_utc': period['start_utc'],
                    'end_utc': period['end_utc']
                })
            else:
                failed_lords = [lord for lord in dasha_lords_list if lord not in qualified_pn_rps]
                if failed_lords:
                     self._log_debug(f"  FAIL: Dasha span rejected. Failed lords not in P/N RP list: {failed_lords}")

        self._log_debug(f"Found {len(suitable_spans)} suitable dasha spans based on the final logic.")
        return suitable_spans

    def _check_transit_suitability_new(self, time_utc, analysis_duration=None):
        """
        (ROBUST VERSION) DYNAMIC TRANSIT LOGIC: Checks suitability based on the analysis time span.
        'analysis_duration' is now an optional argument to prevent TypeErrors from older function calls.
        If it's missing, it defaults to a short-term check (Sun/Moon only).
        """
        # --- Fallback for older function calls ---
        if analysis_duration is None:
            self._log_debug("WARNING: 'analysis_duration' was not provided. Defaulting to short-term transit check.")
            # Set a default short duration to ensure Jupiter/Saturn checks are skipped.
            analysis_duration = datetime.timedelta(days=1)

        self._log_debug(f"--- Running DYNAMIC Transit Check for span {analysis_duration.days} days ---")
        city = self.city_combo.get()
        hsys_const = self._get_selected_hsys()
        horary_num = int(
            self.horary_entry.get()) if self.horary_entry.get() and self.chart_type_var.get() == "Horary" else None

        dyn_planets, _, _ = self._calculate_chart_data(time_utc, city, hsys_const, horary_num)

        all_conditions_met = True
        details = {}

        def get_status_char(planet_name):
            classif = self.planet_classifications.get(planet_name, 'X')
            return f"({classif[0]})" if classif else "(U)"

        # --- Sun Check ---
        sun_data = dyn_planets.get('Sun')
        if sun_data:
            sun_sl, sun_subl = sun_data[3], sun_data[4]
            if self.planet_classifications.get(sun_sl) in ['Positive', 'Neutral'] and \
               self.planet_classifications.get(sun_subl) in ['Positive', 'Neutral']:
                details['Sun'] = f"OK (SL:{sun_sl}{get_status_char(sun_sl)}, SubL:{sun_subl}{get_status_char(sun_subl)})"
            else:
                all_conditions_met = False; details['Sun'] = "FAIL"
        else:
            all_conditions_met = False; details['Sun'] = "FAIL (N/A)"

        # --- Moon Check ---
        moon_data = dyn_planets.get('Moon')
        if moon_data:
            moon_sl, moon_subl, moon_ssl = moon_data[3], moon_data[4], moon_data[5]
            if self.planet_classifications.get(moon_sl) in ['Positive', 'Neutral'] and \
               self.planet_classifications.get(moon_subl) in ['Positive', 'Neutral'] and \
               self.planet_classifications.get(moon_ssl) in ['Positive', 'Neutral']:
                details['Moon'] = f"OK (SL:{moon_sl}{get_status_char(moon_sl)}, SubL:{moon_subl}{get_status_char(moon_subl)}, SSL:{moon_ssl}{get_status_char(moon_ssl)})"
            else:
                all_conditions_met = False; details['Moon'] = "FAIL"
        else:
            all_conditions_met = False; details['Moon'] = "FAIL (N/A)"

        # --- Jupiter Check (conditional: > 90 days) ---
        if analysis_duration.days > 90:
            jupiter_data = dyn_planets.get('Jupiter')
            if jupiter_data:
                jup_sl, jup_subl = jupiter_data[3], jupiter_data[4]
                if self.planet_classifications.get(jup_sl) in ['Positive', 'Neutral'] and \
                   self.planet_classifications.get(jup_subl) in ['Positive', 'Neutral']:
                    details['Jupiter'] = f"OK (SL:{jup_sl}{get_status_char(jup_sl)}, SubL:{jup_subl}{get_status_char(jup_subl)})"
                else:
                    all_conditions_met = False; details['Jupiter'] = "FAIL"
            else:
                all_conditions_met = False; details['Jupiter'] = "FAIL (N/A)"
        else:
            details['Jupiter'] = "Not Checked"

        # --- Saturn Check (conditional: > 1.5 years / 547 days) ---
        if analysis_duration.days > 547:
            saturn_data = dyn_planets.get('Saturn')
            if saturn_data:
                saturn_sl, saturn_subl = saturn_data[3], saturn_data[4]
                if self.planet_classifications.get(saturn_sl) in ['Positive', 'Neutral'] and \
                   self.planet_classifications.get(saturn_subl) in ['Positive', 'Neutral']:
                    details['Saturn'] = f"OK (SL:{saturn_sl}{get_status_char(saturn_sl)}, SubL:{saturn_subl}{get_status_char(saturn_subl)})"
                else:
                    all_conditions_met = False; details['Saturn'] = "FAIL"
            else:
                all_conditions_met = False; details['Saturn'] = "FAIL (N/A)"
        else:
            details['Saturn'] = "Not Checked"

        return all_conditions_met, details

    def _run_cuspal_interlink_analysis_new(self, time_utc, pc_num, sc_nums, qualified_pn_rps):
        """
        MODIFIED FINAL LOGIC: Checks for cuspal interlink at a specific time.
        All involved lords must be in the master list of qualified Positive/Neutral Ruling Planets.
        Returns (bool, dict_with_details).
        """
        city = self.city_combo.get()
        hsys_const = self._get_selected_hsys()
        horary_num = int(
            self.horary_entry.get()) if self.horary_entry.get() and self.chart_type_var.get() == "Horary" else None

        dyn_planets, dyn_cusps, _ = self._calculate_chart_data(time_utc, city, hsys_const, horary_num)

        pc_data = dyn_cusps.get(pc_num)
        if not pc_data:
            return False, {"link_details": "PC data not found"}
        pc_sub_lord = pc_data[4]

        if pc_sub_lord not in qualified_pn_rps:
            return False, {"link_details": f"Link FAIL: PC SubLord ({pc_sub_lord}) is not a P/N RP."}

        pc_sl_data = dyn_planets.get(pc_sub_lord)
        if not pc_sl_data:
            return False, {"link_details": "PC SubLord planet data not found."}
        pc_sl_star_lord = pc_sl_data[3]

        if pc_sl_star_lord not in qualified_pn_rps:
            return False, {"link_details": f"Link FAIL: PC SL's StarLord ({pc_sl_star_lord}) is not a P/N RP."}

        if not sc_nums:
            return True, {"link_details": "Link OK (No SCs)", "pc_sl_star_lord": pc_sl_star_lord}

        for sc_num in sc_nums:
            sc_data = dyn_cusps.get(sc_num)
            if not sc_data:
                return False, {"link_details": f"SC {sc_num} data not found."}
            sc_sub_lord = sc_data[4]

            if sc_sub_lord not in qualified_pn_rps:
                return False, {"link_details": f"Link FAIL: SC {sc_num} SubLord ({sc_sub_lord}) is not a P/N RP."}

            if pc_sl_star_lord != sc_sub_lord:
                return False, {"link_details": f"Link FAIL: PC SL's Star ({pc_sl_star_lord}) doesn't match SC {sc_num}'s SubL ({sc_sub_lord})."}

        return True, {"link_details": "Link OK", "pc_sl_star_lord": pc_sl_star_lord}

    def _is_interlink_active(self, dyn_planets, dyn_cusps, pc_for_analysis, secondary_cusp_nums):
        """
        Checks for a dynamic cuspal interlink, with the new condition that all
        planets involved MUST be in the static Ruling Planets list.
        """
        # Get the Sub Lord of the transiting Primary Cusp
        pc_data = dyn_cusps.get(pc_for_analysis)
        if not pc_data: return False, {}
        pc_sub_lord_name = pc_data[4]

        # --- RP FILTER 1: PC Sub Lord must be a Ruling Planet ---
        if pc_sub_lord_name not in self.all_ruling_planets:
            return False, {}

        # Get its dynamic star/sub lords
        pc_sl_planet_data = dyn_planets.get(pc_sub_lord_name)
        if not pc_sl_planet_data: return False, {}
        _, pc_sl_star_lord, pc_sl_sub_lord, _ = self.get_nakshatra_info(pc_sl_planet_data[0])

        # --- RP FILTER 2 & 3: Its Star Lord and Sub Lord must also be Ruling Planets ---
        if pc_sl_star_lord not in self.all_ruling_planets:
            return False, {}
        if pc_sl_sub_lord not in self.all_ruling_planets:
            return False, {}

        # Also ensure all involved planets are Positively/Neutrally classified
        if self.planet_classifications.get(pc_sub_lord_name, 'Negative') not in ['Positive',
                                                                                 'Neutral']: return False, {}
        if self.planet_classifications.get(pc_sl_star_lord, 'Negative') not in ['Positive', 'Neutral']: return False, {}
        if self.planet_classifications.get(pc_sl_sub_lord, 'Negative') not in ['Positive', 'Neutral']: return False, {}

        # If no secondary cusps, the link is valid if the planets above are RPs
        if not secondary_cusp_nums:
            details = {'pc_sl_sl': pc_sl_star_lord, 'pc_sl_subl': pc_sl_sub_lord,
                       'sc_connected_str': "Link OK (No SCs)"}
            return True, details

        # Check connections with secondary cusps
        connected_sc_details = {}
        for sc_num in secondary_cusp_nums:
            sc_data = dyn_cusps.get(sc_num)
            if not sc_data: return False, {}
            sc_sub_lord = sc_data[4]

            # --- RP FILTER 4: The SC Sub Lord must also be a Ruling Planet ---
            if sc_sub_lord not in self.all_ruling_planets:
                return False, {}

            if self.planet_classifications.get(sc_sub_lord, 'Negative') not in ['Positive', 'Neutral']: return False, {}

            # Check for the star/sub connection
            connection_type = []
            if pc_sl_star_lord == sc_sub_lord: connection_type.append("Star Match")
            if pc_sl_sub_lord == sc_sub_lord: connection_type.append("Sub Match")

            if not connection_type: return False, {}  # Must have a connection
            connected_sc_details[sc_num] = " / ".join(connection_type)

        details = {
            'pc_sl_sl': pc_sl_star_lord,
            'pc_sl_subl': pc_sl_sub_lord,
            'sc_connected_str': "; ".join([f"H{n}: {t}" for n, t in sorted(connected_sc_details.items())])
        }
        return True, details

    def _toggle_chart_type_inputs(self):
        """
        Enables or disables the Horary Number entry field based on the selected chart type.
        """
        if self.chart_type_var.get() == "Horary":
            self.horary_entry.config(state='normal')
            self.horary_label.config(state='normal')
        else:  # Birth Chart
            self.horary_entry.config(state='disabled')
            self.horary_label.config(state='disabled')
            self.horary_entry.delete(0, tk.END)

    # ... (after _create_vehicle_tab, for example) ...

    def _create_court_case_tab(self):
        """Creates the UI for the Court Case analysis tab."""
        self.court_case_frame = ttk.Frame(self.notebook)
        # The tab is not added to the notebook here; it will be added dynamically.

        self.court_case_frame.grid_columnconfigure(0, weight=1)
        self.court_case_frame.grid_rowconfigure(0, weight=1)

        results_frame = ttk.LabelFrame(self.court_case_frame, text="Court Case Analysis Results")
        results_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)  # The treeview will expand

        self.court_case_tree = ttk.Treeview(results_frame, columns=("Rule", "Message"), show="headings")
        self.court_case_tree.heading("Rule", text="Rule Applied")
        self.court_case_tree.heading("Message", text="Astrological Interpretation")

        self.court_case_tree.column("Rule", width=250, anchor='w')
        self.court_case_tree.column("Message", width=500, anchor='w')
        self.court_case_tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.court_case_tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.court_case_tree.config(yscrollcommand=scrollbar.set)

        ttk.Button(results_frame, text="Copy Results",
                   command=lambda: self._copy_treeview_to_clipboard(self.court_case_tree)).grid(
            row=1, column=0, columnspan=2, sticky='ew', pady=(5, 0))


    def _create_vehicle_tab(self):
        """Creates the UI for the Vehicle analysis tab."""
        self.vehicle_frame = ttk.Frame(self.notebook)
        # The tab is not added to the notebook here; it will be added dynamically.

        self.vehicle_frame.grid_columnconfigure(0, weight=1)
        self.vehicle_frame.grid_rowconfigure(0, weight=1)

        # Main container for results
        results_frame = ttk.LabelFrame(self.vehicle_frame, text="Vehicle Purchase Analysis (Static Chart)")
        results_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)  # Let the tree expand

        # Treeview to display the derived information
        vehicle_cols = ("Attribute", "Planet/Lord", "Sign", "Nakshatra", "Nakshatra Lord", "Significators")
        self.vehicle_tree = ttk.Treeview(results_frame, columns=vehicle_cols, show="headings")

        for col in vehicle_cols:
            self.vehicle_tree.heading(col, text=col)
            self.vehicle_tree.column(col, anchor='w')
        self.vehicle_tree.column("Attribute", width=180, anchor='w')
        self.vehicle_tree.column("Planet/Lord", width=100, anchor='w')
        self.vehicle_tree.column("Significators", width=200, anchor='w')
        self.vehicle_tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbar for the treeview
        vehicle_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.vehicle_tree.yview)
        vehicle_scrollbar.grid(row=0, column=1, sticky='ns')
        self.vehicle_tree.config(yscrollcommand=vehicle_scrollbar.set)

        # Placeholder for Rules Analysis
        rules_frame = ttk.LabelFrame(self.vehicle_frame, text="Vehicle Rules Analysis (Placeholder)")
        rules_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=(10, 5))
        rules_frame.grid_columnconfigure(0, weight=1)

        self.vehicle_rules_text = tk.Text(rules_frame, height=5, width=80, wrap="word", state='disabled')
        self.vehicle_rules_text.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        rules_placeholder_text = "Future rules and their results will be displayed here.\n"
        self.vehicle_rules_text.config(state='normal')
        self.vehicle_rules_text.insert('1.0', rules_placeholder_text)
        self.vehicle_rules_text.config(state='disabled')

    # ... (after _run_vehicle_analysis, for example) ...

    def _run_court_case_analysis(self):
        """
        Runs the analysis for Court Case predictions based on 6th CSL significations
        and its characteristics.
        """
        self._log_debug("--- Running Court Case Analysis ---")
        self.court_case_tree.delete(*self.court_case_tree.get_children())

        if not self.current_cuspal_positions or not self.current_planetary_positions or not self.stellar_significators_data:
            messagebox.showerror("Error", "Please generate a chart first on the 'Chart Generation' tab.")
            self.court_case_tree.insert("", "end", values=("Error", "Chart data missing. Generate a chart first."))
            return

        try:
            # Get 6th CSL data
            c6_csl_name = self.current_cuspal_positions[6][4]  # 6th Cusp Sub Lord (index 4)
            if not c6_csl_name or c6_csl_name == "N/A" or c6_csl_name not in self.current_planetary_positions:
                self.court_case_tree.insert("", "end",
                                            values=("Data Error", "6th Cuspal Sub Lord not found or invalid."))
                return

            c6_csl_pos_data = self.current_planetary_positions[c6_csl_name]
            c6_csl_lon = c6_csl_pos_data[0]
            c6_csl_sign = c6_csl_pos_data[1]  # Sign of 6th CSL
            c6_csl_star_lord = c6_csl_pos_data[3]  # Star Lord of 6th CSL

            # Get final significators of 6th CSL
            c6_csl_final_sigs = set(
                self._get_planet_final_significators(c6_csl_name, self._get_original_primary_cusp_from_ui()))

            # --- Helper for checking significations ---
            def signifies_all(planet_sigs, houses_to_check):
                return all(h in planet_sigs for h in houses_to_check)

            results_found = []

            # --- Rules based on 6th CSL significations ---
            rules_by_signification = [
                ([3, 9, 11], "You will gain through Agreements and Negotiations"),
                ([5, 11], "Negotiation will end smoothly"),
                ([5, 8, 11], "Negotiation will end by offering money"),
                ([6, 12], "Both parties will withdraw"),
                ([5, 8, 12], "Loss in court case"),
                ([2, 6, 11], "Great success in Litigation"),
                ([3, 9, 6, 12], "Prolong for Years"),
                ([4, 10], "Case will be pause without any movement"),
                ([3, 12], "You might have to sell properties"),
                ([2, 6, 12], "Financial Losses in Court Case")
            ]

            for houses, message in rules_by_signification:
                if signifies_all(c6_csl_final_sigs, houses):
                    results_found.append((f"6th CSL signifies {', '.join(map(str, houses))}", message))
                    self._log_debug(f"Court Case Rule Matched: {message} for houses {houses}")

            # --- Rules based on 6th CSL characteristics (speed and sign modality) ---
            # Define fast/slow moving planets
            FAST_MOVING_PLANETS = {'Moon', 'Mercury', 'Sun', 'Venus', 'Mars'}
            SLOW_MOVING_PLANETS = {'Jupiter', 'Saturn', 'Rahu',
                                   'Ketu'}  # Rahu/Ketu are often considered slow for transit/influence

            # Define Sign Modalities (already in SIGN_MODALITY constant)
            FIXED_SIGNS = {"Taurus", "Leo", "Scorpio", "Aquarius"}
            DUAL_SIGNS = {"Gemini", "Virgo", "Sagittarius", "Pisces"}
            MOVABLE_SIGNS = {"Aries", "Cancer", "Libra", "Capricorn"}

            c6_csl_star_lord_speed_category = None
            if c6_csl_star_lord in FAST_MOVING_PLANETS:
                c6_csl_star_lord_speed_category = "Fast"
            elif c6_csl_star_lord in SLOW_MOVING_PLANETS:
                c6_csl_star_lord_speed_category = "Slow"

            # Rule: Resolution would be fast
            if c6_csl_name in {'Mercury', 'Moon', 'Sun'} or (c6_csl_star_lord_speed_category == "Fast"):
                results_found.append(("6th CSL / Star Lord Speed", "Resolution would be fast"))
                self._log_debug("Court Case Rule Matched: Resolution would be fast.")

            # Rule: resolution would be Time taking
            if c6_csl_name in SLOW_MOVING_PLANETS:
                results_found.append(("6th CSL Speed", "Resolution would be Time taking"))
                self._log_debug("Court Case Rule Matched: Resolution would be Time taking (6th CSL slow).")

            # Rule: Resolution would be very fast (Fast planet in Fixed sign)
            if c6_csl_name in FAST_MOVING_PLANETS and c6_csl_sign in FIXED_SIGNS:
                results_found.append((f"6th CSL '{c6_csl_name}' in '{c6_csl_sign}'", "Resolution would be very fast"))
                self._log_debug("Court Case Rule Matched: Resolution would be very fast (fast in fixed).")

            # Rule: Resolution will be in Months (Slow moving planet in Fixed sign)
            # Note: The original prompt has two "SLow moving planet in Fixed sign" rules.
            # I'm interpreting this as the one that results in "Resolution will be in Months".
            # The last rule "Resolution will be Delayed" is handled below.
            if c6_csl_name in SLOW_MOVING_PLANETS and c6_csl_sign in FIXED_SIGNS:
                # To prevent this from triggering if the *other* "slow in fixed" rule (delay) applies,
                # you might need to order them, or make conditions mutually exclusive if intended.
                # For now, if both apply, both will be listed.
                results_found.append((f"6th CSL '{c6_csl_name}' in '{c6_csl_sign}'", "Resolution will be in Months"))
                self._log_debug("Court Case Rule Matched: Resolution will be in Months (slow in fixed).")

            # Rule: many ups and downs will be faced (Fast moving planet in Common/Dual sign)
            if c6_csl_name in FAST_MOVING_PLANETS and c6_csl_sign in DUAL_SIGNS:
                results_found.append(
                    (f"6th CSL '{c6_csl_name}' in '{c6_csl_sign}'", "Many ups and downs will be faced"))
                self._log_debug("Court Case Rule Matched: Many ups and downs (fast in common).")

            # Rule: Resolution will be Delayed (Slow moving planet in Fixed sign)
            # Re-checking this condition as a separate rule based on provided text.
            # If this is distinct from "Resolution will be in Months", it's here.
            # There's a slight ambiguity in the prompt, but I'll add it as a separate finding.
            if c6_csl_name in SLOW_MOVING_PLANETS and c6_csl_sign in FIXED_SIGNS:
                results_found.append((f"6th CSL '{c6_csl_name}' in '{c6_csl_sign}'", "Resolution will be Delayed"))
                self._log_debug(
                    "Court Case Rule Matched: Resolution will be Delayed (slow in fixed, duplicate/additional).")

            # Display results
            if results_found:
                # Remove duplicates if any rule leads to the same message, or if multiple conditions lead to one
                unique_results = []
                seen_messages = set()
                for rule, msg in results_found:
                    if msg not in seen_messages:
                        unique_results.append((rule, msg))
                        seen_messages.add(msg)
                for rule, message in unique_results:
                    self.court_case_tree.insert("", "end", values=(rule, message))
                messagebox.showinfo("Court Case Analysis",
                                    f"Analysis complete. Found {len(unique_results)} relevant rule(s).")
            else:
                self.court_case_tree.insert("", "end", values=("No Rules Matched",
                                                               "No specific court case outcomes found based on the rules."))
                messagebox.showinfo("Court Case Analysis",
                                    "No specific court case outcomes found based on the rules for the 6th CSL.")

        except Exception as e:
            self._log_debug(f"Error during Court Case analysis: {e}")
            self.court_case_tree.insert("", "end", values=("Error", f"An error occurred during analysis: {e}"))
            messagebox.showerror("Analysis Error", f"An error occurred during Court Case analysis: {e}")


    def _run_vehicle_analysis(self):
        """Derives and displays specific data points related to the 4th Cusp for vehicle analysis."""
        self._log_debug("Running vehicle-specific analysis.")
        self.vehicle_tree.delete(*self.vehicle_tree.get_children())
        self.vehicle_rules_text.config(state='normal')
        self.vehicle_rules_text.delete('1.0', tk.END)

        if not self.current_cuspal_positions or not self.current_planetary_positions:
            self._log_debug("Vehicle analysis skipped: Chart data not available.")
            self.vehicle_tree.insert("", "end", values=("Error: Generate a chart first.", "", "", "", "", ""))
            self.vehicle_rules_text.insert('1.0', "Error: Generate a chart first to see rule analysis.")
            self.vehicle_rules_text.config(state='disabled')
            return

        try:
            # Helper function to get details for a planet
            def get_planet_details(planet_name):
                if not planet_name or planet_name not in self.current_planetary_positions:
                    return "N/A", "N/A", "N/A"
                planet_lon = self.current_planetary_positions[planet_name][0]
                sign = self.get_sign(planet_lon)
                nak, nak_lord, _, _ = self.get_nakshatra_info(planet_lon)
                return sign, nak, nak_lord

            # 1. Get 4th Cusp and its lords
            cusp_4_data = self.current_cuspal_positions[4]
            cusp_4_lon, cusp_4_sign, cusp_4_sign_lord, cusp_4_star_lord, _, cusp_4_ssl = cusp_4_data
            cusp_4_nak, _, _, _ = self.get_nakshatra_info(cusp_4_lon)
            self.vehicle_tree.insert("", "end", values=("4th Cusp Sign Lord", cusp_4_sign_lord, cusp_4_sign, cusp_4_nak,
                                                        cusp_4_star_lord, ""))

            # 2. Get 4th Cusp SSL details
            ssl_sign, ssl_nak, ssl_nak_lord = get_planet_details(cusp_4_ssl)
            self.vehicle_tree.insert("", "end",
                                     values=("4th Cusp SSL", cusp_4_ssl, ssl_sign, ssl_nak, ssl_nak_lord, ""))

            # Get Star Lord of the SSL
            ssl_star_lord = self.current_planetary_positions.get(cusp_4_ssl, (None, None, None, "N/A"))[3]

            # 3. Get Star Lord of 4th Cusp SSL details
            ssl_sl_sign, ssl_sl_nak, ssl_sl_nak_lord = get_planet_details(ssl_star_lord)
            ssl_sl_sigs = self.stellar_significators_data.get(ssl_star_lord, {}).get('final_sigs', [])
            self.vehicle_tree.insert("", "end", values=("Star Lord of 4th SSL", ssl_star_lord, ssl_sl_sign, ssl_sl_nak,
                                                        ssl_sl_nak_lord, sorted(ssl_sl_sigs)))

            # 4. Get Sub Lord of 4th Cusp SSL details
            ssl_sub_lord = self.current_planetary_positions.get(cusp_4_ssl, (None, None, None, None, "N/A"))[4]
            ssl_subl_sign, ssl_subl_nak, ssl_subl_nak_lord = get_planet_details(ssl_sub_lord)
            ssl_subl_sigs = self.stellar_significators_data.get(ssl_sub_lord, {}).get('final_sigs', [])
            self.vehicle_tree.insert("", "end",
                                     values=("Sub Lord of 4th SSL", ssl_sub_lord, ssl_subl_sign, ssl_subl_nak,
                                             ssl_subl_nak_lord, sorted(ssl_subl_sigs)))

            # 5 & 6. Analyze sign qualities
            self.vehicle_tree.insert("", "end", values=("--- Sign Analysis ---", "", "", "", "", ""))

            signs_to_analyze = {cusp_4_sign, ssl_sign, ssl_sl_sign, ssl_subl_sign}
            signs_to_analyze.discard("N/A")

            for sign in sorted(list(signs_to_analyze)):
                modality = SIGN_MODALITY.get(sign, "N/A")
                element = SIGN_ELEMENT.get(sign, "N/A")
                legs = SIGN_LEGS.get(sign, "N/A")
                self.vehicle_tree.insert("", "end",
                                         values=(f"Sign: {sign}", f"Modality: {modality}", f"Element: {element}",
                                                 f"Legs: {legs}", "", ""))

            # --- Call the new rules analysis function ---
            rule_results = self._analyze_vehicle_rules()
            if rule_results:
                self.vehicle_rules_text.insert('1.0', "\n".join(rule_results))
            else:
                self.vehicle_rules_text.insert('1.0', "No specific vehicle rules were met.")

        except Exception as e:
            self._log_debug(f"Error during vehicle analysis: {e}")
            self.vehicle_tree.insert("", "end", values=(f"Error: {e}", "", "", "", "", ""))
            self.vehicle_rules_text.insert('1.0', f"An error occurred: {e}")
        finally:
            self.vehicle_rules_text.config(state='disabled')


    def _get_day_lord(self, dt_utc):
        """Calculates the Day Lord for a given datetime."""
        try:
            # Use the chart's local timezone for an accurate day of the week
            local_tz_str = self.timezone_combo.get()
            local_tz = pytz.timezone(local_tz_str)
            local_dt = dt_utc.astimezone(local_tz)
        except Exception:
            # Fallback to UTC if timezone is invalid
            local_dt = dt_utc

        weekday = local_dt.weekday()  # Monday is 0, Sunday is 6
        day_lords = {
            0: "Moon",  # Monday
            1: "Mars",  # Tuesday
            2: "Mercury",  # Wednesday
            3: "Jupiter",  # Thursday
            4: "Venus",  # Friday
            5: "Saturn",  # Saturday
            6: "Sun"  # Sunday
        }
        return day_lords.get(weekday, "N/A")

        # <<< This is the real fix for the repetition problem >>>

    def _calculate_ruling_planets(self):
        """
        Identifies and categorizes Ruling Planets using a new, robust method
        that processes each unique planet once to determine its highest rank.
        Includes a special rule for promoting Rahu/Ketu if they are RPs and
        signify all required cusps.
        """
        self._log_debug("Calculating Ruling Planets with new de-duplication and Rahu/Ketu promotion logic.")
        self.rp_tree.delete(*self.rp_tree.get_children())

        # 1. Validation and Setup
        if not self.current_planetary_positions or not self.current_cuspal_positions:
            messagebox.showwarning("Chart Data Missing", "Please generate a chart first.")
            return
        try:
            primary_cusp_num = self._get_original_primary_cusp_from_ui()
            if primary_cusp_num is None: return

            # Use the helper function to get secondary cusps, including resolved Marak/Badhak
            secondary_cusp_nums = self._get_selected_secondary_cusps()

        except Exception as e:
            messagebox.showerror("Cusp Selection Error", "Please ensure cusps are selected in 'Daily Analysis'.")
            return

        # Ensure planet classifications are fresh for the current primary cusp selection
        pc_for_analysis = self._determine_primary_cusp_for_analysis(primary_cusp_num)
        self._cache_static_planet_classifications(pc_for_analysis, primary_cusp_num)

        # 2. Calculate all potential RP categories first

        # Base RPs (Traditional RPs, including the newly added Ascendant Star Lord)
        base_rps = set()
        asc_data = self.current_cuspal_positions[1]
        # CORRECTED LINE: Added asc_data[3] for Ascendant Star Lord
        base_rps.update(
            [asc_data[2], asc_data[3], asc_data[4], asc_data[5]])  # Sign Lord, Star Lord, Sub Lord, SubSub Lord of Asc

        base_rps.add(self._get_day_lord(self.current_general_info['natal_utc_dt']))  # Day Lord

        if 'Moon' in self.current_planetary_positions:
            moon_data = self.current_planetary_positions['Moon']
            # Moon's Sign Lord, Star Lord, Sub Lord, SubSub Lord
            base_rps.update([moon_data[2], moon_data[3], moon_data[4], moon_data[5]])

        # Sun's Sub Lord and SubSub Lord
        if 'Sun' in self.current_planetary_positions:
            sun_data = self.current_planetary_positions['Sun']
            base_rps.update([sun_data[4], sun_data[5]])

        # Jupiter's Sub Lord
        if 'Jupiter' in self.current_planetary_positions:
            jupiter_data = self.current_planetary_positions['Jupiter']
            base_rps.add(jupiter_data[4])  # Only Jupiter's Sub Lord is typically emphasized here

        base_rps.discard(None)  # Remove None if it was accidentally added from empty data
        self.base_rps_label.config(text=f"Base RPs: {', '.join(sorted(list(base_rps)))}")
        self._log_debug(f"Calculated Base RPs: {base_rps}")

        # Strongest RPs (Sub Lord of Relevant Cusps whose Star Lord is a Base RP)
        strongest_rps = {}
        target_cusps_nums = {1, primary_cusp_num}.union(secondary_cusp_nums)
        for cusp_num in target_cusps_nums:
            cusp_data = self.current_cuspal_positions.get(cusp_num)
            if cusp_data:
                sub_lord = cusp_data[4]  # Sub Lord of the current Cusp
                if sub_lord in self.current_planetary_positions:
                    star_lord_of_sub_lord = self.current_planetary_positions[sub_lord][
                        3]  # Star Lord of Cusp's Sub Lord
                    if star_lord_of_sub_lord in base_rps:
                        reason = f"Sub lord of Cusp {cusp_num} ({sub_lord}); its star lord ({star_lord_of_sub_lord}) is a base RP."
                        strongest_rps[sub_lord] = reason
                        self._log_debug(f"Identified Strongest RP: {sub_lord} (Reason: {reason})")

        # Strongest of the Strongest RPs (Advanced Fructification Rule)
        s_of_s_rps = {}
        # Combine all RPs found so far to check against for this rule
        all_initial_rps = base_rps.union(set(strongest_rps.keys()))
        required_cusps = {primary_cusp_num}.union(secondary_cusp_nums)

        for planet_A_name in STELLAR_PLANETS:  # Iterate through all main planets
            if planet_A_name in all_initial_rps: continue  # Skip if already identified as a high-tier RP

            planet_A_data = self.current_planetary_positions.get(planet_A_name)
            if not planet_A_data: continue

            planet_B_name = planet_A_data[3]  # Star Lord of Planet A
            if planet_B_name not in all_initial_rps: continue  # Star Lord must be an RP

            # Check if the Star Lord (B) signifies the Primary Cusp
            star_lord_B_final_sigs = set(self.stellar_significators_data.get(planet_B_name, {}).get('final_sigs', []))
            if primary_cusp_num not in star_lord_B_final_sigs: continue

            # Check if Planet A signifies ALL the required cusps
            planet_A_final_sigs = set(self.stellar_significators_data.get(planet_A_name, {}).get('final_sigs', []))
            if not required_cusps.issubset(planet_A_final_sigs): continue

            reason = f"Star lord {planet_B_name} is an RP signifying PC {primary_cusp_num} & {planet_A_name} signifies all required cusps {sorted(list(required_cusps))}."
            s_of_s_rps[planet_A_name] = reason
            self._log_debug(f"Identified Strongest of Strongest RP: {planet_A_name} (Reason: {reason})")

        # Derived RPs (Rahu & Ketu as Agents)
        derived_rps = {}
        # This set includes all RPs identified before considering special node promotions
        all_rps_for_nodes = all_initial_rps.union(set(s_of_s_rps.keys()))

        rahu_data = self.current_planetary_positions.get('Rahu')
        if rahu_data:
            rahu_sign_lord = rahu_data[2]
            rahu_star_lord = rahu_data[3]
            if rahu_sign_lord in all_rps_for_nodes and rahu_star_lord in all_rps_for_nodes:
                derived_rps['Rahu'] = f"Sign Lord ({rahu_sign_lord}) & Star Lord ({rahu_star_lord}) are RPs."
                self._log_debug(f"Identified Derived RP: Rahu (Reason: {derived_rps['Rahu']})")

        ketu_data = self.current_planetary_positions.get('Ketu')
        if ketu_data:
            ketu_sign_lord = ketu_data[2]
            ketu_star_lord = ketu_data[3]
            if ketu_sign_lord in all_rps_for_nodes and ketu_star_lord in all_rps_for_nodes:
                derived_rps['Ketu'] = f"Sign Lord ({ketu_sign_lord}) & Star Lord ({ketu_star_lord}) are RPs."
                self._log_debug(f"Identified Derived RP: Ketu (Reason: {derived_rps['Ketu']})")

        # --- NEW LOGIC BLOCK: Additional Rule for Rahu/Ketu Promotion to Strongest of Strongest ---
        # Rahu/Ketu become "Strongest of Strongest" if they are already an RP AND signify all required cusps.
        # This rule processes Rahu/Ketu even if they were only 'Derived' initially.
        for node_name in ['Rahu', 'Ketu']:
            node_data = self.current_planetary_positions.get(node_name)
            if node_data:
                node_final_sigs = set(self.stellar_significators_data.get(node_name, {}).get('final_sigs', []))

                # Check if this node is already considered an RP in any category (including derived)
                # and if it signifies all required cusps
                if node_final_sigs and required_cusps.issubset(node_final_sigs):
                    # If it passed, it's promoted/confirmed as Strongest of Strongest
                    reason = f"Is a final RP and signifies all required cusps {sorted(list(required_cusps))}."
                    s_of_s_rps[node_name] = reason  # Add or overwrite in S. of S. category
                    self._log_debug(f"PROMOTED: {node_name} promoted to Strongest of Strongest. Reason: {reason}")
        # --- END OF NEW LOGIC BLOCK ---

        # 3. Create a master set of all unique planets found across all categories
        master_rp_set = base_rps.union(strongest_rps.keys(), s_of_s_rps.keys(), derived_rps.keys())

        # 4. For each unique planet, determine its single highest rank
        final_ranked_list = []
        for planet in master_rp_set:
            rank_score = 99  # Default to lowest rank (higher number = lower rank)
            strength_str = "Unknown"
            reason_str = "N/A"

            # Check from highest rank to lowest and assign the best one found
            if planet in s_of_s_rps:
                rank_score, strength_str, reason_str = (1, "Strongest of Strongest", s_of_s_rps[planet])
            elif planet in strongest_rps:
                rank_score, strength_str, reason_str = (2, "Strongest", strongest_rps[planet])
            elif planet in derived_rps:
                # Only assign Derived if it wasn't promoted to Strongest of Strongest
                if planet not in s_of_s_rps:
                    rank_score, strength_str, reason_str = (3, "Derived", derived_rps[planet])
            elif planet in base_rps:
                # Assign specific categories for Base RPs based on their classification
                classification = self.planet_classifications.get(planet, 'Unclassified')
                if classification == 'Positive':
                    rank_score, strength_str, reason_str = (4, "Second Strong", "Base RP with Positive signification")
                elif classification == 'Neutral':
                    rank_score, strength_str, reason_str = (5, "Weak", "Base RP with Neutral signification")
                else:  # Negative or Unclassified Base RPs
                    rank_score, strength_str, reason_str = (6, "Other Base RP", "Base RP not meeting other criteria")

            final_ranked_list.append((rank_score, strength_str, planet, reason_str))

        # 5. Sort the final list by rank score (1 is highest)
        final_ranked_list.sort(key=lambda x: x[0])

        # 6. Populate the Treeview with the clean, sorted, and unique list
        self.rp_tree.delete(*self.rp_tree.get_children())  # Clear before populating
        for i, (rank, strength, planet, reason) in enumerate(final_ranked_list):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.rp_tree.insert("", "end", values=(strength, planet, reason), tags=(tag,))

        self._log_debug("RP Treeview populated with new, non-repeating logic.")
        self.all_ruling_planets = master_rp_set  # Cache all unique RPs found
        self._log_debug(f"All RPs cached: {self.all_ruling_planets}")
    def _log_debug(self, message, **kwargs):
        """
        Logs a debug message using the configured debug_logger.
        Now accepts arbitrary keyword arguments (**kwargs) to pass to the logger,
        e.g., exc_info=True for printing stack traces.
        """
        if self.is_debug_mode: # Assuming self.is_debug_mode controls logging verbosity
            debug_logger.debug(message, **kwargs) # Pass all kwargs to the underlying logger

    def _on_tab_change(self, event):
        selected_tab_id = self.notebook.select()
        selected_tab_text = self.notebook.tab(selected_tab_id, "text")

        if selected_tab_text == "Stellar Status Significators":
            self._populate_all_stellar_significators_table()
        elif selected_tab_text == "Daily Analysis":
            self._update_daily_analysis_time_inputs()
            self._toggle_analysis_mode_inputs()

    def _update_daily_analysis_time_inputs(self):
        """
        (CORRECTED) Updates the date entry widgets in the Daily Analysis tab to the current date.
        Removes references to non-existent time entry widgets.
        """
        now = datetime.datetime.now()

        # Update the date for the "24 hours" mode
        if hasattr(self, 'analysis_date_entry'):
            self.analysis_date_entry.set_date(now.date())
            # The lines for the old 'analysis_time_entry' have been removed as it no longer exists.

        # Update the dates for the "Custom Date Range" mode
        if hasattr(self, 'analysis_custom_start_date_entry'):
            self.analysis_custom_start_date_entry.set_date(now.date())
            # The lines for the old 'analysis_custom_time_entry' have been removed as it no longer exists.

            # Also set the end date to today by default for a clean UI
            if hasattr(self, 'analysis_custom_end_date_entry'):
                self.analysis_custom_end_date_entry.set_date(now.date())

    def _toggle_analysis_mode_inputs(self):
        """
        CORRECTED: Shows or hides the correct date input fields based on the selected radio button.
        This version no longer manages the cusp widgets, as their position is now fixed.
        """
        mode = self.analysis_mode_var.get()
        if mode == "24_hours":
            # Hide the custom date range frame and show the 24-hour frame
            self.custom_span_inputs_frame.grid_remove()
            self.single_day_inputs_frame.grid(row=3, column=0, columnspan=2, sticky='ew')
        elif mode == "custom_span":
            # Hide the 24-hour frame and show the custom date range frame
            self.single_day_inputs_frame.grid_remove()
            self.custom_span_inputs_frame.grid(row=3, column=0, columnspan=2, sticky='ew')

    @staticmethod
    @staticmethod
    @staticmethod
    def get_khullar_ayanamsha(jd_ut):
        """
        Calculates Khullar Ayanamsha by applying a standard 6-arcminute
        correction to the Lahiri Ayanamsha.
        """
        # Get the standard Lahiri Ayanamsha value for the given Julian Day in UT
        lahiri_ayanamsa = swe.get_ayanamsa_ut(jd_ut)

        # The standard correction for Khullar Ayanamsha is to subtract 6 arcminutes.
        # 6 arcminutes = 6.0 / 60.0 = 0.1 degrees.
        correction_in_degrees = 0.1

        return lahiri_ayanamsa - correction_in_degrees
    @staticmethod
    @staticmethod
    def get_lat_lon(city):
        """
        Returns the latitude and longitude for a given city from the main city dictionary.
        Defaults to Kolkata if the city is not found.
        """
        # Corrected to use the new ALL_INDIAN_CITIES dictionary
        return ALL_INDIAN_CITIES.get(city, (22.5726, 88.3639))

    @staticmethod
    def get_sign(degree):
        sign_index = int(degree / 30) % 12
        return ZODIAC_SIGNS[sign_index]

    @staticmethod
    def get_sign_lord(sign_name):
        return ZODIAC_LORD_MAP.get(sign_name, "N/A")

    @staticmethod
    def get_nakshatra_info(sidereal_degree):
        """
        Calculates Nakshatra, Star, Sub, Sub-Sub, and Sookshma Lords for a given sidereal degree.
        Sookshma Lord is the 5th level (subdivision of Sub-Sub Lord).
        """
        degree_in_nakshatra_cycle = sidereal_degree % 360
        nakshatra_index = int(degree_in_nakshatra_cycle / NAKSHATRA_SPAN_DEG)
        nakshatra_name, nakshatra_lord = NAKSHATRAS[nakshatra_index]

        degree_within_nakshatra = degree_in_nakshatra_cycle % NAKSHATRA_SPAN_DEG

        # Ensure nakshatra_lord_index is valid before use
        try:
            nakshatra_lord_index = LORD_ORDER.index(nakshatra_lord)
        except ValueError:
            # Fallback if nakshatra_lord is not found in LORD_ORDER (shouldn't happen with correct data)
            nakshatra_lord_index = 0  # Default to first lord for calculation consistency

        rotated_lord_order_for_sub = LORD_ORDER[nakshatra_lord_index:] + LORD_ORDER[:nakshatra_lord_index]

        current_span_accumulated_sub = 0.0
        sub_lord = ""
        sub_lord_start_deg_in_nakshatra = 0.0
        sub_lord_span_deg = 0.0

        for lord in rotated_lord_order_for_sub:
            span_for_this_lord = DASHA_PERIODS[lord] / 120 * NAKSHATRA_SPAN_DEG
            if degree_within_nakshatra < current_span_accumulated_sub + span_for_this_lord:
                sub_lord = lord
                sub_lord_start_deg_in_nakshatra = current_span_accumulated_sub
                sub_lord_span_deg = span_for_this_lord
                break
            current_span_accumulated_sub += span_for_this_lord

        sub_sub_lord = ""
        sookshma_lord = ""  # Initialize sookshma_lord

        if sub_lord:  # Only proceed if a sub_lord was successfully determined
            degree_within_sub_lord = degree_within_nakshatra - sub_lord_start_deg_in_nakshatra

            # Ensure sub_lord_index is valid for rotated_lords_for_sub_sub
            try:
                sub_lord_index_for_sub_sub = LORD_ORDER.index(sub_lord)
            except ValueError:
                sub_lord_index_for_sub_sub = 0  # Fallback

            rotated_lords_for_sub_sub = LORD_ORDER[sub_lord_index_for_sub_sub:] + LORD_ORDER[
                                                                                  :sub_lord_index_for_sub_sub]

            current_span_accumulated_sub_sub = 0.0
            sub_sub_lord_start_deg_in_sub = 0.0
            sub_sub_lord_span_deg = 0.0

            for lord in rotated_lords_for_sub_sub:
                # Calculate span for Sub-Sub Lord relative to the Sub Lord's span
                span_for_this_sub_sub_lord = (DASHA_PERIODS[lord] / 120) * sub_lord_span_deg

                # --- THIS IS THE CORRECTED LINE ---
                # It uses 'degree_within_sub_lord' which is correctly defined,
                # NOT 'degree_within_sub_sub_lord' which is for the *next* level.
                if degree_within_sub_lord < current_span_accumulated_sub_sub + span_for_this_sub_sub_lord:
                    sub_sub_lord = lord
                    sub_sub_lord_start_deg_in_sub = current_span_accumulated_sub_sub
                    sub_sub_lord_span_deg = span_for_this_sub_sub_lord
                    break
                current_span_accumulated_sub_sub += span_for_this_sub_sub_lord

            # --- Calculate Sookshma Lord ---
            # This block executes only if a sub_sub_lord was found AND its span is positive
            if sub_sub_lord and sub_sub_lord_span_deg > 0:
                degree_within_sub_sub_lord = degree_within_sub_lord - sub_sub_lord_start_deg_in_sub

                # Ensure sub_sub_lord_index is valid for rotated_lords_for_sookshma
                try:
                    sub_sub_lord_index_for_sookshma = LORD_ORDER.index(sub_sub_lord)
                except ValueError:
                    sub_sub_lord_index_for_sookshma = 0  # Fallback

                rotated_lords_for_sookshma = LORD_ORDER[sub_sub_lord_index_for_sookshma:] + LORD_ORDER[
                                                                                            :sub_sub_lord_index_for_sookshma]

                current_span_accumulated_sookshma = 0.0
                for lord in rotated_lords_for_sookshma:
                    # Calculate span for Sookshma Lord relative to the Sub-Sub Lord's span
                    span_for_this_sookshma_lord = (DASHA_PERIODS[lord] / 120) * sub_sub_lord_span_deg
                    if degree_within_sub_sub_lord < current_span_accumulated_sookshma + span_for_this_sookshma_lord:
                        sookshma_lord = lord
                        break
                    current_span_accumulated_sookshma += span_for_this_sookshma_lord

        return nakshatra_name, nakshatra_lord, sub_lord, sub_sub_lord, sookshma_lord

    def _on_city_keypress(self, event):
        """
        Filters the city combobox dropdown list based on user input.
        """
        typed_text = self.city_combo.get().lower()

        if not typed_text:
            self.city_combo['values'] = self.sorted_city_list
            return

        filtered_cities = [city for city in self.sorted_city_list if city.lower().startswith(typed_text)]

        if filtered_cities:
            self.city_combo['values'] = filtered_cities
        else:
            self.city_combo['values'] = self.sorted_city_list

    def _set_time_to_now(self):
        """Updates the date and time listboxes to the current system time."""
        now = datetime.datetime.now()

        # Helper to select an item in a listbox
        def select_item(listbox, value):
            try:
                # Get all items from the listbox
                items = list(listbox.get(0, tk.END))
                if str(value) in items:
                    idx = items.index(str(value))
                    listbox.selection_clear(0, tk.END)
                    listbox.selection_set(idx)
                    listbox.see(idx)  # Scroll to the item
            except ValueError:
                self._log_debug(f"Value {value} not found in listbox.")

        # Set date
        select_item(self.year_lb, now.year)
        select_item(self.month_lb, MONTH_NAMES[now.month - 1])
        select_item(self.day_lb, f"{now.day:02d}")

        # Set time
        select_item(self.hour_lb, f"{now.hour:02d}")
        select_item(self.minute_lb, f"{now.minute:02d}")
        select_item(self.second_lb, f"{now.second:02d}")

        self._log_debug("Date and Time fields set to NOW.")

    def _set_default_inputs(self):
        """Sets the default values for all input fields on startup."""
        # Set the listboxes to the current time by calling the function above
        self._set_time_to_now()

        # Set other default inputs
        self.city_combo.set("Kolkata")
        self.horary_entry.delete(0, tk.END)
        self.horary_entry.insert(0, "1")
        self.timezone_combo.set("Asia/Kolkata")

        self.analysis_duration_value_entry.delete(0, tk.END)
        if self.analysis_duration_value_entry.get() == "":
            self.analysis_duration_value_entry.insert(0, "24")

        self._log_debug("Default inputs set.")

    def _on_popup_press(self, event):
        """Records the initial mouse position for dragging the tour popup."""
        self._offset_x = event.x
        self._offset_y = event.y

    def _on_popup_release(self, event):
        """Resets the mouse offset when the drag is released."""
        self._offset_x = None
        self._offset_y = None

    def _on_popup_motion(self, event):
        """Moves the tour popup window based on mouse drag."""
        if hasattr(self, '_offset_x') and self._offset_x is not None:
            new_x = self.tour_popup.winfo_x() + (event.x - self._offset_x)
            new_y = self.tour_popup.winfo_y() + (event.y - self._offset_y)
            self.tour_popup.geometry(f"+{new_x}+{new_y}")

    def _blink_widget(self, widgets, count):
        """Causes a list of widgets to 'blink' by changing their style/color."""
        # Check if the tour has ended prematurely or the blink count is zero
        if self._tour_ended or count <= 0:
            # When blinking stops, ensure the widgets are left in the highlighted state.
            # The final reversion to original style happens in end_tour or at the start of the next step.
            if self.last_highlighted_widget_info:
                for info in self.last_highlighted_widget_info:
                    widget = info['widget']
                    if not widget.winfo_exists() or widget not in widgets:
                        continue

                    widget_class = widget.winfo_class()
                    if 'T' in widget_class:
                        widget.configure(style=f"Highlight.{widget_class}")
                    else:  # Handle tk Listbox
                        widget.configure(background=self.highlight_opts['background'])
            return

        # The main blinking logic
        for widget in widgets:
            if not widget.winfo_exists():
                continue

            is_ttk = 'T' in widget.winfo_class()

            if is_ttk:
                # This is a ttk widget, so we toggle its style
                current_style = widget.cget("style")
                highlight_style = f"Highlight.{widget.winfo_class()}"

                original_style = ""
                for info in self.last_highlighted_widget_info:
                    if info.get('widget') == widget:
                        original_style = info.get('style', '')
                        break

                new_style = original_style if current_style == highlight_style else highlight_style
                widget.configure(style=new_style)
            else:
                # This is a standard tk widget (like Listbox), so we toggle its background
                current_bg = str(widget.cget('background'))
                highlight_bg = str(self.highlight_opts['background'])

                original_bg = ''
                for info in self.last_highlighted_widget_info:
                    if info.get('widget') == widget:
                        original_bg = info.get('orig_opts', {}).get('background', '')
                        break

                new_bg = original_bg if current_bg == highlight_bg else highlight_bg
                widget.configure(background=new_bg)

        # Schedule the next blink
        self._blink_job_id = self.root.after(300, self._blink_widget, widgets, count - 1)

    def _show_help_topics(self):
        """Creates and displays the main Help Topics window."""
        if hasattr(self, 'help_window') and self.help_window.winfo_exists():
            self.help_window.lift()
            return

        self.help_window = tk.Toplevel(self.root)
        self.help_window.title("Help Topics")
        self.help_window.geometry("700x500")

        p_window = ttk.PanedWindow(self.help_window, orient=tk.HORIZONTAL)
        p_window.pack(fill="both", expand=True, padx=10, pady=10)

        # Left side: List of topics
        list_frame = ttk.Frame(p_window, width=200)
        p_window.add(list_frame, weight=1)

        self.topic_listbox = tk.Listbox(list_frame, exportselection=False, font=('Helvetica', 10))
        self.topic_listbox.pack(fill="both", expand=True)
        for topic in HELP_TOPICS_CONTENT:
            self.topic_listbox.insert(tk.END, topic)

        self.topic_listbox.bind("<<ListboxSelect>>", self._on_topic_select)

        # Right side: Content display
        content_frame = ttk.Frame(p_window)
        p_window.add(content_frame, weight=3)

        self.help_content_text = tk.Text(content_frame, wrap="word", font=('Helvetica', 10), relief="flat", padx=5)
        self.help_content_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.help_content_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.help_content_text.config(yscrollcommand=scrollbar.set)

        # Load the first topic by default
        self.topic_listbox.select_set(0)
        self._on_topic_select(None)  # Trigger the display update

    def _on_topic_select(self, event):
        """Called when a user clicks a topic in the help window listbox."""
        selection_indices = self.topic_listbox.curselection()
        if not selection_indices:
            return

        selected_topic = self.topic_listbox.get(selection_indices[0])
        content = HELP_TOPICS_CONTENT.get(selected_topic, "Topic not found.")

        self.help_content_text.config(state='normal')  # Must be normal to edit
        self.help_content_text.delete(1.0, tk.END)
        self.help_content_text.insert(tk.END, content)
        self.help_content_text.config(state='disabled')  # Make it read-only for the user

    def _create_chart_generation_tab(self):
        chart_frame = ttk.Frame(self.notebook)
        self.notebook.add(chart_frame, text="Chart Generation")

        chart_frame.grid_columnconfigure(0, weight=1)
        chart_frame.grid_rowconfigure(1, weight=1)

        # --- TOP INPUT FRAME (No changes here) ---
        input_frame = ttk.LabelFrame(chart_frame, text="Chart Input")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)
        self.chart_type_frame = ttk.LabelFrame(input_frame, text="Chart Type")
        self.chart_type_frame.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='ew')
        ttk.Radiobutton(self.chart_type_frame, text="Horary Chart", variable=self.chart_type_var, value="Horary",
                        command=self._toggle_chart_type_inputs).pack(side='left', padx=10)
        ttk.Radiobutton(self.chart_type_frame, text="Birth Chart", variable=self.chart_type_var,
                        value="Birth Chart", command=self._toggle_chart_type_inputs).pack(side='left', padx=10)
        self.horary_label = ttk.Label(input_frame, text="Horary Number (1–2193):")
        self.horary_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')
        self.horary_entry = ttk.Entry(input_frame, width=10)
        self.horary_entry.grid(row=1, column=1, padx=5, pady=2, sticky='w')
        date_frame = ttk.Frame(input_frame)
        date_frame.grid(row=2, column=1, columnspan=3, pady=2, sticky='w')
        ttk.Label(input_frame, text="Date (Y/M/D):").grid(row=2, column=0, padx=5, pady=2, sticky='w')

        def create_scrolled_listbox(parent, height, width):
            lb_frame = ttk.Frame(parent)
            scrollbar = ttk.Scrollbar(lb_frame, orient='vertical')
            listbox = tk.Listbox(lb_frame, yscrollcommand=scrollbar.set, height=height, width=width,
                                 exportselection=False, font=('Helvetica', 9))
            scrollbar.config(command=listbox.yview)
            scrollbar.pack(side='right', fill='y')
            listbox.pack(side='left', fill='both', expand=True)
            return listbox, lb_frame

        self.year_lb, year_frame = create_scrolled_listbox(date_frame, height=5, width=8)
        year_frame.pack(side='left', padx=2)
        for year in range(datetime.datetime.now().year + 1, 1920, -1): self.year_lb.insert(tk.END, str(year))
        self.month_lb, month_frame = create_scrolled_listbox(date_frame, height=5, width=12)
        month_frame.pack(side='left', padx=2)
        for month_name in MONTH_NAMES: self.month_lb.insert(tk.END, month_name)
        self.day_lb, day_frame = create_scrolled_listbox(date_frame, height=5, width=5)
        day_frame.pack(side='left', padx=2)
        for day in range(1, 32): self.day_lb.insert(tk.END, f"{day:02d}")
        time_frame = ttk.Frame(input_frame)
        time_frame.grid(row=3, column=1, columnspan=3, pady=2, sticky='w')
        time_label_frame = ttk.Frame(input_frame)
        time_label_frame.grid(row=3, column=0, padx=5, pady=2, sticky='w')
        ttk.Label(time_label_frame, text="Time (H/M/S):").pack(side='left')
        self.now_button = ttk.Button(time_label_frame, text="Now!", command=self._set_time_to_now, width=5)
        self.now_button.pack(side='left', padx=(5, 0))
        self.hour_lb, hour_frame = create_scrolled_listbox(time_frame, height=5, width=5)
        hour_frame.pack(side='left', padx=2)
        for hour in range(24): self.hour_lb.insert(tk.END, f"{hour:02d}")
        self.minute_lb, minute_frame = create_scrolled_listbox(time_frame, height=5, width=5)
        minute_frame.pack(side='left', padx=2)
        for minute in range(60): self.minute_lb.insert(tk.END, f"{minute:02d}")
        self.second_lb, second_frame = create_scrolled_listbox(time_frame, height=5, width=5)
        second_frame.pack(side='left', padx=2)
        for second in range(60): self.second_lb.insert(tk.END, f"{second:02d}")
        ttk.Label(input_frame, text="City:").grid(row=4, column=0, padx=5, pady=(10, 2), sticky='w')
        self.city_combo = ttk.Combobox(input_frame, values=self.sorted_city_list, state='normal')
        self.city_combo.grid(row=4, column=1, padx=5, pady=(10, 2), sticky='w')
        self.city_combo.bind('<KeyRelease>', self._on_city_keypress)
        ttk.Label(input_frame, text="House System:").grid(row=5, column=0, padx=5, pady=2, sticky='w')
        self.house_sys_combo = ttk.Combobox(input_frame, values=list(HOUSE_SYSTEMS.keys()), state='readonly')
        self.house_sys_combo.grid(row=5, column=1, padx=5, pady=2, sticky='w')
        self.house_sys_combo.set("Placidus")
        ttk.Label(input_frame, text="Time Zone:").grid(row=6, column=0, padx=5, pady=2, sticky='w')
        self.timezone_combo = ttk.Combobox(input_frame, values=pytz.all_timezones, state='readonly')
        self.timezone_combo.grid(row=6, column=1, padx=5, pady=2, sticky='ew')
        self.timezone_combo.set("Asia/Kolkata")
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=7, column=0, columnspan=4, pady=10)
        self.generate_chart_button = ttk.Button(button_frame, text="Generate Chart",
                                                command=self._on_generate_chart_button)
        self.generate_chart_button.pack(side='left', padx=5)
        ttk.Label(button_frame, text="(can take upto 2 min)").pack(side='left', anchor='w')
        self.rectify_button = ttk.Button(button_frame, text="Rectify Time", command=self._run_rectification)
        self.rectify_button.pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save Chart", command=self._popup_save_chart).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Load Chart", command=self._load_chart_and_results).pack(side='left', padx=5)

        # --- 3-COLUMN BOTTOM OUTPUT FRAME ---
        output_panel_frame = ttk.Frame(chart_frame)
        output_panel_frame.grid(row=1, column=0, sticky='nsew')

        output_panel_frame.grid_columnconfigure(0, weight=4, uniform="group1")
        output_panel_frame.grid_columnconfigure(1, weight=4, uniform="group1")
        output_panel_frame.grid_columnconfigure(2, weight=5, uniform="group1")
        output_panel_frame.grid_rowconfigure(0, weight=1)

        # --- Column 1: Planetary Positions ---
        planet_frame = ttk.LabelFrame(output_panel_frame, text="Planetary Positions")
        planet_frame.grid(row=0, column=0, sticky='nsew', padx=(10, 5), pady=10)
        planet_frame.rowconfigure(0, weight=1);
        planet_frame.columnconfigure(0, weight=1)
        planet_columns = ("Planet", "Degree", "Sign", "Sign Lord", "Star Lord", "Sub Lord", "SSL")
        self.planets_tree = ttk.Treeview(planet_frame, columns=planet_columns, show="headings")
        for col in planet_columns:
            self.planets_tree.heading(col, text=col)
            self.planets_tree.column(col, width=65, anchor='w')
        self.planets_tree.column("Planet", width=70, anchor='w')
        self.planets_tree.grid(row=0, column=0, sticky='nsew')

        # --- Column 2: Cuspal Positions ---
        cusp_frame = ttk.LabelFrame(output_panel_frame, text="Cuspal Positions")
        cusp_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=10)
        cusp_frame.rowconfigure(0, weight=1);
        cusp_frame.columnconfigure(0, weight=1)
        cusp_columns = ("House", "Degree", "Sign", "Sign Lord", "Star Lord", "Sub Lord", "SSL")
        self.cusps_tree = ttk.Treeview(cusp_frame, columns=cusp_columns, show="headings")
        for col in cusp_columns:
            self.cusps_tree.heading(col, text=col)
            self.cusps_tree.column(col, width=65, anchor='w')
        self.cusps_tree.column("House", width=70, anchor='w')
        self.cusps_tree.grid(row=0, column=0, sticky='nsew')

        # --- Column 3: Dasha and Other Info ---
        dasha_panel = ttk.Frame(output_panel_frame)
        dasha_panel.grid(row=0, column=2, sticky='nsew', padx=(5, 10), pady=10)
        dasha_panel.columnconfigure(0, weight=1)

        # Row configuration updated: Row 1 (Dasha Tree) now expands
        dasha_panel.rowconfigure(0, weight=0)  # Dasha Info Label
        dasha_panel.rowconfigure(1, weight=1)  # Dasha Tree (EXPANDS)
        dasha_panel.rowconfigure(2, weight=0)  # About Frame

        # General Info has been removed, widgets shifted up
        self.moon_dasha_info_label = ttk.Label(dasha_panel, text="Dasha calculated from Moon's position: (N/A)")
        self.moon_dasha_info_label.grid(row=0, column=0, sticky='w', pady=(0, 5))  # Now in row 0

        dasha_tree_frame = ttk.Frame(dasha_panel)
        dasha_tree_frame.grid(row=1, column=0, sticky='nsew', pady=(5, 0))  # Now in row 1
        dasha_tree_frame.rowconfigure(0, weight=1)
        dasha_tree_frame.columnconfigure(0, weight=1)

        self.dasa_tree = ttk.Treeview(dasha_tree_frame, columns=("Period", "Start Date", "End Date"),
                                      show="tree headings")

        self.dasa_tree.heading("#0", text="Dasha Level / Lord")
        self.dasa_tree.heading("Period", text="Period")
        self.dasa_tree.heading("Start Date", text="Start Date")
        self.dasa_tree.heading("End Date", text="End Date")

        self.dasa_tree.column("#0", width=220, anchor='w')
        self.dasa_tree.column("Period", width=90, anchor='w')
        self.dasa_tree.column("Start Date", width=110, anchor='w')
        self.dasa_tree.column("End Date", width=110, anchor='w')

        dasha_vsb = ttk.Scrollbar(dasha_tree_frame, orient="vertical", command=self.dasa_tree.yview)
        dasha_hsb = ttk.Scrollbar(dasha_tree_frame, orient="horizontal", command=self.dasa_tree.xview)
        self.dasa_tree.configure(yscrollcommand=dasha_vsb.set, xscrollcommand=dasha_hsb.set)

        self.dasa_tree.grid(row=0, column=0, sticky='nsew')
        dasha_vsb.grid(row=0, column=1, sticky='ns')
        dasha_hsb.grid(row=1, column=0, sticky='ew')

        about_frame = ttk.LabelFrame(dasha_panel, text="About")
        about_frame.grid(row=2, column=0, sticky='ew', pady=(10, 0))  # Now in row 2
        about_message = """Concept :  Nilotpal Munshi (2025)
Addition Criticism, functional and coding help by :
 Nabarun Chakraborty ,Aranya Sen and Obaidur Rehman"""
        about_label = ttk.Label(about_frame, text=about_message, justify=tk.LEFT)
        about_label.pack(padx=5, pady=5, anchor='w')

        self._toggle_chart_type_inputs()

    # Assuming ttk, tk, DateEntry are imported (e.g., from tkinter, tkcalendar)

    # This function belongs inside your AstrologyApp class
    def _create_daily_analysis_tab(self):
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="Daily Analysis")
        analysis_frame.grid_columnconfigure(0, weight=1)
        analysis_frame.grid_rowconfigure(1, weight=1)  # Results tree will expand

        analysis_input_frame = ttk.LabelFrame(analysis_frame, text="Analysis Input & Steps")
        analysis_input_frame.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        analysis_input_frame.grid_columnconfigure(0, weight=3)  # Left input column
        analysis_input_frame.grid_columnconfigure(1, weight=2)  # Right buttons column

        # --- Left Input Column Frame ---
        left_input_frame = ttk.Frame(analysis_input_frame)
        left_input_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        left_input_frame.columnconfigure(1, weight=1)  # Allow combobox/date entries to expand

        # Event Selection
        event_label = ttk.Label(left_input_frame, text="Select Event:")
        event_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 2), sticky='w')
        event_types = [f'{e["Query Type"]} (PC: {e["Primary Cusp"]}, SC: {e["Secondary Cusp"]})' for e in EVENT_DATASET]
        self.event_type_combo = ttk.Combobox(left_input_frame, values=event_types, state='readonly')
        self.event_type_combo.grid(row=1, column=0, columnspan=2, padx=5, pady=(5, 2), sticky='ew')
        self.event_type_combo.bind("<<ComboboxSelected>>", self._on_event_type_select)

        # Analysis Period (24 hours / Custom Range)
        mode_frame = ttk.LabelFrame(left_input_frame, text="Analysis Period")
        mode_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        self.analysis_mode_var = tk.StringVar(value="24_hours")
        ttk.Radiobutton(mode_frame, text="24 hours from Start Date", variable=self.analysis_mode_var, value="24_hours",
                        command=self._toggle_analysis_mode_inputs).pack(anchor='w')
        ttk.Radiobutton(mode_frame, text="Custom Date Range", variable=self.analysis_mode_var, value="custom_span",
                        command=self._toggle_analysis_mode_inputs).pack(anchor='w')

        # Single Day (24 hours) Inputs
        self.single_day_inputs_frame = ttk.Frame(left_input_frame)
        self.single_day_inputs_frame.grid(row=3, column=0, columnspan=2, sticky='ew')
        ttk.Label(self.single_day_inputs_frame, text="Start Date:").grid(row=0, column=0, sticky='w', padx=2)
        self.analysis_date_entry = DateEntry(self.single_day_inputs_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.analysis_date_entry.grid(row=0, column=1, sticky='w')
        ttk.Label(self.single_day_inputs_frame, text="Duration (Hours):").grid(row=1, column=0, sticky='w', padx=2)
        self.analysis_duration_value_entry = ttk.Entry(self.single_day_inputs_frame, width=10)
        self.analysis_duration_value_entry.grid(row=1, column=1, sticky='w')

        # Custom Span Inputs
        self.custom_span_inputs_frame = ttk.Frame(left_input_frame)
        # This frame is not gridded here, it's toggled by _toggle_analysis_mode_inputs
        ttk.Label(self.custom_span_inputs_frame, text="Start Date:").grid(row=0, column=0, sticky='w', padx=2)
        self.analysis_custom_start_date_entry = DateEntry(self.custom_span_inputs_frame, selectmode='day',
                                                          date_pattern='yyyy-mm-dd')
        self.analysis_custom_start_date_entry.grid(row=0, column=1, sticky='w')
        ttk.Label(self.custom_span_inputs_frame, text="End Date:").grid(row=1, column=0, sticky='w', padx=2)
        self.analysis_custom_end_date_entry = DateEntry(self.custom_span_inputs_frame, selectmode='day',
                                                        date_pattern='yyyy-mm-dd')
        self.analysis_custom_end_date_entry.grid(row=1, column=1, sticky='w')

        # Cusp Selection
        cusp_frame = ttk.LabelFrame(left_input_frame, text="Cusp Selection")
        cusp_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=5)
        primary_cusp_options = [f"House {i}" for i in range(1, 13)]
        ttk.Label(cusp_frame, text="Primary Cusp:").grid(row=0, column=0, sticky='w', padx=5)
        self.primary_cusp_combo = ttk.Combobox(cusp_frame, values=primary_cusp_options, state='readonly')
        self.primary_cusp_combo.grid(row=0, column=1, sticky='ew', padx=5)
        self.primary_cusp_combo.set("House 1")  # Default selection

        ttk.Label(cusp_frame, text="Secondary Cusps:").grid(row=1, column=0, sticky='w', padx=5)
        self.secondary_cusp_listbox = tk.Listbox(cusp_frame, selectmode="extended", height=5, exportselection=False,
                                                 font=('Helvetica', 9))  # Added font for consistency
        for cusp_opt in primary_cusp_options: self.secondary_cusp_listbox.insert(tk.END, cusp_opt)
        self.secondary_cusp_listbox.insert(tk.END, "Marak")
        self.secondary_cusp_listbox.insert(tk.END, "Badhak")
        self.secondary_cusp_listbox.grid(row=1, column=1, sticky='ew', padx=5)

        # Promise Check elements
        self.promise_button = ttk.Button(cusp_frame, text="Check Promise", command=self._check_promise)
        self.promise_button.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5, padx=5)
        self.asc_promise_label = ttk.Label(cusp_frame, text="Asc:", foreground="gray")
        self.asc_promise_label.grid(row=3, column=0, sticky='w', padx=5)
        self.pcusp_promise_label = ttk.Label(cusp_frame, text="Pcusp:", foreground="gray")
        self.pcusp_promise_label.grid(row=3, column=1, sticky='w', padx=5)

        # Labels for Positive/Neutral Planets
        self.positive_planets_label = ttk.Label(cusp_frame, text="Positive Planets: (Not Calculated)", wraplength=200,
                                                justify=tk.LEFT)
        self.positive_planets_label.grid(row=4, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        self.neutral_planets_label = ttk.Label(cusp_frame, text="Neutral Planets: (Not Calculated)", wraplength=200,
                                               justify=tk.LEFT)
        self.neutral_planets_label.grid(row=5, column=0, columnspan=2, sticky='w', padx=5, pady=2)

        # --- Right Buttons Column Frame ---
        right_button_frame = ttk.LabelFrame(analysis_input_frame, text="Analysis Steps")
        right_button_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        right_button_frame.columnconfigure(0, weight=1)  # Column for buttons to expand

        ttk.Label(right_button_frame, text="Follow these steps in order.", wraplength=200).pack(pady=5, padx=10)

        self.find_dasha_button = ttk.Button(right_button_frame, text="Step 1: Find Favorable Dashas",
                                            command=self.run_step1_dasha_analysis)
        self.find_dasha_button.pack(fill='x', padx=10, pady=5, ipady=4)

        self.find_transit_button = ttk.Button(right_button_frame, text="Step 2: Find Favorable Transits",
                                              command=self.run_step2_transit_analysis, state="disabled")
        self.find_transit_button.pack(fill='x', padx=10, pady=5, ipady=4)

        self.sort_by_rp_button = ttk.Button(right_button_frame, text="Step 3: Filter & Sort by RP",
                                            command=self._sort_by_ruling_planets, state="disabled")
        self.sort_by_rp_button.pack(fill='x', padx=10, pady=5, ipady=4)

        self.rp_interlink_button = ttk.Button(right_button_frame, text="Step 4: Check RP Interlink",
                                              command=self._run_rp_interlink_analysis, state="disabled")
        self.rp_interlink_button.pack(fill='x', padx=10, pady=5, ipady=4)

        self.filter_pc_sign_star_button = ttk.Button(right_button_frame, text="Step 5: Filter by PC Sign/Star",
                                                     command=self._filter_by_pc_sign_star, state="disabled")
        self.filter_pc_sign_star_button.pack(fill='x', padx=10, pady=5, ipady=4)

        self.final_sort_button = ttk.Button(right_button_frame, text="Step 6: Final Sort", command=self._run_final_sort,
                                            state="disabled")
        self.final_sort_button.pack(fill='x', padx=10, pady=5, ipady=4)

        # --- NEW POST-FINAL SORT FILTERS SECTION ---
        ttk.Separator(right_button_frame, orient='horizontal').pack(fill='x', padx=10, pady=10)

        post_filter_frame = ttk.LabelFrame(right_button_frame, text="Post-Final Sort Filters")
        post_filter_frame.pack(fill='x', padx=10, pady=5, ipady=4)
        post_filter_frame.columnconfigure(0, weight=1)
        post_filter_frame.columnconfigure(1, weight=1)
        post_filter_frame.columnconfigure(2, weight=1)

        # BooleanVars to hold checkbox states (already defined in __init__ for common practice)
        # self.ju_plus_var = tk.BooleanVar() # Already defined in __init__
        # self.su_plus_var = tk.BooleanVar() # Already defined in __init__
        # self.mo_plus_var = tk.BooleanVar() # Already defined in __init__

        # Checkbuttons, tied to the new _apply_post_filters method
        self.ju_plus_cb = ttk.Checkbutton(post_filter_frame, text="Ju+", variable=self.ju_plus_var,
                                          command=self._apply_post_filters)
        self.ju_plus_cb.grid(row=0, column=0, sticky='w', padx=5, pady=2)

        self.su_plus_cb = ttk.Checkbutton(post_filter_frame, text="Su+", variable=self.su_plus_var,
                                          command=self._apply_post_filters)
        self.su_plus_cb.grid(row=0, column=1, sticky='w', padx=5, pady=2)

        self.mo_plus_cb = ttk.Checkbutton(post_filter_frame, text="Mo+", variable=self.mo_plus_var,
                                          command=self._apply_post_filters)
        self.mo_plus_cb.grid(row=0, column=2, sticky='w', padx=5, pady=2)

        # Initially disable them until Final Sort has run (will be enabled by _run_final_sort)
        self.ju_plus_cb.config(state='disabled')
        self.su_plus_cb.config(state='disabled')
        self.mo_plus_cb.config(state='disabled')

        # Add a reset button for these filters
        self.reset_post_filters_button = ttk.Button(post_filter_frame, text="Reset Filters",
                                                    command=self._reset_post_filters)
        self.reset_post_filters_button.grid(row=1, column=0, columnspan=3, sticky='ew', padx=5, pady=2)
        self.reset_post_filters_button.config(state='disabled')  # Initially disabled
        # --- END NEW POST-FINAL SORT FILTERS SECTION ---

        # --- Analysis Output Frame (Results Treeview) ---
        analysis_output_frame = ttk.LabelFrame(analysis_frame, text="Analysis Results")
        analysis_output_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        analysis_output_frame.grid_rowconfigure(0, weight=1)  # Treeview row expands
        analysis_output_frame.grid_columnconfigure(0, weight=1)  # Treeview column expands

        self.analysis_results_tree_frame = ttk.Frame(analysis_output_frame)
        self.analysis_results_tree_frame.grid(row=0, column=0, sticky='nsew')
        self.analysis_results_tree_frame.grid_rowconfigure(0, weight=1)
        self.analysis_results_tree_frame.grid_columnconfigure(0, weight=1)

        self.analysis_results_tree = ttk.Treeview(self.analysis_results_tree_frame, selectmode='extended')
        self.analysis_results_tree.grid(row=0, column=0, sticky='nsew')

        self.results_scrollbar = ttk.Scrollbar(self.analysis_results_tree_frame, orient="vertical",
                                               command=self.analysis_results_tree.yview)
        self.results_scrollbar.grid(row=0, column=1, sticky='ns')
        self.analysis_results_tree.config(yscrollcommand=self.results_scrollbar.set)

        # Button to copy results
        bottom_button_frame = ttk.Frame(analysis_output_frame)
        bottom_button_frame.grid(row=1, column=0, sticky='ew', pady=(5, 0))
        self.copy_results_button = ttk.Button(bottom_button_frame, text="Copy Results",
                                              command=lambda: self._copy_treeview_to_clipboard(
                                                  self.analysis_results_tree))
        self.copy_results_button.pack(side='left', fill='x', expand=True, padx=2)

        # Initialize visibility of input fields (default to 24 hours mode)
        self._toggle_analysis_mode_inputs()



    def _filter_by_link_persistence(self):
        """
        (NEW DYNAMIC LOGIC) For each unique interlink planet selected by the user, this
        function scans a dynamic window (2 or 5 minutes) starting from the planet's
        first hit to find the first persistent period of the interlink.
        The results are displayed in a collapsible tree.
        """
        self._log_debug("--- Running Intelligent Link Persistence Filter ---")

        # 1. Determine which results to process (user selection or all)
        all_item_ids = self.analysis_results_tree.get_children()
        if not all_item_ids:
            messagebox.showerror("Error", "Please run an interlink analysis first to generate results to filter.")
            return

        selected_item_ids = self.analysis_results_tree.selection()
        item_ids_to_process = selected_item_ids if selected_item_ids else all_item_ids
        if not item_ids_to_process:
            messagebox.showinfo("Info",
                                "No rows to process. Please run an interlink analysis or select rows from the current results.")
            return

        # 2. Extract and group the hit data by the linking planet
        hits_by_planet = {}
        local_tz = pytz.timezone(self.timezone_combo.get())
        for item_id in item_ids_to_process:
            values = self.analysis_results_tree.item(item_id, 'values')
            try:
                hit_time_str = values[1]
                planet_name = values[2]
                hit_time = datetime.datetime.strptime(hit_time_str, '%Y-%m-%d %H:%M:%S')
                if planet_name not in hits_by_planet: hits_by_planet[planet_name] = []
                hits_by_planet[planet_name].append(hit_time)
            except (ValueError, IndexError):
                self._log_debug(f"Skipping row as it's not a valid 'HIT' result: {values}")
                continue

        if not hits_by_planet:
            messagebox.showerror("Error", "No valid 'HIT' results were selected or found in the table.")
            return

        # 3. Get analysis context
        primary_cusp_num = self._get_original_primary_cusp_from_ui()
        if primary_cusp_num is None: return
        secondary_cusp_nums = self._get_selected_secondary_cusps()
        if not secondary_cusp_nums:
            messagebox.showerror("Input Error", "Please select at least one Secondary Cusp for this analysis.")
            return

        # 4. For each unique planet, scan its DYNAMIC window
        progress_info = self._setup_progress_window("Scanning for Link Persistence...")
        final_results = {}
        scan_interval_seconds = 5

        for i, (planet, hit_times) in enumerate(hits_by_planet.items()):
            # --- NEW DYNAMIC DURATION LOGIC ---
            dasha_length = DASHA_PERIODS.get(planet, 0)
            scan_duration_minutes = 2 if dasha_length <= 10 else 5
            self._log_debug(
                f"Scanning for {planet} (Dasha Length: {dasha_length}yrs) with a {scan_duration_minutes}-minute window.")
            # --- END OF NEW LOGIC ---

            self._update_progress(progress_info, int((i / len(hits_by_planet)) * 100), 100, datetime.datetime.now(),
                                  f"Scanning for {planet}...")

            earliest_hit = min(hit_times)
            scan_start_utc = local_tz.localize(earliest_hit).astimezone(pytz.utc)
            scan_end_utc = scan_start_utc + datetime.timedelta(minutes=scan_duration_minutes)

            time_pointer = scan_start_utc
            block_start_time = None
            found_window_for_this_planet = None

            while time_pointer < scan_end_utc:
                dyn_planets, dyn_cusps, _ = self._calculate_chart_data(time_pointer, self.city_combo.get(),
                                                                       self._get_selected_hsys())
                if not dyn_planets:
                    time_pointer += datetime.timedelta(seconds=scan_interval_seconds)
                    continue

                current_pc_sub_lord = dyn_cusps.get(primary_cusp_num, [None] * 6)[4]
                interlink_active_now = False
                if current_pc_sub_lord == planet:
                    pc_sl_data = dyn_planets.get(current_pc_sub_lord)
                    if pc_sl_data:
                        pc_sl_star_lord = pc_sl_data[3]
                        if all(dyn_cusps.get(sc, [None] * 6)[4] == pc_sl_star_lord for sc in secondary_cusp_nums):
                            interlink_active_now = True

                if interlink_active_now:
                    if block_start_time is None: block_start_time = time_pointer
                elif block_start_time is not None:
                    found_window_for_this_planet = {'start': block_start_time, 'end': time_pointer}
                    break

                time_pointer += datetime.timedelta(seconds=scan_interval_seconds)

            if block_start_time is not None and found_window_for_this_planet is None:
                found_window_for_this_planet = {'start': block_start_time, 'end': scan_end_utc}

            final_results[planet] = found_window_for_this_planet

        progress_info['window'].destroy()

        # 5. Display the results in the new hierarchical tree
        self.analysis_results_tree.delete(*self.analysis_results_tree.get_children())
        self.analysis_results_tree["columns"] = ("Detail", "Start Time", "End Time")
        self.analysis_results_tree.heading("#0", text="Interlink Planet")
        self.analysis_results_tree.heading("Detail", text="Detail")
        self.analysis_results_tree.heading("Start Time", text="Start Time")
        self.analysis_results_tree.heading("End Time", text="End Time")
        # ... (column width settings) ...

        for planet, window_data in sorted(final_results.items()):
            parent_id = self.analysis_results_tree.insert("", "end", text=planet, values=("Linking Planet", "", ""),
                                                          open=True)
            if window_data:
                start_str = window_data['start'].astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
                end_str = window_data['end'].astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
                self.analysis_results_tree.insert(parent_id, "end", text="  ↳ Found Window",
                                                  values=("Persistent Interlink", start_str, end_str))
            else:
                # This handles Rule b: if no window found, proceed to next planet (and show this message)
                self.analysis_results_tree.insert(parent_id, "end", text="  ↳ No Persistent Window Found",
                                                  values=("(Interlink was not stable)", "", ""))

        messagebox.showinfo("Link Persistence Filter Complete",
                            f"Scanned for persistent interlinks for {len(final_results)} planet(s).")

    def _sort_by_ruling_planets(self):
        """
        (UPDATED) Filters Dasha/Transit results by P/N Ruling Planets, sorts them
        by Moon's transit quality, and enables the final RP Interlink analysis button.
        Now stores full row data in `self.rp_sorted_results` for subsequent filters.
        """
        self._log_debug("--- Filtering and Sorting results by Ruling Planets and Moon's transit quality ---")

        # Ensure the tree columns are set to the expected 10-column format first.
        # This also clears the treeview.
        self._update_analysis_results_tree_columns("detailed_full_analysis")

        if not hasattr(self, 'dasha_transit_windows') or not self.dasha_transit_windows:
            messagebox.showerror("Sequence Error", "Please run 'Step 2: Find Favorable Transits' before sorting.")
            return
        if not self.rp_tree.get_children():
            messagebox.showerror("Data Missing", "Please calculate Ruling Planets on the 'Ruling Planet' tab first.")
            return

        # Ensure subsequent buttons are disabled initially
        if hasattr(self, 'rp_interlink_button'): self.rp_interlink_button.config(state="disabled")
        if hasattr(self, 'filter_pc_sign_star_button'): self.filter_pc_sign_star_button.config(state="disabled")
        if hasattr(self, 'final_sort_button'): self.final_sort_button.config(state="disabled")

        qualified_rps = {
            values[1] for item_id in self.rp_tree.get_children()
            if (values := self.rp_tree.item(item_id, 'values')) and self.planet_classifications.get(values[1]) in [
                'Positive', 'Neutral']
        }

        if not qualified_rps:
            messagebox.showinfo("Info",
                                "No Ruling Planets were found that are also Positive or Neutral for this event.")
            # Still re-enable next button if applicable, even if no results
            if hasattr(self, 'rp_interlink_button'): self.rp_interlink_button.config(state="normal")
            return

        # Filter dasha_transit_windows based on qualified RPs
        filtered_results = [
            window for window in self.dasha_transit_windows
            if all(lord in qualified_rps for lord in window['dasha_lords'])
        ]

        if not filtered_results:
            messagebox.showinfo("Filter Complete",
                                "No Dasha/Transit periods were found where all 5 lords are qualified Ruling Planets.")
            if hasattr(self, 'rp_interlink_button'): self.rp_interlink_button.config(state="normal")
            return

        # Score results by Moon's transit quality
        scored_results = []
        local_tz = pytz.timezone(self.timezone_combo.get())

        # Determine analysis_duration for _check_transit_suitability_new
        analysis_duration = datetime.timedelta(days=365)  # Default value
        if hasattr(self, 'suitable_dasha_spans') and self.suitable_dasha_spans:
            if self.suitable_dasha_spans:  # Ensure there's at least one span
                start_of_span = self.suitable_dasha_spans[0]['start_utc']
                end_of_span = self.suitable_dasha_spans[-1]['end_utc']
                analysis_duration = end_of_span - start_of_span

        for item_window in filtered_results:  # `item_window` is a dict with 'dasha_lords', 'start_utc', 'end_utc'
            window_start_utc = item_window['start_utc']

            # Re-calculate dynamic data for Moon's classification details string
            _, transit_details = self._check_transit_suitability_new(window_start_utc, analysis_duration)
            moon_status_str_raw = transit_details.get('Moon', 'N/A')  # Example: "Moon SL:P/SubL:N/SSL:P"

            # Extract just the P/N/U characters for Moon's score
            moon_score = 0
            moon_class_chars = re.findall(r'\((\w)\)', moon_status_str_raw)  # Finds all (X) parts
            for char_code in moon_class_chars:
                if char_code == 'P':
                    moon_score += 2
                elif char_code == 'N':
                    moon_score += 1

            # Construct the full transit string as it appears in the treeview
            full_transit_str = (f"Jup:{transit_details.get('Jupiter', 'N/A')} | "
                                f"Sat:{transit_details.get('Saturn', 'N/A')} | "
                                f"Sun:{transit_details.get('Sun', 'N/A')} | "
                                f"Moon:{moon_status_str_raw}")

            scored_results.append({
                'score': moon_score,  # This score is for Moon's quality for sorting
                'window': item_window,  # Original window details (dasha_lords, start/end_utc)
                'transit_str_for_display': full_transit_str  # Store the generated transit string
            })

        # Sort the results primarily by Moon's score
        scored_results.sort(key=lambda x: x['score'], reverse=True)

        # Store the sorted results in `self.rp_sorted_results`
        # and populate the Treeview with the new 10-column structure
        self.rp_sorted_results = []  # Clear previous contents to rebuild with new structure
        self._log_debug("RP Sort: Clearing self.rp_sorted_results and repopulating with new structure.")
        for item_result in scored_results:
            window = item_result['window']
            start_str = window['start_utc'].astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
            end_str = window['end_utc'].astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')

            remark_content = f"RP Filter Passed (Score: {item_result['score']})"  # Now 'Remark' column
            cuspal_link_content = ""  # 'Cuspal Link' column is empty at this stage for this step

            # Create the 10-column row data
            current_row_data = (*window['dasha_lords'], start_str, end_str,
                                item_result['transit_str_for_display'],  # Use stored transit string
                                cuspal_link_content,  # Empty cuspal link
                                remark_content)  # Remark column

            self.analysis_results_tree.insert("", "end", values=current_row_data)

            # --- CRUCIAL ADDITION: Store the full row data in rp_sorted_results ---
            # This makes rp_sorted_results the source of truth for all column data
            self.rp_sorted_results.append({
                'score': item_result['score'],  # Keep the score
                'window': window,  # Keep the original window (start_utc, end_utc, dasha_lords)
                'display_row_data': current_row_data  # Store the exact row data as inserted into treeview
            })

        # --- DEBUGGING ADDITION ---
        self._log_debug(f"RP Sort: self.rp_sorted_results populated. First item (if any):")
        if self.rp_sorted_results:
            self._log_debug(f"  {self.rp_sorted_results[0]}")
        else:
            self._log_debug("  self.rp_sorted_results is empty after population.")
        # --- END DEBUGGING ADDITION ---

        # Enable the next button in the sequence: RP Interlink button
        if hasattr(self, 'rp_interlink_button'): self.rp_interlink_button.config(state="normal")
        messagebox.showinfo("Sort Complete",
                            f"Filtered and sorted {len(scored_results)} period(s). You may now run the 'Check RP Interlink' analysis.")

    def _run_rp_interlink_analysis(self):
        """
        Performs interlink analysis.
        - Shows a warning if no hits are selected, offering to proceed with all.
        - Shows a warning if multiple days are explicitly selected.
        - Processes selected items if any, otherwise processes all `rp_sorted_results`.
        """
        self._log_debug("--- Running FINAL Interlink analysis with Positive-Only RPs ---")

        # This button is 'filter_pc_sign_star_button', which comes AFTER rp_interlink_button in the flow.
        # It should be disabled at the start of this function.
        if hasattr(self, 'filter_pc_sign_star_button'):
            self.filter_pc_sign_star_button.config(state="disabled")

        # 1. Prerequisite checks
        if not hasattr(self, 'rp_sorted_results') or not self.rp_sorted_results:
            messagebox.showerror("Sequence Error", "Please run 'Filter & Sort by RP' first to generate results.")
            return

        # Define the sets of qualified RPs for different strictness levels
        strict_qualified_rps = {
            values[1] for item_id in self.rp_tree.get_children()
            if (values := self.rp_tree.item(item_id, 'values')) and
               self.planet_classifications.get(values[1]) == 'Positive'
        }

        relaxed_qualified_rps = {
            values[1] for item_id in self.rp_tree.get_children()
            if (values := self.rp_tree.item(item_id, 'values')) and
               self.planet_classifications.get(values[1]) in ['Positive', 'Neutral']
        }

        if not strict_qualified_rps:
            messagebox.showinfo("Info",
                                "No 'Positive' Ruling Planets found. Cannot perform stringent interlink analysis.")
            return

        self._log_debug(f"Strict Qualified RPs (P only): {sorted(list(strict_qualified_rps))}")
        self._log_debug(f"Relaxed Qualified RPs (P/N): {sorted(list(relaxed_qualified_rps))}")

        original_pc_num = self._get_original_primary_cusp_from_ui()
        if original_pc_num is None: return
        pc_for_analysis = self._determine_primary_cusp_for_analysis(original_pc_num)
        secondary_cusp_nums = self._get_selected_secondary_cusps()

        selected_item_ids = self.analysis_results_tree.selection()
        # `windows_to_scan` will now store: {'dasha_lords', 'start_utc', 'end_utc', 'original_display_row'}
        windows_to_scan = []
        process_all_results = False  # Flag to indicate if all results are being processed

        local_tz = pytz.timezone(self.timezone_combo.get())

        # --- Handle 'no selection' warning ---
        if not selected_item_ids:
            warning_no_selection_message = (
                "Analysis for all Hits will take hours. Please choose one entry. "
                "Cancel will take you back so you can choose. OK will proceed with All entries (not recommended)."
            )
            proceed_with_all = messagebox.askokcancel("Warning: No Entry Selected", warning_no_selection_message)
            if not proceed_with_all:
                self._log_debug("User cancelled RP Interlink analysis due to 'no selection' warning.")
                return  # Exit if user cancels

            self._log_debug("User chose to proceed with all results despite no selection.")
            # --- FIX: Ensure original_display_row is included when populating from rp_sorted_results ---
            for item_in_rp_sorted in self.rp_sorted_results:
                windows_to_scan.append({
                    'dasha_lords': item_in_rp_sorted['window']['dasha_lords'],
                    'start_utc': item_in_rp_sorted['window']['start_utc'],
                    'end_utc': item_in_rp_sorted['window']['end_utc'],
                    'original_display_row': item_in_rp_sorted['display_row_data']
                    # This is the crucial line for the fix
                })
            process_all_results = True
        else:
            # User selected specific items from the treeview
            self._log_debug(f"Processing {len(selected_item_ids)} selected item(s).")
            for item_id in selected_item_ids:
                original_display_row = self.analysis_results_tree.item(item_id,
                                                                       'values')  # Get values directly from treeview
                # Ensure the row has enough columns before accessing indices
                if len(original_display_row) >= 9:
                    try:
                        start_time_str = original_display_row[5]
                        end_time_str = original_display_row[6]

                        start_naive = None
                        end_naive = None

                        # Try parsing various time formats
                        try:
                            start_naive = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
                            end_naive = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            try:
                                start_naive = datetime.datetime.strptime(start_time_str, '%d %b \'%y %I:%M:%S %p')
                                end_naive = datetime.datetime.strptime(end_time_str, '%d %b \'%y %I:%M:%S %p')
                            except ValueError:
                                self._log_debug(f"Could not parse time string '{start_time_str}' or '{end_time_str}'.")
                                # If parsing fails for a selected item, it's a critical issue, so abort.
                                messagebox.showwarning("Date Parse Error",
                                                       f"Could not parse time for a selected item: {start_time_str}. Please ensure format is correct.")
                                return  # Exit if parsing fails

                        start_utc = local_tz.localize(start_naive).astimezone(pytz.utc)
                        end_utc = local_tz.localize(end_naive).astimezone(pytz.utc)

                        windows_to_scan.append({
                            'dasha_lords': list(original_display_row[0:5]),  # Copy dasha lords
                            'start_utc': start_utc,
                            'end_utc': end_utc,
                            'original_display_row': original_display_row  # Store the full display row
                        })
                    except Exception as e:  # Catch any other unexpected errors during processing a selected item
                        self._log_debug(f"Error processing selected item {item_id}: {e}. Skipping.")
                        messagebox.showwarning("Processing Error",
                                               f"An error occurred processing a selected item: {e}. Aborting.")
                        return  # Exit if there's an unrecoverable error for a selected item
                else:
                    self._log_debug(
                        f"Selected item {item_id} has insufficient columns ({len(original_display_row)}). Skipping.")

        if not windows_to_scan:  # Check if, after any selection processing, windows_to_scan is still empty.
            messagebox.showinfo("No Valid Periods",
                                "No valid time periods were found to analyze after checking selections.")
            return  # Exit if no windows to scan

        # --- Handle 'multiple days selected' warning ---
        if len(windows_to_scan) > 1 and not process_all_results:  # This condition means user specifically selected > 1
            warning_multiple_days_message = (
                "Cuspal interlink analysis for multiple days is a heavy and time-consuming task "
                "which can take hours. It is not not recommended. "
                "Do you still want to proceed? You can choose a single day from the List."
            )
            proceed_multiple_days = messagebox.askokcancel("Warning: Multiple Days Selected",
                                                           warning_multiple_days_message)
            if not proceed_multiple_days:
                self._log_debug("User cancelled RP Interlink analysis due to 'multiple days selection' warning.")
                return  # Exit if user cancels

        # --- At this point, the user has confirmed they want to proceed with the `windows_to_scan` ---
        # Now, set up the progress window, as the heavy computation will definitely begin.
        progress_info = self._setup_progress_window("Checking RP Interlink...")

        # Pass both strict and relaxed qualified sets to the scan function
        cuspal_hits = self._perform_cuspal_interlink_scan(windows_to_scan, strict_qualified_rps, relaxed_qualified_rps,
                                                          pc_for_analysis,
                                                          secondary_cusp_nums, progress_info)

        # Clean up progress window, ensuring it exists (it should, as we created it just before)
        if progress_info and progress_info['window'].winfo_exists():
            progress_info['window'].destroy()

        # Update UI with results
        self._update_analysis_results_tree_columns("detailed_full_analysis")

        if not cuspal_hits:
            messagebox.showinfo("Analysis Complete", "No precise interlinks found.")
            return

        for hit in cuspal_hits:
            # hit now contains: 'time', 'planet', 'type', 'dasha_lords', 'original_display_row'
            original_values_list = list(hit['original_display_row'])  # Get the full original 10-column row as a list

            # Update 'Cuspal Link' column (index 8) and 'Remark' column (index 9)
            original_values_list[8] = hit['type']  # Update cuspal link details with the HIT type
            # Update Remark to indicate the HIT details.
            original_values_list[9] = f"HIT at {hit['time'].strftime('%H:%M:%S')} via {hit['planet']}"  # Update Remark

            # Insert the modified 10-column row into the treeview
            self.analysis_results_tree.insert("", "end", values=original_values_list)

        # Enable the next button in the sequence
        if hasattr(self, 'filter_pc_sign_star_button'):
            self.filter_pc_sign_star_button.config(state="normal")
        messagebox.showinfo("Analysis Complete",
                            f"Found {len(cuspal_hits)} precise event timing(s). You may now apply the final Sign/Star filter.")


    def _find_suitable_dasha_periods_recursively(self, start_utc, end_utc):
        """
        NEW RECURSIVE ENGINE: Finds suitable Dasha periods by traversing the Dasha tree.
        It checks each lord's classification and only proceeds down the sub-chain if the lord is Positive or Neutral.
        """
        self._log_debug("Starting new recursive Dasha search...")
        suitable_periods = []
        local_tz = pytz.timezone(self.timezone_combo.get())

        def parse_dasha_time(time_str):
            for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.datetime.strptime(time_str, fmt)
                except ValueError:
                    continue
            return None

        def recurse(parent_id, parent_lords):
            # Base case: If we have reached the Prana Dasha level, we have a full, valid chain.
            if len(parent_lords) == 5:
                # Get the time span of this Prana Dasha period
                values = self.dasa_tree.item(parent_id, 'values')
                start_dt_local = parse_dasha_time(values[1])
                end_dt_local = parse_dasha_time(values[2])

                # Convert to UTC to check against the analysis window
                start_dt_utc = local_tz.localize(start_dt_local).astimezone(pytz.utc)
                end_dt_utc = local_tz.localize(end_dt_local).astimezone(pytz.utc)

                # Add it to results if it overlaps with the user's selected time range
                if max(start_utc, start_dt_utc) < min(end_utc, end_dt_utc):
                    suitable_periods.append({
                        'dasha_lords': parent_lords,
                        'start_utc': start_dt_utc,
                        'end_utc': end_dt_utc
                    })
                return

            # Recursive step: Traverse children of the current Dasha lord
            for child_id in self.dasa_tree.get_children(parent_id):
                lord_text = self.dasa_tree.item(child_id, 'text')
                child_lord = lord_text.split(' ')[0]

                classification = self.planet_classifications.get(child_lord)

                # The core of the new logic: only proceed if the lord is not Negative
                if classification in ['Positive', 'Neutral']:
                    recurse(child_id, parent_lords + [child_lord])
                else:
                    self._log_debug(f"  -> Rejecting sub-chain for Negative lord: {parent_lords + [child_lord]}")
                    # If the lord is Negative, we simply do not recurse, effectively skipping its entire sub-chain.

        # Start the recursion from the top-level Mahadashas
        for md_id in self.dasa_tree.get_children(""):
            md_lord = self.dasa_tree.item(md_id, 'text').split(' ')[0]
            classification = self.planet_classifications.get(md_lord)
            if classification in ['Positive', 'Neutral']:
                recurse(md_id, [md_lord])
            else:
                self._log_debug(f"  -> Rejecting entire Mahadasha for Negative lord: {md_lord}")

        return suitable_periods

    def run_step1_dasha_analysis(self):
        """
        STEP 1: Resets the workflow, classifies all planets (now done by Promise button),
        finds all favorable Dasha periods using the recursive engine, and updates the UI.
        """
        self._log_debug("--- Running Analysis Step 1: Dasha (Recursive Logic) ---")

        # 1. Prerequisite check
        if not self.current_planetary_positions:
            messagebox.showerror("Prerequisites Missing", "Please generate a chart first.")
            return

        # Ensure planet classifications are available (should be from Promise button)
        if not self.planet_classifications:
            messagebox.showerror("Prerequisites Missing", "Please click 'Check Promise' first to classify planets.")
            return

        # 2. Clear old results and reset the state of all subsequent buttons
        self._update_analysis_results_tree_columns("detailed_full_analysis")
        self.suitable_dasha_spans = []
        self.dasha_transit_windows = []
        self.rp_sorted_results = []
        self.find_transit_button.config(state="disabled")
        self.sort_by_rp_button.config(state="disabled")
        self.rp_interlink_button.config(state="disabled")
        self.filter_pc_sign_star_button.config(state="disabled")

        # 3. Get cusps for current query (already handled by _on_event_type_select / _check_promise)
        original_pc_num = self._get_original_primary_cusp_from_ui()
        if original_pc_num is None: return
        pc_for_analysis = self._determine_primary_cusp_for_analysis(original_pc_num)
        # self._cache_static_planet_classifications(pc_for_analysis, original_pc_num) # REMOVE THIS LINE!

        # 4. Fallback Logic: If no Positive RPs, find strong significators and treat them as Positive
        #    This now relies on `self.planet_classifications` already being set by `_check_promise`.
        all_rps = {values[1] for item_id in self.rp_tree.get_children() if
                   (values := self.rp_tree.item(item_id, 'values'))}
        positive_rps_list = [p for p, c in self.planet_classifications.items() if c == 'Positive'] # Use existing classification

        if not positive_rps_list: # If after promise check, no positive RPs, then this fallback
            messagebox.showinfo("Fallback Rule Activated",
                                 "No Positive Ruling Planets found. Searching for strong significator planets to include in the analysis.")
            self._log_debug("--- No Positive RPs found. Activating fallback significator logic. ---")

            secondary_cusp_nums = self._get_selected_secondary_cusps()
            num_sc = len(secondary_cusp_nums)
            threshold = math.ceil(num_sc * 0.6) if num_sc > 0 else 0

            for planet_name in STELLAR_PLANETS:
                if self.planet_classifications.get(planet_name) == 'Positive':
                    continue

                # Ensure _get_planet_final_significators is called appropriately based on original_pc_num
                final_sigs = set(self._get_planet_final_significators(planet_name, original_pc_num, exclude_8_12_from_non_8_12_pc=False))
                if pc_for_analysis in final_sigs:
                    signified_sc_count = sum(1 for sc in secondary_cusp_nums if sc in final_sigs)
                    if num_sc == 0 or signified_sc_count >= threshold:
                        self._log_debug(
                            f"FALLBACK: {planet_name} now considered Positive. Signified {signified_sc_count}/{num_sc} SCs.")
                        self.planet_classifications[planet_name] = 'Positive' # Overwrite classification for fallback

        # 5. Update UI to show ALL Positive and Neutral planets based on final classification
        #    (This part remains, as it refreshes the labels for visibility)
        all_positive_planets = sorted([p for p, c in self.planet_classifications.items() if c == 'Positive'])
        all_neutral_planets = sorted([p for p, c in self.planet_classifications.items() if c == 'Neutral'])
        self.positive_planets_label.config(
            text=f"Positive Planets: {', '.join(all_positive_planets) if all_positive_planets else 'None'}")
        self.neutral_planets_label.config(
            text=f"Neutral Planets: {', '.join(all_neutral_planets) if all_neutral_planets else 'None'}")

        # 6. Find suitable dasha spans using the recursive engine
        local_tz = pytz.timezone(self.timezone_combo.get())
        start_utc, end_utc = self._get_analysis_time_range(local_tz)
        if start_utc is None: return
        self.suitable_dasha_spans = self._find_suitable_dasha_periods_recursively(start_utc, end_utc)

        # 7. Populate results and update UI
        if not self.suitable_dasha_spans:
            messagebox.showinfo("Step 1 Complete",
                                 "No suitable Dasha periods found where all lords are Positive or Neutral.")
            return

        self.suitable_dasha_spans.sort(key=lambda x: x['start_utc'])
        for span in self.suitable_dasha_spans:
            start_str = span['start_utc'].astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
            end_str = span['end_utc'].astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
            row_data = (*span['dasha_lords'], start_str, end_str, "Dasha Chain OK", "")
            self.analysis_results_tree.insert("", "end", values=row_data)

        self.find_transit_button.config(state="normal")
        self.sort_by_rp_button.config(state="normal")
        messagebox.showinfo("Step 1 Complete",
                            f"Found {len(self.suitable_dasha_spans)} suitable Dasha combinations. You may now proceed to Step 2.")

    def _find_suitable_dasha_combinations(self, start_utc, end_utc, local_tz):
        """
        (NEW LOGIC) Finds Dasha periods where all 5 lords (MD, AD, PD, SD, PrD)
        are classified as either 'Positive' or 'Neutral'.
        """
        self._log_debug("Finding Dasha combinations where all 5 lords are Positive/Neutral.")
        suitable_spans = []
        all_dasha_periods = self._get_dasha_periods_flat(start_utc, end_utc, local_tz)

        if not all_dasha_periods:
            self._log_debug("No dasha periods found in the given time range.")
            return []

        for period in all_dasha_periods:
            dasha_lords_list = [
                period['md_lord'],
                period['ad_lord'],
                period['pd_lord'],
                period['sd_lord'],
                period['prd_lord']
            ]

            # NEW CORE RULE: Check if all 5 lords are Positive or Neutral.
            # This check is now independent of Ruling Planet status.
            is_suitable = True
            for lord in dasha_lords_list:
                classification = self.planet_classifications.get(lord)
                if classification not in ['Positive', 'Neutral']:
                    is_suitable = False
                    self._log_debug(f"  -> FAIL: Dasha span rejected. Lord '{lord}' is '{classification}'.")
                    break

            if is_suitable:
                self._log_debug(f"  -> SUCCESS: Found suitable Dasha span. Lords {dasha_lords_list} are all P/N.")
                suitable_spans.append({
                    'dasha_lords': dasha_lords_list,
                    'start_utc': period['start_utc'],
                    'end_utc': period['end_utc']
                })

        self._log_debug(f"Found {len(suitable_spans)} suitable dasha spans based on the new P/N logic.")
        return suitable_spans

    def _run_transit_filtered_interlinks_analysis(self):  # RENAMED THIS METHOD
        self._log_debug("Running Transit Filtered Interlinks Analysis.")
        self._update_analysis_results_tree_columns("transit_filtered_interlinks")

        if not self.current_planetary_positions or not self.current_cuspal_positions or not self.stellar_significators_data:
            messagebox.showwarning("Chart Data Missing",
                                   "Please generate a chart first in the 'Chart Generation' tab and ensure stellar significators are calculated.")
            self._log_debug("ERROR: Chart data or stellar significators missing for transit filter analysis.")
            return

        # No longer dependent on cached_interlink_results here for the *initial* run
        # This method will find suitable dasha, then filter by transit, then interlink.

        original_primary_cusp_num = self._get_original_primary_cusp_from_ui()
        if original_primary_cusp_num is None: return

        primary_cusp_num_for_analysis = self._determine_primary_cusp_for_analysis(original_primary_cusp_num)

        # Ensure planet classifications are cached
        self._cache_static_planet_classifications(primary_cusp_num_for_analysis, original_primary_cusp_num)
        if not hasattr(self, 'planet_classifications') or not self.planet_classifications:
            messagebox.showerror("Internal Error", "Planet classifications not cached. Please generate chart first.")
            self._log_debug("ERROR: Planet classifications not cached for transit filter analysis.")
            return

        # Ensure RPs are calculated to create the ranked list
        if not self.rp_tree.get_children():
            messagebox.showinfo("Info",
                                "Please calculate Ruling Planets first on the 'Ruling Planet' tab for transit filtering.")
            return
        # Get ranked list of Ruling Planets from the RP tree
        ranked_rps = [self.rp_tree.item(item, 'values')[1] for item in self.rp_tree.get_children()]
        if not ranked_rps:
            messagebox.showerror("Error", "Could not retrieve ranked Ruling Planets.")
            return
        # Filter the ranked RP list to only include Positive/Neutral planets (for transit lords)
        qualified_rps_for_transits = [
            rp for rp in ranked_rps
            if self.planet_classifications.get(rp, "Negative") in ["Positive", "Neutral"]
        ]
        self._log_debug(f"Qualified (P/N) and Ranked RPs for Transits: {qualified_rps_for_transits}")
        if not qualified_rps_for_transits:
            messagebox.showinfo("Analysis Stop",
                                "No Ruling Planets were found to be Positive or Neutral for transit qualification.")
            return

        secondary_cusp_nums = self._get_selected_secondary_cusps()  # Get selected SCs

        timezone_str = self.timezone_combo.get()
        local_tz = pytz.timezone(timezone_str)
        city = self.city_combo.get()
        hsys_const = self._get_selected_hsys()
        horary_num_value = int(self.horary_entry.get()) if self.horary_entry.get().isdigit() and (
                1 <= int(self.horary_entry.get()) <= 2193) else None

        self.analysis_results_tree.delete(*self.analysis_results_tree.get_children())

        progress_window = tk.Toplevel(self.root)
        progress_window.title("Transit Filter Analysis Progress")
        progress_window.transient(self.root)
        progress_window.grab_set()
        progress_label = ttk.Label(progress_window, text="Searching for suitable Dasha periods...", wraplength=300)
        progress_label.pack(pady=10)
        progress_bar = ttk.Progressbar(progress_window, orient='horizontal', length=250, mode='determinate')
        progress_bar.pack(pady=5)
        progress_label_percent = ttk.Label(progress_window, text="0.0%")
        progress_label_percent.pack()
        progress_bar.start()
        self.root.update_idletasks()

        final_filtered_transit_interlinks = []

        # Step 1: Find suitable Dasha combinations (same as _run_combined_dasha_significator_analysis)
        # Use a reasonable time range for initial dasha search
        initial_analysis_start_utc, initial_analysis_end_utc = self._get_analysis_time_range(local_tz)
        if initial_analysis_start_utc is None:
            progress_window.destroy()
            return

        suitable_dasha_spans = self._find_suitable_dasha_combinations(
            initial_analysis_start_utc, initial_analysis_end_utc, local_tz, self.all_ruling_planets
            # Use all RPs for Dasha check
        )
        self._log_debug(f"Found {len(suitable_dasha_spans)} suitable Dasha spans.")

        if not suitable_dasha_spans:
            progress_window.destroy()
            messagebox.showinfo("No Suitable Dashas", "No Dasha periods met the positivity/neutrality criteria.")
            self.analysis_results_tree.insert("", "end", values=(
                f"House {primary_cusp_num_for_analysis}", "No suitable Dasha periods found.", "", "", "", "", "", ""
            ))
            return

        total_processing_seconds = sum(
            [(span['end_utc'] - span['start_utc']).total_seconds() for span in suitable_dasha_spans])
        processed_seconds = 0
        analysis_interval_seconds = 60  # Check every minute for transits for efficiency within Dasha spans

        progress_label.config(text="Analyzing Jupiter, Sun, Moon Transits within Dasha spans...")
        progress_bar['value'] = 0
        self.root.update_idletasks()

        for dasha_span_data in suitable_dasha_spans:
            current_dasha_start_utc = dasha_span_data['start_utc']
            current_dasha_end_utc = dasha_span_data['end_utc']
            dasha_lords = dasha_span_data['dasha_lords']  # MD,AD,PD,SD,PrD lords

            self._log_debug(
                f"  Processing Dasha span: {dasha_lords} from {current_dasha_start_utc} to {current_dasha_end_utc}")

            span_duration_seconds = (current_dasha_end_utc - current_dasha_start_utc).total_seconds()
            if span_duration_seconds <= 0:
                self._log_debug(f"  Skipping empty Dasha span: {span_duration_seconds}s")
                processed_seconds += span_duration_seconds  # Account for this in progress
                continue

            current_outer_transit_block_start_time = None
            last_jupiter_status = "N/A"
            last_sun_status = "N/A"
            last_moon_status = "N/A"
            last_cuspal_interlink_status = "N/A"

            # Iterate through the dasha span with a reasonable interval (e.g., 1 minute)
            for s_offset in range(0, int(span_duration_seconds) + 1, analysis_interval_seconds):
                current_time_point_utc = current_dasha_start_utc + datetime.timedelta(seconds=s_offset)
                if current_time_point_utc > current_dasha_end_utc:
                    current_time_point_utc = current_dasha_end_utc

                dynamic_planetary_positions, dynamic_cuspal_positions, _ = self._calculate_chart_data(
                    current_time_point_utc, city, hsys_const, horary_num_value
                )

                # --- 1. Jupiter Transit Check ---
                is_jupiter_favorable, jupiter_status_current = self._is_transit_favorable(
                    'Jupiter', dynamic_planetary_positions, primary_cusp_num_for_analysis, original_primary_cusp_num
                )

                # --- 2. Sun Transit Check ---
                is_sun_favorable, sun_status_current = self._is_transit_favorable(
                    'Sun', dynamic_planetary_positions, primary_cusp_num_for_analysis, original_primary_cusp_num
                )

                # --- 3. Moon Transit Check ---
                is_moon_favorable, moon_status_current = self._is_transit_favorable(
                    'Moon', dynamic_planetary_positions, primary_cusp_num_for_analysis, original_primary_cusp_num
                )

                # --- 4. Cuspal Interlink Check (Dynamic) ---
                is_cuspal_interlink_active, cuspal_interlink_details_current = self._is_interlink_active(
                    dynamic_planetary_positions, dynamic_cuspal_positions, primary_cusp_num_for_analysis,
                    secondary_cusp_nums
                )
                cuspal_interlink_status_str = cuspal_interlink_details_current.get('sc_connected_str',
                                                                                   "Link FAIL") if is_cuspal_interlink_active else "Link FAIL"

                # Check if ALL conditions are met for this time point
                all_transits_favorable_now = is_jupiter_favorable and is_sun_favorable and is_moon_favorable
                all_conditions_met_now = all_transits_favorable_now and is_cuspal_interlink_active

                self._log_debug(
                    f"    @{current_time_point_utc.strftime('%H:%M:%S')}: J:{is_jupiter_favorable}, S:{is_sun_favorable}, M:{is_moon_favorable}, CI:{is_cuspal_interlink_active} -> ALL:{all_conditions_met_now}")

                if all_conditions_met_now:
                    if current_outer_transit_block_start_time is None:
                        current_outer_transit_block_start_time = current_time_point_utc
                        last_jupiter_status = jupiter_status_current
                        last_sun_status = sun_status_current
                        last_moon_status = moon_status_current
                        last_cuspal_interlink_status = cuspal_interlink_status_str
                else:
                    if current_outer_transit_block_start_time is not None:
                        # End of a favorable block, record it
                        block_end_utc = current_time_point_utc - datetime.timedelta(seconds=analysis_interval_seconds)
                        if block_end_utc < current_outer_transit_block_start_time: block_end_utc = current_outer_transit_block_start_time  # Prevent negative duration

                        final_filtered_transit_interlinks.append(self._format_transit_interlink_result(
                            primary_cusp_str=f"H{primary_cusp_num_for_analysis}",
                            start_utc=current_outer_transit_block_start_time,
                            end_utc=block_end_utc,
                            local_tz=local_tz,
                            pc_sl_sl=cuspal_interlink_details_current.get('pc_sl_sl', 'N/A'),
                            pc_sl_subl=cuspal_interlink_details_current.get('pc_sl_subl', 'N/A'),
                            sc_connected_str=last_cuspal_interlink_status,
                            jupiter_status=last_jupiter_status,
                            sun_status=last_sun_status,
                            moon_status=last_moon_status,
                            dasha_lords={'md': dasha_lords[0], 'ad': dasha_lords[1], 'pd': dasha_lords[2],
                                         'sd': dasha_lords[3], 'prd': dasha_lords[4]}
                        ))
                        current_outer_transit_block_start_time = None

                processed_seconds += analysis_interval_seconds
                progress = (processed_seconds / total_processing_seconds) * 100 if total_processing_seconds > 0 else 100
                progress_bar['value'] = progress
                progress_label_percent.config(text=f"{progress:.1f}%")
                self.root.update_idletasks()

            # After iterating through the dasha span, if a block was active, add it
            if current_outer_transit_block_start_time is not None:
                final_filtered_transit_interlinks.append(self._format_transit_interlink_result(
                    primary_cusp_str=f"H{primary_cusp_num_for_analysis}",
                    start_utc=current_outer_transit_block_start_time,
                    end_utc=current_dasha_end_utc,  # End at the end of the dasha span
                    local_tz=local_tz,
                    pc_sl_sl=cuspal_interlink_details_current.get('pc_sl_sl', 'N/A'),
                    pc_sl_subl=cuspal_interlink_details_current.get('pc_sl_subl', 'N/A'),
                    sc_connected_str=last_cuspal_interlink_status,
                    jupiter_status=last_jupiter_status,
                    sun_status=last_sun_status,
                    moon_status=last_moon_status,
                    dasha_lords={'md': dasha_lords[0], 'ad': dasha_lords[1], 'pd': dasha_lords[2], 'sd': dasha_lords[3],
                                 'prd': dasha_lords[4]}
                ))

        progress_bar.stop()
        progress_window.destroy()

        for row_data in final_filtered_transit_interlinks:
            self.analysis_results_tree.insert("", "end", values=row_data)

        if not self.analysis_results_tree.get_children():
            self.analysis_results_tree.insert("", "end", values=(
                "", "", "", "", "", "No periods found meeting all Dasha, Transit, and Cuspal Interlink conditions.", "",
                "", "", "", ""
            ))
            self._log_debug("No transit filtered interlink periods found.")
        else:
            messagebox.showinfo("Analysis Complete",
                                f"Found {len(final_filtered_transit_interlinks)} periods meeting all conditions!")
        self._log_debug("Transit Filtered Interlinks Analysis complete.")


    def run_step2_transit_analysis(self):
        """
        STEP 2: Filters the found Dasha spans by checking for suitable transits.
        """
        self._log_debug("--- Running Analysis Step 2: Transits ---")
        if not self.suitable_dasha_spans:
            messagebox.showerror("Sequence Error", "Please run Step 1 to find Dasha combinations first.")
            return

        local_tz = pytz.timezone(self.timezone_combo.get())
        start_utc, end_utc = self._get_analysis_time_range(local_tz)
        if start_utc is None: return
        analysis_duration = end_utc - start_utc

        progress_info = self._setup_progress_window("Step 2: Finding Transits")

        self.dasha_transit_windows = self._find_transit_windows_in_spans(self.suitable_dasha_spans,
                                                                         progress_info, analysis_duration)
        if progress_info['window'].winfo_exists(): progress_info['window'].destroy()

        # CORRECTED: This line ensures the tree columns are set to the expected format before populating.
        self._update_analysis_results_tree_columns("detailed_full_analysis")

        if not self.dasha_transit_windows:
            messagebox.showinfo("Step 2 Complete", "No suitable transit windows were found within the Dasha periods.")
            return

        for window in self.dasha_transit_windows:
            start_str = window['start_utc'].astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
            end_str = window['end_utc'].astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')

            _, transit_details = self._check_transit_suitability_new(window['start_utc'], analysis_duration)

            transit_str = f"Jup:{transit_details.get('Jupiter', 'N/A')} | Sat:{transit_details.get('Saturn', 'N/A')} | Sun:{transit_details.get('Sun', 'N/A')} | Moon:{transit_details.get('Moon', 'N/A')}"
            row_data = (*window['dasha_lords'], start_str, end_str, transit_str, "Transit OK")
            self.analysis_results_tree.insert("", "end", values=row_data)

        messagebox.showinfo("Step 2 Complete",
                            f"Found {len(self.dasha_transit_windows)} windows with suitable transits. You may now proceed to the next step.")

    def _find_transit_windows_in_spans(self, dasha_spans, progress_info, analysis_duration):
        """
        (CORRECTED) Finds favorable transit windows within Dasha spans.
        This version is updated to correctly call the new ETR progress bar.
        """
        transit_windows = []

        # --- Setup for ETR Calculation ---
        total_duration_days = sum([(span['end_utc'] - span['start_utc']).days for span in dasha_spans])
        total_steps = total_duration_days if total_duration_days > 0 else 1
        steps_done = 0
        start_time = datetime.datetime.now()

        time_increment = datetime.timedelta(days=1)

        for dasha_span in dasha_spans:
            time_pointer = dasha_span['start_utc']
            current_block_start = None

            while time_pointer < dasha_span['end_utc']:
                # Call the new update function with all required arguments
                self._update_progress(progress_info, steps_done, total_steps, start_time,
                                      "Step 2/3: Finding suitable transit days...")

                is_transit_ok, _ = self._check_transit_suitability_new(time_pointer, analysis_duration)

                if is_transit_ok and current_block_start is None:
                    current_block_start = time_pointer
                elif not is_transit_ok and current_block_start is not None:
                    transit_windows.append({'start_utc': current_block_start, 'end_utc': time_pointer,
                                            'dasha_lords': dasha_span['dasha_lords']})
                    current_block_start = None

                time_pointer += time_increment
                steps_done += 1

            if current_block_start is not None:
                transit_windows.append({'start_utc': current_block_start, 'end_utc': dasha_span['end_utc'],
                                        'dasha_lords': dasha_span['dasha_lords']})

        self._log_debug(f"Found {len(transit_windows)} suitable Dasha+Transit day(s).")
        return transit_windows

    def _check_transit_suitability_new(self, time_utc, analysis_duration=None):
        """
        (NEW LOGIC) DYNAMIC TRANSIT LOGIC: A transit is favorable if AT LEAST ONE of its key
        lords is classified as Positive or Neutral.
        """
        if analysis_duration is None:
            self._log_debug("WARNING: 'analysis_duration' was not provided. Defaulting to short-term transit check.")
            analysis_duration = datetime.timedelta(days=1)

        self._log_debug(f"--- Running DYNAMIC Transit Check (OR logic) for span {analysis_duration.days} days ---")
        city = self.city_combo.get()
        hsys_const = self._get_selected_hsys()
        horary_num = int(
            self.horary_entry.get()) if self.horary_entry.get() and self.chart_type_var.get() == "Horary" else None

        dyn_planets, _, _ = self._calculate_chart_data(time_utc, city, hsys_const, horary_num)

        all_conditions_met = True
        details = {}

        def get_status_char(planet_name):
            classif = self.planet_classifications.get(planet_name, 'X')
            return f"({classif[0]})" if classif else "(U)"

        # --- Sun Check (New OR Logic) ---
        sun_data = dyn_planets.get('Sun')
        if sun_data:
            sun_sl, sun_subl = sun_data[3], sun_data[4]
            if self.planet_classifications.get(sun_sl) in ['Positive', 'Neutral'] or \
               self.planet_classifications.get(sun_subl) in ['Positive', 'Neutral']:
                details['Sun'] = f"OK (SL:{sun_sl}{get_status_char(sun_sl)}, SubL:{sun_subl}{get_status_char(sun_subl)})"
            else:
                all_conditions_met = False; details['Sun'] = "FAIL"
        else:
            all_conditions_met = False; details['Sun'] = "FAIL (N/A)"

        # --- Moon Check (New OR Logic) ---
        moon_data = dyn_planets.get('Moon')
        if moon_data:
            moon_sl, moon_subl, moon_ssl = moon_data[3], moon_data[4], moon_data[5]
            if self.planet_classifications.get(moon_sl) in ['Positive', 'Neutral'] or \
               self.planet_classifications.get(moon_subl) in ['Positive', 'Neutral'] or \
               self.planet_classifications.get(moon_ssl) in ['Positive', 'Neutral']:
                details['Moon'] = f"OK (SL:{moon_sl}{get_status_char(moon_sl)}, SubL:{moon_subl}{get_status_char(moon_subl)}, SSL:{moon_ssl}{get_status_char(moon_ssl)})"
            else:
                all_conditions_met = False; details['Moon'] = "FAIL"
        else:
            all_conditions_met = False; details['Moon'] = "FAIL (N/A)"

        # --- Jupiter Check (New OR Logic, conditional: > 90 days) ---
        if analysis_duration.days > 90:
            jupiter_data = dyn_planets.get('Jupiter')
            if jupiter_data:
                jup_sl, jup_subl = jupiter_data[3], jupiter_data[4]
                if self.planet_classifications.get(jup_sl) in ['Positive', 'Neutral'] or \
                   self.planet_classifications.get(jup_subl) in ['Positive', 'Neutral']:
                    details['Jupiter'] = f"OK (SL:{jup_sl}{get_status_char(jup_sl)}, SubL:{jup_subl}{get_status_char(jup_subl)})"
                else:
                    all_conditions_met = False; details['Jupiter'] = "FAIL"
            else:
                all_conditions_met = False; details['Jupiter'] = "FAIL (N/A)"
        else:
            details['Jupiter'] = "Not Checked"

        # --- Saturn Check (New OR Logic, conditional: > 1.5 years / 547 days) ---
        if analysis_duration.days > 547:
            saturn_data = dyn_planets.get('Saturn')
            if saturn_data:
                saturn_sl, saturn_subl = saturn_data[3], saturn_data[4]
                if self.planet_classifications.get(saturn_sl) in ['Positive', 'Neutral'] or \
                   self.planet_classifications.get(saturn_subl) in ['Positive', 'Neutral']:
                    details['Saturn'] = f"OK (SL:{saturn_sl}{get_status_char(saturn_sl)}, SubL:{saturn_subl}{get_status_char(saturn_subl)})"
                else:
                    all_conditions_met = False; details['Saturn'] = "FAIL"
            else:
                all_conditions_met = False; details['Saturn'] = "FAIL (N/A)"
        else:
            details['Saturn'] = "Not Checked"

        return all_conditions_met, details






    def run_step3_interlink_analysis(self):
        """STEP 3: Performs the final, high-frequency cuspal interlink scan."""
        self._log_debug("--- Running Analysis Step 3: Cuspal Interlinks ---")
        if not self.dasha_transit_windows:
            messagebox.showerror("Sequence Error", "Please run Step 2 to find transit windows first.")
            return

        # Re-fetch qualified planets and cusps
        original_pc_num = self._get_original_primary_cusp_from_ui()
        pc_for_analysis = self._determine_primary_cusp_for_analysis(original_pc_num)
        secondary_cusp_nums = self._get_selected_secondary_cusps()
        strong_rp_strengths = {"Strongest of Strongest", "Strongest", "Second Strong"}
        self._cache_static_planet_classifications(pc_for_analysis, original_pc_num)
        qualified_planets = {
            rp_name for rp_strength, rp_name, _ in
            [self.rp_tree.item(item, 'values') for item in self.rp_tree.get_children()]
            if
            rp_strength in strong_rp_strengths and self.planet_classifications.get(rp_name, "Negative") in ["Positive",
                                                                                                            "Neutral"]
        }
        local_tz = pytz.timezone(self.timezone_combo.get())
        start_utc, end_utc = self._get_analysis_time_range(local_tz)
        analysis_duration = end_utc - start_utc

        progress_info = self._setup_progress_window("Step 3: Finding Interlinks")
        final_hits = self._perform_cuspal_interlink_scan(self.dasha_transit_windows, qualified_planets, pc_for_analysis,
                                                         secondary_cusp_nums, progress_info)
        progress_info['window'].destroy()

        self.analysis_results_tree.delete(*self.analysis_results_tree.get_children())
        if not final_hits:
            messagebox.showinfo("Step 3 Complete",
                                "No precise cuspal interlinks were found within the suitable Dasha/Transit windows.")
            return

        for hit in final_hits:
            hit_time = hit['time']
            _, transit_details = self._check_transit_suitability_new(hit_time, qualified_planets, analysis_duration)
            transit_str = f"Jup:{transit_details.get('Jupiter', 'N/A')} | Sat:{transit_details.get('Saturn', 'N/A')} | Sun:{transit_details.get('Sun', 'N/A')} | Moon:{transit_details.get('Moon', 'N/A')}"
            cuspal_str = f"Hit via {hit['planet']} ({hit['type']})"

            # Find the window this hit belongs to for start/end times
            start_str, end_str = "", ""
            for window in self.dasha_transit_windows:
                if window['start_utc'] <= hit_time < window['end_utc']:
                    start_str = hit_time.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
                    end_str = "--> " + hit_time.astimezone(local_tz).strftime('%H:%M:%S')  # Indicate precise hit
                    break

            row_data = (*hit['dasha_lords'], start_str, end_str, transit_str, cuspal_str)
            self.analysis_results_tree.insert("", "end", values=row_data)

        messagebox.showinfo("Step 3 Complete", f"Found {len(final_hits)} precise event timings.")


    def _get_selected_secondary_cusps(self):
        """
        Parses the secondary cusp listbox, dynamically resolving 'Marak' and 'Badhak'.
        Returns a set of unique cusp numbers, excluding the primary cusp if it was selected.
        """
        if not self.current_cuspal_positions:
            messagebox.showerror("Chart Error", "Please generate a chart before selecting secondary cusps.")
            return set()

        selected_indices = self.secondary_cusp_listbox.curselection()
        if not selected_indices:
            return set()

        secondary_cusp_nums = set()
        asc_sign = self.current_cuspal_positions[1][1]

        movable_signs = {"Aries", "Cancer", "Libra", "Capricorn"}
        dual_signs = {"Gemini", "Virgo", "Sagittarius", "Pisces"}

        for i in selected_indices:
            selection_text = self.secondary_cusp_listbox.get(i)

            if selection_text.startswith("House"):
                secondary_cusp_nums.add(int(selection_text.split()[-1]))

            elif selection_text == "Marak":
                secondary_cusp_nums.update([2, 7])
                self._log_debug("Resolved 'Marak' to cusps 2, 7.")

            elif selection_text == "Badhak":
                if asc_sign in movable_signs:
                    secondary_cusp_nums.update([2, 7])  # Per user's special rule
                    self._log_debug(f"Resolved 'Badhak' for movable sign '{asc_sign}' to cusps 2, 7.")
                elif asc_sign in dual_signs:
                    secondary_cusp_nums.add(7)
                    self._log_debug(f"Resolved 'Badhak' for dual sign '{asc_sign}' to cusp 7.")
                # No rule provided for fixed signs, so no action is taken.

        # --- NEW LOGIC: Exclude Primary Cusp from Secondary Cusps ---
        try:
            primary_cusp_num = self._get_original_primary_cusp_from_ui()
            if primary_cusp_num is not None and primary_cusp_num in secondary_cusp_nums:
                secondary_cusp_nums.discard(primary_cusp_num) # Remove it if it exists
                self._log_debug(f"Primary Cusp {primary_cusp_num} was in secondary cusps; excluded.")
        except Exception as e:
            self._log_debug(f"Error checking/excluding primary cusp from secondary: {e}")
            # Do not raise error, just log and continue.

        return secondary_cusp_nums

    def _calculate_positivity_score(self, item_values):
        """Calculates a positivity score for a given result row."""
        # The values tuple from a treeview row
        dasha_lords = item_values[0:5]
        jup_status = item_values[-3]
        sun_status = item_values[-2]
        moon_status = item_values[-1]

        dasha_score = 0
        for lord in dasha_lords:
            classification = self.planet_classifications.get(lord)
            if classification == 'Positive':
                dasha_score += 2
            elif classification == 'Neutral':
                dasha_score += 1

        transit_score = 0
        # Parse status strings like "Jup SL:P/SubL:N" and assign points
        for char in jup_status + sun_status + moon_status:
            if char == 'P':
                transit_score += 2
            elif char == 'N':
                transit_score += 1

        # Heavily weight the dasha score to prioritize it
        return (dasha_score * 10) + transit_score

    def _sort_results_by_best(self):
        """
        Sorts results by a positivity score and then categorizes them based on RP strength and
        Moon's Sub-Sub Lord positivity.
        Results where Moon's Sookshma Lord is not Positive are explicitly REJECTED.
        """
        self._log_debug("Running enhanced 'Sort by Best' with Moon's SSL positivity filter.")

        if not self.analysis_results_tree.get_children():
            messagebox.showinfo("Info", "Please run an analysis first to generate results.")
            return
        if not self.rp_tree.get_children():
            messagebox.showinfo("Info",
                                "Please calculate Ruling Planets first on the 'Ruling Planet' tab for this feature.")
            return

        # 1. Get RP strengths into a dictionary. The keys of this dict are all the Ruling Planets.
        rp_strengths = {self.rp_tree.item(item_id, 'values')[1]: self.rp_tree.item(item_id, 'values')[0]
                        for item_id in self.rp_tree.get_children() if len(self.rp_tree.item(item_id, 'values')) > 1}
        self._log_debug(f"All Ruling Planets found: {list(rp_strengths.keys())}")

        # 2. Define strength categories
        strong_categories = {"Strongest of Strongest", "Strongest", "Second Strong"}
        weak_category = "Weak"

        # 3. Get all items and their scores from the results tree
        all_items_with_scores = []
        for item_id in self.analysis_results_tree.get_children():
            values = self.analysis_results_tree.item(item_id, 'values')
            # Assuming 'values' here directly corresponds to the columns of "transit_filtered_interlinks"
            # MD, AD, PD, SD, PrD, Time Interval, Jupiter, Sun, Moon, Cuspal Interlink
            if len(values) < 10: continue  # Ensure it's a full result row with transit data
            score = self._calculate_positivity_score(values)
            all_items_with_scores.append((score, values))

        # 4. Categorize items based on the new rules
        strong_results = []
        weak_results = []
        other_results = []
        rejected_count = 0

        for score, values in all_items_with_scores:
            prana_lord = values[4]  # Prana Dasha Lord is at index 4 (PrD column)
            moon_status_str = values[9]  # Moon Transit status is at index 9 (Moon column)

            # --- NEW REJECTION RULE: Moon's Sookshma (Sub-Sub Lord) must be Positive ---
            is_moon_ssl_positive = ("SSL:P" in moon_status_str)  # Check if the string explicitly contains "SSL:P"

            if not is_moon_ssl_positive:
                rejected_count += 1
                self._log_debug(
                    f"Rejected: Moon's SSL is not Positive for period starting {values[5]}. Moon status: {moon_status_str}")
                continue  # Reject this result entirely and move to the next one

            # --- Existing Logic for accepted results (Moon's SSL is Positive) ---
            # These are from the *interlink* status, not transit, so need to adjust index.
            # PC SL SL and PC SL SubL are NOT in the `transit_filtered_interlinks` columns by default.
            # They are captured in `cuspal_interlink_details_current` in `_run_transit_filtered_interlinks_analysis`.
            # For this rule, we need to adapt based on what's available in 'values' or fetch it differently.
            # Given the `transit_filtered_interlinks` output, the `cuspal_interlink_status_str`
            # (which holds 'PC SL SL', 'PC SL SubL' if available, as 'H#: Type' strings) is at values[9] (Cuspal Interlink column).
            # This is complex to parse back.
            # For simplicity for this *sort* logic, let's just use Prana Lord's strength.
            # If `_sort_results_by_best` needs specific PC SL SL/SubL from dynamic interlink results,
            # that data needs to be explicitly passed as part of the `values` tuple in `_format_transit_interlink_result`.

            # Original sort logic used `cuspal_star_lord = values[7]` which was 'Primary Cusp SL Star Lord'.
            # This column is NOT in the new "transit_filtered_interlinks" view.
            # Assuming the intent is still to categorize based on Prana Lord's strength.

            prana_lord_strength = rp_strengths.get(prana_lord)

            # If Prana Lord's strength itself is not found (e.g., it's not an RP at all),
            # it should fall into 'other_results' or 'weak_results' if that applies.
            # But the user's rule implies it must be an RP (implicitly P/N).
            # If not in rp_strengths, it's not strong/weak category

            if prana_lord_strength is None:  # Not an RP at all. This shouldn't happen if `_find_suitable_dasha_combinations` filtered by all RPs.
                # However, if some RP rules mean it's an RP but not in strong/weak categories, it falls to 'other'
                other_results.append((score, values))
            elif prana_lord_strength in strong_categories:
                strong_results.append((score, values))
            elif prana_lord_strength == weak_category:
                weak_results.append((score, values))
            else:  # E.g. "Derived" or "Other Base RP" or if 'Weak' isn't explicitly defined as a category in rp_strengths.
                other_results.append((score, values))

        # 5. Sort each list by their original positivity score (descending)
        strong_results.sort(key=lambda x: x[0], reverse=True)
        other_results.sort(key=lambda x: x[0], reverse=True)
        weak_results.sort(key=lambda x: x[0], reverse=True)

        # 6. Repopulate the treeview in the correct order with highlighting
        self.analysis_results_tree.delete(*self.analysis_results_tree.get_children())

        # Insert strong results first
        for i, (score, values) in enumerate(strong_results):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.analysis_results_tree.insert("", "end", values=values, tags=(tag,))

        # Insert other results next
        for i, (score, values) in enumerate(other_results):
            # Maintain alternating row color
            # The offset ensures continuous alternating color, even with removed items.
            tag = 'evenrow' if (i + len(strong_results)) % 2 == 0 else 'oddrow'
            self.analysis_results_tree.insert("", "end", values=values, tags=(tag,))

        # Insert weak results at the bottom with a red highlight
        for i, (score, values) in enumerate(weak_results):
            # The 'weak_rp' tag applies the red highlight
            self.analysis_results_tree.insert("", "end", values=values, tags=('weak_rp',))

        # 7. Show a summary message
        messagebox.showinfo("Sort Complete",
                            "Results have been sorted by strength.\n\n"
                            f"Strong Results: {len(strong_results)}\n"
                            f"Other Results: {len(other_results)}\n"
                            f"Weak Results (at bottom): {len(weak_results)}\n\n"
                            f"Rejected (Moon SSL not Positive): {rejected_count}")
        self._log_debug("Sort by Best analysis complete.")

    def _get_planet_cuspal_connections(self, planet_name, planets_with_ps):
        """
        NEW HELPER: Gets the set of cusps a planet is directly connected to.
        A planet is 'connected' to a cusp if:
        1. It is one of the four lords (Sign, Star, Sub, SSL) of that cusp.
        2. It has Positional Status (PS) and is located by degree in that cusp.
        This function does NOT check the planet's star lord. It checks the planet itself.
        """
        connected_cusps = set()
        if not planet_name or planet_name not in self.current_planetary_positions:
            return connected_cusps

        # Check direct lordships
        for cusp_num, cusp_data in self.current_cuspal_positions.items():
            # Cusp lords are at indices 2, 3, 4, 5
            if planet_name in cusp_data[2:]:
                connected_cusps.add(cusp_num)

        # Check positional placement if the planet has Positional Status
        if planet_name in planets_with_ps:
            planet_lon = self.current_planetary_positions[planet_name][0]
            house_of_position = self._get_house_of_degree(planet_lon, self.current_cuspal_positions)
            if house_of_position:
                connected_cusps.add(house_of_position)

        return connected_cusps

    def _check_promise(self):
        """
        Checks the promise of the Ascendant and Primary Cusp based on the new 2025 rules.
        """
        self._log_debug("--- Running New Promise Check (2025 Rules) ---")
        self.asc_promise_label.config(text="Asc:", foreground="gray")
        self.pcusp_promise_label.config(text="Pcusp:", foreground="gray")

        # 1. Prerequisite and Input Validation
        if not self.current_planetary_positions or not self.current_cuspal_positions:
            messagebox.showwarning("Data Missing", "Please generate a chart first.")
            return

        try:
            primary_cusp_num = int(self.primary_cusp_combo.get().split()[-1])
            secondary_cusp_nums = self._get_selected_secondary_cusps()
            if not secondary_cusp_nums:
                messagebox.showerror("Input Error", "Please select at least one Secondary Cusp.")
                return
        except (ValueError, IndexError):
            messagebox.showerror("Input Error", "Invalid cusp selection.")
            return

        # Calculate planets with Positional Status once for efficiency
        planets_with_ps = self._calculate_positional_status(self.current_planetary_positions,
                                                            self.current_cuspal_positions)

        # 2. Ascendant Promise Check
        asc_promise_met = False
        asc_ssl_name = self.current_cuspal_positions.get(1, [None] * 6)[5]

        if asc_ssl_name and asc_ssl_name in self.current_planetary_positions:
            asc_ssl_data = self.current_planetary_positions[asc_ssl_name]
            asc_ssl_star_lord = asc_ssl_data[3]
            asc_ssl_sub_lord = asc_ssl_data[4]

            # Get connections for the star and sub lords
            star_lord_connections = self._get_planet_cuspal_connections(asc_ssl_star_lord, planets_with_ps)
            sub_lord_connections = self._get_planet_cuspal_connections(asc_ssl_sub_lord, planets_with_ps)

            # Condition A1: Star/Sub lord swap logic
            path1_success = (primary_cusp_num in star_lord_connections and secondary_cusp_nums.issubset(
                sub_lord_connections))
            path2_success = (secondary_cusp_nums.issubset(
                star_lord_connections) and primary_cusp_num in sub_lord_connections)

            if path1_success or path2_success:
                asc_promise_met = True
                self._log_debug(f"Ascendant Promise: MET via Star/Sub Lord connections of SSL {asc_ssl_name}.")

            # Condition A2: Positional Status logic
            if not asc_promise_met and asc_ssl_name in planets_with_ps:
                pcusp_lords = self.current_cuspal_positions.get(primary_cusp_num, [None] * 6)[2:]
                if asc_ssl_name in pcusp_lords:
                    asc_promise_met = True
                    self._log_debug(f"Ascendant Promise: MET via Positional Status of SSL {asc_ssl_name}.")

        self.asc_promise_label.config(text="Ascendant", foreground="green" if asc_promise_met else "red")

        # 3. Primary Cusp Promise Check
        pcusp_promise_met = False
        pcusp_ssl_name = self.current_cuspal_positions.get(primary_cusp_num, [None] * 6)[5]

        if pcusp_ssl_name and pcusp_ssl_name in self.current_planetary_positions:
            pcusp_ssl_data = self.current_planetary_positions[pcusp_ssl_name]
            pcusp_ssl_star_lord = pcusp_ssl_data[3]
            pcusp_ssl_sub_lord = pcusp_ssl_data[4]

            # Condition B1: Main check
            # Check if PC SSL's star lord signifies all secondary cusps
            pc_ssl_star_lord_connections = self._get_planet_cuspal_connections(pcusp_ssl_star_lord, planets_with_ps)
            star_lord_fulfills_scs = secondary_cusp_nums.issubset(pc_ssl_star_lord_connections)

            # Check if PC SSL's sub lord negates by showing PC-1
            negating_cusp = primary_cusp_num - 1 if primary_cusp_num > 1 else 12
            sub_lord_connections = self._get_planet_cuspal_connections(pcusp_ssl_sub_lord, planets_with_ps)
            sub_lord_negates = negating_cusp in sub_lord_connections

            if star_lord_fulfills_scs and not sub_lord_negates:
                pcusp_promise_met = True
                self._log_debug(f"P.Cusp Promise: MET via main rule for SSL {pcusp_ssl_name}.")

            # Condition B2: Positional Status logic
            if not pcusp_promise_met and pcusp_ssl_name in planets_with_ps:
                pcusp_lords = self.current_cuspal_positions.get(primary_cusp_num, [None] * 6)[2:]
                if pcusp_ssl_name in pcusp_lords:
                    pcusp_promise_met = True
                    self._log_debug(f"P.Cusp Promise: MET via Positional Status of SSL {pcusp_ssl_name}.")

        self.pcusp_promise_label.config(text="Pcusp", foreground="green" if pcusp_promise_met else "red")

    def _update_analysis_results_tree_columns(self, analysis_type):
        """Dynamically updates the columns and headings of the analysis_results_tree."""
        for item in self.analysis_results_tree.get_children():
            self.analysis_results_tree.delete(item)

        # Configure the tree to show headings, not the '#0' column
        self.analysis_results_tree.config(columns=[], displaycolumns=[])
        self.analysis_results_tree["show"] = "headings"
        self.analysis_results_tree.heading("#0", text="")
        self.analysis_results_tree.column("#0", width=0, stretch=False)

        if analysis_type == "interlink":
            columns = ("Primary Cusp", "Time Interval", "Primary Cusp SL Star Lord",
                       "Primary Cusp SL Sub Lord", "Secondary Cusps Connected")
            self.analysis_results_tree["columns"] = columns
            self.analysis_results_tree["displaycolumns"] = columns
            self.analysis_results_tree.heading("Primary Cusp", text="Primary Cusp")
            self.analysis_results_tree.heading("Time Interval", text="Time Interval (Local Time)")
            self.analysis_results_tree.heading("Primary Cusp SL Star Lord", text="Primary Cusp SL Star Lord")
            self.analysis_results_tree.heading("Primary Cusp SL Sub Lord", text="Primary Cusp SL Sub Lord")
            self.analysis_results_tree.heading("Secondary Cusps Connected",
                                               text="Secondary Cusps Connected (House: Connection Type)")
            self.analysis_results_tree.column("Primary Cusp", width=100, anchor='center')
            self.analysis_results_tree.column("Time Interval", width=250, anchor='center')
            self.analysis_results_tree.column("Primary Cusp SL Star Lord", width=150, anchor='center')
            self.analysis_results_tree.column("Primary Cusp SL Sub Lord", width=150, anchor='center')
            self.analysis_results_tree.column("Secondary Cusps Connected", width=400, anchor='w')

        elif analysis_type == "dasha_classification":
            columns = ("MD", "AD", "PD", "SD", "PrD", "Type", "Start Time", "End Time", "Details")
            self.analysis_results_tree["columns"] = columns
            self.analysis_results_tree["displaycolumns"] = columns
            self.analysis_results_tree.heading("MD", text="MD Lord")
            self.analysis_results_tree.heading("AD", text="AD Lord")
            self.analysis_results_tree.heading("PD", text="PD Lord")
            self.analysis_results_tree.heading("SD", text="SD Lord")
            self.analysis_results_tree.heading("PrD", text="PrD Lord")
            self.analysis_results_tree.heading("Type", text="Overall Type")
            self.analysis_results_tree.heading("Start Time", text="Start Time (Local)")
            self.analysis_results_tree.heading("End Time", text="End Time (Local)")
            self.analysis_results_tree.heading("Details", text="Classification Details")
            for col in ["MD", "AD", "PD", "SD", "PrD"]:
                self.analysis_results_tree.column(col, width=60, anchor='center')
            self.analysis_results_tree.column("Type", width=90, anchor='center')
            self.analysis_results_tree.column("Start Time", width=160, anchor='center')
            self.analysis_results_tree.column("End Time", width=160, anchor='center')
            self.analysis_results_tree.column("Details", width=300, anchor='w')

        elif analysis_type == "combined_dasha_significators":
            columns = ("MD", "AD", "PD", "SD", "PrD", "Fruitful?", "Signified PC", "Signified SCs", "Start Time",
                       "End Time")
            self.analysis_results_tree["columns"] = columns
            self.analysis_results_tree["displaycolumns"] = columns
            self.analysis_results_tree.heading("MD", text="MD Lord")
            self.analysis_results_tree.heading("AD", text="AD Lord")
            self.analysis_results_tree.heading("PD", text="PD Lord")
            self.analysis_results_tree.heading("SD", text="SD Lord")
            self.analysis_results_tree.heading("PrD", text="PrD Lord")
            self.analysis_results_tree.heading("Fruitful?", text="Fruitful?")
            self.analysis_results_tree.heading("Signified PC", text="Signified PC?")
            self.analysis_results_tree.heading("Signified SCs", text="Signified SCs")
            self.analysis_results_tree.heading("Start Time", text="Start Time (Local)")
            self.analysis_results_tree.heading("End Time", text="End Time (Local)")
            for col in ["MD", "AD", "PD", "SD", "PrD"]:
                self.analysis_results_tree.column(col, width=50, anchor='center')
            self.analysis_results_tree.column("Fruitful?", width=80, anchor='center')
            self.analysis_results_tree.column("Signified PC", width=100, anchor='center')
            self.analysis_results_tree.column("Signified SCs", width=150, anchor='w')
            self.analysis_results_tree.column("Start Time", width=160, anchor='center')
            self.analysis_results_tree.column("End Time", width=160, anchor='center')

        elif analysis_type == "jupiter_transit":
            columns = ("Primary Cusp", "Time Interval", "Jupiter SL Type", "Jupiter SubL Signifies PC", "Jupiter SL",
                       "Jupiter SubL")
            self.analysis_results_tree["columns"] = columns
            self.analysis_results_tree["displaycolumns"] = columns
            self.analysis_results_tree.heading("Primary Cusp", text="Primary Cusp")
            self.analysis_results_tree.heading("Time Interval", text="Time Interval (Local Time)")
            self.analysis_results_tree.heading("Jupiter SL Type", text="Jupiter SL Type (P/N)")
            self.analysis_results_tree.heading("Jupiter SubL Signifies PC", text="Jupiter SubL Signifies PC")
            self.analysis_results_tree.heading("Jupiter SL", text="Jupiter Star Lord")
            self.analysis_results_tree.heading("Jupiter SubL", text="Jupiter Sub Lord")
            self.analysis_results_tree.column("Primary Cusp", width=100, anchor='center')
            self.analysis_results_tree.column("Time Interval", width=250, anchor='center')
            self.analysis_results_tree.column("Jupiter SL Type", width=150, anchor='center')
            self.analysis_results_tree.column("Jupiter SubL Signifies PC", width=180, anchor='center')
            self.analysis_results_tree.column("Jupiter SL", width=120, anchor='center')
            self.analysis_results_tree.column("Jupiter SubL", width=120, anchor='center')

        elif analysis_type == "transit_filtered_interlinks":
            # THIS BLOCK IS NOW CORRECTLY INDENTED
            columns = ("MD", "AD", "PD", "SD", "PrD", "Time Interval", "Jupiter", "Saturn", "Sun", "Moon",
                       "Cuspal Interlink")
            self.analysis_results_tree["columns"] = columns
            self.analysis_results_tree["displaycolumns"] = columns

            # Set headings
            self.analysis_results_tree.heading("MD", text="MD")
            self.analysis_results_tree.heading("AD", text="AD")
            self.analysis_results_tree.heading("PD", text="PD")
            self.analysis_results_tree.heading("SD", text="SD")
            self.analysis_results_tree.heading("PrD", text="PrD")
            self.analysis_results_tree.heading("Time Interval", text="Event Time (Local)")
            self.analysis_results_tree.heading("Jupiter", text="Jupiter Transit")
            self.analysis_results_tree.heading("Saturn", text="Saturn Transit")
            self.analysis_results_tree.heading("Sun", text="Sun Transit")
            self.analysis_results_tree.heading("Moon", text="Moon Transit")
            self.analysis_results_tree.heading("Cuspal Interlink", text="Cuspal Interlink Status")

            # Set column widths
            for col in ["MD", "AD", "PD", "SD", "PrD"]:
                self.analysis_results_tree.column(col, width=60, anchor='center')
            self.analysis_results_tree.column("Time Interval", width=250, anchor='center')
            self.analysis_results_tree.column("Jupiter", width=120, anchor='w')
            self.analysis_results_tree.column("Saturn", width=120, anchor='w')
            self.analysis_results_tree.column("Sun", width=120, anchor='w')
            self.analysis_results_tree.column("Moon", width=150, anchor='w')
            self.analysis_results_tree.column("Cuspal Interlink", width=180, anchor='w')
    def _create_significators_tab(self):
        significators_frame = ttk.Frame(self.notebook)
        self.notebook.add(significators_frame, text="Significators")

        self.sig_text = tk.Text(significators_frame, height=30, width=100)
        self.sig_text.pack(padx=10, pady=10, fill='both', expand=True)

    def _create_stellar_status_tab(self):
        stellar_frame = ttk.Frame(self.notebook)
        self.notebook.add(stellar_frame, text="Stellar Status Significators")

        stellar_frame.grid_columnconfigure(0, weight=1)
        stellar_frame.grid_rowconfigure(0, weight=1)

        output_frame = ttk.LabelFrame(stellar_frame, text="Planetary Significators Results")
        output_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        self.stellar_significators_tree = ttk.Treeview(output_frame,
                                                       columns=("Planet", "Star Significators", "Sub Significators",
                                                                "Final Significators"),
                                                       show="headings")
        self.stellar_significators_tree.heading("Planet", text="Planet")
        self.stellar_significators_tree.heading("Star Significators", text="Star Significators (Cusps)")
        self.stellar_significators_tree.heading("Sub Significators", text="Sub Significators (Cusps)")
        self.stellar_significators_tree.heading("Final Significators", text="Final Significators (Cusps)")

        self.stellar_significators_tree.column("Planet", width=100, anchor='center')
        self.stellar_significators_tree.column("Star Significators", width=200, anchor='w')
        self.stellar_significators_tree.column("Sub Significators", width=200, anchor='w')
        self.stellar_significators_tree.column("Final Significators", width=200, anchor='w')
        self.stellar_significators_tree.grid(row=0, column=0, sticky='nsew')

        stellar_scrollbar = ttk.Scrollbar(output_frame, orient="vertical",
                                          command=self.stellar_significators_tree.yview)
        stellar_scrollbar.grid(row=0, column=1, sticky='ns')
        self.stellar_significators_tree.config(yscrollcommand=stellar_scrollbar.set)

        ttk.Button(output_frame, text="Copy Table",
                   command=lambda: self._copy_treeview_to_clipboard(self.stellar_significators_tree)).grid(
            row=1, column=0, columnspan=2, sticky='ew', pady=(5, 0))

    def _get_house_of_degree(self, degree, cuspal_positions):
        """
        Determines the house number a degree falls into based on cuspal positions.
        """
        for i in range(1, 13):
            cusp_start_degree = cuspal_positions[i][0]

            if i < 12:
                cusp_end_degree = cuspal_positions[i + 1][0]
            else:
                cusp_end_degree = cuspal_positions[1][0] + 360

            normalized_degree = degree
            if cusp_end_degree < cusp_start_degree:
                if normalized_degree < cusp_end_degree:
                    normalized_degree += 360

            if cusp_start_degree <= normalized_degree < cusp_end_degree:
                return i

        return None

    def _get_relative_house(self, start_house_num, offset):
        """
        Calculates the house number that is 'offset' houses away from 'start_house_num'.
        Example: _get_relative_house(1, 10) for 11th from Ascendant (House 1).
                 _get_relative_house(7, 11) for 12th from 7th house.
        """
        result = ((start_house_num - 1 + offset) % 12) + 1
        self._log_debug(f"  Relative house from {start_house_num} with offset {offset}: {result}")
        return result

    def _calculate_positional_status(self, planets_data, cusps_data):
        """
        Calculates positional status for all planets based on Rule 1, Rule 2,
        and the new "own star lord" rule.
        """
        positional_status_planets = set()
        self._log_debug("Calculating positional status.")

        if not planets_data or not cusps_data:
            self._log_debug("No planet/cusp data for positional status calculation.")
            return set()

        planets_who_are_star_lords_of_others = set()

        # Rule 1: Not Star Lord of any other planet
        for p_name_checking_others_star_lordship in STELLAR_PLANETS:
            planet_data_checking_others = planets_data.get(p_name_checking_others_star_lordship)
            if planet_data_checking_others:
                # planet_data_checking_others[3] is the Star Lord of this planet
                if planet_data_checking_others[3] in STELLAR_PLANETS:
                    planets_who_are_star_lords_of_others.add(planet_data_checking_others[3])
        self._log_debug(f"Planets that are star lords of others: {planets_who_are_star_lords_of_others}")

        for p_name in STELLAR_PLANETS:
            # New Rule: Planet in its own star lord
            planet_info = planets_data.get(p_name)
            if planet_info:
                # planet_info[3] is the star lord of the current planet (p_name)
                if planet_info[3] == p_name:
                    positional_status_planets.add(p_name)
                    self._log_debug(f"PS New Rule (Own Star Lord): {p_name} added to PS because it is in its own star.")
                    continue # If this rule gives PS, no need to check other rules for this planet

            if p_name not in planets_who_are_star_lords_of_others:
                positional_status_planets.add(p_name)
                self._log_debug(f"PS Rule 1: {p_name} added to PS because it's not a star lord of another planet.")

        # Rule 2: Mutual star-lordship
        for p1_name in STELLAR_PLANETS:
            p1_data = planets_data.get(p1_name)
            if not p1_data: continue
            p1_star_lord = p1_data[3]

            for p2_name in STELLAR_PLANETS:
                if p1_name == p2_name: continue # Avoid self-comparison

                p2_data = planets_data.get(p2_name)
                if not p2_data: continue
                p2_star_lord = p2_data[3]

                if p1_star_lord == p2_name and p2_star_lord == p1_name:
                    positional_status_planets.add(p1_name)
                    positional_status_planets.add(p2_name)
                    self._log_debug(
                        f"PS Rule 2: Mutual star-lordship between {p1_name} and {p2_name}. Both added to PS.")

        self._log_debug(f"Final Positional Status Planets: {positional_status_planets}")
        return positional_status_planets

    def _create_ruling_planet_tab(self):
        """Creates the UI for the Ruling Planet analysis tab."""
        rp_frame = ttk.Frame(self.notebook)
        self.notebook.add(rp_frame, text="Ruling Planet")

        rp_frame.grid_columnconfigure(0, weight=1)
        rp_frame.grid_rowconfigure(0, weight=1) # The results frame will expand

        # Frame to contain the results
        results_frame = ttk.LabelFrame(rp_frame, text="Calculated Ruling Planets")
        results_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)  # The Treeview's row will expand

        # Label to display the identified Base RPs
        self.base_rps_label = ttk.Label(results_frame, text="Base RPs: (Generate a chart to calculate)", font=('Helvetica', 9, 'bold'))
        self.base_rps_label.grid(row=0, column=0, sticky='w', padx=5, pady=2)

        # Treeview for the categorized list of RPs
        self.rp_tree = ttk.Treeview(results_frame, columns=("Strength", "Planet", "Details"), show="headings")
        self.rp_tree.heading("Strength", text="Strength")
        self.rp_tree.heading("Planet", text="Planet")
        self.rp_tree.heading("Details", text="Details")
        self.rp_tree.column("Strength", width=120, anchor='w')
        self.rp_tree.column("Planet", width=100, anchor='w')
        self.rp_tree.column("Details", width=500, anchor='w')
        self.rp_tree.grid(row=1, column=0, sticky='nsew', pady=(5, 0))

        # Scrollbar for the treeview
        rp_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.rp_tree.yview)
        rp_scrollbar.grid(row=1, column=1, sticky='ns', pady=(5, 0))
        self.rp_tree.config(yscrollcommand=rp_scrollbar.set)

    def _generate_static_stellar_significators(self, planets_data, cusps_data, progress_info=None, start_percent=0,
                                                end_percent=100):
        """
        (NEW LOGIC) Calculates planetary significators based on the revised 2025 rules.
        Updated to correctly unpack 5 values from get_nakshatra_info.
        """
        self._log_debug("--- Generating significators with NEW REVISED rules ---")
        temp_static_stellar_data = {}
        planets_with_ps = self._calculate_positional_status(planets_data, cusps_data)

        total_planets = len(STELLAR_PLANETS)
        progress_span = end_percent - start_percent
        pass1_span = progress_span * 0.9  # Allocate 90% of the time to the main loop

        # --- PASS 1: Calculate initial significators for each planet ---
        for i, planet_name in enumerate(STELLAR_PLANETS):
            if progress_info:
                progress = start_percent + ((i + 1) / total_planets) * pass1_span
                self._update_progress(progress_info, progress,
                                       f"Step 2/4: Analyzing significators for {planet_name}...")

            planet_info = planets_data.get(planet_name)
            if not planet_info:
                continue

            # --- FIX IS HERE: Unpack 5 values from get_nakshatra_info ---
            _, planet_star_lord_of_self, planet_sub_lord_of_self, _, _ = self.get_nakshatra_info(planet_info[0])
            # Added an extra '_' for the sookshma_lord which is not directly used here.

            # --- Star Significators (NEW LOGIC) ---
            # Primary Rule: Find all cusps where the planet's star lord is a cuspal lord.
            star_sigs_raw = set()
            if planet_star_lord_of_self:
                for cusp_num, cusp_data in cusps_data.items():
                    # Cusp lords are at indices 2, 3, 4, 5 (Sign, Star, Sub, SSL)
                    if planet_star_lord_of_self in cusp_data[2:]:
                        star_sigs_raw.add(cusp_num)

            # Fallback Rule: If the primary rule yields no results, use the house of deposition.
            if not star_sigs_raw:
                self._log_debug(f"Star Significators for {planet_name} are empty. Applying fallback rule.")
                house_of_deposition = self._get_house_of_degree(planet_info[0], cusps_data)
                if house_of_deposition:
                    star_sigs_raw.add(house_of_deposition)
                    self._log_debug(f"  -> Fallback applied. Star Sig for {planet_name} is now: {star_sigs_raw}")

            # --- Sub Significators (UNCHANGED LOGIC) ---
            # Rule: Find all cusps where the planet's sub lord is a cuspal lord.
            sub_sigs_raw = set()
            if planet_sub_lord_of_self:
                for cusp_num, cusp_data in cusps_data.items():
                    if planet_sub_lord_of_self in cusp_data[2:]:
                        sub_sigs_raw.add(cusp_num)

            # --- Final Significators (NEW COMBINATION LOGIC) ---
            # Step 1 & 2: Start with star significators and apply negation (Logic is unchanged).
            final_sigs = set(self._apply_negation_logic(list(star_sigs_raw), list(sub_sigs_raw)))

            # Step 3 & 4: Add own position and direct lordships ONLY if the planet has Positional Status (NEW LOGIC).
            if planet_name in planets_with_ps:
                self._log_debug(f"Planet {planet_name} has Positional Status. Adding direct significations.")
                # Add the house the planet is physically located in.
                house_of_pos = self._get_house_of_degree(planet_info[0], cusps_data)
                if house_of_pos:
                    final_sigs.add(house_of_pos)
                    self._log_debug(f"  -> Added posited house: {house_of_pos}")

                # Add houses where the planet itself is a cuspal lord.
                for cusp_num, cusp_data in cusps_data.items():
                    if planet_name in cusp_data[2:]:
                        final_sigs.add(cusp_num)
                        self._log_debug(f"  -> Added direct lordship of cusp: {cusp_num}")

            # Store the calculated data for this planet
            temp_static_stellar_data[planet_name] = {
                'star_sigs': sorted(list(star_sigs_raw)),
                'sub_sigs': sorted(list(sub_sigs_raw)),
                'final_sigs': sorted(list(final_sigs))
            }

        # --- PASS 2: Finalize Rahu and Ketu with new agency rule ---
        if progress_info:
            self._update_progress(progress_info, start_percent + pass1_span, "Step 2/4: Applying Rahu/Ketu rules...")

        for node_name in ['Rahu', 'Ketu']:
            node_info = planets_data.get(node_name)
            if not node_info or node_name not in temp_static_stellar_data:
                continue

            current_final_sigs_for_node = set(temp_static_stellar_data[node_name].get('final_sigs', []))

            # NEW RULE: Only include significators from Sign Lord and Star Lord
            node_sign_lord = node_info[2]
            node_star_lord = node_info[3]

            lords_to_add = []
            if node_sign_lord in STELLAR_PLANETS: lords_to_add.append(node_sign_lord)
            if node_star_lord in STELLAR_PLANETS: lords_to_add.append(node_star_lord)

            self._log_debug(f"Applying new agency rule for {node_name}. Adding sigs from: {lords_to_add}")

            for lord in lords_to_add:
                # Important: Use the already calculated final_sigs from the temp dictionary
                lord_final_sigs = set(temp_static_stellar_data.get(lord, {}).get('final_sigs', []))
                if lord_final_sigs:
                    current_final_sigs_for_node.update(lord_final_sigs)
                    self._log_debug(f"  -> Added sigs from {lord}: {sorted(list(lord_final_sigs))}")

            # Update the node's final significators in the temp dictionary
            temp_static_stellar_data[node_name]['final_sigs'] = sorted(list(current_final_sigs_for_node))

        if progress_info:
            self._update_progress(progress_info, end_percent, "Step 2/4: Significator analysis complete.")

        # Final assignment to the class variable
        self.stellar_significators_data = temp_static_stellar_data
        self._log_debug("Static stellar significators generation complete with new rules.")
        return self.stellar_significators_data

    def _run_dasha_classification_analysis(self):
        self._log_debug("Running Dasha Classification Analysis.")
        self._update_analysis_results_tree_columns("dasha_classification")

        if not self.current_planetary_positions or not self.current_cuspal_positions or not self.stellar_significators_data:
            messagebox.showwarning("Chart Data Missing",
                                   "Please generate a chart and ensure Stellar Status Significators are calculated first.")
            self._log_debug("ERROR: Chart data or stellar significators missing for dasha classification analysis.")
            return

        original_primary_cusp_num = self._get_original_primary_cusp_from_ui()
        if original_primary_cusp_num is None: return

        primary_cusp_num_for_analysis = self._determine_primary_cusp_for_analysis(original_primary_cusp_num)

        # Ensure planet classifications are cached before starting analysis
        self._cache_static_planet_classifications(primary_cusp_num_for_analysis, original_primary_cusp_num)
        if not hasattr(self, 'planet_classifications') or not self.planet_classifications:
            messagebox.showerror("Internal Error", "Planet classifications not cached. Please generate chart first.")
            self._log_debug("ERROR: Planet classifications not cached for dasha classification analysis.")
            return

        ascendant_house_num = 1  # Ascendant is always House 1 in this context

        timezone_str = self.timezone_combo.get()
        local_tz = pytz.timezone(timezone_str)

        overall_analysis_start_dt_utc, overall_analysis_end_dt_utc = self._get_analysis_time_range(local_tz)
        if overall_analysis_start_dt_utc is None: return

        self.analysis_results_tree.delete(*self.analysis_results_tree.get_children())

        progress_window = tk.Toplevel(self.root)
        progress_window.title("Dasha Classification Progress")
        progress_window.transient(self.root)
        progress_window.grab_set()
        progress_window.geometry("350x100")
        ttk.Label(progress_window, text="Generating Dasha Periods for analysis...").pack(pady=10)
        progress_bar = ttk.Progressbar(progress_window, orient='horizontal', length=250, mode='indeterminate')
        progress_bar.pack(pady=5)
        progress_label = ttk.Label(progress_window, text="0.0%")
        progress_label.pack()
        self.root.update_idletasks()

        # Natal UTC date is crucial for _get_dasha_periods_flat to span the correct 120 years
        natal_utc_dt = self.current_general_info.get('natal_utc_dt')
        if not natal_utc_dt:
            if progress_window: progress_window.destroy()
            messagebox.showerror("Data Error", "Natal chart UTC time not found. Please regenerate chart.")
            self._log_debug("ERROR: Natal UTC datetime not found in general info for dasha classification.")
            return

        # Fetch all Prana Dasha periods from the entire 120-year Dasa Tree
        all_prana_dasha_periods = self._get_dasha_periods_flat(
            natal_utc_dt,
            natal_utc_dt + datetime.timedelta(days=365.25 * 120),  # Span entire 120 years
            local_tz
        )
        self._log_debug(
            f"Fetched {len(all_prana_dasha_periods)} Prana Dasha periods from the entire tree for classification.")

        # Filter periods to only include those within the requested analysis range
        periods_for_analysis_range = [
            p for p in all_prana_dasha_periods
            if p['start_utc'] < overall_analysis_end_dt_utc and p['end_utc'] > overall_analysis_start_dt_utc
        ]
        periods_for_analysis_range.sort(key=lambda x: x['start_utc'])
        self._log_debug(f"Filtered down to {len(periods_for_analysis_range)} periods within the analysis range.")

        total_periods = len(periods_for_analysis_range)
        processed_periods = 0

        final_dasha_results = []

        for prana_period_data in periods_for_analysis_range:
            md_lord = prana_period_data['md_lord']
            ad_lord = prana_period_data['ad_lord']
            pd_lord = prana_period_data['pd_lord']
            sd_lord = prana_period_data['sd_lord']
            prd_lord = prana_period_data['prd_lord']
            start_local = prana_period_data['start_local']
            end_local = prana_period_data['end_local']

            # Pass original_primary_cusp_num to classification methods to handle Rule 2
            # Retrieve classifications from cache
            md_type_str = self.planet_classifications.get(md_lord, 'Unclassified')
            ad_type_str = self.planet_classifications.get(ad_lord, 'Unclassified')
            pd_type_str = self.planet_classifications.get(pd_lord, 'Unclassified')
            sd_type_str = self.planet_classifications.get(sd_lord, 'Unclassified')
            prd_type_str = self.planet_classifications.get(prd_lord, 'Unclassified')

            combined_positive_neutral = False
            overall_type_str = "Negative/Unclassified"
            overall_details_list = []

            # For detailed logging/display, re-run classification with details
            md_is_positive, md_pos_details = self._is_dasha_positive(md_lord, primary_cusp_num_for_analysis,
                                                                     ascendant_house_num, original_primary_cusp_num)
            md_is_neutral, md_neut_details = self._is_dasha_neutral(md_lord, primary_cusp_num_for_analysis,
                                                                    ascendant_house_num, original_primary_cusp_num)
            md_is_negative, md_neg_details = self._is_dasha_negative(md_lord, primary_cusp_num_for_analysis,
                                                                     ascendant_house_num, original_primary_cusp_num)

            ad_is_positive, ad_pos_details = self._is_dasha_positive(ad_lord, primary_cusp_num_for_analysis,
                                                                     ascendant_house_num, original_primary_cusp_num)
            ad_is_neutral, ad_neut_details = self._is_dasha_neutral(ad_lord, primary_cusp_num_for_analysis,
                                                                    ascendant_house_num, original_primary_cusp_num)
            ad_is_negative, ad_neg_details = self._is_dasha_negative(ad_lord, primary_cusp_num_for_analysis,
                                                                     ascendant_house_num, original_primary_cusp_num)

            pd_is_positive, pd_pos_details = self._is_dasha_positive(pd_lord, primary_cusp_num_for_analysis,
                                                                     ascendant_house_num, original_primary_cusp_num)
            pd_is_neutral, pd_neut_details = self._is_dasha_neutral(pd_lord, primary_cusp_num_for_analysis,
                                                                    ascendant_house_num, original_primary_cusp_num)
            pd_is_negative, pd_neg_details = self._is_dasha_negative(pd_lord, primary_cusp_num_for_analysis,
                                                                     ascendant_house_num, original_primary_cusp_num)

            # Determine combined P/N status for MD, AD, PD
            if (md_is_positive or md_is_neutral) and \
                    (ad_is_positive or ad_is_neutral) and \
                    (pd_is_positive or pd_is_neutral):
                combined_positive_neutral = True
                overall_type_str = "Combined P/N"
                overall_details_list.append(
                    f"MD ({md_lord}): {md_type_str} ({md_pos_details if md_is_positive else md_neut_details})")
                overall_details_list.append(
                    f"AD ({ad_lord}): {ad_type_str} ({ad_pos_details if ad_is_positive else ad_neut_details})")
                overall_details_list.append(
                    f"PD ({pd_lord}): {pd_type_str} ({pd_pos_details if pd_is_positive else pd_neut_details})")
            else:
                overall_details_list.append(
                    f"MD ({md_lord}): {md_type_str} ({md_pos_details if md_is_positive else (md_neut_details if md_is_neutral else md_neg_details)})")
                overall_details_list.append(
                    f"AD ({ad_lord}): {ad_type_str} ({ad_pos_details if ad_is_positive else (ad_neut_details if ad_is_neutral else ad_neg_details)})")
                overall_details_list.append(
                    f"PD ({pd_lord}): {pd_type_str} ({pd_pos_details if pd_is_positive else (pd_neut_details if pd_is_neutral else pd_neg_details)})")

            overall_details_text = " | ".join(overall_details_list)

            sookshma_type = "N/A"
            sookshma_details_text = ""
            if combined_positive_neutral:
                selected_secondary_cusp_indices = self.secondary_cusp_listbox.curselection()
                secondary_cusp_nums_for_sookshma = [int(self.secondary_cusp_listbox.get(i).split()[-1]) for i in
                                                    selected_secondary_cusp_indices]

                # Pass original_primary_cusp_num to _check_sookshma_lord_condition to handle Rule 2
                sookshma_condition_met, sookshma_check_details, num_sc_signified = \
                    self._check_sookshma_lord_condition(sd_lord, primary_cusp_num_for_analysis, ascendant_house_num,
                                                        secondary_cusp_nums_for_sookshma, original_primary_cusp_num)

                if sookshma_condition_met:
                    sookshma_type = "Sookshma (Favorable)"
                    sookshma_details_text = sookshma_check_details + f" (Signified {num_sc_signified} secondary cusps out of {len(secondary_cusp_nums_for_sookshma)})."
                else:
                    sookshma_type = "Sookshma (Unfavorable)"
                    sookshma_details_text = sookshma_check_details
            else:
                sookshma_type = "N/A (MD/AD/PD not favorable)"
                sookshma_details_text = "Skipped Sookshma check as MD/AD/PD combination not Positive/Neutral."

            final_dasha_results.append((
                md_lord, ad_lord, pd_lord, sd_lord, prd_lord,
                f"{overall_type_str} ({sookshma_type})",
                start_local.strftime('%Y-%m-%d %H:%M:%S'),
                end_local.strftime('%Y-%m-%d %H:%M:%S'),
                overall_details_text + f" | SD: {sookshma_details_text}"
            ))

            processed_periods += 1
            progress = (processed_periods / total_periods) * 100
            progress_bar['value'] = progress
            progress_label.config(text=f"Classifying Dasha periods: {progress:.1f}%")
            self.root.update_idletasks()

        progress_window.destroy()

        final_dasha_results.sort(key=lambda x: (x[6], x[0], x[1], x[2], x[3], x[4]))

        for row_data in final_dasha_results:
            self.analysis_results_tree.insert("", "end", values=row_data)

        if not self.analysis_results_tree.get_children():
            self.analysis_results_tree.insert("", "end", values=(
                "", "", "", "", "", "No suitable Dasha periods found.", "", "", ""
            ))
            self._log_debug("No suitable Dasha periods found for classification.")
    def _apply_negation_logic(self, star_significators_raw, sub_significators_raw):
        """
        Applies negation logic to filter significators, with an exception for Cusp 2.
        """
        final_significators = set(star_significators_raw)
        star_set = set(star_significators_raw)
        sub_set = set(sub_significators_raw)
        cusps_to_remove = set()

        self._log_debug(f"  Negation Logic Input: Star {star_set}, Sub {sub_set}")

        for star_cusp in star_set:
            previous_cusp = star_cusp - 1
            if previous_cusp == 0:
                previous_cusp = 12

            if previous_cusp in sub_set and star_cusp not in sub_set:
                cusps_to_remove.add(star_cusp)
                self._log_debug(
                    f"  Negation: Cusp {star_cusp} removed because {previous_cusp} is in sub-set and {star_cusp} is not.")

        if 2 in star_set and 1 in sub_set:
            if 2 in cusps_to_remove:
                cusps_to_remove.remove(2)
                self._log_debug(
                    "  Exception Rule 2 Applied: Cusp 2 kept despite negation logic due to 2 in star_set and 1 in sub_set.")

        final_significators.difference_update(cusps_to_remove)
        self._log_debug(f"  Negation Logic Output: Final {sorted(list(final_significators))}")
        return sorted(list(final_significators))

    def _populate_all_stellar_significators_table(self):
        """
        Populates the stellar significators table for all planets, using the *static* chart data.
        """
        if not self.current_planetary_positions or not self.current_cuspal_positions:
            self.stellar_significators_tree.delete(*self.stellar_significators_tree.get_children())
            self.stellar_significators_tree.insert("", "end", values=("N/A",
                                                                      "Please generate a chart first in 'Chart Generation' tab.",
                                                                      "", ""))
            self._log_debug("Stellar status table not populated: Chart data missing.")
            return

        self.stellar_significators_tree.delete(*self.stellar_significators_tree.get_children())

        # stellar_significators_data is already calculated by _on_generate_chart_button
        # If it's not populated, something went wrong with chart generation, but it shouldn't be empty here.
        if not self.stellar_significators_data:
            self._log_debug("Stellar significators data is unexpectedly empty, attempting to regenerate.")
            self.stellar_significators_data = self._generate_static_stellar_significators(
                self.current_planetary_positions, self.current_cuspal_positions
            )

        for planet_name in STELLAR_PLANETS:
            planet_data = self.stellar_significators_data.get(planet_name)
            if not planet_data:
                self.stellar_significators_tree.insert("", "end", values=(planet_name, "N/A", "N/A", "N/A"))
                self._log_debug(f"No static significator data for {planet_name} for table display.")
                continue

            star_sigs_str = " ".join(map(str, planet_data['star_sigs']))
            sub_sigs_str = " ".join(map(str, planet_data['sub_sigs']))
            final_sigs_str = " ".join(map(str, planet_data['final_sigs']))

            self.stellar_significators_tree.insert("", "end", values=(
                planet_name,
                star_sigs_str,
                sub_sigs_str,
                final_sigs_str
            ))
            self._log_debug(f"Populated stellar status for {planet_name} in table.")

    def _set_default_inputs(self):
        self._set_time_to_now()
        self.city_combo.set("Kolkata")
        self.horary_entry.delete(0, tk.END)
        self.horary_entry.insert(0, "1")
        self.timezone_combo.set("Asia/Kolkata")
        self.analysis_duration_value_entry.delete(0, tk.END)
        if self.analysis_duration_value_entry.get() == "":
            self.analysis_duration_value_entry.insert(0, "24")
        self._log_debug("Default inputs set.")

    def _get_selected_hsys(self):
        hsys_name = self.house_sys_combo.get()
        hsys_const = HOUSE_SYSTEMS.get(hsys_name)
        if hsys_const is None:
            messagebox.showerror("House System Error", f"Unknown House system: {hsys_name}")
            self._log_debug(f"ERROR: Unknown House system: {hsys_name}")
            return None
        return hsys_const

    def _calculate_chart_data(self, dt_utc, city, hsys_const, horary_num_value=None):
        """
        Calculates planetary and cuspal positions.
        MODIFIED: Now uses the Khullar Ayanamsha.
        Updated to correctly unpack 5 values from get_nakshatra_info.
        """
        latitude, longitude = self.get_lat_lon(city)
        jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                        dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600)

        # Call the new Khullar Ayanamsha function
        current_ayan_value = self.get_khullar_ayanamsha(jd)

        planetary_positions = {}
        planet_ids = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER, swe.VENUS, swe.SATURN, swe.MEAN_NODE]
        for p_id in planet_ids:
            lon = swe.calc_ut(jd, p_id)[0][0]
            sidereal = (lon - current_ayan_value) % 360
            name = SWE_PLANET_NAMES.get(p_id, f"Planet_{p_id}")
            sign = self.get_sign(sidereal)
            sign_lord = self.get_sign_lord(sign)

            # --- FIX 1: Unpack 5 values from get_nakshatra_info ---
            _, star_lord, sub_lord, sub_sub_lord, _ = self.get_nakshatra_info(sidereal)  # Added '_' for sookshma_lord

            planetary_positions[name] = (sidereal, sign, sign_lord, star_lord, sub_lord, sub_sub_lord)

            if p_id == swe.MEAN_NODE:
                ketu_sidereal = (sidereal + 180) % 360
                ketu_sign = self.get_sign(ketu_sidereal)
                ketu_sign_lord = self.get_sign_lord(ketu_sign)

                # --- FIX 2: Unpack 5 values for Ketu ---
                _, ketu_star_lord, ketu_sub_lord, ketu_sub_sub_lord, _ = self.get_nakshatra_info(
                    ketu_sidereal)  # Added '_' for sookshma_lord

                planetary_positions['Ketu'] = (ketu_sidereal, ketu_sign, ketu_sign_lord, ketu_star_lord, ketu_sub_lord,
                                               ketu_sub_sub_lord)

        cuspal_positions = {}

        if horary_num_value is not None:
            # --- HORARY CHART LOGIC ---
            self._log_debug("Using HORARY logic for cusp calculation.")
            horary_asc_sidereal = (horary_num_value - 1) * (360 / 2193) % 360
            h1_sign = self.get_sign(horary_asc_sidereal)
            h1_sign_lord = self.get_sign_lord(h1_sign)

            # --- FIX 3: Unpack 5 values for Ascendant in Horary ---
            _, h1_star_lord, h1_sub_lord, h1_sub_sub_lord, _ = self.get_nakshatra_info(
                horary_asc_sidereal)  # Added '_' for sookshma_lord

            cuspal_positions[1] = (horary_asc_sidereal, h1_sign, h1_sign_lord, h1_star_lord, h1_sub_lord,
                                   h1_sub_sub_lord)

            cusps_tropical, _ = swe.houses(jd, latitude, longitude, hsys_const)
            for i in range(2, 13):
                sid_cusp = (cusps_tropical[i - 1] - current_ayan_value) % 360
                cusp_sign = self.get_sign(sid_cusp)
                cusp_sign_lord = self.get_sign_lord(cusp_sign)

                # --- FIX 4: Unpack 5 values for other cusps in Horary ---
                _, cusp_star_lord, cusp_sub_lord, cusp_sub_sub_lord, _ = self.get_nakshatra_info(
                    sid_cusp)  # Added '_' for sookshma_lord

                cuspal_positions[i] = (sid_cusp, cusp_sign, cusp_sign_lord, cusp_star_lord, cusp_sub_lord,
                                       cusp_sub_sub_lord)
        else:
            # --- BIRTH CHART LOGIC ---
            self._log_debug("Using BIRTH CHART logic for cusp calculation.")
            cusps_tropical, _ = swe.houses(jd, latitude, longitude, hsys_const)
            for i in range(1, 13):
                sid_cusp = (cusps_tropical[i - 1] - current_ayan_value) % 360
                cusp_sign = self.get_sign(sid_cusp)
                cusp_sign_lord = self.get_sign_lord(cusp_sign)

                # --- FIX 5: Unpack 5 values for all cusps in Birth Chart ---
                _, cusp_star_lord, cusp_sub_lord, cusp_sub_sub_lord, _ = self.get_nakshatra_info(
                    sid_cusp)  # Added '_' for sookshma_lord

                cuspal_positions[i] = (sid_cusp, cusp_sign, cusp_sign_lord, cusp_star_lord, cusp_sub_lord,
                                       cusp_sub_sub_lord)

        general_info_dict = {"julian_day": jd, "ayanamsha_value": current_ayan_value,
                             "house_system": hsys_const.decode('utf-8'), "natal_utc_dt": dt_utc}
        return planetary_positions, cuspal_positions, general_info_dict

    def _on_generate_chart_button(self):
        """
        (CORRECTED) Main chart generation function.
        This version is updated to correctly call the new ETR progress bar.
        Crucially, it no longer triggers `_cache_static_planet_classifications` or `_calculate_ruling_planets`
        as these are now event-dependent and triggered by `_check_promise`.
        Includes extensive debugging logs for diagnosing initial data population.
        """
        self._log_debug("--- _on_generate_chart_button: Start ---")
        self._log_debug("Generate Chart button clicked.")

        # Clear previous analysis results or warnings
        self.analysis_results_tree.delete(*self.analysis_results_tree.get_children())
        self.rp_tree.delete(*self.rp_tree.get_children())
        self.positive_planets_label.config(text="Positive Planets: (Not Calculated)")
        self.neutral_planets_label.config(text="Neutral Planets: (Not Calculated)")
        self.asc_promise_label.config(text="Asc:", foreground="gray")
        self.pcusp_promise_label.config(text="Pcusp:", foreground="gray")
        self.planet_classifications = {}  # Ensure classifications are reset for a new chart

        try:
            year_str = self.year_lb.get(self.year_lb.curselection())
            month_name = self.month_lb.get(self.month_lb.curselection())
            day_str = self.day_lb.get(self.day_lb.curselection())
            hour_str = self.hour_lb.get(self.hour_lb.curselection())
            minute_str = self.minute_lb.get(self.minute_lb.curselection())
            second_str = self.second_lb.get(self.second_lb.curselection())

            month_num = MONTH_NAMES.index(month_name) + 1
            date_str = f"{year_str}-{month_num:02d}-{day_str}"
            time_str = f"{hour_str}:{minute_str}:{second_str}"

            self._log_debug(f"Input Date: {date_str}, Time: {time_str}")

        except (tk.TclError, ValueError, IndexError) as e:
            messagebox.showerror("Input Error",
                                 f"Please select a value for Year, Month, Day, Hour, Minute, and Second: {e}")
            self._log_debug(f"ERROR: Input parsing failed: {e}")
            return

        horary_num_value = None
        if self.chart_type_var.get() == "Horary":
            horary_num_str = self.horary_entry.get()
            if horary_num_str.isdigit():
                num = int(horary_num_str)
                if not (1 <= num <= 2193):
                    messagebox.showerror("Invalid Horary Number", "Please enter a number between 1 and 2193.")
                    self._log_debug(f"ERROR: Invalid Horary Number: {num}")
                    return
                horary_num_value = num
            else:
                messagebox.showerror("Invalid Horary Number", "Please enter a valid number for a Horary Chart.")
                self._log_debug("ERROR: Non-digit Horary Number entered.")
                return

        city = self.city_combo.get()
        timezone_str = self.timezone_combo.get()

        self._log_debug(f"Input City: {city}, Timezone: {timezone_str}")

        try:
            local_dt_naive = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
            local_tz = pytz.timezone(timezone_str)
            local_dt_aware = local_tz.localize(local_dt_naive)
            utc_dt = local_dt_aware.astimezone(pytz.utc)
            self._log_debug(f"Converted UTC DateTime: {utc_dt}")

        except (ValueError, pytz.exceptions.UnknownTimeZoneError) as e:
            messagebox.showerror("Date/Time Error", f"Could not process the date or timezone.\nError: {e}")
            self._log_debug(f"ERROR: DateTime/Timezone conversion failed: {e}")
            return

        progress_info = self._setup_progress_window("Generating Chart")

        start_time = datetime.datetime.now()
        total_steps = 100

        try:
            self._update_progress(progress_info, 0, total_steps, start_time, "Step 1/3: Calculating chart data...")
            hsys_const = self._get_selected_hsys()
            if hsys_const is None:
                self._log_debug("ERROR: House System constant is None.")
                if progress_info['window'].winfo_exists(): progress_info['window'].destroy()
                return

            planetary_positions, cuspal_positions, general_info_dict = self._calculate_chart_data(utc_dt, city,
                                                                                                  hsys_const,
                                                                                                  horary_num_value)

            # CRITICAL CHECK: Ensure core calculation returned valid data
            if planetary_positions is None or not planetary_positions or \
                    cuspal_positions is None or not cuspal_positions:
                messagebox.showerror("Calculation Error",
                                     "Failed to calculate planetary or cuspal positions. Check inputs.")
                self._log_debug("CRITICAL ERROR: Planetary or cuspal positions are empty after calculation.")
                if progress_info['window'].winfo_exists(): progress_info['window'].destroy()
                return

            self.current_planetary_positions = planetary_positions
            self.current_cuspal_positions = cuspal_positions
            self.current_general_info = general_info_dict

            self._log_debug(
                f"DEBUG: Core Chart Data Calculated. Planets: {len(self.current_planetary_positions)}, Cusps: {len(self.current_cuspal_positions)}.")

            self._update_progress(progress_info, 40, total_steps, start_time, "Step 2/3: Analyzing significators...")
            # Stellar significators are still calculated here as they are foundational, static properties of the chart itself.
            self.stellar_significators_data = self._generate_static_stellar_significators(planetary_positions,
                                                                                          cuspal_positions)

            # --- DEBUG CHECKS FOR STELLAR SIGNIFICATORS ---
            self._log_debug(f"DEBUG: After stellar_significators_data populated (Step 2/3).")
            if not self.stellar_significators_data:
                self._log_debug(
                    "CRITICAL ERROR: self.stellar_significators_data is EMPTY after generation. This will cause downstream errors.")
                messagebox.showerror("Internal Error",
                                     "Stellar significators data is empty after chart generation. This is a critical error. Please check logs.")
                if progress_info['window'].winfo_exists(): progress_info['window'].destroy()
                return  # Exit early if this fundamental data is missing
            self._log_debug(
                f"DEBUG: self.stellar_significators_data has {len(self.stellar_significators_data)} planets with significators.")
            # Example: check if Sun has significators
            if 'Sun' in self.stellar_significators_data:
                self._log_debug(f"DEBUG: Sun's final_sigs: {self.stellar_significators_data['Sun'].get('final_sigs')}")
            # --- END DEBUG ADDITION ---

            self._update_progress(progress_info, 80, total_steps, start_time, "Step 3/3: Populating UI tables...")
            self._update_main_chart_display(planetary_positions, cuspal_positions, general_info_dict)
            self._populate_all_stellar_significators_table()
            moon_sidereal_degree = planetary_positions['Moon'][0]  # Ensure Moon exists
            self._calculate_dasha_levels(start_dt=utc_dt, moon_sidereal_degree=moon_sidereal_degree)

            self._update_progress(progress_info, 100, total_steps, start_time, "Done!")
            if progress_info['window'].winfo_exists(): progress_info['window'].destroy()

            messagebox.showinfo("Chart Generated",
                                "Chart data has been successfully generated. Proceed to 'Daily Analysis' to select an event.")
            self._log_debug("--- _on_generate_chart_button: End (Success) ---")

        except Exception as e:
            self._log_debug(f"CRITICAL ERROR during chart generation: {e}", exc_info=True)  # Log full traceback
            messagebox.showerror("Generation Error",
                                 f"An unexpected error occurred during chart generation:\n{e}\n\nCheck the debug log for more details.")
            if 'progress_info' in locals() and progress_info['window'].winfo_exists():
                progress_info['window'].destroy()
            self._log_debug("--- _on_generate_chart_button: End (Failure) ---")

    def _update_main_chart_display(self, planetary_positions, cuspal_positions, general_info_dict):
        """
        (Corrected Version) Populates the main chart tables and no longer
        references the deleted general_output_text widget.
        """
        self.planets_tree.delete(*self.planets_tree.get_children())
        self.cusps_tree.delete(*self.cusps_tree.get_children())

        # Correctly populate the Planetary Positions table
        for planet_name, data_tuple in planetary_positions.items():
            row_values = (
                planet_name,
                f"{data_tuple[0]:.4f}",  # Degree
                data_tuple[1],  # Sign
                data_tuple[2],  # Sign Lord
                data_tuple[3],  # Star Lord
                data_tuple[4],  # Sub Lord
                data_tuple[5]  # Sub-Sub Lord
            )
            self.planets_tree.insert("", "end", values=row_values)

        # Correctly populate the Cuspal Positions table
        for house_num, data_tuple in cuspal_positions.items():
            row_values = (
                f"House {house_num}",
                f"{data_tuple[0]:.4f}",  # Degree
                data_tuple[1],  # Sign
                data_tuple[2],  # Sign Lord
                data_tuple[3],  # Star Lord
                data_tuple[4],  # Sub Lord
                data_tuple[5]  # Sub-Sub Lord
            )
            self.cusps_tree.insert("", "end", values=row_values)

        # The lines that tried to write to self.general_output_text are now gone.

        self._log_debug("Main chart display updated successfully.")

    def _calculate_dasha_levels(self, start_dt, moon_sidereal_degree):
        """
        (NEW LOGIC) Calculates a full 120-year Dasha tree and then prunes it
        based on whether the chart is Horary (next 10 years) or Natal (90 years from birth).
        Updated to correctly unpack 5 values from get_nakshatra_info.
        """
        self.dasa_tree.delete(*self.dasa_tree.get_children())

        # --- FIX IS HERE: Unpack 5 values from get_nakshatra_info ---
        # We need to receive all 5 values, even if we only use the first two here.
        moon_nakshatra_name, moon_nakshatra_lord, _, _, _ = self.get_nakshatra_info(moon_sidereal_degree)
        # Added three '_' placeholders for sub_lord, sub_sub_lord, and sookshma_lord

        self.moon_dasha_info_label.config(text=f"Dasha calculated from Moon's position ({moon_sidereal_degree:.4f}° "
                                                 f"in {moon_nakshatra_name} / Lord: {moon_nakshatra_lord})")

        # Calculate the balance of the first Dasha period
        degree_into_nakshatra = moon_sidereal_degree % NAKSHATRA_SPAN_DEG
        remaining_nakshatra_portion = (NAKSHATRA_SPAN_DEG - degree_into_nakshatra) / NAKSHATRA_SPAN_DEG
        initial_dasha_period_years = DASHA_PERIODS[moon_nakshatra_lord]
        balance_dasha_years = initial_dasha_period_years * remaining_nakshatra_portion

        try:
            start_lord_index = LORD_ORDER.index(moon_nakshatra_lord)
        except ValueError:
            messagebox.showerror("Dasha Calculation Error",
                                 f"Moon's Nakshatra Lord '{moon_nakshatra_lord}' not found in LORD_ORDER. Check NAKSHATRAS data consistency.")
            self._log_debug(f"ERROR: Moon's Nakshatra Lord '{moon_nakshatra_lord}' not found in LORD_ORDER during dasha calculation.")
            return

        def get_scaled_sub_periods(parent_lord, parent_period_actual_years):
            sub_periods_list = []
            try:
                parent_lord_index = LORD_ORDER.index(parent_lord)
            except ValueError:
                self._log_debug(f"WARNING: Parent lord '{parent_lord}' not found in LORD_ORDER during sub-period calculation. Skipping sub-periods for this lord.")
                return []
            rotated_lords = LORD_ORDER[parent_lord_index:] + LORD_ORDER[:parent_lord_index]
            for sub_lord_name in rotated_lords:
                sub_lord_full_period = DASHA_PERIODS[sub_lord_name]
                scaled_sub_period = (sub_lord_full_period / 120) * parent_period_actual_years
                sub_periods_list.append((sub_lord_name, scaled_sub_period))
            return sub_periods_list

        def add_dasha_level(parent_id, lord_name, period_years, start_date, level_name):
            if period_years <= 0: return
            end_date = start_date + datetime.timedelta(days=period_years * 365.25)

            item_id = self.dasa_tree.insert(parent_id, "end", text=f"{lord_name}",
                                             values=(f"{period_years:.2f}y", start_date.strftime("%Y-%m-%d"),
                                                     end_date.strftime("%Y-%m-%d")),
                                             open=False) # Keep items closed by default

            next_level_map = {"Mahadasha": "Antardasha", "Antardasha": "Pratyantardasha",
                              "Pratyantardasha": "Sookshmadasha", "Sookshmadasha": "Prana Dasha"}
            if level_name in next_level_map:
                sub_start_date = start_date
                for sub_lord, sub_period in get_scaled_sub_periods(lord_name, period_years):
                    add_dasha_level(item_id, sub_lord, sub_period, sub_start_date, next_level_map[level_name])
                    sub_start_date += datetime.timedelta(days=sub_period * 365.25)

        # --- Step 1: Generate the full 120-year Dasha cycle in memory ---
        current_date = start_dt
        # This loop calculates the full cycle starting from the birth/query time
        for i in range(len(LORD_ORDER)):
            current_lord_index = (start_lord_index + i) % len(LORD_ORDER)
            lord_name = LORD_ORDER[current_lord_index]
            period_years = balance_dasha_years if i == 0 else DASHA_PERIODS[lord_name]
            add_dasha_level("", lord_name, period_years, current_date, "Mahadasha")
            current_date += datetime.timedelta(days=period_years * 365.25)

        # --- Step 2: Prune the generated tree based on the chart type ---
        chart_type = self.chart_type_var.get()
        if chart_type == "Horary":
            # For Horary, show the next 10 years from the time of the query
            start_limit = start_dt # The query time itself
            end_limit = start_dt + datetime.timedelta(days=10 * 365.25)
            self._prune_dasha_tree(start_limit, end_limit)
        elif chart_type == "Birth Chart":
            # For Natal, show 90 years from birth
            start_limit = start_dt # The birth time
            end_limit = start_dt + datetime.timedelta(days=90 * 365.25)
            self._prune_dasha_tree(start_limit, end_limit)

    def _prune_dasha_tree(self, start_limit_utc, end_limit_utc):
        """
        NEW HELPER: Recursively prunes the Dasha tree to only show items
        that fall within the specified time window.
        """
        self._log_debug(f"Pruning Dasha tree for window: {start_limit_utc} to {end_limit_utc}")

        def parse_tree_date(date_str):
            try:
                # Naive datetime is fine here as we only care about the date part for pruning
                return datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                return None

        def prune_recursive(parent_id):
            # We must iterate over a copy of the children list as we are deleting from it
            for item_id in list(self.dasa_tree.get_children(parent_id)):
                values = self.dasa_tree.item(item_id, 'values')
                start_str, end_str = values[1], values[2]

                item_start_dt = parse_tree_date(start_str)
                item_end_dt = parse_tree_date(end_str)

                if not item_start_dt or not item_end_dt: continue

                # Convert limits to naive for direct comparison
                start_limit_naive = start_limit_utc.replace(tzinfo=None)
                end_limit_naive = end_limit_utc.replace(tzinfo=None)

                # Check for overlap: The period must start before the limit ends,
                # AND end after the limit starts.
                if item_end_dt < start_limit_naive or item_start_dt > end_limit_naive:
                    self.dasa_tree.delete(item_id)
                else:
                    # If the parent period overlaps, we must check its children
                    prune_recursive(item_id)

        # Start pruning from the top-level (Mahadashas)
        prune_recursive("")

    import datetime
    import pytz
    import swisseph as swe  # Assuming swisseph is installed and configured
    import logging
    import tkinter as tk  # Needed for messagebox if used
    from tkinter import messagebox  # Needed for messagebox if used

    # Assuming these are available from your broader application's constants/setup
    # Replace with your actual global constants or ensure they are imported/defined
    NAKSHATRA_SPAN_DEG = 13 + 20 / 60
    DASHA_PERIODS = {
        "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
        "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
    }
    LORD_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    ZODIAC_SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    ZODIAC_LORD_MAP = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }
    SWE_PLANET_NAMES = {
        swe.SUN: 'Sun', swe.MOON: 'Moon', swe.MARS: 'Mars', swe.MERCURY: 'Mercury',
        swe.JUPITER: 'Jupiter', swe.VENUS: 'Venus', swe.SATURN: 'Saturn',
        swe.MEAN_NODE: 'Rahu'
    }
    HOUSE_SYSTEMS = {
        "Placidus": b'P', "Koch": b'K', "Equal": b'E', "Regiomontanus": b'R', "Campanus": b'C'
    }
    ALL_INDIAN_CITIES = {
        'Mumbai': (19.0760, 72.8777), 'Delhi': (28.7041, 77.1025), 'Bangalore': (12.9716, 77.5946),
        'Kolkata': (22.5726, 88.3639), 'Chennai': (13.0827, 80.2707), 'Hyderabad': (17.3850, 78.4867)
    }
    STELLAR_PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']

    # Mock logger for standalone function (replace with your app's actual logger)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    _logger = logging.getLogger(__name__)

    import re  # Make sure this is imported at the top of your file or within the method's scope

    # This function belongs inside your AstrologyApp class
    def _run_final_sort(self):
        """
        Final Sort: Filters the current results based on stringent criteria.
        The results meeting these criteria are stored in `self.final_sort_base_results`.
        Then, `_apply_post_filters` is called to display them and enable post-sort filters.
        """
        self._log_debug("--- _run_final_sort: Start (Final Refinements Applied) ---")

        # 1. Prerequisites
        if not self.analysis_results_tree.get_children():
            messagebox.showinfo("Info", "No results to sort. Please run a full analysis first.")
            self._log_debug("Final Sort: No results in treeview. Exiting.")
            return
        if not self.rp_tree.get_children():
            messagebox.showinfo("Info",
                                "Ruling Planets are required for final sort. Please calculate them on the 'Ruling Planet' tab.")
            self._log_debug("Final Sort: Ruling Planets not calculated. Exiting.")
            return
        if not self.planet_classifications:
            messagebox.showerror("Error",
                                 "Planet classifications are missing. Please generate chart and click 'Check Promise' first.")
            self._log_debug("Final Sort: Planet classifications missing. Exiting.")
            return
        if not self.current_planetary_positions or not self.current_cuspal_positions:
            messagebox.showerror("Error",
                                 "Base chart data (planetary/cuspal positions) is missing. Please generate chart first.")
            self._log_debug("Final Sort: Base chart data missing. Exiting.")
            return

        # Get RP strengths from the RP tree
        rp_strengths = {
            values[1]: values[0] for item_id in self.rp_tree.get_children()
            if (values := self.rp_tree.item(item_id, 'values')) and len(values) > 1
        }
        self._log_debug(f"Final Sort: Available RP strengths: {rp_strengths}")

        # Define the acceptable RP strength categories for the 'via' planet (UNCHANGED)
        required_rp_strengths_for_via_planet = {"Strongest of Strongest", "Strongest", "Second Strong"}
        self._log_debug(
            f"Final Sort: Required 'via' Planet RP Strength Categories: {required_rp_strengths_for_via_planet}")

        # Define the acceptable RP strengths for Moon's TRANSIT lords (RELAXED)
        # They must be at least 'Second Strong'
        acceptable_rp_strengths_for_moon_transit_lords = {"Strongest of Strongest", "Strongest", "Second Strong"}
        self._log_debug(
            f"Final Sort: Moon's Transit Lords must be at least: {acceptable_rp_strengths_for_moon_transit_lords} RP.")

        # Get all actual Ruling Planets (their names) for easier lookup
        all_ruling_planet_names = set(rp_strengths.keys())
        self._log_debug(f"Final Sort: All identified Ruling Planet names: {all_ruling_planet_names}")

        # 2. Iterate through current displayed results and apply strict filter
        qualified_hits_for_final_sort = []
        total_hits_processed = 0

        # Get all items currently in the treeview to iterate over
        all_current_items_values = []
        for item_id in self.analysis_results_tree.get_children():
            all_current_items_values.append(self.analysis_results_tree.item(item_id, 'values'))

        self._log_debug(f"Final Sort: Processing {len(all_current_items_values)} hits from current display.")

        # Get current chart context (needed for dynamic Moon position calculation)
        city = self.city_combo.get()
        hsys_const = self._get_selected_hsys()
        original_primary_cusp_num_selected = self._get_original_primary_cusp_from_ui()
        if original_primary_cusp_num_selected is None:
            self._log_debug(
                "Final Sort: Original primary cusp not found, cannot apply classification-dependent rules. Exiting.")
            messagebox.showerror("Error",
                                 "Original primary cusp not found. Please ensure it's selected in 'Daily Analysis' tab.")
            return

        horary_num = int(self.horary_entry.get()) if self.horary_entry.get().isdigit() and (
                1 <= int(self.horary_entry.get()) <= 2193) else None
        local_tz = pytz.timezone(self.timezone_combo.get())

        for values in all_current_items_values:
            total_hits_processed += 1

            # Ensure the row has enough data for filtering (at least up to Remark column)
            if len(values) < 10:
                self._log_debug(f"  Skipping row {values}: insufficient columns for final sort analysis.")
                continue

            remark_text = values[9]  # 'Remark' column (e.g., "HIT at 18:28:00 via Rahu")
            transit_details_str = values[7]  # 'Transits' column
            hit_time_str = values[5]  # 'Start Time' column (e.g., "2025-07-31 00:00:00" or "31 Jul '25 00:00:00 AM")

            # Parse the precise hit time (local time string from UI to UTC datetime)
            hit_time_naive = None
            try:
                hit_time_naive = datetime.datetime.strptime(hit_time_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    hit_time_naive = datetime.datetime.strptime(hit_time_str, '%d %b \'%y %I:%M:%S %p')
                except ValueError:
                    self._log_debug(f"  FAILED to parse hit time string: {hit_time_str}. Skipping hit.")
                    continue

            hit_time_utc = local_tz.localize(hit_time_naive).astimezone(pytz.utc)
            self._log_debug(f"\n  Processing hit at {hit_time_str} (UTC: {hit_time_utc})...")

            # --- CRITERIA 1 & 2: 'Via' Planet (PC Sub Lord) Check ---
            linking_planet_name = None
            linking_planet_match = re.search(r'via\s+(\w+)', remark_text)
            if linking_planet_match:
                linking_planet_name = linking_planet_match.group(1)

            if not linking_planet_name or linking_planet_name == "N/A":
                self._log_debug(f"  FILTERED OUT: No valid 'via' planet found in Remark: '{remark_text}'.")
                continue

            planet_classification = self.planet_classifications.get(linking_planet_name, 'Unclassified')
            planet_rp_strength = rp_strengths.get(linking_planet_name, 'None')

            is_via_planet_positive = (planet_classification == 'Positive')
            is_via_planet_at_least_second_strong_rp = (planet_rp_strength in required_rp_strengths_for_via_planet)

            if not (is_via_planet_positive and is_via_planet_at_least_second_strong_rp):
                self._log_debug(
                    f"  FILTERED OUT: 'Via' planet '{linking_planet_name}' (Class: {planet_classification}, RP Strength: {planet_rp_strength}) does not meet criteria (Positive={is_via_planet_positive}, AtLeastSecondStrongRP={is_via_planet_at_least_second_strong_rp}).")
                continue

            self._log_debug(f"  PASSED: 'Via' planet '{linking_planet_name}' meets criteria.")

            # --- REMOVED CRITERIA: Moon's *Natal* SSL and Sookshma Lord Check ---
            # This logic has been intentionally removed as per the new requirements.

            # --- NEW/UPDATED CRITERIA: Moon's *Transit* SSL and Sookshma Lord Check at HIT time ---
            # Dynamically calculate chart data for the precise hit time
            dyn_planets_at_hit_time, _, _ = self._calculate_chart_data(hit_time_utc, city, hsys_const, horary_num)

            if not dyn_planets_at_hit_time or 'Moon' not in dyn_planets_at_hit_time:
                self._log_debug(
                    f"  FILTERED OUT: Could not get dynamic Moon data at hit time {hit_time_utc} for transit check.")
                continue

            transit_moon_lon_at_hit = dyn_planets_at_hit_time['Moon'][0]

            # Use the extended get_nakshatra_info to get all 5 lords of TRANSITING Moon
            _, _, _, transit_moon_ssl_at_hit, transit_moon_sookshma_at_hit = self.get_nakshatra_info(
                transit_moon_lon_at_hit)

            self._log_debug(
                f"  Transit Moon's Lords at Hit: SSL={transit_moon_ssl_at_hit}, Sookshma={transit_moon_sookshma_at_hit}")

            # Check Transit Moon's SSL: must be Positive AND in acceptable_rp_strengths_for_moon_transit_lords
            transit_moon_ssl_class = self.planet_classifications.get(transit_moon_ssl_at_hit, 'Unclassified')
            transit_moon_ssl_rp_strength = rp_strengths.get(transit_moon_ssl_at_hit, 'None')

            is_transit_moon_ssl_qualified = (
                    transit_moon_ssl_class == 'Positive' and
                    transit_moon_ssl_rp_strength in acceptable_rp_strengths_for_moon_transit_lords
            )
            # NEW EXCLUSION: If SSL is below acceptable strength, filter out.
            if not is_transit_moon_ssl_qualified:
                self._log_debug(
                    f"  FILTERED OUT: Transit Moon SSL '{transit_moon_ssl_at_hit}' (Class:{transit_moon_ssl_class}, RP:{transit_moon_ssl_rp_strength}) is not a Qualified RP.")
                continue

            # Check Transit Moon's Sookshma Lord: must be Positive AND in acceptable_rp_strengths_for_moon_transit_lords
            transit_moon_sookshma_class = self.planet_classifications.get(transit_moon_sookshma_at_hit, 'Unclassified')
            transit_moon_sookshma_rp_strength = rp_strengths.get(transit_moon_sookshma_at_hit, 'None')

            is_transit_moon_sookshma_qualified = (
                    transit_moon_sookshma_class == 'Positive' and
                    transit_moon_sookshma_rp_strength in acceptable_rp_strengths_for_moon_transit_lords
            )
            # NEW EXCLUSION: If Sookshma Lord is below acceptable strength, filter out.
            if not is_transit_moon_sookshma_qualified:
                self._log_debug(
                    f"  FILTERED OUT: Transit Moon Sookshma Lord '{transit_moon_sookshma_at_hit}' (Class:{transit_moon_sookshma_class}, RP:{transit_moon_sookshma_rp_strength}) is not a Qualified RP.")
                continue

            # If all above checks passed, add to qualified list
            qualified_hits_for_final_sort.append(values)
            self._log_debug(
                f"  PASSED: Hit at {values[5]} meets ALL Final Sort criteria (including Transit Moon's strong RPs).")

        # 3. Sort the qualified hits
        # Use a custom sort key: Higher RP strength for 'via' planet first, then by overall positivity score.
        rp_strength_priority = {"Strongest of Strongest": 3, "Strongest": 2, "Second Strong": 1,
                                "Derived": 0.5, "Other Base RP": 0.2, "None": 0}

        def get_final_sort_key(item_values):
            # Extract linking planet from Remark column (index 9) for sorting priority
            remark_text_for_sort = item_values[9]
            linking_planet_name_for_sort = None
            linking_planet_match_for_sort = re.search(r'via\s+(\w+)', remark_text_for_sort)
            if linking_planet_match_for_sort:
                linking_planet_name_for_sort = linking_planet_match_for_sort.group(1)

            rp_strength_for_sort = rp_strengths.get(linking_planet_name_for_sort, 'None')
            rp_priority_score = rp_strength_priority.get(rp_strength_for_sort, 0)

            # Use existing _calculate_positivity_score for secondary sort
            positivity_score = self._calculate_positivity_score(item_values)

            return (rp_priority_score, positivity_score)

        qualified_hits_for_final_sort.sort(key=get_final_sort_key, reverse=True)

        # 4. Clear and Repopulate Treeview (ONLY with strictly qualified hits)
        self._update_analysis_results_tree_columns("detailed_full_analysis")  # Clears existing entries

        if not qualified_hits_for_final_sort:
            self._log_debug("Final Sort: No hits remained after strict filtering. Displaying message.")
            messagebox.showinfo("Final Sort Complete",
                                "No events found that meet the highly strict 'Final Sort' criteria.")
            # Ensure post-filter checkboxes are disabled if no results
            self.ju_plus_cb.config(state='disabled')
            self.su_plus_cb.config(state='disabled')
            self.mo_plus_cb.config(state='disabled')
            self.reset_post_filters_button.config(state='disabled')
            # Clear stored base results as there are none
            self.final_sort_base_results = []
            return

        # Store the qualified results for potential post-filtering
        self.final_sort_base_results = qualified_hits_for_final_sort

        # Call the new post-filtering function to display results and enable checkboxes
        self._apply_post_filters()

        self._log_debug(
            "--- _run_final_sort: End (Success, Strictly Filtered Results Stored & Displayed by _apply_post_filters) ---")
        messagebox.showinfo("Final Sort Complete",
                            f"Successfully found and displayed {len(qualified_hits_for_final_sort)} highly favorable event(s).")

    def _filter_by_pc_sign_star(self):
        """
        Filters the analysis results based on the PC Sign Lord and Star Lord quality.
        It processes "HIT" results and filters them if PC's Sign Lord OR Star Lord
        (at the hit time) are classified as Positive or Neutral.

        ADDITION: Only keeps and displays "super-hits" where PC connected to ALL SCs.
        All other results are filtered out from the display.
        """
        self._log_debug("--- _filter_by_pc_sign_star: Start (Final Filtering applied) ---")

        # --- Initial Checks & Early Exits ---
        if not self.analysis_results_tree.get_children():
            self._log_debug("Filter by PC Sign/Star: No results in treeview. Returning.")
            messagebox.showinfo("Info", "Please run an analysis first to generate results.")
            return
        if not self.rp_tree.get_children():
            self._log_debug("Filter by PC Sign/Star: No RPs found. Returning.")
            messagebox.showinfo("Info", "Please calculate Ruling Planets first (on the 'Ruling Planet' tab).")
            return
        if not self.planet_classifications:
            self._log_debug("Filter by PC Sign/Star: Planet classifications not available. Returning.")
            messagebox.showerror("Error",
                                 "Planet classifications are not loaded. Please generate chart and then click 'Check Promise' first.")
            return

        # Disable the next button in the workflow ('Final Sort') at the start of this step
        if hasattr(self, 'final_sort_button'):
            self.final_sort_button.config(state="disabled")

        # --- Extract Current "HIT" Results from Treeview ---
        current_hits = []  # Will store dictionaries with parsed hit info
        self._log_debug("Filter by PC Sign/Star: Extracting HITs from analysis_results_tree.")
        for item_id in self.analysis_results_tree.get_children():
            values = self.analysis_results_tree.item(item_id, 'values')

            # Ensure row has enough columns for 'Remark' and 'Cuspal Link'
            if len(values) < 10:
                self._log_debug(f"  Skipping row {values}: not enough columns for HIT check.")
                continue

            remark_text = values[9]  # 'Remark' column
            cuspal_link_text = values[8]  # 'Cuspal Link' column

            if "HIT" in remark_text:
                self._log_debug(f"  Row identified as a HIT: Remark='{remark_text}'")
                try:
                    hit_time_str = values[5]  # 'Start Time' column
                    hit_time = None
                    # Try parsing various time formats
                    try:
                        hit_time = datetime.datetime.strptime(hit_time_str, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        hit_time = datetime.datetime.strptime(hit_time_str, '%d %b \'%y %I:%M:%S %p')

                    # Extract linking planet name from the Remark string (e.g., "HIT ... via [Planet]")
                    linking_planet_match = re.search(r'via\s+(\w+)', remark_text)
                    linking_planet = linking_planet_match.group(1) if linking_planet_match else "N/A"

                    # Extract actually linked SCs from the Cuspal Link string (e.g., "H7: Star Match; H9: Rahu Agency")
                    actual_linked_scs_for_hit = self._extract_linked_sc_nums_from_string(cuspal_link_text)

                    self._log_debug(
                        f"  Successfully parsed HIT time: {hit_time}, Linking planet: {linking_planet}, Linked SCs: {actual_linked_scs_for_hit}")

                    current_hits.append({
                        'time': hit_time,
                        'planet': linking_planet,  # The PC Sub Lord that initiated the interlink
                        'dasha_lords': list(values[0:5]),  # MD, AD, PD, SD, PrD
                        'original_row_values': values,  # Keep original values to reconstruct row later
                        'actual_linked_scs_for_hit': actual_linked_scs_for_hit
                        # New: Store the SCs actually linked in THIS hit
                    })
                except (ValueError, IndexError, AttributeError) as e:
                    self._log_debug(
                        f"  ERROR: Failed to parse or extract data from HIT row {values}: {e}. Skipping this row.")
                    continue
            else:
                self._log_debug(f"  Row is not a HIT: '{remark_text}'. Skipping.")

        if not current_hits:
            self._log_debug(
                "Filter by PC Sign/Star: No valid HITs extracted from treeview after initial scan. Returning.")
            messagebox.showerror("Error",
                                 "No valid 'HIT' results found in the table to filter by PC Sign/Star. Ensure previous steps generated proper HITs (check 'Remark' column).")
            return

        # --- Perform PC Sign/Star Lord Quality Check (Main Filtering Loop) ---
        progress_info = self._setup_progress_window("Filtering by PC Sign/Star...")
        passed_filter_results = []  # Hits that pass the PC Sign/Star Lord quality check

        primary_cusp_num = self._get_original_primary_cusp_from_ui()
        if primary_cusp_num is None:
            self._log_debug("Filter by PC Sign/Star: Primary Cusp not selected from UI. Returning.")
            if progress_info['window'].winfo_exists(): progress_info['window'].destroy()
            return

        # Use the adjusted primary cusp for analysis classification rules
        pc_for_analysis = self._determine_primary_cusp_for_analysis(primary_cusp_num)
        if pc_for_analysis is None:
            self._log_debug("Filter by PC Sign/Star: Adjusted PC for analysis is None. Returning.")
            if progress_info['window'].winfo_exists(): progress_info['window'].destroy()
            return

        self._log_debug(
            f"Filter by PC Sign/Star: Starting dynamic chart calculations for {len(current_hits)} hits. Primary Cusp for analysis: H{pc_for_analysis}.")
        start_time_process = datetime.datetime.now()

        # Get chart context from UI elements once for the loop (for efficiency)
        city = self.city_combo.get()
        hsys_const = self._get_selected_hsys()
        horary_num = int(self.horary_entry.get()) if self.horary_entry.get().isdigit() and (
                1 <= int(self.horary_entry.get()) <= 2193) else None

        for i, hit in enumerate(current_hits):
            # Update progress bar
            if progress_info and progress_info['window'].winfo_exists():
                self._update_progress(progress_info, i + 1, len(current_hits), start_time_process,
                                      f"Checking Hit {i + 1}/{len(current_hits)} at {hit['time'].strftime('%H:%M:%S')}")

            self._log_debug(f"\n  Processing HIT (Time: {hit['time']}, Planet: {hit['planet']}):")

            # Calculate dynamic chart data for the precise hit time
            dyn_planets, dyn_cusps, _ = self._calculate_chart_data(hit['time'], city, hsys_const, horary_num)

            if not dyn_cusps:
                self._log_debug(f"  ERROR: Dynamic cuspal data not generated for {hit['time']}. Skipping hit.")
                continue

            pc_data = dyn_cusps.get(pc_for_analysis)
            if not pc_data:
                self._log_debug(
                    f"  ERROR: PC data for H{pc_for_analysis} not found in dynamic cusps at {hit['time']}. Skipping hit.")
                continue

            pc_sign_lord = pc_data[2]  # Sign Lord of the Primary Cusp
            pc_star_lord = pc_data[3]  # Star Lord of the Primary Cusp
            self._log_debug(f"  Dynamic PC ({pc_for_analysis}) Sign Lord: {pc_sign_lord}, Star Lord: {pc_star_lord}")

            # Retrieve classifications for PC Sign Lord and Star Lord
            pc_sl_class = self.planet_classifications.get(pc_sign_lord, 'Unclassified')
            pc_starl_class = self.planet_classifications.get(pc_star_lord, 'Unclassified')
            self._log_debug(f"  PC SL Classification: {pc_sl_class}, PC StarL Classification: {pc_starl_class}")

            # --- CORE FILTERING CONDITION: AT LEAST ONE (PC SL or PC StarL) must be P/N ---
            is_pc_sl_favorable = (pc_sl_class in ['Positive', 'Neutral'])
            is_pc_starl_favorable = (pc_starl_class in ['Positive', 'Neutral'])

            if is_pc_sl_favorable or is_pc_starl_favorable:
                passed_filter_results.append(hit)  # Add the full hit data if it passes this filter
                self._log_debug(
                    f"  Hit at {hit['time']} PASSED PC Sign/Star filter: PC SL P/N ({is_pc_sl_favorable}) OR PC StarL P/N ({is_pc_starl_favorable}).")
            else:
                self._log_debug(
                    f"  Hit at {hit['time']} FILTERED OUT: Neither PC SL ({pc_sign_lord}, {pc_sl_class}) nor PC StarL ({pc_star_lord}, {pc_starl_class}) is P/N.")

        # Close progress window
        if progress_info['window'].winfo_exists():
            self._log_debug("Filter by PC Sign/Star: Progress window destroying.")
            progress_info['window'].destroy()

        if not passed_filter_results:
            self._log_debug(
                "Filter by PC Sign/Star: No hits remained after PC Sign/Star filtering. Displaying message.")
            messagebox.showinfo("Filter Complete", "No hits remained after filtering by PC Sign/Star Lord quality.")
            return

        # --- Identify "Super-Hits" (ALL Secondary Cusps linked) ---
        super_hits = []

        # Get the original secondary cusps selected by the user for the event query
        required_secondary_cusps_for_query = self._get_selected_secondary_cusps()
        self._log_debug(f"Required Secondary Cusps for event query: {required_secondary_cusps_for_query}")

        for hit in passed_filter_results:
            # This applies only if there ARE secondary cusps selected by the user.
            # And the hit's actual linked SCs must contain ALL required SCs.
            if required_secondary_cusps_for_query and \
                    required_secondary_cusps_for_query.issubset(hit['actual_linked_scs_for_hit']):
                super_hits.append(hit)
                self._log_debug(f"  Identified SUPER-HIT: {hit['time']} (all SCs linked).")
            else:
                self._log_debug(
                    f"  Hit at {hit['time']} did NOT qualify as a SUPER-HIT (not all SCs linked or no SCs required).")

        # --- Prepare for sorting and then populate Treeview ---
        # Sort super_hits by their positivity score
        rp_ranks = {
            vals[1]: vals[0] for item in self.rp_tree.get_children()
            if (vals := self.rp_tree.item(item, 'values')) and len(vals) > 1
        }
        strong_ranks_for_sorting = {"Strongest of Strongest", "Strongest"}

        def get_sort_score(hit_item):
            score = 0
            # Prioritize hits where the linking planet is a strong RP
            linking_planet = hit_item['planet']
            if rp_ranks.get(linking_planet) in strong_ranks_for_sorting and \
                    self.planet_classifications.get(linking_planet) == 'Positive':
                score += 1000  # Higher bonus for super strong RP (make it distinct from dasha/transit scores)
            elif self.planet_classifications.get(linking_planet) == 'Positive':
                score += 500  # Medium bonus for positive linking planet

            # Add general positivity score (dasha and transit)
            # The structure of `original_row_values` must match what _calculate_positivity_score expects.
            # Assuming values[0:5] for dasha and values[7:10] for transits.
            if len(hit_item['original_row_values']) >= 10:
                score += self._calculate_positivity_score(hit_item['original_row_values'])
            return score

        super_hits.sort(key=get_sort_score, reverse=True)

        # --- Update Results Treeview (ONLY SUPER-HITS ARE DISPLAYED NOW) ---
        self._update_analysis_results_tree_columns("detailed_full_analysis")  # Clears existing entries

        if not super_hits:
            self._log_debug("Filter by PC Sign/Star: No 'SUPER-HIT' events found. Displaying message.")
            messagebox.showinfo("Final Filter Complete",
                                "No 'SUPER-HIT' events (where all secondary cusps were linked) were found after applying all filters.")
            return

        # Insert super-hits first with a 'top_event' tag (green highlight)
        for i, hit in enumerate(super_hits):
            original_values_list = list(hit['original_row_values'])
            # Update the Remark column (index 9) to reflect this filter's success and "SUPER-HIT" status
            new_remark_content = f"PC SL/StarL OK | SUPER-HIT (All SCs Linked)"
            if len(original_values_list) > 9:
                original_values_list[9] = f"{original_values_list[9]} | {new_remark_content}"
            else:
                original_values_list.append(new_remark_content)  # Append if column didn't exist

            self.analysis_results_tree.insert("", "end", values=original_values_list, tags=('top_event',))
            self._log_debug(f"  Inserted SUPER-HIT into display: {original_values_list}")

        # Enable the next button in the workflow sequence: Final Sort button
        if hasattr(self, 'final_sort_button'):
            self.final_sort_button.config(state="normal")

        self._log_debug("--- _filter_by_pc_sign_star: End (Success, Super-Hits Displayed) ---")
        messagebox.showinfo("Final Filter Complete",
                            f"Successfully found and displayed {len(super_hits)} 'SUPER-HIT' event(s).")

    def _prune_dasha_tree_for_horary(self, query_time_utc):
        """NEW HELPER: Prunes the Dasha tree to show -10/+10 years for Horary charts."""
        self._log_debug("Pruning Dasha tree for Horary view (-10/+10 years).")
        start_limit = query_time_utc - datetime.timedelta(days=10 * 365.25)
        end_limit = query_time_utc + datetime.timedelta(days=10 * 365.25)

        def parse_tree_time(time_str):
            for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.datetime.strptime(time_str, fmt)
                except ValueError:
                    continue
            return None

        def prune_recursive(parent_id):
            # We must iterate over a copy of the children list as we are deleting from it
            for item_id in list(self.dasa_tree.get_children(parent_id)):
                values = self.dasa_tree.item(item_id, 'values')
                start_str, end_str = values[1], values[2]

                item_start_dt = parse_tree_time(start_str)
                item_end_dt = parse_tree_time(end_str)

                if not item_start_dt or not item_end_dt: continue

                # If the item's entire range is outside the window, delete it and its children
                if item_end_dt < start_limit or item_start_dt > end_limit:
                    self.dasa_tree.delete(item_id)
                else:
                    # If it overlaps, check its children
                    prune_recursive(item_id)

        # Start pruning from the top-level (Mahadashas)
        prune_recursive("")

    def _prune_dasha_tree_for_natal(self, birth_time_utc):
        """NEW HELPER: Prunes the Dasha tree to show 90 years for Natal charts."""
        self._log_debug("Pruning Dasha tree for Natal view (90 years).")
        end_limit = birth_time_utc + datetime.timedelta(days=90 * 365.25)

        def parse_tree_time(time_str):
            for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.datetime.strptime(time_str, fmt)
                except ValueError:
                    continue
            return None

        # Iterate over a copy of Mahadasha items
        for item_id in list(self.dasa_tree.get_children("")):
            start_str = self.dasa_tree.item(item_id, 'values')[1]
            item_start_dt = parse_tree_time(start_str)

            if item_start_dt and item_start_dt > end_limit:
                self.dasa_tree.delete(item_id)

    def _extract_linked_sc_nums_from_string(self, cuspal_link_text: str) -> set:
        """
        Parses the 'Cuspal Link' string (e.g., "Std. Link to H7; Rahu Agency to H9")
        and extracts the set of house numbers that were explicitly linked within it.
        """
        linked_houses = set()
        # Find all occurrences of "H" followed by one or more digits
        matches = re.findall(r'H(\d+)', cuspal_link_text)
        for num_str in matches:
            try:
                linked_houses.add(int(num_str))
            except ValueError:
                self._log_debug(f"Warning: Could not parse house number '{num_str}' from '{cuspal_link_text}'.")
                pass  # Ignore non-numeric matches
        return linked_houses

    def _get_planet_final_significators(self, planet_name, primary_cusp_num_selected,
                                         exclude_8_12_from_non_8_12_pc=True):
        """
        (CORRECTED) Returns the set of final significators (houses) for a given planet.
        This version has been simplified to remove the aggressive filtering of houses 8 and 12,
        which was causing planets to be incorrectly disqualified from Positive/Neutral status.
        The classification logic is now handled entirely within the _is_dasha_positive/neutral functions.

        Additionally, it now explicitly handles the special case where primary cusp is 8 or 12.
        """
        planet_data = self.stellar_significators_data.get(planet_name)
        if not planet_data or 'final_sigs' not in planet_data:
            self._log_debug(
                f"WARNING: No stellar significator data found for {planet_name} when getting final significators.")
            return set()

        final_sigs = set(planet_data['final_sigs'])

        # --- NEW LOGIC FOR RULE 2: Special case for Primary Cusp 8 or 12 ---
        # If the primary cusp chosen is 8 or 12, then 8 or 12 should be considered positive
        # and should NOT be excluded from final significators for any planet.
        if exclude_8_12_from_non_8_12_pc: # This flag controls the original exclusion behavior
            if primary_cusp_num_selected in [8, 12]:
                # If PC is 8 or 12, do not exclude 8 or 12 from *any* planet's significators.
                # The existing logic should already be returning the full set, so no explicit
                # removal of exclusion is needed here if `_apply_negation_logic` already doesn't
                # prematurely filter these based on the primary_cusp context.
                # Since the original change was to *remove* general 8/12 filtering from here,
                # this method now primarily returns the core final significators.
                pass # The removal of general 8/12 exclusion already achieves this.
            else:
                # If primary cusp is NOT 8 or 12, then the traditional exclusion for 8 and 12 (if they were
                # part of *some* negation logic that resulted in their removal from final_sigs) would apply.
                # However, the previous changes removed aggressive filtering *here*.
                # The logic for whether 8 or 12 is 'negative' is now handled in `_is_dasha_positive`/`_is_dasha_neutral`.
                # So, this function should simply return the raw final_sigs as calculated from `_apply_negation_logic`.
                pass # No additional filtering here.

        self._log_debug(f"  Returning final significators for {planet_name} (PC: {primary_cusp_num_selected}): {sorted(list(final_sigs))}")
        return final_sigs

    def _get_combined_significators_for_lords_static(self, lords_list, original_primary_cusp_num_selected):
        """
        Calculates the combined set of static final significators for a list of lords.
        Applies the Rule 2 filtering for each individual lord's significators.

        Args:
            lords_list (list): A list of planet names (strings) that are Dasha lords.
            original_primary_cusp_num_selected (int): The primary cusp number used for Rule 2 filtering.

        Returns:
            set: A set of combined house numbers.
        """
        combined_sigs = set()
        self._log_debug(f"  Combining static significators for lords: {lords_list}")
        for lord in lords_list:
            # Use _get_planet_final_significators which applies Rule 2 filtering
            # We pass exclude_8_12_from_non_8_12_pc=True as this is for the *dasha lord* classification
            lord_sigs = self._get_planet_final_significators(lord, original_primary_cusp_num_selected,
                                                              exclude_8_12_from_non_8_12_pc=True)
            combined_sigs.update(lord_sigs)
            self._log_debug(
                f"    {lord}'s final sigs: {sorted(list(lord_sigs))}. Current combined: {sorted(list(combined_sigs))}")
        return combined_sigs

    def _get_planet_cuspal_connections(self, planet_name, planets_with_ps):
        """
        HELPER: Gets the set of cusps a planet is directly connected to.
        A planet is 'connected' to a cusp if:
        1. It is one of the four lords (Sign, Star, Sub, SSL) of that cusp.
        2. It has Positional Status (PS) and is located by degree in that cusp.
        This function checks the planet itself, not its star or sub lord.
        """
        connected_cusps = set()
        if not planet_name or planet_name not in self.current_planetary_positions:
            return connected_cusps

        # Check direct lordships
        for cusp_num, cusp_data in self.current_cuspal_positions.items():
            if planet_name in cusp_data[2:]:
                connected_cusps.add(cusp_num)

        # Check positional placement if the planet has Positional Status
        if planet_name in planets_with_ps:
            planet_lon = self.current_planetary_positions[planet_name][0]
            house_of_position = self._get_house_of_degree(planet_lon, self.current_cuspal_positions)
            if house_of_position:
                connected_cusps.add(house_of_position)

        return connected_cusps

    def _is_dasha_positive(self, dasha_lord_name, primary_cusp_num, ascendant_house_num,
                           original_primary_cusp_num_selected):
        """
        Positive Dasha: A Dasha lord is classified as Positive if it meets any of the following conditions:
        1. Special Rule (PC 8 or 12): If primary cusp is 8 or 12, and the planet signifies 8 or 12 (or both).
        2. Special Rule (PC 6 for Disease/Sick Event): If primary cusp is 6 for a disease/sick event, and the planet signifies 8 or 12 (or both).
        3. Strong Positive (PC, 11th from PC, 12th from PC): Signifies Primary Cusp, 11th from PC, AND 12th from PC.
        4. NEW RULE (PC & All Secondary Cusps): Signifies Primary Cusp AND ALL selected secondary cusps.
        5. General Positive (PC + supportive houses): Signifies Primary Cusp AND (2nd/3rd from PC OR 11th from Asc).

        Args:
            dasha_lord_name (str): The name of the planet being classified.
            primary_cusp_num (int): The primary cusp number (potentially adjusted by Rule 1).
            ascendant_house_num (int): The house number of the ascendant (usually 1).
            original_primary_cusp_num_selected (int): The primary cusp number initially selected by the user.

        Returns:
            tuple: (bool: True if positive, False otherwise, str: detailed reason)
        """
        # Retrieve the full set of final significators for the planet.
        # It's crucial not to filter out 8/12 here, as the classification rules decide their meaning.
        dasha_lord_sigs = self._get_planet_final_significators(dasha_lord_name,
                                                               original_primary_cusp_num_selected,
                                                               exclude_8_12_from_non_8_12_pc=False)
        details = []
        self._log_debug(
            f"  Checking POSITIVE status for {dasha_lord_name}. Sigs: {sorted(list(dasha_lord_sigs))}. PC: {primary_cusp_num}")

        # Get the currently selected secondary cusps (dynamically, as they can change)
        current_secondary_cusp_nums = self._get_selected_secondary_cusps()

        # --- 1. SPECIAL RULE: If primary cusp chosen is 8 or 12 ---
        if primary_cusp_num in [8, 12]:
            if 8 in dasha_lord_sigs or 12 in dasha_lord_sigs:
                details.append(
                    f"Positive by special rule: Primary Cusp is {primary_cusp_num} and signifies 8 ({8}) or 12 ({12}) or both (for harm to ascendant, hospitalization, etc.).")
                self._log_debug(f"  {dasha_lord_name} IS Positive (PC 8/12 special rule).")
                return True, " ".join(details)
            # If primary cusp is 8 or 12, but the planet doesn't signify 8 or 12, it fails this specific rule.
            # It might still be positive by other rules, so don't return False yet.
            details.append(
                f"Not Positive by special rule: Primary Cusp is {primary_cusp_num}, but does not signify 8 or 12.")

        # --- 2. SPECIAL RULE: If primary cusp chosen is 6 AND event is disease/sick related ---
        event_type_text = self.event_type_combo.get().lower()
        is_disease_event = "disease" in event_type_text or "sick" in event_type_text

        if is_disease_event and primary_cusp_num == 6:  # Only applies if PC is explicitly 6 and it's a disease event
            self._log_debug(f"  Disease event (PC 6) detected. Applying special Positive rule for {dasha_lord_name}.")
            # The rule states: "any planet which has 8 or 12 or both will be considered positive."
            if 8 in dasha_lord_sigs or 12 in dasha_lord_sigs:
                details.append(
                    f"Positive due to disease exception (PC 6): signifies 8 ({8}) or 12 ({12}) or both, indicating support for serious disease/hospitalization for current disease.")
                self._log_debug(f"  {dasha_lord_name} IS Positive (Disease Exception).")
                return True, " ".join(details)
            details.append(f"Disease event (PC 6), but does not signify 8 or 12 to support the disease.")

        # --- 3. STRONG POSITIVE: Primary Cusp, 11th from PC, and 12th from PC ---
        eleventh_from_primary_cusp = self._get_relative_house(primary_cusp_num, 10)  # 11th from PC
        twelfth_from_primary_cusp = self._get_relative_house(primary_cusp_num, 11)  # 12th from PC

        if (primary_cusp_num in dasha_lord_sigs and
                eleventh_from_primary_cusp in dasha_lord_sigs and
                twelfth_from_primary_cusp in dasha_lord_sigs):
            details.append(
                f"Signifies Primary Cusp ({primary_cusp_num}), 11th from PC ({eleventh_from_primary_cusp}), AND 12th from PC ({twelfth_from_primary_cusp}). Classified as Positive by specific rule.")
            self._log_debug(f"  {dasha_lord_name} IS Positive (Strong Rule: PC, 11PC, 12PC).")
            return True, " ".join(details)

        # --- 4. NEW RULE: If planet signifies Primary Cusp AND ALL Secondary Cusps ---
        # First, ensure it signifies the primary cusp, as this is a fundamental requirement
        if primary_cusp_num not in dasha_lord_sigs:
            details.append(f"Does not signify Primary Cusp ({primary_cusp_num}).")
            self._log_debug(f"  {dasha_lord_name} NOT Positive: PC not signified for general rules.")
            return False, " ".join(details)  # If PC is not signified, it cannot be Positive by general rules

        # Now check if it signifies ALL selected secondary cusps
        if current_secondary_cusp_nums:  # Only apply if there are secondary cusps selected
            all_secondary_cusps_signified = all(sc_num in dasha_lord_sigs for sc_num in current_secondary_cusp_nums)
            if all_secondary_cusps_signified:
                details.append(
                    f"Positive: Signifies Primary Cusp ({primary_cusp_num}) AND ALL selected secondary cusps ({sorted(list(current_secondary_cusp_nums))}).")
                self._log_debug(f"  {dasha_lord_name} IS Positive (NEW RULE: PC & ALL SCs).")
                return True, " ".join(details)
            else:
                missing_scs = [sc for sc in current_secondary_cusp_nums if sc not in dasha_lord_sigs]
                details.append(f"Does not signify all selected secondary cusps (missing: {sorted(missing_scs)}).")
        else:  # If no secondary cusps are selected, this rule is implicitly not met/not applicable in this way.
            details.append("No secondary cusps selected for 'all secondary cusps' rule evaluation.")

        # --- 5. GENERAL POSITIVE LOGIC ---
        # At this point, we know PC is signified (due to earlier check)
        # And the stronger rules (1-4) were not met.
        details.append(f"Signifies Primary Cusp ({primary_cusp_num}).")  # Re-add PC signification detail.

        sec_positive_houses_relative_to_PC = {
            self._get_relative_house(primary_cusp_num, 1),  # 2nd from PC
            self._get_relative_house(primary_cusp_num, 2)  # 3rd from PC
        }
        eleventh_from_asc = self._get_relative_house(ascendant_house_num, 10)  # 11th from Asc

        signifies_2_or_3_from_pc = any(h in dasha_lord_sigs for h in sec_positive_houses_relative_to_PC)
        signifies_11_from_asc = eleventh_from_asc in dasha_lord_sigs

        if signifies_2_or_3_from_pc:
            s_houses = [str(h) for h in sec_positive_houses_relative_to_PC if h in dasha_lord_sigs]
            details.append(f"Signifies 2nd/3rd to PC ({', '.join(s_houses)}).")
        if signifies_11_from_asc:
            details.append(f"Signifies 11th from Ascendant ({eleventh_from_asc}).")

        # The core condition for this general positivity rule
        is_general_positive = (signifies_2_or_3_from_pc or signifies_11_from_asc)

        if is_general_positive:
            negation_cusp_to_primary = self._get_relative_house(primary_cusp_num,
                                                                11)  # 12th from PC (or previous cusp).
            if negation_cusp_to_primary in dasha_lord_sigs:
                details.append(f"Also signifies PC's negation cusp ({negation_cusp_to_primary}).")
            self._log_debug(f"  {dasha_lord_name} IS Positive (General Rule).")
            return True, " ".join(details)
        else:
            details.append(
                "Lacks sufficient supportive house significations (2nd/3rd to PC, or 11th to Asc) to be strictly positive by general rule.")
            self._log_debug(f"  {dasha_lord_name} NOT Positive: Lacks general supportive houses.")
            return False, " ".join(details)

    def _is_dasha_neutral(self, dasha_lord_name, primary_cusp_num, ascendant_house_num,
                           original_primary_cusp_num_selected):
        """
        UPDATED DEFINITION of Neutral Dasha:
        - Incorporates new specific rule: If a planet does not signify PC, PC-1,
          and any Secondary Cusps, it's Neutral. (No RP check in this phase)
        - General Rule: A planet is Neutral if it does NOT signify PC AND does NOT signify PC-1.
        - EXCEPTION for PC=2: The rule for PC-1 (i.e., Cusp 1) is ignored. A planet is Neutral
          if it simply does NOT signify PC 2.

        - NEW RULE (Primary Cusp 8 or 12 neutrality): If primary cusp is 8, but a planet does not have 8 in its final significator but has 12, then the planet is considered neutral. Same when Primary cusp is 12, but a planet does not have 12 but has 8 in its final significator, then the planet is also neutral.
        - NEW RULE (Growth Houses): If primary cusp is absent but signifies PC's growth houses (2nd, 3rd, 11th).
        """
        dasha_lord_sigs = self._get_planet_final_significators(dasha_lord_name, original_primary_cusp_num_selected, exclude_8_12_from_non_8_12_pc=False)
        details = []
        self._log_debug(
            f"  Checking NEUTRAL status for {dasha_lord_name} (PC={primary_cusp_num}). Sigs: {sorted(list(dasha_lord_sigs))}")

        # Calculate relevant cusps (PC-1, 11th from PC, 12th from PC, etc.)
        negating_cusp = primary_cusp_num - 1
        if negating_cusp == 0:
            negating_cusp = 12 # Wrap around for Cusp 1 (PC 12 -> PC-1 = 11)

        eleventh_from_primary_cusp = self._get_relative_house(primary_cusp_num, 10) # 11th from PC
        twelfth_from_primary_cusp = self._get_relative_house(primary_cusp_num, 11) # 12th from PC
        eighth_from_primary_cusp = self._get_relative_house(primary_cusp_num, 7)    # 8th from PC
        twelfth_from_asc = self._get_relative_house(ascendant_house_num, 11)        # 12th from Asc

        signifies_pc = primary_cusp_num in dasha_lord_sigs
        signifies_pc_minus_1 = negating_cusp in dasha_lord_sigs # Check if PC-1 is signified
        signifies_11_from_pc = eleventh_from_primary_cusp in dasha_lord_sigs
        signifies_12_from_pc = twelfth_from_primary_cusp in dasha_lord_sigs

        # Get selected secondary cusps for other neutrality rules
        selected_secondary_cusp_nums = self._get_selected_secondary_cusps()
        signifies_any_secondary_cusp = any(sc in dasha_lord_sigs for sc in selected_secondary_cusp_nums)

        # --- Priority 1: Check if it's Positive by any rule (should be handled by _is_dasha_positive first) ---
        # (This check is implicitly assumed to have happened by the calling _cache_static_planet_classifications sequence)

        # --- Priority 2: SPECIAL NEUTRAL RULE for Primary Cusp 8 or 12 ---
        if primary_cusp_num == 8:
            if 8 not in dasha_lord_sigs and 12 in dasha_lord_sigs:
                details.append(f"Neutral by special rule: Primary Cusp is 8, signifies 12 ({12}) but not 8 ({8}).")
                self._log_debug(f"  {dasha_lord_name} IS Neutral (PC 8 special case).")
                return True, " ".join(details)
        elif primary_cusp_num == 12:
            if 12 not in dasha_lord_sigs and 8 in dasha_lord_sigs:
                details.append(f"Neutral by special rule: Primary Cusp is 12, signifies 8 ({8}) but not 12 ({12}).")
                self._log_debug(f"  {dasha_lord_name} IS Neutral (PC 12 special case).")
                return True, " ".join(details)

        # --- Priority 3: Neutral by (11PC, 12PC, but NOT PC) rule ---
        if signifies_11_from_pc and signifies_12_from_pc and not signifies_pc:
            details.append(f"Neutral: Signifies 11th from PC ({eleventh_from_primary_cusp}) AND 12th from PC ({twelfth_from_primary_cusp}), but NOT Primary Cusp. Classified as 'Neutral' by specific rule.")
            self._log_debug(f"  {dasha_lord_name} IS Neutral (Rule: 11PC, 12PC, !PC).")
            return True, " ".join(details)

        # --- Priority 4: If it signifies PC, it's not neutral (unless a special neutral rule above applied) ---
        if signifies_pc:
            details.append(f"Signifies Primary Cusp ({primary_cusp_num}).")
            self._log_debug(f"  {dasha_lord_name} is NOT Neutral (Signifies PC and not caught by special neutral rules).")
            return False, " ".join(details)

        # --- From here on, we know the planet DOES NOT signify Primary Cusp. ---

        # --- Priority 5: SPECIAL EXCEPTION for PC = 2 ---
        if primary_cusp_num == 2:
            details.append("Neutral: Does not signify PC (2). Rule for Cusp 1 (PC-1) is ignored as per exception for PC 2.")
            self._log_debug(f"  {dasha_lord_name} IS Neutral (Special rule for PC 2).")
            return True, " ".join(details)

        # --- From here on, we know:
        #      - It DOES NOT signify Primary Cusp.
        #      - The Primary Cusp is NOT 2.

        # --- Priority 6: NEW RULE: If PC is absent but signifies growth houses (2nd, 3rd, 11th from PC) ---
        # This is the rule you specifically asked to add, and it was missing in the code you shared.
        growth_houses_for_pc = {
            self._get_relative_house(primary_cusp_num, 1),  # 2nd from PC
            self._get_relative_house(primary_cusp_num, 2),  # 3rd from PC
            self._get_relative_house(primary_cusp_num, 10) # 11th from PC
        }
        signifies_any_growth_house = any(h in dasha_lord_sigs for h in growth_houses_for_pc)

        if signifies_any_growth_house:
            growth_houses_present = [str(h) for h in growth_houses_for_pc if h in dasha_lord_sigs]
            details.append(f"Neutral: Primary Cusp absent, but signifies growth houses: {', '.join(growth_houses_present)}.")
            self._log_debug(f"  {dasha_lord_name} IS Neutral (NEW RULE: !PC && Growth Houses).")
            return True, " ".join(details)
        else:
            # If this rule is not met, add a detail for debugging and let it fall through to the next priority.
            details.append("Does not signify PC's growth houses (2nd, 3rd, 11th from PC).")


        # --- Priority 7: NEW USER RULE for Neutrality (!PC && !PC-1 && !SCs) ---
        # This was Priority 5 in your previous code.
        if not signifies_pc_minus_1 and not signifies_any_secondary_cusp:
            details.append(f"Neutral: Does not signify PC ({primary_cusp_num}), PC-1 ({negating_cusp}), or any selected secondary cusps.")
            self._log_debug(f"  {dasha_lord_name} IS Neutral (New User Rule: !PC && !PC-1 && !SCs).")
            return True, " ".join(details)
        else:
            # Add details if it fails this specific rule (for a better trace if not Neutral)
            if signifies_pc_minus_1: details.append(f"Signifies PC-1 cusp ({negating_cusp}).")
            if signifies_any_secondary_cusp: details.append(f"Signifies some secondary cusps ({[sc for sc in selected_secondary_cusp_nums if sc in dasha_lord_sigs]}).")


        # --- Priority 8: Fallback to general PC-1 check if not caught by new user rule ---
        # This was Priority 6 in your previous code.
        if signifies_pc_minus_1:
            details.append(f"Signifies PC-1 cusp ({negating_cusp}).")
            self._log_debug(f"  {dasha_lord_name} is NOT Neutral (Signifies PC-1 cusp).")
            return False, " ".join(details)


        # --- Priority 9: Original "Additional Neutrality Rule" (no 8th or 12th from PC/Asc) ---
        # This was Priority 7 in your previous code.
        signifies_12th_from_general = signifies_12_from_pc or (twelfth_from_asc in dasha_lord_sigs)
        signifies_8th_from_general = eighth_from_primary_cusp in dasha_lord_sigs

        if not signifies_8th_from_general and not signifies_12th_from_general:
            details.append("Neutral: Meets neutrality rule (no 8th or 12th house significations from PC/Asc).")
            self._log_debug(f"  {dasha_lord_name} IS Neutral (Additional Rule).")
            return True, " ".join(details)
        else:
            # If it *does* signify 8th or 12th from PC/Asc, then it's NOT neutral by this rule.
            if signifies_12_from_pc: details.append(f"Signifies 12th from PC ({twelfth_from_primary_cusp}).")
            if (twelfth_from_asc in dasha_lord_sigs): details.append(f"Signifies 12th from Asc ({twelfth_from_asc}).")
            if eighth_from_primary_cusp in dasha_lord_sigs: details.append(f"Signifies 8th from PC ({eighth_from_primary_cusp}).")
            self._log_debug(f"  {dasha_lord_name} is NOT Neutral (has 8th/12th from PC/Asc).")
            return False, " ".join(details)

        self._log_debug(f"  {dasha_lord_name} is UNCLASSIFIED by Neutral rules (fell through all conditions).")
        return False, "Unclassified by Neutral rules (should not happen)."


    def _is_dasha_negative(self, dasha_lord_name, primary_cusp_num, ascendant_house_num,
                           original_primary_cusp_num_selected):
        """
        Negative Dasha: If a Dasha planet signifies no primary cusp and
        only 12th from primary cusp and or 12th from secondary cusps then the dasha is said to be negative.
        """
        dasha_lord_sigs = self._get_planet_final_significators(dasha_lord_name, original_primary_cusp_num_selected)
        details = []
        self._log_debug(
            f"  Checking NEGATIVE status for {dasha_lord_name}. Sigs: {sorted(list(dasha_lord_sigs))}. PC: {primary_cusp_num}")

        if primary_cusp_num in dasha_lord_sigs:
            details.append(f"Signifies Primary Cusp ({primary_cusp_num}) (not negative).")
            self._log_debug(f"  {dasha_lord_name} is NOT Negative: Signifies Primary Cusp.")
            return False, " ".join(details)
        details.append("Does not signify Primary Cusp.")

        twelfth_from_primary_cusp = self._get_relative_house(primary_cusp_num, 11)
        twelfth_from_asc = self._get_relative_house(ascendant_house_num, 11)

        signifies_main_negative = False
        negative_details_list = []
        if twelfth_from_primary_cusp in dasha_lord_sigs:
            signifies_main_negative = True
            negative_details_list.append(f"Signifies 12th from Primary Cusp ({twelfth_from_primary_cusp}).")
        if twelfth_from_asc in dasha_lord_sigs:
            signifies_main_negative = True
            negative_details_list.append(f"Signifies 12th from Ascendant ({twelfth_from_asc}).")

        if not signifies_main_negative:
            details.append("Does not signify 12th from Primary Cusp or 12th from Ascendant.")
            self._log_debug(f"  {dasha_lord_name} is NOT Negative: No 12th related significations.")
            return False, " ".join(details)
        details.extend(negative_details_list)

        # "only 12th from primary cusp and or 12th from secondary cusps"
        # This implies no other "beneficial/neutral" cusps should be signified.

        negative_consideration_cusps = {
            twelfth_from_primary_cusp,
            twelfth_from_asc,
        }

        for h in dasha_lord_sigs:
            if h not in negative_consideration_cusps:
                details.append(f"Signifies other houses (e.g., {h}), thus not 'only' negative.")
                self._log_debug(f"  {dasha_lord_name} is NOT Negative: Signifies non-12th negative houses (e.g. {h}).")
                return False, " ".join(details)

        self._log_debug(f"  {dasha_lord_name} IS Negative.")
        return True, " ".join(details)

    def _check_pandemic_rule(self, planetary_positions, cuspal_positions, jul_day, current_ayan_value):
        """
        Calculates a comprehensive risk score for Pandemics based on various astrological rules.

        Rules incorporated:
        - Moon Affliction: Moon tightly afflicted by malefics (Saturn, Rahu, Pluto, Uranus) (within ~6°). (+2 per affliction)
        - Lunar Phases: Proximity to New or Full Moon. (+1)
        - Nodes Activation: Rahu/Ketu tightly conjunct Moon or angular cusps (1st, 4th, 7th, 10th). (+2 per conjunction)
        - Outer Planet Tensions:
            - Neptune with Mercury or Moon tight aspect. (+2)
            - Uranus/Saturn or Uranus/Mars hard aspect. (+2)
            - Mars–Pluto hard aspect. (+3)
            - Saturn/Pluto square. (+3)
        - KP/Vedic Sub-Lord Confirmation: Moon's or Ascendant's Sub-lord signifying 6th/8th/12th houses. (+2 per signification)
        - Nodes Compromising Angular Houses: (Covered by Nodes Activation)

        Args:
            planetary_positions (dict): Current planetary positions (sidereal).
            cuspal_positions (dict): Current cuspal positions (sidereal).
            jul_day (float): Julian Day for outer planet calculation.
            current_ayan_value (float): Ayanamsha value for outer planet calculation.

        Returns:
            tuple: (total_risk_score: int, details: list of str)
        """
        score = 0
        details = []

        # --- Helper functions (re-defined locally for clarity within this function) ---
        def get_sidereal_lon(planet_name_str):
            planet_data = planetary_positions.get(planet_name_str)
            if planet_data and isinstance(planet_data, (list, tuple)) and len(planet_data) > 0:
                return planet_data[0]  # Sidereal degree is at index 0
            return None

        def get_cusp_sidereal_lon(cusp_num):
            cusp_data = cuspal_positions.get(cusp_num)
            if cusp_data and isinstance(cusp_data, (list, tuple)) and len(cusp_data) > 0:
                return cusp_data[0]  # Sidereal degree is at index 0
            return None

        def get_aspect_orb(lon1, lon2):
            if lon1 is None or lon2 is None:
                return float('inf')  # Indicate invalid input
            angle = abs((lon1 - lon2 + 180) % 360 - 180)
            return angle

        # Function to check for hard aspects (conjunction, square, opposition)
        def is_hard_aspect(orb, tolerance=6):
            return orb < tolerance or \
                (abs(orb - 90) < tolerance) or \
                (abs(orb - 180) < tolerance)

        # Function to get outer planet sidereal longitude using swe.calc_ut
        def get_outer_planet_sidereal_lon(planet_id_swe):
            try:
                lon_trop, _ = swe.calc_ut(jul_day, planet_id_swe)
                return (lon_trop - current_ayan_value) % 360
            except Exception as e:
                self._log_debug(f"Could not calculate {planet_id_swe} position: {e}")
                return None

        self._log_debug("--- Checking Pandemic Rules ---")

        # Get all necessary planet and cusp longitudes
        moon_lon = get_sidereal_lon('Moon')
        mars_lon = get_sidereal_lon('Mars')
        saturn_lon = get_sidereal_lon('Saturn')
        rahu_lon = get_sidereal_lon('Rahu')
        ketu_lon = get_sidereal_lon('Ketu')
        mercury_lon = get_sidereal_lon('Mercury')
        sun_lon = get_sidereal_lon('Sun')  # for moon phases

        uranus_lon = get_outer_planet_sidereal_lon(swe.URANUS)
        neptune_lon = get_outer_planet_sidereal_lon(swe.NEPTUNE)
        pluto_lon = get_outer_planet_sidereal_lon(swe.PLUTO)

        # --- Rule 1: Moon Affliction & Lunar Phases ---
        if moon_lon is not None:
            moon_affliction_hits = []
            # Malefics to check for Moon affliction (inner + outer)
            moon_malefics_to_check = {
                'Saturn': saturn_lon, 'Rahu': rahu_lon, 'Ketu': ketu_lon,
                'Pluto': pluto_lon, 'Uranus': uranus_lon
            }
            for malefic_name, malefic_lon in moon_malefics_to_check.items():
                if malefic_lon is not None:
                    orb = get_aspect_orb(moon_lon, malefic_lon)
                    if orb < 6:  # Tight affliction
                        score += 2
                        moon_affliction_hits.append(f"Moon–{malefic_name} ({orb:.1f}° orb).")
            if moon_affliction_hits:
                details.append("Moon Afflictions: " + " & ".join(moon_affliction_hits))
                self._log_debug(f"Moon affliction risk added: {moon_affliction_hits}")

            # Lunar Phases (New or Full Moon)
            if sun_lon is not None:
                sun_moon_orb = get_aspect_orb(sun_lon, moon_lon)
                if sun_moon_orb < 5:  # New Moon (conjunction)
                    score += 1
                    details.append(f"New Moon phase detected ({sun_moon_orb:.1f}° orb Sun-Moon).")
                elif abs(sun_moon_orb - 180) < 5:  # Full Moon (opposition)
                    score += 1
                    details.append(f"Full Moon phase detected ({sun_moon_orb:.1f}° orb Sun-Moon).")
            self._log_debug(f"Moon phase check: Sun-Moon orb {sun_moon_orb:.1f}")
        else:
            self._log_debug("Moon longitude not available for Moon Affliction/Phase check.")

        # --- Rule 2: Nodes (Rahu/Ketu) activated, especially conj. Moon or angles ---
        node_activation_hits = []
        angular_cusps_lons = {1: get_cusp_sidereal_lon(1), 4: get_cusp_sidereal_lon(4),
                              7: get_cusp_sidereal_lon(7), 10: get_cusp_sidereal_lon(10)}

        if rahu_lon is not None and ketu_lon is not None:
            # Conj. Moon
            if moon_lon is not None:
                if get_aspect_orb(rahu_lon, moon_lon) < 6:
                    score += 2
                    node_activation_hits.append(f"Rahu–Moon Conjunction.")
                if get_aspect_orb(ketu_lon, moon_lon) < 6:
                    score += 2
                    node_activation_hits.append(f"Ketu–Moon Conjunction.")
            # Conj. Angles
            for cusp_num, cusp_lon in angular_cusps_lons.items():
                if cusp_lon is not None:
                    if get_aspect_orb(rahu_lon, cusp_lon) < 5:
                        score += 2
                        node_activation_hits.append(
                            f"Rahu near H{cusp_num} ({get_aspect_orb(rahu_lon, cusp_lon):.1f}°).")
                    if get_aspect_orb(ketu_lon, cusp_lon) < 5:
                        score += 2
                        node_activation_hits.append(
                            f"Ketu near H{cusp_num} ({get_aspect_orb(ketu_lon, cusp_lon):.1f}°).")
        if node_activation_hits:
            details.append("Nodes Activation: " + " & ".join(node_activation_hits))
            self._log_debug(f"Nodes activation risk added: {node_activation_hits}")

        # --- Rule 3: Outer planet tensions ---
        outer_tension_hits = []

        # Neptune with Mercury or Moon (misinformation/confusion)
        if neptune_lon is not None:
            if mercury_lon is not None:
                if get_aspect_orb(neptune_lon, mercury_lon) < 6:  # Conjunction/tight aspect
                    score += 2
                    outer_tension_hits.append(f"Neptune–Mercury tight aspect.")
            if moon_lon is not None:
                if get_aspect_orb(neptune_lon, moon_lon) < 6:
                    score += 2
                    outer_tension_hits.append(f"Neptune–Moon tight aspect.")

        # Uranus/Saturn or Uranus/Mars (crisis management vs. sudden break)
        if uranus_lon is not None:
            if saturn_lon is not None:
                if is_hard_aspect(get_aspect_orb(uranus_lon, saturn_lon), tolerance=6):
                    score += 2
                    outer_tension_hits.append(f"Uranus–Saturn hard aspect.")
            if mars_lon is not None:
                if is_hard_aspect(get_aspect_orb(uranus_lon, mars_lon), tolerance=6):
                    score += 2
                    outer_tension_hits.append(f"Uranus–Mars hard aspect.")

        # Mars–Pluto aspects (power-driven escalation)
        if mars_lon is not None and pluto_lon is not None:
            if is_hard_aspect(get_aspect_orb(mars_lon, pluto_lon), tolerance=6):
                score += 3  # Potent
                outer_tension_hits.append(f"Mars–Pluto hard aspect.")

        # Saturn/Pluto squares (structural collapse, lockdown)
        if saturn_lon is not None and pluto_lon is not None:
            orb = get_aspect_orb(saturn_lon, pluto_lon)
            if abs(orb - 90) < 6:  # Check for square aspect
                score += 3  # Very potent
                outer_tension_hits.append(f"Saturn–Pluto square ({orb:.1f}°).")

        if outer_tension_hits:
            details.append("Outer Planet Tensions: " + " & ".join(outer_tension_hits))
            self._log_debug(f"Outer planet tension risk added: {outer_tension_hits}")

        # --- Rule 4: Sub-lords of Moon or Ascendant in 6/8/12 houses (KP/Vedic confirmation) ---
        # Get Moon's Sub-sub-lord (SSL) and Ascendant's Sub-sub-lord (SSL)
        # Using SSL for deeper KP confirmation as per the pattern for significators
        moon_ssl_name = planetary_positions.get('Moon')[5] if planetary_positions.get('Moon') else None
        asc_ssl_name = cuspal_positions.get(1)[5] if cuspal_positions.get(1) else None

        relevant_disease_crisis_houses = [6, 8, 12]
        sl_significator_hits = []

        # Check Moon's SSL
        if moon_ssl_name and moon_ssl_name in self.stellar_significators_data:
            moon_ssl_sigs = self.stellar_significators_data[moon_ssl_name]['final_sigs']
            for house in relevant_disease_crisis_houses:
                if house in moon_ssl_sigs:
                    score += 2
                    sl_significator_hits.append(f"Moon's SSL ({moon_ssl_name}) signifies H{house}.")

        # Check Ascendant's SSL
        if asc_ssl_name and asc_ssl_name in self.stellar_significators_data:
            asc_ssl_sigs = self.stellar_significators_data[asc_ssl_name]['final_sigs']
            for house in relevant_disease_crisis_houses:
                if house in asc_ssl_sigs:
                    score += 2
                    sl_significator_hits.append(f"Ascendant's SSL ({asc_ssl_name}) signifies H{house}.")

        if sl_significator_hits:
            details.append("KP/Vedic Sub-Lord Confirmations: " + " & ".join(sl_significator_hits))
            self._log_debug(f"Sub-lord significator risk added: {sl_significator_hits}")

        # --- Rule 5: Nodes compromising angular houses (re-emphasized) ---
        # This is primarily covered by Rule 2 (Nodes activated on angles).
        # We ensure it's logged as a theme if not explicitly captured.
        angular_cusps = [1, 4, 7, 10]
        node_angular_compromise = []
        for cusp_num in angular_cusps:
            cusp_lon = get_cusp_sidereal_lon(cusp_num)
            if cusp_lon is not None:
                if rahu_lon is not None and get_aspect_orb(rahu_lon, cusp_lon) < 5:
                    if not any(f"Rahu near H{cusp_num}" in s for s in
                               node_activation_hits):  # Avoid re-listing same detail
                        node_angular_compromise.append(f"Rahu near H{cusp_num}.")
                if ketu_lon is not None and get_aspect_orb(ketu_lon, cusp_lon) < 5:
                    if not any(f"Ketu near H{cusp_num}" in s for s in
                               node_activation_hits):  # Avoid re-listing same detail
                        node_angular_compromise.append(f"Ketu near H{cusp_num}.")
        if node_angular_compromise:
            details.append("Nodes Compromising Angular Houses: " + " & ".join(node_angular_compromise))
            self._log_debug(f"Nodes angular compromise noted: {node_angular_compromise}")

        self._log_debug(f"Pandemic Rules check complete. Total Score: {score}. Details: {details}")
        return score, details


    def _check_sookshma_lord_condition(self, sookshma_lord_name, primary_cusp_num, ascendant_house_num,
                                       secondary_cusp_nums, original_primary_cusp_num_selected):
        """
        For Sookshma lord: signifies (primary Cusp OR 11th cusp from ascendant) AND secondary Cusps.
        If all secondary houses are not found, look for minimum number of secondary cups.
        Returns (True/False, details_string, num_secondary_cusps_signified)
        """
        sookshma_lord_sigs = self._get_planet_final_significators(sookshma_lord_name,
                                                                   original_primary_cusp_num_selected)
        details = []
        self._log_debug(
            f"  Checking Sookshma Lord condition for {sookshma_lord_name}. Sigs: {sorted(list(sookshma_lord_sigs))}. PC: {primary_cusp_num}, SCs: {secondary_cusp_nums}")

        signifies_pc = primary_cusp_num in sookshma_lord_sigs
        eleventh_from_asc = self._get_relative_house(ascendant_house_num, 10)
        signifies_11_from_asc = eleventh_from_asc in sookshma_lord_sigs

        first_condition_met = False
        if signifies_pc:
            first_condition_met = True
            details.append(f"Signifies Primary Cusp ({primary_cusp_num}).")
        if signifies_11_from_asc:
            first_condition_met = True
            details.append(f"Signifies 11th from Ascendant ({eleventh_from_asc}).")

        if not first_condition_met:
            self._log_debug(f"  Sookshma Lord {sookshma_lord_name} NOT met: Does not signify PC or 11th from Asc.")
            return False, "Does not signify Primary Cusp or 11th from Ascendant.", 0

        num_secondary_cusps_signified = 0
        secondary_cusp_details = []
        for sc_num in secondary_cusp_nums:
            if sc_num in sookshma_lord_sigs:
                num_secondary_cusps_signified += 1
                secondary_cusp_details.append(str(sc_num))

        if num_secondary_cusps_signified > 0:
            details.append(f"Signifies secondary cusps: {', '.join(secondary_cusp_details)}.")
            self._log_debug(f"  Sookshma Lord {sookshma_lord_name} met: Signifies {num_secondary_cusps_signified} SCs.")
        else:
            details.append("Does not signify any selected secondary cusps.")
            self._log_debug(f"  Sookshma Lord {sookshma_lord_name} NOT met: Does not signify any selected SCs.")

        return True, " ".join(details), num_secondary_cusps_signified

    def _get_dasha_periods_flat(self, start_date_utc, end_date_utc, local_tz):
        """
        Recursively collects all Dasha periods (MD, AD, PD, SD, PrD) within a given UTC time range,
        including start and end dates in local time, and their lords.
        Returns a flat list of dictionaries, each representing a Prana Dasha period
        with its full hierarchy of lords.
        """
        flat_prana_periods = []
        self._log_debug(f"Getting flat Dasha periods for range UTC: {start_date_utc} to {end_date_utc} from Dasa Tree.")

        def parse_dasha_time(time_str_raw):
            for fmt in ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]:
                try:
                    return datetime.datetime.strptime(time_str_raw, fmt)
                except ValueError:
                    continue
            self._log_debug(f"ERROR: Could not parse date/time string: {time_str_raw}")
            raise ValueError(f"Could not parse date/time: {time_str_raw}")

        def build_prana_periods_recursive(parent_id, current_md_lord):
            ad_children_ids = self.dasa_tree.get_children(parent_id)
            for ad_id in ad_children_ids:
                ad_lord = self.dasa_tree.item(ad_id, 'text').split(' ')[0]

                pd_children_ids = self.dasa_tree.get_children(ad_id)
                for pd_id in pd_children_ids:
                    pd_lord = self.dasa_tree.item(pd_id, 'text').split(' ')[0]

                    sd_children_ids = self.dasa_tree.get_children(pd_id)
                    for sd_id in sd_children_ids:
                        sd_lord = self.dasa_tree.item(sd_id, 'text').split(' ')[0]

                        prd_children_ids = self.dasa_tree.get_children(sd_id)
                        for prd_id in prd_children_ids:
                            prd_lord = self.dasa_tree.item(prd_id, 'text').split(' ')[0]

                            item_values = self.dasa_tree.item(prd_id, 'values')
                            start_dt_local = parse_dasha_time(item_values[1])
                            end_dt_local = parse_dasha_time(item_values[2])

                            start_dt_utc_aware = local_tz.localize(start_dt_local).astimezone(pytz.utc)
                            end_dt_utc_aware = local_tz.localize(end_dt_local).astimezone(pytz.utc)

                            # Check for overlap with the requested analysis range
                            overlap_start_utc = max(start_dt_utc_aware, start_date_utc)
                            overlap_end_utc = min(end_dt_utc_aware, end_date_utc)

                            if overlap_start_utc < overlap_end_utc:  # If there's any overlap
                                flat_prana_periods.append({
                                    'md_lord': current_md_lord,
                                    'ad_lord': ad_lord,
                                    'pd_lord': pd_lord,
                                    'sd_lord': sd_lord,
                                    'prd_lord': prd_lord,
                                    'start_utc': start_dt_utc_aware,  # Store original period boundaries
                                    'end_utc': end_dt_utc_aware,
                                    'start_local': start_dt_local,
                                    'end_local': end_dt_local
                                })
                                # self._log_debug(f"  Found Prana Period (MD:{current_md_lord}, AD:{ad_lord}, PD:{pd_lord}, SD:{sd_lord}, PrD:{prd_lord}) from {start_dt_utc_aware} to {end_dt_utc_aware}")

        # Start recursion from Mahadashas
        for md_id in self.dasa_tree.get_children(""):
            md_lord_name = self.dasa_tree.item(md_id, 'text').split(' ')[0]
            build_prana_periods_recursive(md_id, md_lord_name)

        flat_prana_periods.sort(key=lambda x: x['start_utc'])
        self._log_debug(f"Finished flattening Dasha periods. Found {len(flat_prana_periods)} periods within range.")
        return flat_prana_periods

    def _get_analysis_time_range(self, local_tz):
        """
        CORRECTED: Gets the analysis start and end UTC datetimes based on the current UI.
        Handles both "24 hours" and "Custom Date Range" modes correctly.
        """
        analysis_mode = self.analysis_mode_var.get()
        start_utc = None
        end_utc = None
        self._log_debug(f"Determining analysis time range for mode: {analysis_mode}")

        try:
            if analysis_mode == "24_hours":
                start_date = self.analysis_date_entry.get_date()
                # Ensure the entry has a valid integer
                duration_str = self.analysis_duration_value_entry.get()
                duration_hours = int(duration_str) if duration_str.isdigit() else 24

                # Analysis for 24-hour mode starts from the beginning of the selected day
                start_dt_naive = datetime.datetime.combine(start_date, datetime.time(0, 0, 0))
                end_dt_naive = start_dt_naive + datetime.timedelta(hours=duration_hours)

            elif analysis_mode == "custom_span":
                start_date = self.analysis_custom_start_date_entry.get_date()
                end_date = self.analysis_custom_end_date_entry.get_date()

                # Custom span covers the full days from start to end
                start_dt_naive = datetime.datetime.combine(start_date, datetime.time(0, 0, 0))
                end_dt_naive = datetime.datetime.combine(end_date, datetime.time(23, 59, 59))

            else:
                messagebox.showerror("Analysis Mode Error", f"Unknown analysis mode: {analysis_mode}")
                return None, None

            start_utc = local_tz.localize(start_dt_naive).astimezone(pytz.utc)
            end_utc = local_tz.localize(end_dt_naive).astimezone(pytz.utc)

            if end_utc < start_utc:
                messagebox.showerror("Invalid Date Range", "End Date/Time cannot be before Start Date/Time.")
                return None, None

            self._log_debug(f"  Mode: {analysis_mode}, Start: {start_utc}, End: {end_utc}")
            return start_utc, end_utc

        except Exception as e:
            messagebox.showerror("Input Error", f"Please enter valid analysis parameters.\nError: {e}")
            return None, None

    def _cache_static_planet_classifications(self, primary_cusp_num_for_analysis, original_primary_cusp_num,
                                             progress_info=None, start_percent=0, end_percent=100):
        """
        Caches planet classifications (Positive, Neutral, Negative) for the CURRENTLY selected
        Primary Cusp and Secondary Cusps. This function is now triggered by the Promise button.
        Ensures self.planet_classifications is always populated.
        """
        self._log_debug("Caching planet classifications for current event (PC/SC).")
        self.planet_classifications = {}  # Ensure it's cleared before re-populating
        ascendant_house_num = 1

        total_planets = len(STELLAR_PLANETS)
        progress_span = end_percent - start_percent

        # Determine if a real progress_info window is active
        is_progress_active = progress_info and progress_info['window'].winfo_exists()

        # Use a dummy progress_info if no active one is provided, to prevent errors in _update_progress calls
        if not is_progress_active:
            class DummyProgressInfo:
                def __init__(self):
                    self.bar = type('obj', (object,), {'__setitem__': lambda self, key, value: None})()
                    self.percent = type('obj', (object,), {'config': lambda self, text: None})()
                    self.status = type('obj', (object,), {'config': lambda self, text: None})()
                    self.etr_label = type('obj', (object,), {'config': lambda self, text: None})()
                    self.window = type('obj', (object,),
                                       {'winfo_exists': lambda self: False})()  # Always return False for exists

            local_progress_info = DummyProgressInfo()
            start_time_dummy = datetime.datetime.now()  # Needed for _update_progress signature
        else:
            local_progress_info = progress_info
            start_time_dummy = datetime.datetime.now()  # Still need a start time for ETR calculation

        for i, planet_name in enumerate(STELLAR_PLANETS):
            # Update progress only if a real progress window is active
            if is_progress_active:
                progress = start_percent + ((i + 1) / total_planets) * progress_span
                self._update_progress(local_progress_info, progress, total_steps=100, start_time=start_time_dummy,
                                      status_text=f"Classifying {planet_name}...")

            is_positive, _ = self._is_dasha_positive(planet_name, primary_cusp_num_for_analysis, ascendant_house_num,
                                                     original_primary_cusp_num)

            if is_positive:
                self.planet_classifications[planet_name] = 'Positive'
            else:
                is_neutral, _ = self._is_dasha_neutral(planet_name, primary_cusp_num_for_analysis, ascendant_house_num,
                                                       original_primary_cusp_num)
                if is_neutral:
                    self.planet_classifications[planet_name] = 'Neutral'
                else:
                    self.planet_classifications[planet_name] = 'Negative'

        # Final update for progress info, if it was active
        if is_progress_active:
            self._update_progress(local_progress_info, end_percent, total_steps=100, start_time=start_time_dummy,
                                  status_text="Classification caching complete.")

        self._log_debug(f"Planet classification caching complete: {self.planet_classifications}")

    def _setup_progress_window(self, title):
        """
        (CORRECTED) Creates and returns a standard progress bar popup window,
        now with the 'etr_label' correctly included.
        """
        progress_window = tk.Toplevel(self.root)
        progress_window.title(title)
        progress_window.transient(self.root)
        progress_window.grab_set()
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)

        status_label = ttk.Label(progress_window, text="Initializing...")
        status_label.pack(pady=(15, 5))

        progress_bar = ttk.Progressbar(progress_window, orient='horizontal', length=350, mode='determinate')
        progress_bar.pack(pady=5)

        # Frame for percent and ETR to sit side-by-side
        bottom_frame = ttk.Frame(progress_window)
        bottom_frame.pack(fill='x', padx=25, pady=5)

        percent_label = ttk.Label(bottom_frame, text="0%")
        percent_label.pack(side='left')

        etr_label = ttk.Label(bottom_frame, text="Time Remaining: Calculating...")
        etr_label.pack(side='right')

        # This dictionary now correctly contains the 'etr_label' key
        return {
            'window': progress_window,
            'bar': progress_bar,
            'status': status_label,
            'percent': percent_label,
            'etr_label': etr_label,
            'root': self.root
        }

    def _update_progress(self, progress_info, current_step, total_steps, start_time, status_text=""):
        """
        (CORRECTED) Updates the progress bar, percentage, and Estimated Time Remaining.
        This function correctly expects the 'etr_label' key from the progress_info dictionary.
        """
        if not progress_info or not progress_info['window'].winfo_exists():
            return
        if total_steps <= 0: total_steps = 1  # Avoid division by zero

        # Update progress bar and percentage
        percent = (current_step / total_steps) * 100
        progress_info['bar']['value'] = percent
        progress_info['percent'].config(text=f"{int(percent)}%")
        if status_text:
            progress_info['status'].config(text=status_text)

        # Calculate and update ETR after a few initial steps for better accuracy
        if current_step > 5:
            elapsed_seconds = (datetime.datetime.now() - start_time).total_seconds()
            time_per_step = elapsed_seconds / current_step
            steps_remaining = total_steps - current_step
            etr_seconds = time_per_step * steps_remaining
            etr_text = f"Time Remaining: ~{self._format_time_remaining(etr_seconds)}"
        else:
            etr_text = "Time Remaining: Calculating..."

        # This line will no longer cause a KeyError
        progress_info['etr_label'].config(text=etr_text)
        progress_info['root'].update_idletasks()

    def _format_time_remaining(self, seconds):
        """(HELPER) Formats a duration in seconds into a '1m 25s' string."""
        if seconds < 0 or seconds > 3600 * 4:  # Don't show for very long or invalid periods
            return "..."
        if seconds < 60:
            return f"{int(seconds)}s"
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes}m {seconds}s"

    def _is_transit_lord_all_positive(self, transit_details_str: str, planet_key: str) -> bool:
        """
        Helper to parse a transit detail string (e.g., "Jup:OK (SL:Jupiter(P), SubL:Mars(N))")
        and check if ALL lords for the specified planet (Jupiter, Sun, Moon) are 'Positive'.
        """
        if f"{planet_key}:FAIL" in transit_details_str or f"{planet_key}:N/A" in transit_details_str:
            return False  # Immediately false if explicitly failed or not applicable

        # Regex to find the part for the specific planet, then extract all (X) classifications
        # Example for Jupiter: Jup:(?:OK \(SL:\w+\((\w)\), SubL:\w+\((\w)\)\))
        # Example for Moon: Moon:(?:OK \(SL:\w+\((\w)\), SubL:\w+\((\w)\), SSL:\w+\((\w)\)\))

        pattern = ""
        if planet_key == "Jup":
            pattern = r"Jup:OK \(SL:\w+\((\w)\), SubL:\w+\((\w)\)\)"
        elif planet_key == "Sat":  # Although not requested, good to have it ready if needed.
            pattern = r"Sat:OK \(SL:\w+\((\w)\), SubL:\w+\((\w)\)\)"
        elif planet_key == "Sun":
            pattern = r"Sun:OK \(SL:\w+\((\w)\), SubL:\w+\((\w)\)\)"
        elif planet_key == "Moon":
            pattern = r"Moon:OK \(SL:\w+\((\w)\), SubL:\w+\((\w)\), SSL:\w+\((\w)\)\)"
        else:
            return False  # Unknown planet key

        match = re.search(pattern, transit_details_str)
        if match:
            # Check if ALL captured groups are 'P'
            return all(group == 'P' for group in match.groups())

        # If the pattern doesn't match (e.g., "Not Checked" or malformed string for this planet)
        if f"{planet_key}:Not Checked" in transit_details_str:
            return False  # If it wasn't checked, it's not "all positive"

        return False  # Default to false if pattern not found or not positive

    def _apply_post_filters(self):
        """
        Applies the Ju+, Su+, Mo+ checkbox filters to the results stored after Final Sort.
        Updates the analysis_results_tree dynamically.
        """
        self._log_debug("--- _apply_post_filters: Start ---")

        # Disable checkboxes first while filtering, then re-enable
        self.ju_plus_cb.config(state='disabled')
        self.su_plus_cb.config(state='disabled')
        self.mo_plus_cb.config(state='disabled')
        self.reset_post_filters_button.config(state='disabled')

        # Clear existing display
        self._update_analysis_results_tree_columns("detailed_full_analysis")

        # Ensure base results exist
        if not hasattr(self, 'final_sort_base_results') or not self.final_sort_base_results:
            self._log_debug("Post-filters: No base results from Final Sort. Exiting.")
            messagebox.showinfo("Filter Info", "No results from the 'Final Sort' step to filter.")
            return

        current_filtered_results = []

        # Get checkbox states
        filter_ju_plus = self.ju_plus_var.get()
        filter_su_plus = self.su_plus_var.get()
        filter_mo_plus = self.mo_plus_var.get()

        self._log_debug(f"Post-filters active: Ju+:{filter_ju_plus}, Su+:{filter_su_plus}, Mo+:{filter_mo_plus}")

        for values in self.final_sort_base_results:
            # values: ("MD", "AD", "PD", "SD", "PrD", "Start Time", "End Time", "Transits", "Cuspal Link", "Remark")
            transit_details_str = values[7]  # 'Transits' column

            # Apply filters cumulatively
            pass_filters = True

            if filter_ju_plus:
                if not self._is_transit_lord_all_positive(transit_details_str, "Jup"):
                    pass_filters = False
                    self._log_debug(f"  Hit {values[5]} failed Ju+ filter.")

            if pass_filters and filter_su_plus:  # Only check Sun if it passed previous filters
                if not self._is_transit_lord_all_positive(transit_details_str, "Sun"):
                    pass_filters = False
                    self._log_debug(f"  Hit {values[5]} failed Su+ filter.")

            if pass_filters and filter_mo_plus:  # Only check Moon if it passed previous filters
                if not self._is_transit_lord_all_positive(transit_details_str, "Moon"):
                    pass_filters = False
                    self._log_debug(f"  Hit {values[5]} failed Mo+ filter.")

            if pass_filters:
                current_filtered_results.append(values)
                self._log_debug(f"  Hit {values[5]} passed all active post-filters.")
            else:
                self._log_debug(f"  Hit {values[5]} filtered out by post-filters.")

        if not current_filtered_results:
            messagebox.showinfo("Filter Results", "No events found matching the selected post-filters.")
            self._log_debug("Post-filters: No results found after applying filters.")
        else:
            self._log_debug(f"Post-filters: Displaying {len(current_filtered_results)} results.")

        # Repopulate treeview with filtered results
        for values in current_filtered_results:
            self.analysis_results_tree.insert("", "end", values=values, tags=('top_event',))  # Keep green highlight

        # Re-enable the checkboxes and reset button
        self.ju_plus_cb.config(state='normal')
        self.su_plus_cb.config(state='normal')
        self.mo_plus_cb.config(state='normal')
        self.reset_post_filters_button.config(state='normal')

        self._log_debug("--- _apply_post_filters: End ---")

    def _reset_post_filters(self):
        """
        Resets all post-Final Sort filter checkboxes and re-displays all base Final Sort results.
        """
        self._log_debug("--- _reset_post_filters: Start ---")
        self.ju_plus_var.set(False)
        self.su_plus_var.set(False)
        self.mo_plus_var.set(False)
        self._log_debug("Post-filters reset. Re-applying filters (should show all base results).")
        self._apply_post_filters()  # Calling this will re-display the non-filtered base results
        self._log_debug("--- _reset_post_filters: End ---")



    def _is_transit_favorable(self, planet_name, dyn_planets, primary_cusp_num_for_analysis, original_primary_cusp_num):
        """
        Checks if a planet's transit is favorable (SL/SubL are P/N). Moon also checks SSL.
        Additionally, the transit planet itself must signify the primary cusp.
        """
        planet_data = dyn_planets.get(planet_name)
        if not planet_data: return False, f"{planet_name[:3]} N/A"

        sl_name, subl_name, subsubl_name = planet_data[3], planet_data[4], planet_data[5]
        sl_class = self.planet_classifications.get(sl_name, 'U')
        subl_class = self.planet_classifications.get(subl_name, 'U')

        is_favorable = False
        status_str = "N/A"

        # Check if the transit planet itself signifies the primary cusp (using its static final significators)
        # Use _get_planet_final_significators for this check as it applies Rule 2
        planet_static_final_sigs = self._get_planet_final_significators(
            planet_name, original_primary_cusp_num, exclude_8_12_from_non_8_12_pc=True
        )
        signifies_pc = primary_cusp_num_for_analysis in planet_static_final_sigs

        if not signifies_pc:
            status_str = f"{planet_name[:3]} does not signify PC ({primary_cusp_num_for_analysis})."
            self._log_debug(f"  Transit FAIL: {status_str}")
            return False, status_str

        # Now proceed with original SL/SubL (and SSL for Moon) classification checks
        if planet_name == 'Moon':
            subsubl_class = self.planet_classifications.get(subsubl_name, 'U')
            if sl_class in ['Positive', 'Neutral'] and \
                    subl_class in ['Positive', 'Neutral'] and \
                    subsubl_class in ['Positive', 'Neutral']:
                is_favorable = True
                status_str = f"Moon SL:{sl_class[0]}/SubL:{subl_class[0]}/SSL:{subsubl_class[0]} (Signifies PC)"
            else:
                status_str = f"Moon SL:{sl_class[0]}/SubL:{subl_class[0]}/SSL:{subsubl_class[0]} (Not P/N Lords)"
        else:  # Jupiter or Sun
            if sl_class in ['Positive', 'Neutral'] and subl_class in ['Positive', 'Neutral']:
                is_favorable = True
                status_str = f"{planet_name[:3]} SL:{sl_class[0]}/SubL:{subl_class[0]} (Signifies PC)"
            else:
                status_str = f"{planet_name[:3]} SL:{sl_class[0]}/SubL:{subl_class[0]} (Not P/N Lords)"

        self._log_debug(f"  Transit status for {planet_name}: {status_str} -> Favorable: {is_favorable}")
        return is_favorable, status_str

    def _check_promise(self):
        """
        Checks the promise of the Ascendant and Primary Cusp based on the new 2025 rules.
        Also triggers re-calculation of planet classifications based on the selected PC/SCs.
        Includes extensive debugging logs to pinpoint classification issues.
        """
        self._log_debug("--- _check_promise: Start ---")
        self._log_debug("Running New Promise Check (2025 Rules).")
        self._log_debug(
            f"State on entering _check_promise: Planets: {bool(self.current_planetary_positions)}, Cusps: {bool(self.current_cuspal_positions)}, StellarSigs: {bool(self.stellar_significators_data)}")

        # Reset UI labels immediately
        self.asc_promise_label.config(text="Asc:", foreground="gray")
        self.pcusp_promise_label.config(text="Pcusp:", foreground="gray")
        self.positive_planets_label.config(text="Positive Planets: (Calculating...)")
        self.neutral_planets_label.config(text="Neutral Planets: (Calculating...)")

        # 1. Prerequisites Check: Ensure chart data is loaded
        if not self.current_planetary_positions or not self.current_cuspal_positions or not self.stellar_significators_data:
            messagebox.showwarning("Data Missing",
                                   "Please generate a chart first on the 'Chart Generation' tab to proceed with the Promise check.")
            self._log_debug(
                "ERROR: Chart data (planetary, cuspal, or stellar significators) missing in _check_promise. Exiting.")
            return

        # 2. Get Primary and Secondary Cusp selections from UI
        try:
            original_primary_cusp_num = self._get_original_primary_cusp_from_ui()
            if original_primary_cusp_num is None:
                self._log_debug(
                    "ERROR: Original Primary Cusp number could not be retrieved from UI in _check_promise. Exiting.")
                return

            secondary_cusp_nums = self._get_selected_secondary_cusps()
            self._log_debug(f"Resolved Secondary Cusps for Promise check: {secondary_cusp_nums}")

        except (ValueError, IndexError) as e:
            messagebox.showerror("Input Error",
                                 f"Invalid cusp selection. Please check the 'Daily Analysis' tab for correct primary/secondary cusp setup. Error: {e}")
            self._log_debug(f"ERROR: Invalid cusp selection in _check_promise. Exiting due to: {e}")
            return

        # 3. Dynamic Planet Classification (Positive, Neutral, Negative)
        # This is the core logic that the error message complains about.
        self._log_debug("DEBUG: Entering dynamic classification block in _check_promise.")
        try:
            # Determine the effective Primary Cusp for analysis (Rule 1 adjustment)
            self._log_debug("Calling _determine_primary_cusp_for_analysis to get adjusted PC...")
            pc_for_analysis = self._determine_primary_cusp_for_analysis(original_primary_cusp_num)
            if pc_for_analysis is None:
                self._log_debug(
                    "ERROR: pc_for_analysis is None after _determine_primary_cusp_for_analysis. This means the adjustment failed or returned nothing. Exiting _check_promise.")
                return

            self._log_debug(f"Primary Cusp for analysis (after adjustment): {pc_for_analysis}")

            # Re-classify all planets based on the current PC/SC context
            self._log_debug(
                "Calling _cache_static_planet_classifications from _check_promise to re-classify planets...")
            self._cache_static_planet_classifications(pc_for_analysis, original_primary_cusp_num)

            # Verify that self.planet_classifications is indeed populated after the call
            if not self.planet_classifications:
                self._log_debug(
                    "CRITICAL ERROR: self.planet_classifications is EMPTY AFTER _cache_static_planet_classifications call. This is unexpected.")
                messagebox.showerror("Classification Error",
                                     "Planet classifications could not be generated. Please check console logs for details. This may indicate a deeper issue with the chart data or classification rules.")
                return
            self._log_debug(
                f"_cache_static_planet_classifications completed. self.planet_classifications (from _check_promise): {self.planet_classifications}")

        except Exception as e:
            messagebox.showerror("Classification Error",
                                 f"An unexpected error occurred during planet classification: {e}\n\nCheck the debug log for more details.")
            self._log_debug(f"CRITICAL ERROR: Exception in dynamic classification block: {e}", exc_info=True)
            return  # Exit if this critical part fails

        # 4. Recalculate Ruling Planets
        # Their strength and relevance depend on the newly classified planets
        self._log_debug("Calling _calculate_ruling_planets to refresh RPs based on new classifications...")
        self._calculate_ruling_planets()
        self._log_debug(f"_calculate_ruling_planets completed. All RPs: {self.all_ruling_planets}")

        # Update UI to show ALL Positive and Neutral planets based on newly calculated classification
        all_positive_planets = sorted([p for p, c in self.planet_classifications.items() if c == 'Positive'])
        all_neutral_planets = sorted([p for p, c in self.planet_classifications.items() if c == 'Neutral'])
        self.positive_planets_label.config(
            text=f"Positive Planets: {', '.join(all_positive_planets) if all_positive_planets else 'None'}")
        self.neutral_planets_label.config(
            text=f"Neutral Planets: {', '.join(all_neutral_planets) if all_neutral_planets else 'None'}")
        self._log_debug(f"Updated Positive/Neutral Planets labels in UI.")

        # 5. Calculate planets with Positional Status for Promise Logic
        self._log_debug("Calculating positional status (for Promise Check logic)...")
        planets_with_ps = self._calculate_positional_status(self.current_planetary_positions,
                                                            self.current_cuspal_positions)
        self._log_debug(f"Planets with PS: {planets_with_ps}")

        # 6. Ascendant Promise Check
        asc_promise_met = False
        asc_ssl_name = self.current_cuspal_positions.get(1, [None] * 6)[5]  # Ascendant Sub-Sub-Lord

        if asc_ssl_name and asc_ssl_name in self.current_planetary_positions:
            asc_ssl_data = self.current_planetary_positions[asc_ssl_name]
            asc_ssl_star_lord = asc_ssl_data[3]
            asc_ssl_sub_lord = asc_ssl_data[4]

            # Get connections for the star and sub lords (using the correctly configured `_get_planet_final_significators`)
            # For promise check, we check the actual houses signified, irrespective of P/N classification.
            star_lord_connections = self._get_planet_cuspal_connections(asc_ssl_star_lord, planets_with_ps)
            sub_lord_connections = self._get_planet_cuspal_connections(asc_ssl_sub_lord, planets_with_ps)

            # Condition A1: Star/Sub lord swap logic
            path1_success = (
                        pc_for_analysis in star_lord_connections and secondary_cusp_nums.issubset(sub_lord_connections))
            path2_success = (
                        secondary_cusp_nums.issubset(star_lord_connections) and pc_for_analysis in sub_lord_connections)

            if path1_success or path2_success:
                asc_promise_met = True
                self._log_debug(f"Ascendant Promise: MET via Star/Sub Lord connections of SSL {asc_ssl_name}.")

            # Condition A2: Positional Status logic
            if not asc_promise_met and asc_ssl_name in planets_with_ps:
                # Check if Asc SSL, being a PS planet, signifies the primary cusp (itself)
                asc_ssl_sigs = self._get_planet_final_significators(asc_ssl_name, original_primary_cusp_num,
                                                                    exclude_8_12_from_non_8_12_pc=False)
                if pc_for_analysis in asc_ssl_sigs:
                    asc_promise_met = True
                    self._log_debug(
                        f"Ascendant Promise: MET via Positional Status of SSL {asc_ssl_name} signifying PC.")

        self.asc_promise_label.config(text="Asc:", foreground="green" if asc_promise_met else "red")
        self._log_debug(f"Ascendant Promise status: {asc_promise_met}")

        # 7. Primary Cusp Promise Check
        pcusp_promise_met = False
        pcusp_ssl_name = self.current_cuspal_positions.get(pc_for_analysis, [None] * 6)[5]  # Primary Cusp Sub-Sub-Lord

        if pcusp_ssl_name and pcusp_ssl_name in self.current_planetary_positions:
            pcusp_ssl_data = self.current_planetary_positions[pcusp_ssl_name]
            pcusp_ssl_star_lord = pcusp_ssl_data[3]
            pcusp_ssl_sub_lord = pcusp_ssl_data[4]

            # Get connections for the star and sub lords (using the correctly configured `_get_planet_final_significators`)
            pc_ssl_star_lord_connections = self._get_planet_cuspal_connections(pcusp_ssl_star_lord, planets_with_ps)
            sub_lord_connections = self._get_planet_cuspal_connections(pcusp_ssl_sub_lord, planets_with_ps)

            # Condition B1: Main check
            # Check if PC SSL's star lord signifies all secondary cusps
            star_lord_fulfills_scs = secondary_cusp_nums.issubset(pc_ssl_star_lord_connections)

            # Check if PC SSL's sub lord negates by showing PC-1
            negating_cusp = pc_for_analysis - 1 if pc_for_analysis > 1 else 12  # 12th from PC
            sub_lord_negates = negating_cusp in sub_lord_connections

            if star_lord_fulfills_scs and not sub_lord_negates:
                pcusp_promise_met = True
                self._log_debug(f"P.Cusp Promise: MET via main rule for SSL {pcusp_ssl_name}.")

            # Condition B2: Positional Status logic
            if not pcusp_promise_met and pcusp_ssl_name in planets_with_ps:
                # Check if PC SSL, being a PS planet, signifies the primary cusp (itself)
                pcusp_ssl_sigs = self._get_planet_final_significators(pcusp_ssl_name, original_primary_cusp_num,
                                                                      exclude_8_12_from_non_8_12_pc=False)
                if pc_for_analysis in pcusp_ssl_sigs:
                    pcusp_promise_met = True
                    self._log_debug(f"P.Cusp Promise: MET via Positional Status of SSL {pcusp_ssl_name} signifying PC.")

        self.pcusp_promise_label.config(text="Pcusp:", foreground="green" if pcusp_promise_met else "red")
        self._log_debug(f"Primary Cusp Promise status: {pcusp_promise_met}")
        self._log_debug("--- _check_promise: End ---")


    def _check_static_interlink_promise(self, pc_for_analysis, secondary_cusp_nums):
        """
        Checks for the cuspal interlink promise in the STATIC chart.
        Returns (True, details_dict) if promise exists, otherwise (False, None).
        """
        self._log_debug("Checking for STATIC cuspal interlink promise...")

        # Use the main static chart data
        static_cusps = self.current_cuspal_positions
        static_planets = self.current_planetary_positions

        pc_data = static_cusps.get(pc_for_analysis)
        if not pc_data: return False, None

        # Get the Sub Lord of the Primary Cusp (from the static chart)
        pc_sub_lord_name = pc_data[4]
        if self.planet_classifications.get(pc_sub_lord_name, 'Negative') not in ['Positive', 'Neutral']:
            self._log_debug(f"Interlink fails: PC Sub Lord ({pc_sub_lord_name}) is classified as Negative.")
            return False, None

        pc_sl_planet_data = static_planets.get(pc_sub_lord_name)
        if not pc_sl_planet_data: return False, None

        # Get the Star Lord and Sub Lord of the PC's Sub Lord (from the static chart)
        _, pc_sl_star_lord, pc_sl_sub_lord, _ = self.get_nakshatra_info(pc_sl_planet_data[0])

        # These lords must also be P/N
        if self.planet_classifications.get(pc_sl_star_lord, 'Negative') not in ['Positive', 'Neutral'] or \
                self.planet_classifications.get(pc_sl_sub_lord, 'Negative') not in ['Positive', 'Neutral']:
            self._log_debug(f"Interlink fails: PC SL's lords ({pc_sl_star_lord}, {pc_sl_sub_lord}) are Negative.")
            return False, None

        # Check connection with Secondary Cusps (from the static chart)
        if not secondary_cusp_nums:
            details = {'pc_sl_sl': pc_sl_star_lord, 'pc_sl_subl': pc_sl_sub_lord,
                       'sc_connected_str': "Link OK (No SCs)"}
            return True, details

        connected_sc_details = {}
        for sc_num in secondary_cusp_nums:
            sc_data = static_cusps.get(sc_num)
            if not sc_data: return False, None

            sc_sub_lord = sc_data[4]
            if self.planet_classifications.get(sc_sub_lord, 'Negative') not in ['Positive', 'Neutral']:
                self._log_debug(f"Interlink fails: SC {sc_num} Sub Lord ({sc_sub_lord}) is Negative.")
                return False, None

            connection_type = []
            if pc_sl_star_lord == sc_sub_lord: connection_type.append("Star Match")
            if pc_sl_sub_lord == sc_sub_lord: connection_type.append("Sub Match")

            if not connection_type:
                self._log_debug(f"Interlink fails: No connection to SC {sc_num} Sub Lord ({sc_sub_lord}).")
                return False, None  # Must have a connection to ALL secondary cusps
            connected_sc_details[sc_num] = " / ".join(connection_type)

        details = {
            'pc_sl_sl': pc_sl_star_lord,
            'pc_sl_subl': pc_sl_sub_lord,
            'sc_connected_str': "; ".join([f"H{n}: {t}" for n, t in sorted(connected_sc_details.items())])
        }
        self._log_debug(f"Static interlink promise FOUND. Details: {details}")
        return True, details

    def _run_rectification(self):
        """
        Main function to perform birth time rectification over a given time window.
        """
        self._log_debug("Starting birth time rectification process.")

        # 1. Get base input data from the UI
        try:
            year_str = self.year_lb.get(self.year_lb.curselection())
            month_name = self.month_lb.get(self.month_lb.curselection())
            day_str = self.day_lb.get(self.day_lb.curselection())
            hour_str = self.hour_lb.get(self.hour_lb.curselection())
            minute_str = self.minute_lb.get(self.minute_lb.curselection())
            second_str = self.second_lb.get(self.second_lb.curselection())
            month_num = MONTH_NAMES.index(month_name) + 1
        except (tk.TclError, ValueError, IndexError):
            messagebox.showerror("Input Error",
                                 "Please select a full date and time to use as the center of the search.")
            return

        base_dt_local = datetime.datetime(int(year_str), month_num, int(day_str),
                                          int(hour_str), int(minute_str), int(second_str))

        city = self.city_combo.get()
        if city not in ALL_INDIAN_CITIES:
            messagebox.showerror("Input Error", f"Please select a valid city from the list before rectifying.")
            return
        lat, lon = self.get_lat_lon(city)
        local_tz = pytz.timezone(self.timezone_combo.get())

        # 2. Define search window (+/- 30 minutes from selected time) and known events
        time_window_minutes = 30
        search_interval_seconds = 5

        # --- CORRECTED LINES HERE ---
        start_dt_local = base_dt_local - datetime.timedelta(minutes=time_window_minutes)
        end_dt_local = base_dt_local + datetime.timedelta(minutes=time_window_minutes)

        # Using the hardcoded known events from your example
        known_events = [
            {"type": "marriage", "date": datetime.date(2005, 3, 12)},
            {"type": "job", "date": datetime.date(2010, 6, 10)},
            {"type": "childbirth", "date": datetime.date(2008, 8, 5)},
        ]

        # 3. Setup and show a progress window
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Rectifying Time...")
        progress_window.transient(self.root)
        progress_window.grab_set()
        progress_window.geometry("350x100")
        status_label = ttk.Label(progress_window,
                                 text=f"Searching from {start_dt_local.strftime('%H:%M:%S')} to {end_dt_local.strftime('%H:%M:%S')}...")
        status_label.pack(pady=10)
        progress_bar = ttk.Progressbar(progress_window, orient='horizontal', length=300, mode='determinate')
        progress_bar.pack(pady=5)
        self.root.update_idletasks()

        # 4. Iterate through the time window and find best candidates
        best_score = -1
        candidates = []
        current_dt_local = start_dt_local
        total_steps = (end_dt_local - start_dt_local).total_seconds() / search_interval_seconds
        steps_done = 0

        while current_dt_local <= end_dt_local:
            aware_local_dt = local_tz.localize(current_dt_local)
            utc_dt = aware_local_dt.astimezone(pytz.utc)
            jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                               utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)

            ayanamsa = self.get_khullar_ayanamsha(jd_ut)
            cusps, ascmc = swe.houses(jd_ut, lat, lon, b'P')
            lagna_lon = (cusps[0] - ayanamsa) % 360
            moon_lon_trop = swe.calc_ut(jd_ut, swe.MOON)[0][0]
            moon_lon = (moon_lon_trop - ayanamsa) % 360

            score = self._rectify_event_score(lagna_lon, moon_lon, known_events)

            if score > best_score:
                best_score = score
                candidates = [(current_dt_local, lagna_lon, cusps)]
            elif score == best_score > -1:
                candidates.append((current_dt_local, lagna_lon, cusps))

            # --- CORRECTED LINE HERE ---
            current_dt_local += datetime.timedelta(seconds=search_interval_seconds)
            steps_done += 1
            if total_steps > 0:
                progress_bar['value'] = (steps_done / total_steps) * 100
            self.root.update_idletasks()

        # 5. Apply final filtering to the best candidates
        final_rectified_time = None
        if not candidates:
            messagebox.showwarning("Rectification Failed", "No potential time candidates found in the search window.")
            progress_window.destroy()
            return

        self._log_debug(f"Found {len(candidates)} candidates with top score of {best_score}.")
        status_label.config(text="Filtering candidates...")
        self.root.update_idletasks()

        for time_obj, lagna_lon, cusps_trop in candidates:
            aware_local_dt = local_tz.localize(time_obj)
            utc_dt = aware_local_dt.astimezone(pytz.utc)
            jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                               utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0)

            ruling_planets = self._rectify_get_ruling_planets(jd_ut)
            _nak, _star, lagna_sub, _ssl = self.get_nakshatra_info(lagna_lon)

            if lagna_sub in ruling_planets:
                ayanamsa = self.get_khullar_ayanamsha(jd_ut)
                cusps_lons_sidereal = [(c - ayanamsa) % 360 for c in cusps_trop]
                if self._rectify_check_9th_cusp(lagna_lon, cusps_lons_sidereal):
                    final_rectified_time = time_obj
                    self._log_debug(f"Found final rectified time: {final_rectified_time} with RP and 9th Cusp match.")
                    break

        progress_window.destroy()

        # 6. Update UI with the result
        if final_rectified_time:
            messagebox.showinfo("Rectification Successful",
                                f"Best rectified time found: {final_rectified_time.strftime('%H:%M:%S')}")
            now = final_rectified_time

            def select_item(listbox, value):
                try:
                    items = list(listbox.get(0, tk.END))
                    if str(value) in items:
                        idx = items.index(str(value))
                        listbox.selection_clear(0, tk.END)
                        listbox.selection_set(idx)
                        listbox.see(idx)
                except ValueError:
                    pass

            select_item(self.hour_lb, f"{now.hour:02d}")
            select_item(self.minute_lb, f"{now.minute:02d}")
            select_item(self.second_lb, f"{now.second:02d}")
        else:
            messagebox.showwarning("Rectification Complete",
                                   "No time found that satisfies all rectification conditions. The highest-scoring candidates did not match the final filters.")

    def _update_analysis_results_tree_columns(self, analysis_type):
        """
        Dynamically updates the columns and headings of the analysis_results_tree
        based on the analysis type.
        """
        # Clear any existing items in the treeview
        self.analysis_results_tree.delete(*self.analysis_results_tree.get_children())

        # Configure the tree to show headings and hide the default '#0' column
        self.analysis_results_tree.config(columns=[], displaycolumns=[])
        self.analysis_results_tree["show"] = "headings"
        self.analysis_results_tree.heading("#0", text="")
        self.analysis_results_tree.column("#0", width=0, stretch=False)  # Hide the default first column

        if analysis_type == "detailed_full_analysis":
            # Define 10 columns including "Remark"
            columns = ("MD", "AD", "PD", "SD", "PrD", "Start Time", "End Time", "Transits", "Cuspal Link", "Remark")
            self.analysis_results_tree["columns"] = columns
            self.analysis_results_tree["displaycolumns"] = columns  # Ensure all defined columns are displayed

            # Set column headings
            self.analysis_results_tree.heading("MD", text="MD")
            self.analysis_results_tree.heading("AD", text="AD")
            self.analysis_results_tree.heading("PD", text="PD")
            self.analysis_results_tree.heading("SD", text="SD")
            self.analysis_results_tree.heading("PrD", text="PrD")
            self.analysis_results_tree.heading("Start Time", text="Start Time (Local)")
            self.analysis_results_tree.heading("End Time", text="End Time (Local)")
            self.analysis_results_tree.heading("Transits", text="Transits")
            self.analysis_results_tree.heading("Cuspal Link", text="Cuspal Link")
            self.analysis_results_tree.heading("Remark", text="Remark")  # New heading for the Remark column

            # Set column widths and alignment
            for col in ["MD", "AD", "PD", "SD", "PrD"]:
                self.analysis_results_tree.column(col, width=50, anchor='center')
            self.analysis_results_tree.column("Start Time", width=140, anchor='w')
            self.analysis_results_tree.column("End Time", width=140, anchor='w')
            self.analysis_results_tree.column("Transits", width=250,
                                              anchor='w')  # Can be wide for detailed transit info
            self.analysis_results_tree.column("Cuspal Link", width=180, anchor='w')  # Can be wide for link details
            self.analysis_results_tree.column("Remark", width=100, anchor='w')  # Width for the Remark column

        # You might have other 'analysis_type' branches here if you use them, e.g.:
        elif analysis_type == "dasha_classification":
            columns = ("MD", "AD", "PD", "SD", "PrD", "Type", "Start Time", "End Time", "Details")
            self.analysis_results_tree["columns"] = columns
            self.analysis_results_tree["displaycolumns"] = columns
            self.analysis_results_tree.heading("MD", text="MD Lord")
            # ... (rest of headings and columns for dasha_classification) ...

        # Add any other analysis_type branches you may have...

        else:
            # Fallback for unknown analysis types, or a generic default
            columns = ("Info",)
            self.analysis_results_tree["columns"] = columns
            self.analysis_results_tree["displaycolumns"] = columns
            self.analysis_results_tree.heading("Info", text="Results Information")
            self.analysis_results_tree.column("Info", width=600, anchor='w')

    def _find_next_favorable_transit_period(self, planet_name, start_utc, end_utc, city, hsys_const, horary_num,
                                            pc_for_analysis, original_pc_num):
        """Finds the next continuous period within a range where a planet's transit is favorable."""
        interval_seconds = 60  # Check every minute
        current_block_start = None

        time_pointer = start_utc
        while time_pointer < end_utc:
            dyn_planets, _, _ = self._calculate_chart_data(time_pointer, city, hsys_const, horary_num)

            planet_data = dyn_planets.get(planet_name)
            is_favorable = False
            status_str = "N/A"

            if planet_data:
                sl_name = planet_data[3]
                subl_name = planet_data[4]
                sl_class = self.planet_classifications.get(sl_name, 'Unclassified')
                subl_class = self.planet_classifications.get(subl_name, 'Unclassified')

                if planet_name == 'Moon':
                    subsubl_name = planet_data[5]
                    subsubl_class = self.planet_classifications.get(subsubl_name, 'Unclassified')
                    if sl_class in ['Positive', 'Neutral'] and subl_class in ['Positive',
                                                                              'Neutral'] and subsubl_class in [
                        'Positive', 'Neutral']:
                        is_favorable = True
                    status_str = f"SL:{sl_class}, SubL:{subl_class}, SubSubL:{subsubl_class}"
                else:  # Jupiter or Sun
                    if sl_class in ['Positive', 'Neutral'] and subl_class in ['Positive', 'Neutral']:
                        is_favorable = True
                    status_str = f"SL:{sl_class}, SubL:{subl_class}"

            if is_favorable:
                if current_block_start is None:
                    current_block_start = time_pointer  # Start of a favorable block
            else:
                if current_block_start is not None:
                    # End of a favorable block, return it
                    return current_block_start, time_pointer, status_str

            time_pointer += datetime.timedelta(seconds=interval_seconds)

        if current_block_start is not None:
            # Block is favorable until the end of the search window
            return current_block_start, end_utc, status_str

        return None, None, None  # No favorable period found

    def _find_interlink_periods_in_span(self, start_utc, end_utc, pc_for_analysis, secondary_cusp_nums, city,
                                        hsys_const, horary_num_value):
        """
        Runs the cuspal interlink analysis for a specific time span and returns the results.
        """
        self._log_debug(f"  Running Interlink Analysis within: {start_utc} to {end_utc}")
        interlink_results = []
        # Changed step size from 10 seconds to 60 seconds (1 minute) for lighter computation
        interval_seconds = 60
        time_pointer = start_utc

        current_interlink_block_start_time = None
        last_pc_sl_star_lord = "N/A"
        last_pc_sl_sub_lord = "N/A"
        last_connected_sc_details = {}

        while time_pointer < end_utc:
            dynamic_planetary_positions, dynamic_cuspal_positions, _ = self._calculate_chart_data(
                time_pointer, city, hsys_const, horary_num_value
            )

            is_interlinked_now = False
            pc_data = dynamic_cuspal_positions.get(pc_for_analysis)
            if pc_data:
                pc_sub_lord_name = pc_data[4]
                pc_sl_class = self.planet_classifications.get(pc_sub_lord_name, 'Unclassified')

                if pc_sl_class in ['Positive', 'Neutral']:
                    pc_sl_planet_data = dynamic_planetary_positions.get(pc_sub_lord_name)
                    if pc_sl_planet_data and pc_sub_lord_name in STELLAR_PLANETS:
                        _, current_pc_sl_star_lord, current_pc_sl_sub_lord, _ = self.get_nakshatra_info(
                            pc_sl_planet_data[0])
                        sl_class = self.planet_classifications.get(current_pc_sl_star_lord, 'Unclassified')
                        subl_class = self.planet_classifications.get(current_pc_sl_sub_lord, 'Unclassified')

                        if sl_class in ['Positive', 'Neutral'] and subl_class in ['Positive', 'Neutral']:
                            all_scs_ok = True
                            current_second_connected_sc_details = {}
                            if not secondary_cusp_nums:  # If no SCs, condition is met
                                is_interlinked_now = True
                            else:
                                for sc_num in secondary_cusp_nums:
                                    sc_data = dynamic_cuspal_positions.get(sc_num)
                                    if not sc_data: all_scs_ok = False; break

                                    sc_sub_lord = sc_data[4]
                                    sc_sl_class = self.planet_classifications.get(sc_sub_lord, 'Unclassified')
                                    if sc_sl_class not in ['Positive', 'Neutral']: all_scs_ok = False; break

                                    connection_type = []
                                    if current_pc_sl_star_lord == sc_sub_lord: connection_type.append("Star Match")
                                    if current_pc_sl_sub_lord == sc_sub_lord: connection_type.append("Sub Match")

                                    if connection_type:
                                        current_second_connected_sc_details[sc_num] = " / ".join(connection_type)
                                    else:
                                        all_scs_ok = False;
                                        break

                                if all_scs_ok:
                                    is_interlinked_now = True
                                    last_pc_sl_star_lord = current_pc_sl_star_lord
                                    last_pc_sl_sub_lord = current_pc_sl_sub_lord
                                    last_connected_sc_details = current_second_connected_sc_details

            # --- Manage start/end of interlink time blocks ---
            if is_interlinked_now:
                if current_interlink_block_start_time is None:
                    current_interlink_block_start_time = time_pointer
            else:
                if current_interlink_block_start_time is not None:
                    end_time_of_block_utc = time_pointer
                    sc_connections_str = "; ".join([f"H{num}: {type_str}" for num, type_str in sorted(
                        last_connected_sc_details.items())]) if last_connected_sc_details else "PC/SC Link OK"
                    interlink_results.append({
                        "start_utc": current_interlink_block_start_time, "end_utc": end_time_of_block_utc,
                        "pc_sl_sl": last_pc_sl_star_lord, "pc_sl_subl": last_pc_sl_sub_lord,
                        "sc_connected_str": sc_connections_str
                    })
                    current_interlink_block_start_time = None

            time_pointer += datetime.timedelta(seconds=interval_seconds)

        if current_interlink_block_start_time is not None:
            sc_connections_str = "; ".join([f"H{num}: {type_str}" for num, type_str in sorted(
                last_connected_sc_details.items())]) if last_connected_sc_details else "PC/SC Link OK"
            interlink_results.append({
                "start_utc": current_interlink_block_start_time, "end_utc": end_utc,
                "pc_sl_sl": last_pc_sl_star_lord, "pc_sl_subl": last_pc_sl_sub_lord,
                "sc_connected_str": sc_connections_str
            })

        self._log_debug(f"  Interlink search found {len(interlink_results)} period(s).")
        return interlink_results

    def _format_transit_interlink_result(self, primary_cusp_str, start_utc, end_utc, local_tz,
                                         pc_sl_sl, pc_sl_subl, sc_connected_str,
                                         jupiter_status, sun_status, moon_status, dasha_lords):
        """Helper to format a single row for the transit filtered interlinks treeview."""
        # Format date as '19 Jun '25' and time as 'HH:MM:SS AM/PM'
        start_display_time = start_utc.astimezone(local_tz).strftime("%d %b '%y %I:%M:%S %p")
        end_display_time = end_utc.astimezone(local_tz).strftime("%d %b '%y %I:%M:%S %p")

        return (
            dasha_lords['md'],
            dasha_lords['ad'],
            dasha_lords['pd'],
            dasha_lords['sd'],
            dasha_lords['prd'],
            f"{start_display_time} - {end_display_time}",
            jupiter_status,
            sun_status,
            moon_status,
            # Note: The original request for transit_filtered_interlinks asked for PC SL SL, PC SL SubL, SCs Connected
            # These are now nested within the Jupiter/Sun/Moon blocks by the prompt.
            # If you want them displayed in the main table columns, you need to add them back as new columns
            # to the self.analysis_results_tree["columns"] and self.analysis_results_tree["displaycolumns"]
            # in _update_analysis_results_tree_columns for "transit_filtered_interlinks" analysis type.
            # For now, I'm assuming you want the interlink status condensed.
            sc_connected_str # This is cuspal interlink status for the block
        )

    def _get_original_primary_cusp_from_ui(self):
        """Helper to safely get the original primary cusp number from UI."""
        original_primary_cusp_str = self.primary_cusp_combo.get()
        if not original_primary_cusp_str:
            messagebox.showerror("Input Error", "Please select a Primary Cusp.")
            self._log_debug("ERROR: No primary cusp selected in UI.")
            return None
        return int(original_primary_cusp_str.split()[-1])

    def _determine_primary_cusp_for_analysis(self, original_primary_cusp_num):
        """Applies Rule 1 to determine the primary cusp for analysis."""
        self._log_debug(f"Determining primary cusp for analysis. Original PC: {original_primary_cusp_num}")
        is_original_pc_signified_by_any_planet = False
        # For this check, we use the raw (non-rule 2 filtered) significators
        temp_stellar_significators_data = self._generate_static_stellar_significators(
            self.current_planetary_positions, self.current_cuspal_positions
        )
        for planet_name in STELLAR_PLANETS:
            # Note: For this initial check of PC signification, we temporarily don't apply Rule 2
            # filtering for the planet's own significators, as we just need to see if PC is AT ALL signified.
            # The _get_planet_final_significators itself defaults to apply Rule 2,
            # so we'll pass exclude_8_12_from_non_8_12_pc=False for this specific check.
            planet_final_sigs = self._get_planet_final_significators(planet_name, original_primary_cusp_num,
                                                                      exclude_8_12_from_non_8_12_pc=False)
            if original_primary_cusp_num in planet_final_sigs:
                is_original_pc_signified_by_any_planet = True
                self._log_debug(f"  Original PC ({original_primary_cusp_num}) is signified by {planet_name}.")
                break

        if not is_original_pc_signified_by_any_planet:
            messagebox.showinfo("Primary Cusp Adjusted",
                                f"Selected Primary Cusp (House {original_primary_cusp_num}) is not a significator for any planet. Adjusting Primary Cusp to House 11 as per Rule 1 for this analysis.")
            self.primary_cusp_combo.set(f"House 11")
            self._log_debug(
                f"Primary Cusp adjusted to House 11 as original PC {original_primary_cusp_num} is not signified.")
            return 11
        else:
            current_ui_pc_str = self.primary_cusp_combo.get()
            if current_ui_pc_str != f"House {original_primary_cusp_num}":
                self.primary_cusp_combo.set(f"House {original_primary_cusp_num}")
                self._log_debug(f"Primary Cusp reset to original House {original_primary_cusp_num}.")
            self._log_debug(f"Primary Cusp for analysis: {original_primary_cusp_num}.")
            return original_primary_cusp_num

    def _is_combined_dasha_fruitful(self, combined_dasha_sigs, primary_cusp_num, secondary_cusp_nums):
        """
        Checks if the combined significators of a Dasha combination are "fruitful".
        A Dasha combination is fruitful if:
        1. It signifies the primary cusp.
        2. It signifies ALL of the selected secondary cusps (if any are selected).
        """
        details = []
        num_secondary_cusps_signified = 0

        # Condition 1: Primary Cusp must be signified
        if primary_cusp_num not in combined_dasha_sigs:
            details.append(f"Does not signify Primary Cusp ({primary_cusp_num}).")
            self._log_debug(f"    Combined NOT fruitful: PC ({primary_cusp_num}) not in combined sigs.")
            return False, " ".join(details), 0
        details.append(f"Signifies Primary Cusp ({primary_cusp_num}).")

        # Condition 2: ALL selected secondary cusps must be signified if secondary cusps are selected
        if secondary_cusp_nums:
            all_secondary_cusps_signified = True
            signified_secondary_cusps = []
            for sc_num in secondary_cusp_nums:
                if sc_num in combined_dasha_sigs:
                    num_secondary_cusps_signified += 1
                    signified_secondary_cusps.append(sc_num)
                else:
                    all_secondary_cusps_signified = False
                    details.append(f"Does not signify all selected Secondary Cusps (missing {sc_num}).")
                    break  # No need to check further secondary cusps

            if not all_secondary_cusps_signified:
                self._log_debug(f"    Combined NOT fruitful: Not all SCs signified out of {secondary_cusp_nums}.")
                return False, " ".join(details), num_secondary_cusps_signified
            else:
                details.append(
                    f"Signifies ALL secondary cusps: {', '.join(map(str, sorted(signified_secondary_cusps)))}.")
                self._log_debug(f"    Combined IS fruitful: Signifies ALL SCs {signified_secondary_cusps}.")
                return True, " ".join(details), num_secondary_cusps_signified
        else:
            # If no secondary cusps are selected, then just primary cusp signification makes it fruitful
            self._log_debug(f"    Combined IS fruitful: Only PC ({primary_cusp_num}) check, no SCs selected.")
            return True, "Signifies Primary Cusp (no secondary cusps selected).", 0

    def _run_combined_dasha_significator_analysis(self, only_return_fruitful_spans=False):
        self._log_debug("Running Combined Dasha Significator Analysis (Optimized).")
        if not only_return_fruitful_spans:
            self._update_analysis_results_tree_columns("combined_dasha_significators")

        if not self.current_planetary_positions or not self.current_cuspal_positions or not self.stellar_significators_data:
            if not only_return_fruitful_spans:
                messagebox.showwarning("Chart Data Missing",
                                       "Please generate a chart and ensure Stellar Status Significators are calculated first.")
            self._log_debug("ERROR: Chart data or stellar significators missing for combined dasha analysis.")
            return

        original_primary_cusp_num = self._get_original_primary_cusp_from_ui()
        if original_primary_cusp_num is None: return

        primary_cusp_num_for_analysis = self._determine_primary_cusp_for_analysis(original_primary_cusp_num)

        selected_secondary_cusp_indices = self.secondary_cusp_listbox.curselection()
        secondary_cusp_nums = [int(self.secondary_cusp_listbox.get(i).split()[-1]) for i in
                               selected_secondary_cusp_indices]
        if not secondary_cusp_nums and not only_return_fruitful_spans:
            messagebox.showwarning("Input Warning",
                                   "No secondary cusps selected. Fruitful spans will be based on primary cusp signification only.")
            self._log_debug("WARNING: No secondary cusps selected.")

        timezone_str = self.timezone_combo.get()
        local_tz = pytz.timezone(timezone_str)

        # Ensure planet classifications are cached before starting analysis
        self._cache_static_planet_classifications(primary_cusp_num_for_analysis, original_primary_cusp_num)
        if not hasattr(self, 'planet_classifications') or not self.planet_classifications:
            messagebox.showerror("Internal Error", "Planet classifications not cached. Please generate chart first.")
            self._log_debug("ERROR: Planet classifications not cached for combined dasha analysis.")
            return

        if not only_return_fruitful_spans:
            self.analysis_results_tree.delete(*self.analysis_results_tree.get_children())

            progress_window = tk.Toplevel(self.root)
            progress_window.title("Combined Dasha Analysis Progress")
            progress_window.transient(self.root)
            progress_window.grab_set()
            progress_label = ttk.Label(progress_window, text="Searching for fruitful Dasha periods...")
            progress_label.pack(pady=10)
            progress_bar = ttk.Progressbar(progress_window, orient='horizontal', length=250, mode='indeterminate')
            progress_bar.pack(pady=5)
            progress_bar.start()
            self.root.update_idletasks()
        else:
            progress_window = None

        self.fruitful_dasha_spans = []
        fruitful_periods_display = []

        # Get initial analysis time range from UI
        initial_analysis_start_utc, initial_analysis_end_utc = self._get_analysis_time_range(local_tz)
        if initial_analysis_start_utc is None:
            if progress_window: progress_window.destroy()
            return

        # Natal UTC date is crucial for _get_dasha_periods_flat to span the correct 120 years
        natal_utc_dt = self.current_general_info.get('natal_utc_dt')
        if not natal_utc_dt:
            if not only_return_fruitful_spans:
                messagebox.showerror("Data Error", "Natal chart UTC time not found. Please regenerate chart.")
            if progress_window: progress_window.destroy()
            self._log_debug("ERROR: Natal UTC datetime not found in general info.")
            return

        # Fetch all Prana Dasha periods from the entire 120-year Dasa Tree
        # This is efficient as it uses the pre-built self.dasa_tree
        all_dasha_periods_from_tree = self._get_dasha_periods_flat(
            natal_utc_dt,
            natal_utc_dt + datetime.timedelta(days=365.25 * 120),  # Span entire 120 years
            local_tz
        )
        self._log_debug(f"Fetched {len(all_dasha_periods_from_tree)} Prana Dasha periods from the entire tree.")

        # Extended search logic
        search_start_utc = initial_analysis_start_utc
        search_end_utc = initial_analysis_end_utc
        max_iterations = 7  # Max iterations for extended search
        analysis_mode = self.analysis_mode_var.get()
        # Initialize current_fruitful_periods for the loop
        current_fruitful_periods_this_iteration = []

        for iteration in range(max_iterations):
            self._log_debug(
                f"Combined Dasha Analysis - Iteration {iteration + 1}. Current search window: {search_start_utc} to {search_end_utc}")

            current_fruitful_periods_this_iteration = []  # Reset for each iteration

            # Collect periods that fall within the current search window for this iteration
            periods_for_current_iteration = [
                p for p in all_dasha_periods_from_tree
                if p['start_utc'] < search_end_utc and p['end_utc'] > search_start_utc
            ]

            # Sort periods to ensure processing order
            periods_for_current_iteration.sort(key=lambda x: x['start_utc'])

            self._log_debug(f"  {len(periods_for_current_iteration)} periods to check in this iteration.")

            for prana_period_data in periods_for_current_iteration:
                md_lord = prana_period_data['md_lord']
                ad_lord = prana_period_data['ad_lord']
                pd_lord = prana_period_data['pd_lord']
                sd_lord = prana_period_data['sd_lord']
                prd_lord = prana_period_data['prd_lord']

                # Retrieve classifications from cache
                md_class = self.planet_classifications.get(md_lord, 'Unclassified')
                ad_class = self.planet_classifications.get(ad_lord, 'Unclassified')
                pd_class = self.planet_classifications.get(pd_lord, 'Unclassified')
                sd_class = self.planet_classifications.get(sd_lord, 'Unclassified')
                prd_class = self.planet_classifications.get(prd_lord, 'Unclassified')

                is_this_combination_fruitful_by_lords = True

                # All 5 lords (MD, AD, PD, SD, PrD) must be Positive or Neutral
                if md_class not in ['Positive', 'Neutral']:
                    is_this_combination_fruitful_by_lords = False
                if ad_class not in ['Positive', 'Neutral']:
                    is_this_combination_fruitful_by_lords = False
                if pd_class not in ['Positive', 'Neutral']:
                    is_this_combination_fruitful_by_lords = False
                if sd_class not in ['Positive', 'Neutral']:
                    is_this_combination_fruitful_by_lords = False
                if prd_class not in ['Positive', 'Neutral']:
                    is_this_combination_fruitful_by_lords = False

                # If all lords are P/N, it is considered fruitful by the new rule
                if is_this_combination_fruitful_by_lords:
                    current_fruitful_periods_this_iteration.append(prana_period_data)

                    # For display purposes, we can still show PC/SC signification,
                    # but it's no longer a *condition* for 'Fruitful? YES'.
                    all_lords_in_combination = [md_lord, ad_lord, pd_lord, sd_lord, prd_lord]
                    combined_static_sigs = self._get_combined_significators_for_lords_static(
                        all_lords_in_combination, original_primary_cusp_num
                    )

                    # We still call _is_combined_dasha_fruitful to get the display strings for PC/SCs,
                    # but its boolean return value is no longer used for 'Fruitful?' column.
                    # It will always be True based on the 'is_this_combination_fruitful_by_lords' check.
                    # The return values of _is_combined_dasha_fruitful (cusp_details_str, num_sc_signified) are still used for display.
                    _, cusp_details_str, num_sc_signified = \
                        self._is_combined_dasha_fruitful(combined_static_sigs, primary_cusp_num_for_analysis,
                                                         secondary_cusp_nums)

                    if not only_return_fruitful_spans:
                        signified_pc_display = "YES" if primary_cusp_num_for_analysis in combined_static_sigs else "NO"
                        signified_sc_display = "None"
                        if num_sc_signified > 0:
                            actual_signified_sc = [str(sc) for sc in secondary_cusp_nums if
                                                   sc in combined_static_sigs]
                            signified_sc_display = f"{num_sc_signified}/{len(secondary_cusp_nums)} ({', '.join(sorted(actual_signified_sc))})"
                        elif len(secondary_cusp_nums) == 0:
                            signified_sc_display = "N/A (no SCs selected)"

                        fruitful_periods_display.append((
                            md_lord, ad_lord, pd_lord, sd_lord, prd_lord,
                            "YES", # Always YES if lords are P/N
                            signified_pc_display,
                            signified_sc_display,
                            prana_period_data['start_local'].strftime('%Y-%m-%d %H:%M:%S'),
                            prana_period_data['end_local'].strftime('%Y-%m-%d %H:%M:%S')
                        ))

            self.fruitful_dasha_spans.extend(current_fruitful_periods_this_iteration)

            if current_fruitful_periods_this_iteration:  # Check if any periods were found in this iteration
                if not only_return_fruitful_spans:
                    if iteration == 0:
                        messagebox.showinfo("Fruitful Spans Found",
                                           "Fruitful Dasha periods found within the initial range.")
                    else:
                        messagebox.showinfo("Extended Search Success",
                                           f"No fruitful periods found in initial range. Found some in extended search (Iteration {iteration + 1}).")
                self._log_debug(
                    f"Found {len(current_fruitful_periods_this_iteration)} fruitful spans in iteration {iteration + 1}. Stopping search.")
                break  # Found some, stop searching further iterations

            # Prepare for next search window
            if analysis_mode == "24_hours":
                if iteration == 0:  # Only one 7-day extension for 24-hour mode
                    search_start_utc = initial_analysis_end_utc  # Start from the end of the initial 24h period
                    search_end_utc = search_start_utc + datetime.timedelta(days=7)
                    self._log_debug(f"  Extending 24-hour search to {search_end_utc} (next 7 days).")
                else:  # After the first 7-day extension, if still nothing, break
                    self._log_debug("  24-hour search exhausted (1 initial + 1x7-day extension).")
                    break
            elif analysis_mode == "custom_span":
                search_start_utc = search_end_utc
                search_end_utc += datetime.timedelta(days=90)
                self._log_debug(f"  Extending custom search by 90 days. New end: {search_end_utc}")

            if not only_return_fruitful_spans and progress_label:
                progress_label.config(
                    text=f"No fruitful periods found. Extending search (Iteration {iteration + 2})...")
                self.root.update_idletasks()

        if not only_return_fruitful_spans:
            if progress_window:
                progress_bar.stop()
                progress_window.destroy()

            fruitful_periods_display.sort(key=lambda x: (x[8], x[0], x[1], x[2], x[3], x[4]))

            for row_data in fruitful_periods_display:
                self.analysis_results_tree.insert("", "end", values=row_data)

            if not self.analysis_results_tree.get_children():
                self.analysis_results_tree.insert("", "end", values=(
                    "", "", "", "", "", "", "",
                    "No Dasha periods found in the selected range or after 7 search iterations.", "", ""
                ))
                self._log_debug("No fruitful dasha periods found after all iterations.")
        self._log_debug("Combined Dasha Significator Analysis complete.")

    def _run_positive_jupiter_transit_analysis(self):
        self._log_debug("Running Positive Jupiter Transit Analysis.")
        self._update_analysis_results_tree_columns("jupiter_transit")

        if not self.current_planetary_positions or not self.current_cuspal_positions or not self.stellar_significators_data:
            messagebox.showwarning("Chart Data Missing",
                                   "Please generate a chart first in the 'Chart Generation' tab and ensure stellar significators are calculated (check 'Stellar Status Significators' tab once).")
            self._log_debug("ERROR: Chart data or stellar significators missing for Jupiter transit analysis.")
            return

        original_primary_cusp_num = self._get_original_primary_cusp_from_ui()
        if original_primary_cusp_num is None: return

        primary_cusp_num_for_analysis = self._determine_primary_cusp_for_analysis(original_primary_cusp_num)

        # Ensure planet classifications are cached
        self._cache_static_planet_classifications(primary_cusp_num_for_analysis, original_primary_cusp_num)
        if not hasattr(self, 'planet_classifications') or not self.planet_classifications:
            messagebox.showerror("Internal Error", "Planet classifications not cached. Please generate chart first.")
            self._log_debug("ERROR: Planet classifications not cached for Jupiter transit analysis.")
            return

        timezone_str = self.timezone_combo.get()
        local_tz = pytz.timezone(timezone_str)

        # Ensure fruitful dasha spans are populated based on the current analysis mode.
        # This will call _run_combined_dasha_significator_analysis in helper mode.
        self._run_combined_dasha_significator_analysis(only_return_fruitful_spans=True)

        if not self.fruitful_dasha_spans:
            messagebox.showwarning("Prerequisite Missing",
                                   "Please run 'Find Fruitful Dasha Spans' first (which applies relevant filters) to determine the time periods for Jupiter Transit analysis. No fruitful Dasha periods were found.")
            self._log_debug("No fruitful Dasha periods found to analyze Jupiter transit. Exiting.")
            return

        overall_analysis_start_dt_utc = min(span['start_utc'] for span in self.fruitful_dasha_spans)
        overall_analysis_end_dt_utc = max(span['end_utc'] for span in self.fruitful_dasha_spans)
        self._log_debug(
            f"Jupiter Transit analysis range: {overall_analysis_start_dt_utc} to {overall_analysis_end_dt_utc}")

        city = self.city_combo.get()
        hsys_const = self._get_selected_hsys()
        if hsys_const is None: return

        horary_num_str = self.horary_entry.get()
        horary_num_value = int(horary_num_str) if horary_num_str.isdigit() and (
                1 <= int(horary_num_str) <= 2193) else None

        self.analysis_results_tree.delete(*self.analysis_results_tree.get_children())

        progress_window = tk.Toplevel(self.root)
        progress_window.title("Positive Jupiter Transit Progress")
        progress_window.transient(self.root)
        progress_window.grab_set()
        progress_label = ttk.Label(progress_window, text="Analyzing Jupiter Transits in Fruitful Spans...")
        progress_label.pack(pady=10)
        progress_bar = ttk.Progressbar(progress_window, orient='horizontal', length=250, mode='determinate')
        progress_bar.pack(pady=5)
        progress_label_percent = ttk.Label(progress_window, text="0.0%")
        progress_label_percent.pack()
        progress_bar.start()
        self.root.update_idletasks()

        consolidated_jupiter_transit_results = []
        total_seconds_to_process = sum(
            [(span['end_utc'] - span['start_utc']).total_seconds() for span in self.fruitful_dasha_spans])
        seconds_processed = 0

        analysis_interval_seconds = 60  # Check every minute

        for fruitful_span_data in self.fruitful_dasha_spans:
            current_span_start_utc = fruitful_span_data['start_utc']
            current_span_end_utc = fruitful_span_data['end_utc']
            self._log_debug(
                f"  Checking Jupiter Transit for fruitful span: {current_span_start_utc} - {current_span_end_utc}")

            span_duration_seconds = (current_span_end_utc - current_span_start_utc).total_seconds()
            if span_duration_seconds <= 0:
                self._log_debug(f"  Skipping empty or negative duration Jupiter transit span: {span_duration_seconds}s")
                seconds_processed += span_duration_seconds
                continue

            current_jupiter_block_start_time = None
            last_jupiter_sl = "N/A"
            last_jupiter_subl = "N/A"
            last_jupiter_sl_type = "N/A"
            last_jupiter_subl_signifies_pc = "NO"

            for s_offset in range(0, int(span_duration_seconds) + 1, analysis_interval_seconds):
                current_time_point_utc = current_span_start_utc + datetime.timedelta(seconds=s_offset)

                if current_time_point_utc > current_span_end_utc:
                    current_time_point_utc = current_span_end_utc

                dynamic_planetary_positions, _, _ = self._calculate_chart_data(
                    current_time_point_utc, city, hsys_const, horary_num_value
                )

                is_jupiter_favorable_now = False
                jupiter_data = dynamic_planetary_positions.get('Jupiter')
                self._log_debug(f"    @ {current_time_point_utc}: Checking Jupiter transit.")

                if jupiter_data:
                    jupiter_sl_at_this_second = jupiter_data[3]  # Star Lord
                    jupiter_subl_at_this_second = jupiter_data[4]  # Sub Lord
                    self._log_debug(f"    Jupiter SL: {jupiter_sl_at_this_second}, SubL: {jupiter_subl_at_this_second}")

                    # Check Jupiter Star Lord condition (Positive or Neutral)
                    jupiter_sl_class = self.planet_classifications.get(jupiter_sl_at_this_second, 'Unclassified')

                    current_jupiter_sl_type = "N/A"
                    if jupiter_sl_class == 'Positive':
                        current_jupiter_sl_type = "Positive"
                    elif jupiter_sl_class == 'Neutral':
                        current_jupiter_sl_type = "Neutral"

                    is_jupiter_sl_favorable = (jupiter_sl_class == 'Positive' or jupiter_sl_class == 'Neutral')
                    self._log_debug(
                        f"    Jupiter SL ({jupiter_sl_at_this_second}) classified as: {jupiter_sl_class}. Favorable: {is_jupiter_sl_favorable}")

                    # Check Jupiter Sub Lord condition (Positive significator for Primary Cusp)
                    # This implies checking if Jupiter Sub Lord's static significators (from cache) contain PC.
                    # IMPORTANT: When checking Jupiter Sub Lord's static significators, we must use the
                    # 'original_primary_cusp_num' (before Rule 1 adjustment) for Rule 2 filtering.
                    jupiter_subl_sigs = self._get_planet_final_significators(
                        jupiter_subl_at_this_second, original_primary_cusp_num, exclude_8_12_from_non_8_12_pc=True
                    )
                    is_jupiter_subl_positive_for_pc = primary_cusp_num_for_analysis in jupiter_subl_sigs
                    self._log_debug(
                        f"    Jupiter SubL ({jupiter_subl_at_this_second}) static sigs: {sorted(list(jupiter_subl_sigs))}. Signifies PC ({primary_cusp_num_for_analysis}): {is_jupiter_subl_positive_for_pc}")

                    current_jupiter_subl_signifies_pc = "YES" if is_jupiter_subl_positive_for_pc else "NO"

                    is_jupiter_favorable_now = is_jupiter_sl_favorable and is_jupiter_subl_positive_for_pc
                    self._log_debug(f"    Overall Jupiter favorable: {is_jupiter_favorable_now}")

                    if is_jupiter_favorable_now:
                        last_jupiter_sl = jupiter_sl_at_this_second
                        last_jupiter_subl = jupiter_subl_at_this_second
                        last_jupiter_sl_type = current_jupiter_sl_type
                        last_jupiter_subl_signifies_pc = current_jupiter_subl_signifies_pc

                if is_jupiter_favorable_now:
                    if current_jupiter_block_start_time is None:
                        current_jupiter_block_start_time = current_time_point_utc
                        self._log_debug(f"    Jupiter block started at {current_jupiter_block_start_time}")
                else:
                    if current_jupiter_block_start_time is not None:
                        end_time_of_block_utc = current_time_point_utc - datetime.timedelta(
                            seconds=analysis_interval_seconds)
                        if end_time_of_block_utc < current_jupiter_block_start_time:
                            end_time_of_block_utc = current_jupiter_block_start_time

                        start_display_time = current_jupiter_block_start_time.astimezone(local_tz).strftime(
                            '%Y-%m-%d %H:%M:%S')
                        end_display_time = end_time_of_block_utc.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')

                        consolidated_jupiter_transit_results.append((
                            f"House {primary_cusp_num_for_analysis}",
                            f"{start_display_time} - {end_display_time}",
                            last_jupiter_sl_type,
                            last_jupiter_subl_signifies_pc,
                            last_jupiter_sl,
                            last_jupiter_subl
                        ))
                        self._log_debug(f"    Jupiter block ended: {start_display_time} - {end_display_time}")
                        current_jupiter_block_start_time = None

                seconds_processed += analysis_interval_seconds
                progress = (seconds_processed / total_seconds_to_process) * 100 if total_seconds_to_process > 0 else 100
                progress_bar['value'] = progress
                progress_label_percent.config(text=f"{progress:.1f}%")
                self.root.update_idletasks()

            if current_jupiter_block_start_time is not None:
                end_time_of_block_utc = current_span_end_utc
                start_display_time = current_jupiter_block_start_time.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
                end_display_time = end_time_of_block_utc.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')

                consolidated_jupiter_transit_results.append((
                    f"House {primary_cusp_num_for_analysis}",
                    f"{start_display_time} - {end_display_time}",
                    last_jupiter_sl_type,
                    last_jupiter_subl_signifies_pc,
                    last_jupiter_sl,
                    last_jupiter_subl
                ))
                self._log_debug(f"    Jupiter block ended (span end): {start_display_time} - {end_display_time}")

        progress_bar.stop()
        progress_window.destroy()

        for row_data in consolidated_jupiter_transit_results:
            self.analysis_results_tree.insert("", "end", values=row_data)

        if not self.analysis_results_tree.get_children():
            self.analysis_results_tree.insert("", "end", values=(
                f"House {primary_cusp_num_for_analysis}",
                "No periods of positive Jupiter transit found within fruitful Dasha spans.",
                "", "", "", ""
            ))
            self._log_debug("No positive Jupiter transit periods found.")
        self._log_debug("Positive Jupiter Transit Analysis complete.")

    def _copy_treeview_to_clipboard(self, treeview_widget):
        header = [treeview_widget.heading(col_id)['text'] for col_id in treeview_widget['columns']]
        data = []
        for item_id in treeview_widget.get_children():
            data.append(list(treeview_widget.item(item_id)['values']))

        output_str = "\t".join(map(str, header)) + "\n"
        for row in data:
            output_str += "\t".join(map(str, row)) + "\n"

        self.root.clipboard_clear()
        self.root.clipboard_append(output_str)
        messagebox.showinfo("Copied", "Table data copied to clipboard.")
        self._log_debug("Table data copied to clipboard.")

    def _copy_listbox_to_clipboard(self, listbox_widget):
        data = "\n".join(listbox_widget.get(0, tk.END))
        self.root.clipboard_clear()
        self.root.clipboard_append(data)
        messagebox.showinfo("Copied", "Results copied to clipboard.")
        self._log_debug("Listbox data copied to clipboard.")

    def _popup_save_chart(self):
        """Creates the popup window for saving a chart."""
        if not self.current_planetary_positions:
            messagebox.showerror("Error", "Please generate a chart before saving.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Save Chart Details")
        popup.geometry("350x200")
        popup.transient(self.root)
        popup.grab_set()

        # Make the popup movable
        popup.bind("<ButtonPress-1>", lambda e: popup.lift())

        main_frame = ttk.Frame(popup, padding="10")
        main_frame.pack(expand=True, fill="both")

        # Name field
        ttk.Label(main_frame, text="Chart Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(main_frame, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        name_entry.insert(0, f"Chart_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")

        # Category field
        ttk.Label(main_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        category_frame = ttk.Frame(main_frame)
        category_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        category_var = tk.StringVar(value=self.chart_type_var.get())
        ttk.Radiobutton(category_frame, text="Birth Chart", variable=category_var, value="Birth Chart").pack(
            side="left")
        ttk.Radiobutton(category_frame, text="Horary", variable=category_var, value="Horary").pack(side="left", padx=10)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))

        ok_button = ttk.Button(button_frame, text="OK",
                               command=lambda: self._execute_save(name_entry, category_var, popup))
        ok_button.pack(side="left", padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side="left", padx=10)

        popup.focus_set()
        popup.wait_window()

    def _get_data_from_treeview(self, tree):
        """Helper to extract all data from a Treeview, including headers."""
        if not tree.winfo_exists(): return None

        headers = [tree.heading(col)["text"] for col in tree["columns"]]
        data = [list(tree.item(item_id, "values")) for item_id in tree.get_children()]
        return {"headers": headers, "rows": data}

    def _execute_save(self, name_entry, category_var, popup_window):
        """Gathers all data and saves it to a JSON file."""
        chart_name = name_entry.get().strip()
        if not chart_name:
            messagebox.showerror("Input Error", "Chart Name cannot be empty.", parent=popup_window)
            return

        # Create the save directory if it doesn't exist
        save_dir = r"C:\Chart"
        try:
            os.makedirs(save_dir, exist_ok=True)
        except OSError as e:
            messagebox.showerror("Directory Error", f"Could not create directory {save_dir}:\n{e}", parent=popup_window)
            return

        file_path = os.path.join(save_dir, f"{chart_name}.json")

        if os.path.exists(file_path):
            if not messagebox.askyesno("Confirm Overwrite",
                                       f"File '{chart_name}.json' already exists.\nDo you want to overwrite it?",
                                       parent=popup_window):
                return

        # Gather all data into a dictionary
        full_chart_data = {
            "chart_name": chart_name,
            "category": category_var.get(),
            "saved_at_utc": datetime.datetime.now(pytz.utc).isoformat(),
            "inputs": {
                "horary_num": self.horary_entry.get(),
                "date": f"{self.year_lb.get(self.year_lb.curselection())}-{MONTH_NAMES.index(self.month_lb.get(self.month_lb.curselection())) + 1:02d}-{self.day_lb.get(self.day_lb.curselection())}",
                "time": f"{self.hour_lb.get(self.hour_lb.curselection())}:{self.minute_lb.get(self.minute_lb.curselection())}:{self.second_lb.get(self.second_lb.curselection())}",
                "city": self.city_combo.get(),
                "timezone": self.timezone_combo.get(),
                "house_system": self.house_sys_combo.get()
            },
            "results": {
                "general_info": self.current_general_info,
                "planetary_positions": self.current_planetary_positions,
                "cuspal_positions": self.current_cuspal_positions,
                "stellar_significators_data": self.stellar_significators_data,
                "ruling_planets_tree": self._get_data_from_treeview(self.rp_tree),
                "daily_analysis_tree": self._get_data_from_treeview(self.analysis_results_tree)
            }
        }

        # Convert datetime objects in general_info to strings for JSON compatibility
        if 'natal_utc_dt' in full_chart_data['results']['general_info']:
            full_chart_data['results']['general_info']['natal_utc_dt'] = full_chart_data['results']['general_info'][
                'natal_utc_dt'].isoformat()

        try:
            with open(file_path, 'w') as f:
                json.dump(full_chart_data, f, indent=4)
            messagebox.showinfo("Success", f"Chart and all results saved to:\n{file_path}")
            popup_window.destroy()
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save chart file:\n{e}", parent=popup_window)

    def _populate_treeview_from_data(self, tree, data_dict):
        """Helper to clear and populate a Treeview from a dictionary with headers and rows."""
        if not tree.winfo_exists() or not data_dict or not data_dict.get("rows"):
            return

        tree.delete(*tree.get_children())

        # Optionally set headers if needed, though they are usually static
        # for col_id, header_text in zip(tree['columns'], data_dict.get("headers", [])):
        #     tree.heading(col_id, text=header_text)

        for i, row_values in enumerate(data_dict["rows"]):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=row_values, tags=(tag,))

    def _analyze_vehicle_rules(self):
        """
        Analyzes and returns a list of conclusions based on a detailed set of rules
        for vehicle purchase from the static chart.
        """
        self._log_debug("Applying detailed vehicle analysis rules.")
        results = []

        # --- 1. Gather Prerequisite Data ---
        try:
            c4_data = self.current_cuspal_positions[4]
            c4sl_name = c4_data[4]  # 4th Cusp Sub Lord

            if not c4sl_name or c4sl_name not in self.current_planetary_positions:
                return ["Error: 4th Cusp Sub Lord could not be determined."]

            c4sl_planet_data = self.current_planetary_positions[c4sl_name]
            c4sl_sl_name = c4sl_planet_data[3]  # Star Lord of 4th Cusp Sub Lord
            c4sl_subl_name = c4sl_planet_data[4]  # Sub Lord of 4th Cusp Sub Lord

            c4sl_sl_sigs = set(self.stellar_significators_data.get(c4sl_sl_name, {}).get('final_sigs', []))
            c4sl_subl_sigs = set(self.stellar_significators_data.get(c4sl_name, {}).get('final_sigs',
                                                                                        []))  # Corrected to get sigs of C4SL itself

            c4sl_sign = self.get_sign(c4sl_planet_data[0])

        except Exception as e:
            self._log_debug(f"Error gathering data for vehicle rules: {e}")
            return [f"An error occurred during analysis setup: {e}"]

        # --- Promise Check ---
        promise_fulfilled = False
        if {4, 6}.issubset(c4sl_sl_sigs):
            results.append("Promise Check: Yes, Native will Purchase Vehicle.")
            promise_fulfilled = True
        elif {3}.issubset(c4sl_sl_sigs) and 6 not in c4sl_sl_sigs:
            results.append("Promise Check: Native will not Purchase a vehicle.")
            return results  # Stop processing further rules
        else:
            results.append("Promise Check: Promise for vehicle purchase is not clearly indicated.")
            return results  # Stop processing further rules

        # --- Step A: Detailed Rules (only if promise is fulfilled) ---
        if not promise_fulfilled:
            return results

        # Rule 1
        if {4, 6}.issubset(c4sl_sl_sigs):
            results.append("Rule 1: Luxorius Vehicle.")
        # Rule 2 & 4 (Identical)
        if {4, 9, 6}.issubset(c4sl_sl_sigs):
            results.append("Rule 2/4: Old/Used Car.")
        # Rule 3
        if {4, 3, 9, 10}.issubset(c4sl_sl_sigs):
            results.append("Rule 3: Exchange Of Vehicle.")
        # Rule 5
        if {9, 10, 2, 11}.issubset(c4sl_sl_sigs):  # Changed from c4sl_subl_sigs to c4sl_sl_sigs as per pattern
            results.append("Rule 5: Vehicle had Accident.")
        # Rule 6
        if {4, 3, 10, 11}.issubset(c4sl_sl_sigs):
            results.append("Rule 6: Will Borrow Vehicle.")
        # Rule 7
        if c4sl_name == 'Ketu' and {4, 3, 10, 11}.issubset(c4sl_sl_sigs):
            results.append("Rule 7: Govt. Vehicle.")
        # Rule 8
        if {4, 3, 12}.issubset(c4sl_subl_sigs):
            results.append("Rule 8: Will Frequently Change Vehicle.")
        # Rule 9
        if c4sl_name == 'Saturn' and {4, 11}.issubset(c4sl_sl_sigs):
            results.append("Rule 9: Vehicle will be Bi-Cycle.")
        # Rule 10
        if c4sl_sign == 'Gemini' and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 10: Will Purchase a MO-ped.")
        # Rule 11
        if c4sl_sign == 'Sagittarius' and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 11: Two wheeler with Gear.")
        # Rule 12
        if c4sl_sign == 'Pisces' and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 12: Will Purchase a Scooter.")
        # Rule 13
        if c4sl_sign in ['Taurus', 'Cancer', 'Scorpio'] and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 13: A Car will be Purchased.")
        # Rule 14
        if c4sl_name == 'Rahu' and c4sl_sign == 'Taurus' and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 14: A Jeep will be purchased.")
        # Rule 15
        if c4sl_name == 'Saturn' and c4sl_sign == 'Aquarius' and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 15: Will Purchase a 3 Wheeler.")
        # Rule 16
        if c4sl_sign == 'Aries' and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 16: Will Purchase Good Vehicle.")
        # Rule 17
        if c4sl_sign == 'Leo' and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 17: Hire for Transport vehicle.")
        # Rule 18
        if c4sl_sign == 'Cancer' and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 18: Will Purchase a Lorry.")
        # Rule 19
        if c4sl_sign == 'Scorpio' and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 19: Tanker/ Multi wheel.")
        # Rule 20
        if c4sl_sign == 'Sagittarius' and c4sl_name in ['Saturn', 'Mercury'] and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 20: Bullock Cart.")
        # Rule 21
        if c4sl_sign == 'Cancer' and c4sl_name == 'Moon' and {4, 6}.issubset(c4sl_subl_sigs):
            results.append("Rule 21: Purchase Boat.")
        # Rule 22
        if (c4sl_name == 'Jupiter' or c4sl_sl_name == 'Jupiter' or c4sl_subl_name == 'Jupiter') and {4, 6}.issubset(
                c4sl_subl_sigs):
            results.append("Rule 22: Will Appoint a Driver.")
        # Rule 23
        if {6}.issubset(c4sl_subl_sigs):
            results.append("Rule 23: Car Purchase Through taking loans.")
        # Rule 24
        if {2, 11}.issubset(c4sl_subl_sigs):
            results.append("Rule 24: Vehicle Purchase through Cash.")
        # Rule 25
        if c4sl_name == 'Jupiter' and SIGN_LEGS.get(c4sl_sign, "").startswith("Quadruped") and {4, 6}.issubset(
                c4sl_subl_sigs):
            results.append("Rule 25: Owner of Multiple Vehicle.")
        # Rule 26
        if (c4sl_name in ['Jupiter', 'Sun'] or c4sl_sl_name in ['Jupiter', 'Sun'] or c4sl_subl_name in ['Jupiter',
                                                                                                        'Sun']) and {3,
                                                                                                                     6,
                                                                                                                     8,
                                                                                                                     12}.issubset(
                c4sl_subl_sigs):
            results.append("Rule 26: Vehicle will be Seized.")
        # Rule 27
        if (c4sl_name in ['Ketu', 'Saturn'] or c4sl_sl_name in ['Ketu', 'Saturn'] or c4sl_subl_name in ['Ketu',
                                                                                                        'Saturn']) and {
            3, 5, 8, 12}.issubset(c4sl_subl_sigs):
            results.append("Rule 27: Vehicle will be Stolen.")
        # Rule 28
        if {4, 8, 12}.issubset(c4sl_subl_sigs):
            results.append("Rule 28: Vehicle will Give frequent Trouble.")
        # Rule 29
        if (c4sl_name in ['Mars', 'Saturn'] or c4sl_sl_name in ['Mars', 'Saturn'] or c4sl_subl_name in ['Mars',
                                                                                                        'Saturn']) and {
            4, 8, 12}.issubset(c4sl_subl_sigs):
            results.append("Rule 29: Vehicle will cause Accidents.")
        # Rule 30
        if (c4sl_name in ['Mars', 'Sun'] or c4sl_sl_name in ['Mars', 'Sun'] or c4sl_subl_name in ['Mars',
                                                                                                  'Sun']) and SIGN_ELEMENT.get(
                c4sl_sign) == "Fire" and {4, 8}.issubset(c4sl_subl_sigs):
            results.append("Rule 30: Vehicle will cause Fire Accident.")

        return results

    def _load_chart_and_results(self):
        """
        (UPDATED) Loads a full chart state from a JSON file.
        It no longer automatically re-calculates Ruling Planets or classifications upon load,
        as these are now event-dependent and triggered by the Promise button.
        """
        save_dir = r"C:\Chart"
        file_path = filedialog.askopenfilename(
            title="Load Chart File",
            initialdir=save_dir,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            # --- Restore Inputs from saved file ---
            inputs = data.get("inputs", {})
            self.horary_entry.delete(0, tk.END)
            self.horary_entry.insert(0, inputs.get("horary_num", ""))

            loaded_date = datetime.datetime.strptime(inputs.get("date"), "%Y-%m-%d").date()
            loaded_time = datetime.datetime.strptime(inputs.get("time"), "%H:%M:%S").time()

            def select_item_by_value(listbox, value):
                for i, item in enumerate(listbox.get(0, tk.END)):
                    if str(item) == str(value):
                        listbox.selection_clear(0, tk.END)
                        listbox.selection_set(i)
                        listbox.see(i)
                        return

            select_item_by_value(self.year_lb, loaded_date.year)
            select_item_by_value(self.month_lb, MONTH_NAMES[loaded_date.month - 1])
            select_item_by_value(self.day_lb, f"{loaded_date.day:02d}")
            select_item_by_value(self.hour_lb, f"{loaded_time.hour:02d}")
            select_item_by_value(self.minute_lb, f"{loaded_time.minute:02d}")
            select_item_by_value(self.second_lb, f"{loaded_time.second:02d}")

            self.city_combo.set(inputs.get("city", "Kolkata"))
            self.timezone_combo.set(inputs.get("timezone", "Asia/Kolkata"))
            self.house_sys_combo.set(inputs.get("house_system", "Placidus"))
            self.chart_type_var.set(data.get("category", "Horary"))
            self._toggle_chart_type_inputs()

            # --- Restore Core Astrological Data ---
            results = data.get("results", {})
            self.current_planetary_positions = results.get("planetary_positions", {})
            self.current_cuspal_positions = {int(k): v for k, v in results.get("cuspal_positions", {}).items()}
            self.current_general_info = results.get("general_info", {})
            if 'natal_utc_dt' in self.current_general_info and isinstance(self.current_general_info['natal_utc_dt'],
                                                                           str):
                self.current_general_info['natal_utc_dt'] = datetime.datetime.fromisoformat(
                    self.current_general_info['natal_utc_dt'])
            self.stellar_significators_data = results.get("stellar_significators_data", {})

            # --- Refresh UI with loaded data ---
            self._update_main_chart_display(self.current_planetary_positions, self.current_cuspal_positions,
                                             self.current_general_info)
            self._populate_all_stellar_significators_table()
            self._calculate_dasha_levels(start_dt=self.current_general_info['natal_utc_dt'],
                                         moon_sidereal_degree=self.current_planetary_positions['Moon'][0])

            # RP Tree and Daily Analysis Tree will be empty or show outdated data initially.
            # User must re-calculate them by interacting with Daily Analysis tab.
            self.rp_tree.delete(*self.rp_tree.get_children()) # Clear old RPs
            self.analysis_results_tree.delete(*self.analysis_results_tree.get_children()) # Clear old analysis results

            # Inform the user what to do next
            messagebox.showinfo("Load Complete",
                                f"Successfully loaded chart: {data.get('chart_name')}.\n\n"
                                "Please go to the 'Daily Analysis' tab, select your event/cusps, and click 'Check Promise' to update planet classifications and Ruling Planets for this query.")

        except FileNotFoundError:
            messagebox.showerror("Load Error", "File not found.")
        except Exception as e:
            self._log_debug(f"Error during chart load: {e}")
            messagebox.showerror("Load Error", f"Failed to load and parse chart file:\n{e}")

    def _save_chart_input(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if not file_path:
            self._log_debug("Save chart input cancelled by user.")
            return
        try:
            year_str = self.year_lb.get(self.year_lb.curselection())
            month_name = self.month_lb.get(self.month_lb.curselection())
            day_str = self.day_lb.get(self.day_lb.curselection())
            hour_str = self.hour_lb.get(self.hour_lb.curselection())
            minute_str = self.minute_lb.get(self.minute_lb.curselection())
            second_str = self.second_lb.get(self.second_lb.curselection())
            month_num = MONTH_NAMES.index(month_name) + 1
            date_to_save = f"{year_str}-{month_num:02d}-{day_str}"
            time_to_save = f"{hour_str}:{minute_str}:{second_str}"
        except (tk.TclError, ValueError, IndexError):
            messagebox.showerror("Save Error", "Cannot save. Please ensure a value is selected for all date and time fields.")
            return
        city_to_save = self.city_combo.get()
        if city_to_save not in ALL_INDIAN_CITIES:
            messagebox.showerror("Save Error", f"'{city_to_save}' is not a valid city from the list. Please select a valid city before saving.")
            return
        data = {
            "horary_num": self.horary_entry.get(),
            "date": date_to_save,
            "time": time_to_save,
            "city": city_to_save,
            "timezone": self.timezone_combo.get(),
            "house_system": self.house_sys_combo.get()
        }
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Save Chart Input", "Chart input saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save chart input: {e}")

    def _load_chart_input(self):
        file_path = filedialog.askopenfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if not file_path:
            self._log_debug("Load chart input cancelled by user.")
            return
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.horary_entry.delete(0, tk.END)
            self.horary_entry.insert(0, data.get("horary_num", ""))
            def select_item(listbox, value):
                try:
                    items = list(listbox.get(0, tk.END))
                    if str(value) in items:
                        idx = items.index(str(value))
                        listbox.selection_clear(0, tk.END)
                        listbox.selection_set(idx)
                        listbox.see(idx)
                except ValueError:
                    self._log_debug(f"Value {value} not found in listbox during load.")
            loaded_date_str = data.get("date", "")
            if loaded_date_str:
                loaded_date = datetime.datetime.strptime(loaded_date_str, "%Y-%m-%d").date()
                select_item(self.year_lb, loaded_date.year)
                select_item(self.month_lb, MONTH_NAMES[loaded_date.month - 1])
                select_item(self.day_lb, f"{loaded_date.day:02d}")
            loaded_time_str = data.get("time", "")
            if loaded_time_str:
                loaded_time = datetime.datetime.strptime(loaded_time_str, "%H:%M:%S").time()
                select_item(self.hour_lb, f"{loaded_time.hour:02d}")
                select_item(self.minute_lb, f"{loaded_time.minute:02d}")
                select_item(self.second_lb, f"{loaded_time.second:02d}")
            self.city_combo.set(data.get("city", "Kolkata"))
            self.timezone_combo.set(data.get("timezone", "Asia/Kolkata"))
            self.house_sys_combo.set(data.get("house_system", "Placidus"))
            self._on_generate_chart_button()
            messagebox.showinfo("Load Chart Input", "Chart input loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Load Error", "File not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Load Error", "Invalid JSON file format.")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load chart input: {e}")

    def start_tour(self):
        """Initializes and starts the interactive guided tour."""
        self._tour_ended = False
        self._blink_job_id = None

        # --- The tour steps list has been updated ---
        self.tour_steps = [
            {
                'widget': self.chart_type_frame,
                'text': ("Step 1: You can choose between Birth chart or Prashna/Horary chart here.\n\n"
                         "When you choose Birth chart, the Horary number input field will be ghosted as it is not needed.\n\n"
                         "For a Horary number: Meditate on the issue for 2 minutes, then think of a random number from 1 to 2193. It must be random, not a lucky number or a date."),
                'pos': 'bottom',
                'tab_name': 'Chart Generation'
            },
            {
                'widget': self.horary_entry,
                'text': 'Step 2: Here, you will enter the random horary number.',
                'pos': 'right',
                'tab_name': 'Chart Generation'
            },
            {
                'widget': self.generate_chart_button,
                'text': 'Step 3: Press this button to perform the main calculation for planetary positions and charts.',
                'pos': 'bottom',
                'tab_name': 'Chart Generation'
            },
            {
                'widget': [self.event_type_combo, self.primary_cusp_combo, self.secondary_cusp_listbox],
                'text': 'Step 4: Go to the Daily Analysis tab. Here you can choose your question. This will auto-select the Primary and Secondary cusps for you, which will blink to draw your attention.',
                'pos': 'right',
                'tab_name': 'Daily Analysis',
                'blink': True
            },
            {
                'widget': self.full_analysis_button,
                'text': 'Step 5: Press this button to run a Full Analysis and find all possible dates for the selected event.',
                'pos': 'top',
                'tab_name': 'Daily Analysis'
            },
            {
                'widget': self.sort_best_button,
                'text': 'Step 6: After the analysis, use this button to sort the results and bring the strongest, most favorable dates to the top of the list.',
                'pos': 'top',
                'tab_name': 'Daily Analysis'
            },
            # --- THIS STEP HAS BEEN CORRECTED ---
            {
                'widget': self.notebook, # Point to the notebook itself
                'text': "Step 7: When a disease-related event is selected in the 'Daily Analysis' tab, the 'Disease' tab (which is normally hidden) will appear here automatically, and the analysis will run instantly.",
                'pos': 'top',
                # We will manually show the tab for the guide's purpose
                'action': lambda: self.notebook.add(self.disease_frame, text="Disease") if str(self.disease_frame) not in self.notebook.tabs() else None,
                'tab_name': 'Disease'
            },
            # --- END OF CORRECTION ---
            {
                'widget': self.root,  # Use the main window as an anchor for the final message
                'text': "Step 8: End of the guide. You can now explore the application freely. Click 'End Tour' to close this window.",
                'pos': 'center'
            }
        ]
        self.current_step = -1
        self.last_highlighted_widget_info = None

        # Create or lift the pop-up window for the tour
        if not hasattr(self, 'tour_popup') or not self.tour_popup.winfo_exists():
            self._create_tour_popup()
        self.tour_popup.lift()

        # Start with the first step
        self.next_step()

    from typing import Any  # Needed for type hinting list[Any]
    import datetime
    import re  # Needed for the unique signature part if used, otherwise remove
    # Assume swisseph, pytz, logging, etc. are already imported in your main app file.

    # This function belongs INSIDE your AstrologyApp class
    def _perform_cuspal_interlink_scan(self, windows_to_scan, strict_qualified_rps, relaxed_qualified_rps,
                                       pc_for_analysis, secondary_cusp_nums,
                                       progress_info):
        """
        Performs the high-frequency cuspal interlink scan.
        It iterates through time windows and for each minute, checks if a strong cuspal
        interlink is active, based on the following revised rules:

        1.  **Primary Cusp's Sub Lord (PC SL):** Must be a STRICTLY qualified RP (Positive RP).
        2.  **Star Lord of PC SL (PC SL's SL):** Must be a RELAXED qualified RP (Positive OR Neutral RP).
        3.  **Secondary Cusps Connection:**
            * PC SL's SL must connect (Star Match, Rahu/Ketu Agency, or Shared SL) to the Sub Lords of AT LEAST ONE of the chosen Secondary Cusps.
            * Connecting SC's Sub Lord (and its dispositors for Rahu/Ketu agency, or its Star Lord for Shared SL)
                needs to be a Positive OR Neutral *planet* (not necessarily an RP).
            (Note: Secondary cusps are now assumed to always be present as a requirement for interlink, if chosen by event type.)
        """
        self._log_debug("--- _perform_cuspal_interlink_scan: Start ---")
        final_hits: list[Any] = []
        last_hit_signature = None  # For de-duplication

        # Get chart context from UI elements (assuming these are methods/attributes of self)
        city = self.city_combo.get()
        hsys_const = self._get_selected_hsys()
        horary_num = int(
            self.horary_entry.get()) if self.horary_entry.get() and self.chart_type_var.get() == "Horary" else None

        # Define scan interval (e.g., every 2 minutes for faster scanning)
        scan_interval_seconds = 120
        # Calculate total duration for progress bar display
        total_seconds_to_scan = sum((w['end_utc'] - w['start_utc']).total_seconds() for w in windows_to_scan if
                                    'end_utc' in w and 'start_utc' in w)
        processed_secs = 0
        start_time_process = datetime.datetime.now()

        # Iterate through each broad time window provided (from Dasha/Transit analysis)
        for window_detail in windows_to_scan:
            # --- DEBUGGING ADDITION (from previous step) ---
            self._log_debug(f"  Processing window_detail: {window_detail}")
            if 'original_display_row' not in window_detail:
                self._log_debug(
                    "  ERROR: 'original_display_row' key is MISSING in window_detail. Skipping this window.")
                continue  # Skip this malformed window_detail
            original_display_row = window_detail['original_display_row']  # Full original row data for reconstruction
            # --- END DEBUGGING ADDITION ---

            time_pointer = window_detail['start_utc']
            dasha_lords = window_detail.get('dasha_lords', [])  # Dasha lords active for this window

            # Scan minute-by-minute (or by scan_interval_seconds) within this broad window
            while time_pointer <= window_detail['end_utc']:
                # Calculate dynamic chart data (planetary and cuspal positions) for the current minute
                dyn_planets, dyn_cusps, _ = self._calculate_chart_data(time_pointer, city, hsys_const, horary_num)
                if not dyn_planets:  # Basic check to ensure chart data was generated
                    time_pointer += datetime.timedelta(seconds=scan_interval_seconds)
                    self._log_debug(f"  Skipping {time_pointer}: Dynamic chart data not generated.")
                    continue

                interlink_found_this_minute = False  # Flag to track if an interlink is found at THIS specific minute
                pc_sub_lord = dyn_cusps.get(pc_for_analysis, [None] * 6)[
                    4]  # Get the Primary Cusp's Sub Lord at this minute

                # Condition 1: Primary Cusp's Sub Lord MUST be a STRICTLY qualified RP (Positive RP)
                if pc_sub_lord in strict_qualified_rps:
                    pc_sl_data = dyn_planets.get(pc_sub_lord)  # Get the PC Sub Lord's own planetary data at this minute
                    if pc_sl_data:
                        pc_sl_star_lord = pc_sl_data[3]  # Get the Star Lord of the PC Sub Lord

                        # Condition 2: PC SL's Star Lord MUST be a RELAXED qualified RP (Positive OR Neutral RP)
                        if pc_sl_star_lord in relaxed_qualified_rps:

                            # Rahu and Ketu dispositors (their Sign/Star Lords) qualifications.
                            # They just need to be Positive or Neutral planets (not RPs).
                            # --- FIX: Change 'disposer' to 'disposer_name' in the first part of comprehension ---
                            rahu_dispositors = {disposer_name for disposer_name in
                                                [dyn_planets.get('Rahu', [None] * 6)[2],
                                                 dyn_planets.get('Rahu', [None] * 6)[3]]
                                                if disposer_name and self.planet_classifications.get(disposer_name) in [
                                                    'Positive', 'Neutral']}

                            ketu_dispositors = {disposer_name for disposer_name in
                                                [dyn_planets.get('Ketu', [None] * 6)[2],
                                                 dyn_planets.get('Ketu', [None] * 6)[3]]
                                                if disposer_name and self.planet_classifications.get(disposer_name) in [
                                                    'Positive', 'Neutral']}
                            # --- END FIX ---

                            linked_secondary_cusp_details = []  # List to store details of SCs that DO link

                            # Secondary Cusps Connection Condition (now the primary path)
                            if not secondary_cusp_nums:  # If no SCs are actually selected by the user for this query
                                self._log_debug(
                                    "  Warning: secondary_cusp_nums is empty for this query. No SCs to link to. Interlink will not be found via SCs.")
                                # This path will implicitly lead to no interlink found unless specific query doesn't require SCs for linking.
                                # The rule stated "Secondary cusp will always be present", so this `if` block implies a misconfiguration
                                # or that the event does not require SCs for linking in which case `len(linked_secondary_cusp_details) >= 1`
                                # would fail below. So, we're assuming if this path is taken, no interlink should be found *unless the specific query definition requires otherwise*.

                            for sc_num in secondary_cusp_nums:
                                sc_sub_lord = dyn_cusps.get(sc_num, [None] * 6)[
                                    4]  # Get Secondary Cusp's Sub Lord at this minute
                                link_type = None  # Stores the type of link found for this specific SC

                                # Check that SC Sub Lord itself is a Positive OR Neutral planet before checking links to it
                                sc_sub_lord_class = self.planet_classifications.get(sc_sub_lord)
                                if sc_sub_lord_class in ['Positive', 'Neutral']:
                                    # Basic Star Match: PC SL's Star Lord == SC Sub Lord
                                    if pc_sl_star_lord == sc_sub_lord:
                                        link_type = f"Std. Link to H{sc_num}"
                                    # Rahu Agency: SC Sub Lord is Rahu, AND PC SL's SL is one of Rahu's qualified dispositors
                                    elif sc_sub_lord == 'Rahu' and pc_sl_star_lord in rahu_dispositors:
                                        link_type = f"Rahu Agency to H{sc_num}"
                                    # Ketu Agency: SC Sub Lord is Ketu, AND PC SL's SL is one of Ketu's qualified dispositors
                                    elif sc_sub_lord == 'Ketu' and pc_sl_star_lord in ketu_dispositors:
                                        link_type = f"Ketu Agency to H{sc_num}"
                                    # Shared Star Lord: SC's Sub Lord's Star Lord == PC SL's Star Lord
                                    else:
                                        sc_sub_lord_planet_data = dyn_planets.get(sc_sub_lord)
                                        if sc_sub_lord_planet_data:
                                            sc_sub_lord_sl = sc_sub_lord_planet_data[
                                                3]  # Get SC Sub Lord's own Star Lord
                                            # Check if this Star Lord matches PC SL's Star Lord AND is P/N
                                            if sc_sub_lord_sl == pc_sl_star_lord and self.planet_classifications.get(
                                                    sc_sub_lord_sl) in ['Positive', 'Neutral']:
                                                link_type = f"Shared SL to H{sc_num}"

                                    if link_type:
                                        linked_secondary_cusp_details.append(link_type)
                                    else:
                                        self._log_debug(
                                            f"  SC Sub Lord '{sc_sub_lord}' (H{sc_num}) qualifies, but no link type found with {pc_sl_star_lord}.")
                                else:
                                    self._log_debug(
                                        f"  SC Sub Lord '{sc_sub_lord}' (H{sc_num}) is not a Positive/Neutral planet. Link skipped.")

                            # After checking all chosen secondary cusps:
                            # Interlink is active IF at least one SC linked.
                            if len(linked_secondary_cusp_details) >= 1:
                                interlink_found_this_minute = True
                                self._log_debug(
                                    f"  Interlink active: PC SubL ({pc_sub_lord}) qualified, its SL ({pc_sl_star_lord}) qualified, connected to AT LEAST ONE SC.")
                            else:
                                self._log_debug(
                                    f"  Interlink NOT active: PC SubL ({pc_sub_lord}) failed to connect to any chosen SC.")
                        else:  # Condition 2 (PC SL's Star Lord) not met
                            self._log_debug(
                                f"  Interlink NOT active: PC SubL's SL ({pc_sl_star_lord}) not in relaxed qualified RPs.")
                    # else: PC Sub Lord's data not found or PC Sub Lord not in strict_qualified_rps

                # If an interlink was truly found for the current minute, apply de-duplication and record it
                if interlink_found_this_minute:
                    # Create a unique signature for this specific hit type to prevent consecutive duplicates.
                    # Sorting `linked_secondary_cusp_details` ensures the order of linked SCs doesn't change the signature.
                    current_hit_signature = (pc_sub_lord, tuple(sorted(linked_secondary_cusp_details)))

                    if current_hit_signature != last_hit_signature:
                        final_link_details_str = "; ".join(sorted(linked_secondary_cusp_details))
                        final_hits.append({
                            'time': time_pointer,
                            'planet': pc_sub_lord,
                            'type': final_link_details_str,
                            'dasha_lords': dasha_lords,
                            'original_display_row': original_display_row  # Pass the original row data with the hit
                        })
                        last_hit_signature = current_hit_signature

                # If no valid interlink was found at this moment, reset the signature tracker.
                # This allows the same hit type to be recorded again if it appears after a break.
                if not interlink_found_this_minute:
                    last_hit_signature = None

                time_pointer += datetime.timedelta(seconds=scan_interval_seconds)
                processed_secs += scan_interval_seconds
                # Update progress bar in the UI
                if progress_info and progress_info['window'].winfo_exists():
                    self._update_progress(progress_info, processed_secs, total_seconds_to_scan, start_time_process,
                                          "Scanning for cuspal interlinks...")

        self._log_debug("--- _perform_cuspal_interlink_scan: End ---")
        return final_hits


    def _create_tour_popup(self):
        """Creates the Toplevel window used for showing tour steps."""
        self.tour_popup = tk.Toplevel(self.root)
        self.tour_popup.overrideredirect(True)  # Borderless window
        self.tour_popup.attributes('-topmost', True)

        popup_frame = ttk.Frame(self.tour_popup, borderwidth=2, relief="raised", style='Highlight.TFrame')
        popup_frame.pack(expand=True, fill="both")

        # Bind events to the frame to make the popup draggable
        popup_frame.bind("<ButtonPress-1>", self._on_popup_press)
        popup_frame.bind("<ButtonRelease-1>", self._on_popup_release)
        popup_frame.bind("<B1-Motion>", self._on_popup_motion)

        self.tour_label = ttk.Label(popup_frame, text="", wraplength=280, justify="left")
        self.tour_label.pack(padx=10, pady=10)
        # Also bind the label, so dragging works when clicking anywhere on the popup
        self.tour_label.bind("<ButtonPress-1>", self._on_popup_press)
        self.tour_label.bind("<ButtonRelease-1>", self._on_popup_release)
        self.tour_label.bind("<B1-Motion>", self._on_popup_motion)

        button_frame = ttk.Frame(popup_frame)
        button_frame.pack(pady=5, padx=10, fill='x')

        end_button = ttk.Button(button_frame, text="End Tour", command=self.end_tour)
        end_button.pack(side="left", expand=True, fill='x')

        self.prev_button = ttk.Button(button_frame, text="< Prev", command=self.prev_step)
        self.prev_button.pack(side="left", expand=True, fill='x', padx=5)

        self.next_button = ttk.Button(button_frame, text="Next >", command=self.next_step)
        self.next_button.pack(side="left", expand=True, fill='x')

    def show_tour_step(self):
        """Displays the current step of the tour, highlighting one or more widgets."""
        # Stop any previous blinking job
        if hasattr(self, '_blink_job_id') and self._blink_job_id:
            self.root.after_cancel(self._blink_job_id)
            self._blink_job_id = None

        # Revert the style of the previously highlighted widgets
        if self.last_highlighted_widget_info:
            for info in self.last_highlighted_widget_info:
                widget = info['widget']
                if not widget.winfo_exists(): continue
                if 'style' in info:  # ttk widget
                    widget.configure(style=info['style'])
                elif 'orig_opts' in info:  # tk widget
                    widget.configure(**info['orig_opts'])
            self.last_highlighted_widget_info = None

        if self.current_step >= len(self.tour_steps):
            self.end_tour()
            return

        step_info = self.tour_steps[self.current_step]

        if 'tab_name' in step_info:
            for i in range(self.notebook.index('end')):
                if self.notebook.tab(i, "text") == step_info['tab_name']:
                    self.notebook.select(i)
                    break

        self.root.update_idletasks()

        widgets = step_info['widget']
        if not isinstance(widgets, list):
            widgets = [widgets]

        self.last_highlighted_widget_info = []
        main_widget = widgets[0]

        for widget in widgets:
            if not widget.winfo_exists(): continue
            if widget == self.root: continue  # Don't highlight the root window

            widget_class = widget.winfo_class()
            if 'T' in widget_class:
                original_style = widget.cget("style")
                self.last_highlighted_widget_info.append({'widget': widget, 'style': original_style})
                highlight_style = f"Highlight.{widget_class}"
                widget.configure(style=highlight_style)
            else:
                original_opts = self.original_listbox_opts.copy()
                self.last_highlighted_widget_info.append({'widget': widget, 'orig_opts': original_opts})
                widget.configure(background=self.highlight_opts['background'])

        if step_info.get('blink'):
            self._blink_widget(widgets, 6)

        self.tour_label.config(text=step_info['text'])
        self.tour_popup.update_idletasks()

        # Position the popup
        pos = step_info.get('pos', 'bottom')
        popup_w, popup_h = self.tour_popup.winfo_reqwidth(), self.tour_popup.winfo_reqheight()

        if pos == 'center':
            root_x, root_y = self.root.winfo_rootx(), self.root.winfo_rooty()
            root_w, root_h = self.root.winfo_width(), self.root.winfo_height()
            self.tour_popup.geometry(f"+{root_x + (root_w - popup_w) // 2}+{root_y + (root_h - popup_h) // 2}")
        else:
            x, y = main_widget.winfo_rootx(), main_widget.winfo_rooty()
            w, h = main_widget.winfo_width(), main_widget.winfo_height()
            if pos == 'bottom':
                self.tour_popup.geometry(f"+{x}+{y + h + 5}")
            elif pos == 'top':
                self.tour_popup.geometry(f"+{x}+{y - popup_h - 10}")
            elif pos == 'right':
                self.tour_popup.geometry(f"+{x + w + 5}+{y}")

        # --- BUTTON STATE LOGIC ---
        self.prev_button.config(state='normal' if self.current_step > 0 else 'disabled')

        # Check if the current step is the last one in the tour
        is_last_step = self.current_step >= len(self.tour_steps) - 1

        if is_last_step:
            self.next_button.config(state='disabled')  # Disable Next on the last step
        else:
            self.next_button.config(state='normal')  # Keep Next active on all other steps

    def end_tour(self):
        """Ends the interactive tour and cleans up."""
        self._tour_ended = True
        if hasattr(self, '_blink_job_id') and self._blink_job_id:
            self.root.after_cancel(self._blink_job_id)
            self._blink_job_id = None

        if self.last_highlighted_widget_info:
            for info in self.last_highlighted_widget_info:
                widget = info['widget']
                if not widget.winfo_exists(): continue
                if 'style' in info:  # ttk widget
                    widget.configure(style=info['style'])
                elif 'orig_opts' in info:  # tk widget
                    widget.configure(**info['orig_opts'])
            self.last_highlighted_widget_info = None

        if hasattr(self, 'tour_popup') and self.tour_popup.winfo_exists():
            self.tour_popup.destroy()
    def next_step(self):
        """Moves to the next step in the tour."""
        self.current_step += 1
        self.show_tour_step()

    def prev_step(self):
        """Moves to the previous step in the tour."""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_tour_step()

import tkinter as tk
from tkinter import ttk

# This class should be added somewhere accessible in your script, e.g., after the AstrologyApp class definition




if __name__ == "__main__":
    app = AstrologyApp()
    app.root.mainloop()