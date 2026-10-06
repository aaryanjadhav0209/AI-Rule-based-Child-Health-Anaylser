import streamlit as st
from datetime import datetime

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Child Health Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    min-height: 100vh;
}

/* Hero Header */
.hero-header {
    background: linear-gradient(120deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 40px 50px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 40%, rgba(82, 216, 211, 0.08) 0%, transparent 60%),
                radial-gradient(circle at 70% 60%, rgba(255, 107, 107, 0.06) 0%, transparent 50%);
    pointer-events: none;
}
.hero-title {
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #52d8d3 0%, #a8edea 50%, #fed6e3 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.hero-subtitle {
    color: rgba(255,255,255,0.55);
    font-size: 1rem;
    margin-top: 10px;
    font-family: 'Space Mono', monospace;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Section Cards */
.section-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 20px;
}
.section-title {
    color: #52d8d3;
    font-size: 0.8rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(82, 216, 211, 0.25);
}

/* Metric Cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}
.metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 20px 18px;
    text-align: center;
}
.metric-value {
    font-size: 2rem;
    font-weight: 900;
    color: #52d8d3;
    line-height: 1;
}
.metric-label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
    font-family: 'Space Mono', monospace;
}
.metric-sub {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.6);
    margin-top: 4px;
    font-weight: 600;
}

/* Alert Flags */
.flag-red {
    background: rgba(255, 77, 77, 0.12);
    border-left: 4px solid #ff4d4d;
    border-radius: 0 10px 10px 0;
    padding: 14px 20px;
    margin: 8px 0;
    color: #ffb3b3;
    font-weight: 700;
}
.flag-yellow {
    background: rgba(255, 200, 50, 0.1);
    border-left: 4px solid #ffc832;
    border-radius: 0 10px 10px 0;
    padding: 14px 20px;
    margin: 8px 0;
    color: #ffe599;
    font-weight: 700;
}
.flag-green {
    background: rgba(82, 216, 130, 0.1);
    border-left: 4px solid #52d882;
    border-radius: 0 10px 10px 0;
    padding: 14px 20px;
    margin: 8px 0;
    color: #a8f0c0;
    font-weight: 700;
}

/* Score Bar */
.score-bar-wrapper {
    background: rgba(255,255,255,0.08);
    border-radius: 100px;
    height: 14px;
    overflow: hidden;
    margin: 10px 0;
}
.score-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.6s ease;
}

/* Deficiency Badge */
.badge {
    display: inline-block;
    background: rgba(255, 107, 107, 0.15);
    border: 1px solid rgba(255, 107, 107, 0.35);
    color: #ff9999;
    border-radius: 100px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 700;
    margin: 4px 3px;
    font-family: 'Space Mono', monospace;
}
.badge-ok {
    background: rgba(82, 216, 130, 0.1);
    border-color: rgba(82, 216, 130, 0.3);
    color: #a8f0c0;
}

/* Advice Item */
.advice-item {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #52d8d3;
    border-radius: 0 10px 10px 0;
    padding: 12px 18px;
    margin: 8px 0;
    color: rgba(255,255,255,0.8);
    font-size: 0.92rem;
}

/* Disease Card */
.disease-card {
    background: linear-gradient(135deg, rgba(255, 200, 50, 0.08) 0%, rgba(255, 107, 107, 0.08) 100%);
    border: 1px solid rgba(255, 200, 50, 0.25);
    border-radius: 14px;
    padding: 22px 26px;
    margin: 12px 0;
}
.disease-name {
    font-size: 1.5rem;
    font-weight: 900;
    color: #ffc832;
    margin-bottom: 4px;
}

/* Medicine Section */
.medicine-category {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 10px 0;
}
.medicine-category-title {
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    color: #52d8d3;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.medicine-item {
    color: rgba(255,255,255,0.75);
    padding: 5px 0;
    font-size: 0.88rem;
}
.medicine-item::before {
    content: '→ ';
    color: #52d8d3;
}

/* Report Box */
.report-box {
    background: #0d1117;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 24px;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #c9d1d9;
    white-space: pre-wrap;
    line-height: 1.7;
}

/* Streamlit overrides */
.stSelectbox label, .stRadio label, .stMultiSelect label,
.stNumberInput label, .stTextInput label, .stSlider label {
    color: rgba(255,255,255,0.7) !important;
    font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.88rem !important;
}
.stButton > button {
    background: linear-gradient(135deg, #52d8d3 0%, #43b8b4 100%) !important;
    color: #0f2027 !important;
    font-weight: 800 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 40px !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 6px 20px rgba(82,216,211,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(82,216,211,0.4) !important;
}
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
}
.stMarkdown p {
    color: rgba(255,255,255,0.75);
}
</style>
""", unsafe_allow_html=True)


# ─── LOGIC FUNCTIONS ─────────────────────────────────────────────────────────

def calculate_score(activity, diet, sleep, screen, stress):
    score = 100
    if activity == "Low":     score -= 20
    elif activity == "Medium": score -= 10
    if diet == "Junk":         score -= 20
    elif diet == "Mix":        score -= 10
    if sleep == "No":          score -= 15
    elif sleep == "Sometimes": score -= 10
    if screen == "High":       score -= 15
    if stress == "Yes":        score -= 15
    return score

def get_risk(score):
    if score >= 75:   return "Low Risk"
    elif score >= 50: return "Moderate Risk"
    else:             return "High Risk"

def calculate_bmi(weight, height):
    return round(weight * 10000 / (height * height), 2)

def get_bmi_category_for_age(bmi, age):
    if age <= 5:
        if bmi < 14: return "Underweight"
        elif bmi <= 17: return "Normal"
        elif bmi <= 18.5: return "Overweight"
        else: return "Obese"
    elif age <= 10:
        if bmi < 14.5: return "Underweight"
        elif bmi <= 19: return "Normal"
        elif bmi <= 21: return "Overweight"
        else: return "Obese"
    elif age <= 14:
        if bmi < 15.5: return "Underweight"
        elif bmi <= 21.5: return "Normal"
        elif bmi <= 24: return "Overweight"
        else: return "Obese"
    else:
        if bmi < 16.5: return "Underweight"
        elif bmi <= 23: return "Normal"
        elif bmi <= 26: return "Overweight"
        else: return "Obese"

def diseasepredict(age, activity, diet, sleep, screen, stress, weight, height):
    bmi = calculate_bmi(weight, height)
    bmi_cat = get_bmi_category_for_age(bmi, age)
    obesity, underweight = "Low", "Low"
    act_l = activity.lower(); diet_l = diet.lower(); screen_l = screen.lower(); stress_l = stress.lower()
    if act_l == "low" and diet_l == "junk" and bmi_cat == "Obese":
        obesity = "High"
    elif (act_l == "low" or diet_l == "junk" or screen_l == "high") and bmi_cat in ["Overweight", "Obese"]:
        obesity = "Moderate"
    if diet_l == "junk" and stress_l == "yes" and bmi_cat == "Underweight":
        underweight = "High"
    elif bmi_cat == "Underweight":
        underweight = "Moderate"
    return obesity, underweight, bmi, bmi_cat

def get_reasons(activity, diet, sleep, screen, stress):
    reasons = []
    if activity == "Low":     reasons.append("Low physical activity")
    if diet == "Junk":        reasons.append("Unhealthy eating habits (junk food)")
    if diet == "Mix":         reasons.append("Diet could be improved (currently mixed)")
    if sleep == "No":         reasons.append("Insufficient sleep")
    if screen == "High":      reasons.append("Excessive screen time")
    if stress == "Yes":       reasons.append("Child is under stress")
    return reasons

def lifestyle_advice(activity, diet, sleep, screen, stress):
    advice = []
    if activity == "Low":     advice.append("Encourage at least 60 minutes of outdoor play daily")
    if diet == "Junk":        advice.append("Reduce junk food and include more fruits and home-cooked meals")
    if diet == "Mix":         advice.append("Gradually shift toward more whole foods and home-cooked meals")
    if sleep == "No":         advice.append("Ensure the child gets 7–9 hours of proper sleep")
    if screen == "High":      advice.append("Limit screen time and promote physical or creative activities")
    if stress == "Yes":       advice.append("Talk to the child and create a supportive environment")
    return advice

def calculate_calorie_needs(age, weight, height, gender, activity):
    g = gender.lower()
    if g == "male":
        if age < 3:    bmr = 59.512 * weight - 30.4
        elif age < 10: bmr = 22.706 * weight + 504.3
        elif age < 18: bmr = 17.686 * weight + 658.2
        else:          bmr = 15.057 * weight + 692.2
    else:
        if age < 3:    bmr = 58.317 * weight - 31.1
        elif age < 10: bmr = 20.315 * weight + 485.9
        elif age < 18: bmr = 13.384 * weight + 692.6
        else:          bmr = 14.818 * weight + 486.6
    multipliers = {"Low": 1.40, "Medium": 1.65, "High": 1.82}
    tdee = round(bmr * multipliers.get(activity, 1.55))
    return tdee, round((tdee * 0.50) / 4), round((tdee * 0.25) / 4), round((tdee * 0.25) / 9)

def check_nutritional_deficiencies(food_items, diet):
    nutrient_sources = {
        "Calcium": ["dairy", "fish", "legumes", "vegetables"],
        "Iron": ["meat", "legumes", "eggs", "fish", "vegetables"],
        "Vitamin C": ["fruits", "vegetables"],
        "Vitamin D": ["dairy", "fish", "eggs"],
        "Vitamin A": ["dairy", "eggs", "fruits", "vegetables"],
        "Vitamin B12": ["meat", "fish", "eggs", "dairy"],
        "Zinc": ["meat", "legumes", "grains", "eggs"],
        "Omega-3": ["fish"],
        "Fiber": ["fruits", "vegetables", "grains", "legumes"],
        "Protein": ["meat", "eggs", "dairy", "legumes", "fish"],
        "Folate": ["vegetables", "legumes", "fruits", "grains"],
        "Magnesium": ["grains", "legumes", "vegetables", "fruits"],
    }
    deficiency_advice = {
        "Calcium": "Add milk, yogurt, cheese, or leafy greens to diet.",
        "Iron": "Include spinach, lentils, red meat, or fortified cereals.",
        "Vitamin C": "Add oranges, guava, tomatoes, or bell peppers.",
        "Vitamin D": "Include eggs, fish, fortified milk. Ensure sunlight exposure.",
        "Vitamin A": "Add carrots, sweet potato, eggs, or leafy greens.",
        "Vitamin B12": "Include eggs, dairy, fish, or meat.",
        "Zinc": "Add lentils, chickpeas, meat, or pumpkin seeds.",
        "Omega-3": "Include fish (salmon, sardines) or flaxseed/walnuts.",
        "Fiber": "Add whole grains, fruits, vegetables, and legumes.",
        "Protein": "Include eggs, dal, paneer, chicken, or legumes.",
        "Folate": "Add leafy greens, beans, lentils, or fortified grains.",
        "Magnesium": "Include nuts, seeds, whole grains, or leafy vegetables.",
    }
    food_lower = [f.lower() for f in food_items]
    deficiencies = []
    for nutrient, sources in nutrient_sources.items():
        if not any(food in food_lower for food in sources):
            deficiencies.append({"nutrient": nutrient, "advice": deficiency_advice[nutrient]})
    extra_warnings = []
    if diet.lower() == "junk":
        extra_warnings.append("High junk food intake raises risk of excess sodium, sugar, and trans fats.")
    if "sweets" in food_lower:
        extra_warnings.append("High sugar intake detected – risk of dental cavities and energy crashes.")
    return deficiencies, extra_warnings

def get_alert_flags(score, bmi_cat, obesity, underweight, stress, sleep, best_disease):
    flags = []
    if bmi_cat == "Obese" and obesity == "High":
        flags.append(("RED", "Severe obesity risk detected. Consult a pediatric nutritionist immediately."))
    if underweight == "High":
        flags.append(("RED", "Severe underweight risk. Seek immediate medical evaluation."))
    if best_disease in ["Pneumonia", "Malaria", "Dengue", "Typhoid", "Measles"]:
        flags.append(("RED", f"{best_disease} suspected – requires immediate medical attention."))
    if score < 40:
        flags.append(("RED", "Very low health score. Multiple risk factors present. See a doctor urgently."))
    if bmi_cat == "Overweight" or obesity == "Moderate":
        flags.append(("YELLOW", "Child is overweight. Schedule a checkup with a pediatrician."))
    if underweight == "Moderate":
        flags.append(("YELLOW", "Child may be underweight for their age. Consult a doctor."))
    if stress == "Yes" and sleep == "No":
        flags.append(("YELLOW", "Stress combined with poor sleep can harm development. Seek guidance."))
    if best_disease in ["Asthma", "Anemia", "Ear Infection", "Bronchitis", "Conjunctivitis", "Allergies"]:
        flags.append(("YELLOW", f"{best_disease} detected – visit a doctor within 1–2 days."))
    if 40 <= score < 55:
        flags.append(("YELLOW", "Low health score. Lifestyle improvements and a doctor visit are recommended."))
    if not flags:
        flags.append(("GREEN", "No immediate medical concern. Continue healthy habits and monitor regularly."))
    return flags

def symptomdisease(symptoms):
    if not symptoms: return None, 0
    diseases = {
        "Common Cold": ["runny nose", "sneezing", "mild fever", "cough", "sore throat"],
        "Flu": ["high fever", "body aches", "fatigue", "dry cough"],
        "Stomach Infection": ["diarrhea", "vomiting", "stomach pain"],
        "Malaria": ["high fever", "chills", "sweating"],
        "Pneumonia": ["cough", "difficulty breathing", "chest pain"],
        "Dengue": ["high fever", "joint pain", "rash"],
        "Typhoid": ["prolonged fever", "weakness", "stomach pain"],
        "Asthma": ["wheezing", "shortness of breath", "chest tightness"],
        "Chickenpox": ["itchy rash", "blisters", "fever", "fatigue", "loss of appetite"],
        "Ear Infection": ["ear pain", "fever", "irritability", "difficulty hearing", "fluid from ear"],
        "Allergies": ["sneezing", "itchy eyes", "runny nose", "skin rash", "swelling"],
        "Bronchitis": ["persistent cough", "mucus", "fatigue", "chest discomfort", "mild fever"],
        "Teething": ["drooling", "gum swelling", "irritability", "chewing objects", "mild fever"],
        "Measles": ["high fever", "red rash", "runny nose", "cough", "red eyes"],
        "Food Poisoning": ["vomiting", "diarrhea", "stomach cramps", "nausea", "fever"],
        "HFMD": ["mouth sores", "rash on hands", "rash on feet", "fever", "loss of appetite"],
        "Conjunctivitis": ["red eyes", "itchy eyes", "eye discharge", "watery eyes", "swelling"],
        "Anemia": ["fatigue", "pale skin", "weakness", "dizziness", "shortness of breath"],
    }
    sym_lower = [s.lower().strip() for s in symptoms]
    best, best_score = "", 0
    for disease, sym_list in diseases.items():
        matches = sum(1 for us in sym_lower if any(us == ds or us in ds or ds == us for ds in sym_list))
        if matches > best_score:
            best, best_score = disease, matches
    confidence = round((best_score / max(len(sym_lower), 1)) * 100)
    return (best if best else None), confidence

def get_disease_advice(best):
    advice_map = {
        "Common Cold": "Give fluids, rest, steam inhalation, and light food.",
        "Flu": "Give fluids, rest, and control fever. See a doctor if fever is very high.",
        "Stomach Infection": "Give ORS, fluids, light diet, and maintain hygiene.",
        "Malaria": "Consult a doctor immediately and ensure full treatment.",
        "Pneumonia": "Serious condition. Seek medical help immediately.",
        "Dengue": "Give fluids, avoid ibuprofen, and monitor platelet count closely.",
        "Typhoid": "Antibiotics required. Visit a doctor promptly.",
        "Asthma": "Use the prescribed inhaler and identify and avoid triggers.",
        "Chickenpox": "Keep nails trimmed, apply calamine lotion, avoid scratching. Consult a doctor.",
        "Ear Infection": "See a doctor. Keep the ear dry and avoid inserting anything into it.",
        "Allergies": "Identify and avoid the trigger. Antihistamines may help — consult a doctor.",
        "Bronchitis": "Rest, fluids, and steam. See a doctor if symptoms persist beyond a week.",
        "Teething": "Use a chilled teething ring. Consult a doctor if fever is high.",
        "Measles": "Isolate the child, ensure rest and fluids. Seek medical guidance.",
        "Food Poisoning": "Give ORS and bland food. See a doctor if vomiting or diarrhoea persists.",
        "HFMD": "Keep the child home; it is contagious. Ensure rest and fluids. Consult a doctor.",
        "Conjunctivitis": "Clean eyes gently with a damp cloth. See a doctor for appropriate eye drops.",
        "Anemia": "Include iron-rich foods (spinach, lentils, meat). Consult a doctor for supplements.",
    }
    return advice_map.get(best, "Please consult a doctor for specific advice.")

def get_medicines(best):
    medicines_map = {
        "Common Cold": {
            "OTC Medicines": ["Paracetamol (Calpol) – for fever and discomfort", "Cetirizine (Zyrtec) – for runny nose and sneezing", "Dextromethorphan syrup – for cough relief"],
            "Home Remedies": ["Honey + warm water (for children over 1 year)", "Steam inhalation with eucalyptus oil", "Warm turmeric milk"],
            "Note": "Avoid antibiotics – colds are viral. Consult a doctor if symptoms last over 7 days."
        },
        "Flu": {
            "OTC Medicines": ["Paracetamol (Calpol/Tylenol) – for fever and body ache", "Ibuprofen (Advil) – for pain and fever"],
            "Home Remedies": ["Warm chicken soup or broth", "Ginger tea with honey", "Adequate rest and hydration"],
            "Note": "See a doctor if fever exceeds 103°F or breathing is labored."
        },
        "Stomach Infection": {
            "OTC Medicines": ["ORS (Oral Rehydration Salts) – to prevent dehydration", "Zinc supplements – helps reduce diarrhea duration", "Probiotics (Lactobacillus) – to restore gut flora"],
            "Home Remedies": ["Rice water (kanji) to soothe the stomach", "Banana and plain toast (BRAT diet)", "Coconut water for electrolytes"],
            "Note": "Avoid anti-diarrheal drugs without a doctor's advice in young children."
        },
        "Dengue": {
            "OTC Medicines": ["Paracetamol (Calpol) – ONLY for fever. DO NOT use Ibuprofen or Aspirin.", "ORS – for hydration"],
            "Home Remedies": ["Papaya leaf extract – may help raise platelet count", "Plenty of fluids: coconut water, juice, water"],
            "Note": "Monitor platelet count daily. Seek emergency care if platelet count drops below 50,000."
        },
        "Asthma": {
            "OTC Medicines": ["Salbutamol inhaler (Ventolin) – quick relief during attacks"],
            "Prescription Required": ["Budesonide inhaler – daily controller medication", "Montelukast (Singulair) – reduces inflammation"],
            "Note": "Always carry the relief inhaler. Have an asthma action plan from your doctor."
        },
        "Chickenpox": {
            "OTC Medicines": ["Paracetamol – for fever (NOT Aspirin)", "Calamine lotion – for itch relief", "Cetirizine – to reduce itching"],
            "Home Remedies": ["Oatmeal bath to soothe itching", "Trim child's nails to prevent scratching", "Loose, cotton clothing"],
            "Note": "Keep child isolated until all blisters crust over (~7 days)."
        },
        "Anemia": {
            "OTC Medicines": ["Ferrous sulfate (iron syrup) – for iron-deficiency anemia", "Folic acid supplements", "Vitamin C – enhances iron absorption"],
            "Dietary Sources": ["Spinach, lentils, beans, tofu", "Red meat, chicken, fish", "Fortified cereals and dates"],
            "Note": "Iron supplements should be taken on an empty stomach if tolerated."
        },
        "Conjunctivitis": {
            "OTC Medicines": ["Lubricant eye drops (artificial tears) – for irritation"],
            "Prescription Required": ["Chloramphenicol eye drops – for bacterial conjunctivitis", "Antihistamine eye drops – for allergic conjunctivitis"],
            "Home Remedies": ["Clean eye discharge with a warm, damp cloth (wipe outward)", "Avoid touching or rubbing the eye"],
            "Note": "Wash hands frequently. Do not share towels or pillowcases."
        },
    }
    return medicines_map.get(best, None)


# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🏥 Child Health Analyzer</div>
    <div class="hero-subtitle">Pediatric Health Assessment & Advisory System</div>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-size:2.5rem;'>👶</div>
        <div style='color: #52d8d3; font-weight: 800; font-size: 1.1rem; margin-top:8px;'>Child Details</div>
        <div style='color: rgba(255,255,255,0.4); font-size: 0.75rem; font-family: monospace; letter-spacing:1px;'>ENTER INFORMATION BELOW</div>
    </div>
    <hr style='border-color: rgba(255,255,255,0.1);'>
    """, unsafe_allow_html=True)

    name   = st.text_input("Child's Name", placeholder="e.g. Arjun")
    age    = st.number_input("Age (years)", min_value=1, max_value=17, value=8)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=5.0, max_value=150.0, value=25.0, step=0.5)
    with col2:
        height = st.number_input("Height (cm)", min_value=50.0, max_value=220.0, value=120.0, step=0.5)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    activity = st.select_slider("Physical Activity Level", options=["Low", "Medium", "High"], value="Medium")
    diet     = st.select_slider("Diet Quality", options=["Junk", "Mix", "Healthy"], value="Mix")
    sleep    = st.radio("Sleeps ≥ 7 hours?", ["Yes", "Sometimes", "No"], horizontal=True)
    screen   = st.radio("Screen Time", ["Low", "High"], horizontal=True)
    stress   = st.radio("Under Stress?", ["No", "Yes"], horizontal=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    st.markdown("<div style='color: rgba(255,255,255,0.5); font-size:0.8rem; margin-bottom:8px;'>🍽️ Food Items Consumed</div>", unsafe_allow_html=True)
    food_options = ["dairy", "fruits", "vegetables", "meat", "grains", "legumes", "junk", "sweets", "eggs", "fish"]
    food_items   = st.multiselect("Select all that apply", food_options, default=["fruits", "vegetables", "grains"])

    st.markdown("<br>", unsafe_allow_html=True)
    analyze = st.button("🔍 Analyze Health", use_container_width=True)

# ─── SYMPTOM INPUT ───────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
    <div class="section-title">🤒 Symptom Checker</div>
</div>
""", unsafe_allow_html=True)

with st.container():
    all_symptoms = [
        "runny nose", "sneezing", "mild fever", "cough", "sore throat", "high fever",
        "body aches", "fatigue", "dry cough", "diarrhea", "vomiting", "stomach pain",
        "chills", "sweating", "difficulty breathing", "chest pain", "joint pain", "rash",
        "prolonged fever", "weakness", "wheezing", "shortness of breath", "chest tightness",
        "itchy rash", "blisters", "loss of appetite", "ear pain", "irritability",
        "difficulty hearing", "fluid from ear", "itchy eyes", "skin rash", "swelling",
        "persistent cough", "mucus", "chest discomfort", "drooling", "gum swelling",
        "chewing objects", "red rash", "red eyes", "stomach cramps", "nausea",
        "mouth sores", "rash on hands", "rash on feet", "eye discharge", "watery eyes",
        "pale skin", "dizziness"
    ]
    selected_symptoms = st.multiselect(
        "Select any symptoms your child is experiencing:",
        options=all_symptoms,
        help="Select all applicable symptoms for disease prediction"
    )

# ─── MAIN ANALYSIS ───────────────────────────────────────────────────────────
if analyze:
    if not name.strip():
        st.error("⚠️ Please enter the child's name to proceed.")
    else:
        # Compute everything
        score                              = calculate_score(activity, diet, sleep, screen, stress)
        risk                               = get_risk(score)
        obesity, underweight, bmi, bmi_cat = diseasepredict(age, activity, diet, sleep, screen, stress, weight, height)
        reasons                            = get_reasons(activity, diet, sleep, screen, stress)
        advice                             = lifestyle_advice(activity, diet, sleep, screen, stress)
        tdee, carbs, protein, fats         = calculate_calorie_needs(age, weight, height, gender, activity)
        deficiencies, extra_warnings       = check_nutritional_deficiencies(food_items, diet)
        best_disease, confidence           = symptomdisease(selected_symptoms)
        flags                              = get_alert_flags(score, bmi_cat, obesity, underweight, stress, sleep, best_disease or "")

        # ── ALERT FLAGS ──
        flag_html = ""
        for level, message in flags:
            icons = {"RED": "🔴", "YELLOW": "🟡", "GREEN": "🟢"}
            css_class = {"RED": "flag-red", "YELLOW": "flag-yellow", "GREEN": "flag-green"}
            flag_html += f'<div class="{css_class[level]}">{icons[level]} {message}</div>'
        st.markdown(f'<div class="section-card"><div class="section-title">⚠️ Alert Flags</div>{flag_html}</div>', unsafe_allow_html=True)

        # ── CORE METRICS ──
        score_color = "#52d882" if score >= 75 else "#ffc832" if score >= 50 else "#ff4d4d"
        bmi_color   = "#52d882" if bmi_cat == "Normal" else "#ffc832" if bmi_cat in ["Overweight","Underweight"] else "#ff4d4d"

        st.markdown(f"""
        <div class="section-card">
            <div class="section-title">📊 Health Overview — {name.title()}</div>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value" style="color:{score_color}">{score}</div>
                    <div class="metric-label">Health Score</div>
                    <div class="metric-sub">{risk}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:{bmi_color}">{bmi}</div>
                    <div class="metric-label">BMI</div>
                    <div class="metric-sub">{bmi_cat}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="font-size:1.4rem; color:{'#ff4d4d' if obesity=='High' else '#ffc832' if obesity=='Moderate' else '#52d882'}">{obesity}</div>
                    <div class="metric-label">Obesity Risk</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="font-size:1.4rem; color:{'#ff4d4d' if underweight=='High' else '#ffc832' if underweight=='Moderate' else '#52d882'}">{underweight}</div>
                    <div class="metric-label">Underweight Risk</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{tdee}</div>
                    <div class="metric-label">kcal / day</div>
                    <div class="metric-sub">Daily Calories</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="font-size:1.1rem">{carbs}g | {protein}g | {fats}g</div>
                    <div class="metric-label">Carbs | Protein | Fats</div>
                </div>
            </div>
            <div style="margin-top:8px;">
                <div style="color:rgba(255,255,255,0.45); font-size:0.75rem; font-family:monospace; margin-bottom:6px;">HEALTH SCORE — {score}/100</div>
                <div class="score-bar-wrapper">
                    <div class="score-bar-fill" style="width:{score}%; background: linear-gradient(90deg, {score_color}88, {score_color});"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── DISEASE PREDICTION ──
        if best_disease:
            adv = get_disease_advice(best_disease)
            disease_emoji = {"Common Cold":"🤧","Flu":"🤒","Stomach Infection":"🤢","Malaria":"🦟","Pneumonia":"🫁","Dengue":"🦟","Typhoid":"🌡️","Asthma":"😮‍💨","Chickenpox":"🔴","Ear Infection":"👂","Allergies":"🌿","Bronchitis":"😮‍💨","Teething":"🦷","Measles":"🔴","Food Poisoning":"🤢","HFMD":"✋","Conjunctivitis":"👁️","Anemia":"💉"}.get(best_disease, "🏥")
            medicines = get_medicines(best_disease)
            med_html = ""
            if medicines:
                for cat, items in medicines.items():
                    if isinstance(items, list):
                        items_html = "".join(f'<div class="medicine-item">{item}</div>' for item in items)
                        med_html += f'<div class="medicine-category"><div class="medicine-category-title">{cat}</div>{items_html}</div>'
                    else:
                        med_html += f'<div class="medicine-category"><div class="medicine-category-title">{cat}</div><div style="color:rgba(255,200,50,0.85); font-size:0.85rem; font-style:italic;">⚠️ {items}</div></div>'

            st.markdown(f"""
            <div class="section-card">
                <div class="section-title">🔬 Symptom Analysis & Disease Prediction</div>
                <div class="disease-card">
                    <div class="disease-name">{disease_emoji} {best_disease}</div>
                    <div style="color:rgba(255,255,255,0.45); font-size:0.78rem; font-family:monospace;">SYMPTOM MATCH CONFIDENCE: {confidence}%</div>
                    <div style="margin-top:14px; color:rgba(255,255,255,0.75); font-size:0.92rem; line-height:1.6;">💡 {adv}</div>
                </div>
                {"<div style='margin-top:16px;'><div class='section-title' style='margin-bottom:12px;'>💊 Treatment Guide</div>" + med_html + "</div>" if med_html else ""}
            </div>
            """, unsafe_allow_html=True)

        # ── NUTRITIONAL DEFICIENCIES ──
        if deficiencies or extra_warnings:
            def_badges = "".join(f'<span class="badge">{d["nutrient"]}</span>' for d in deficiencies) if deficiencies else '<span class="badge-ok badge">✓ No Major Deficiencies</span>'
            def_details = "".join(f'<div class="advice-item">⚠️ <strong>{d["nutrient"]}</strong> — {d["advice"]}</div>' for d in deficiencies)
            warn_html   = "".join(f'<div class="advice-item" style="border-color:#ffc832;">🚨 {w}</div>' for w in extra_warnings)
            st.markdown(f"""
            <div class="section-card">
                <div class="section-title">🧪 Nutritional Deficiency Flags</div>
                <div style="margin-bottom:16px;">{def_badges}</div>
                {def_details}
                {warn_html}
            </div>
            """, unsafe_allow_html=True)

        # ── RISK FACTORS & LIFESTYLE ──
        if reasons or advice:
            reasons_html = "".join(f'<div class="advice-item" style="border-color:#ff6b6b;">⚡ {r}</div>' for r in reasons) if reasons else '<div class="advice-item" style="border-color:#52d882;">✅ No major risk factors identified.</div>'
            advice_html  = "".join(f'<div class="advice-item">💚 {a}</div>' for a in advice) if advice else '<div class="advice-item" style="border-color:#52d882;">✅ Keep maintaining healthy habits!</div>'
            st.markdown(f"""
            <div class="section-card">
                <div class="section-title">⚡ Risk Factors</div>
                {reasons_html}
                <div class="section-title" style="margin-top:24px;">💡 Lifestyle Recommendations</div>
                {advice_html}
            </div>
            """, unsafe_allow_html=True)

        # ── DOCTOR REPORT ──
        with st.expander("📋 Generate Doctor Summary Report"):
            date_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
            flag_lines = "\n".join(f"  [{lv}] {msg}" for lv, msg in flags)
            def_lines  = "\n".join(f"  - {d['nutrient']}: {d['advice']}" for d in deficiencies) if deficiencies else "  None detected."
            warn_lines = "\n".join(f"  ! {w}" for w in extra_warnings) if extra_warnings else ""
            risk_lines = "\n".join(f"  - {r}" for r in reasons) if reasons else "  None identified."

            report = f"""{'='*55}
       CHILD HEALTH REPORT – FOR DOCTOR
       Generated on: {date_str}
{'='*55}

[CHILD INFORMATION]
  Name   : {name.title()}
  Age    : {age} years
  Gender : {gender}
  Weight : {weight} kg
  Height : {height} cm
  BMI    : {bmi}  ({bmi_cat})

[HEALTH SCORE]
  Score  : {score} / 100
  Risk   : {risk}

[OBESITY / UNDERWEIGHT PREDICTION]
  Obesity Risk     : {obesity}
  Underweight Risk : {underweight}

[ALERT FLAGS]
{flag_lines}

[RISK FACTORS IDENTIFIED]
{risk_lines}

[SUSPECTED ILLNESS]
  {best_disease if best_disease else 'No specific illness detected.'}
  {"Confidence: " + str(confidence) + "%" if best_disease else ""}

[NUTRITIONAL DEFICIENCY FLAGS]
{def_lines}
{("" if not warn_lines else chr(10) + "[DIETARY WARNINGS]" + chr(10) + warn_lines)}

[ESTIMATED DAILY CALORIE NEEDS]
  Total Calories : {tdee} kcal/day
  Carbohydrates  : {carbs} g/day
  Protein        : {protein} g/day
  Fats           : {fats} g/day

{'='*55}
  NOTE: This report is generated by a health analyzer
  tool and is NOT a substitute for professional medical
  diagnosis. Please consult a qualified pediatrician.
{'='*55}"""

            st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
            st.download_button(
                label="⬇️ Download Report (.txt)",
                data=report,
                file_name=f"health_report_{name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )

        # ── FOOTER ──
        st.markdown("""
        <div style="text-align:center; padding:30px 0 10px; color:rgba(255,255,255,0.25); font-size:0.78rem; font-family:monospace; letter-spacing:1px;">
            ⚕️ THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY · NOT A SUBSTITUTE FOR MEDICAL ADVICE<br>
            Always consult a qualified pediatrician for diagnosis and treatment.
        </div>
        """, unsafe_allow_html=True)

else:
    # Welcome state
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px;">
        <div style="font-size: 5rem; margin-bottom: 20px;">👶</div>
        <div style="color: rgba(255,255,255,0.6); font-size: 1.1rem; max-width: 500px; margin: 0 auto; line-height: 1.8;">
            Fill in your child's details in the sidebar on the left, select any symptoms if present, 
            and click <strong style="color:#52d8d3;">Analyze Health</strong> to get a complete health report.
        </div>
        <div style="margin-top: 40px; display:flex; justify-content:center; gap:30px; flex-wrap:wrap;">
            <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:20px 28px; text-align:center;">
                <div style="font-size:2rem;">📊</div>
                <div style="color:#52d8d3; font-weight:700; margin-top:8px;">BMI & Health Score</div>
                <div style="color:rgba(255,255,255,0.4); font-size:0.82rem;">Age-adjusted analysis</div>
            </div>
            <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:20px 28px; text-align:center;">
                <div style="font-size:2rem;">🔬</div>
                <div style="color:#52d8d3; font-weight:700; margin-top:8px;">Disease Prediction</div>
                <div style="color:rgba(255,255,255,0.4); font-size:0.82rem;">18 condition database</div>
            </div>
            <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:20px 28px; text-align:center;">
                <div style="font-size:2rem;">🧪</div>
                <div style="color:#52d8d3; font-weight:700; margin-top:8px;">Nutrition Analysis</div>
                <div style="color:rgba(255,255,255,0.4); font-size:0.82rem;">12 nutrient checks</div>
            </div>
            <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:20px 28px; text-align:center;">
                <div style="font-size:2rem;">📋</div>
                <div style="color:#52d8d3; font-weight:700; margin-top:8px;">Doctor Report</div>
                <div style="color:rgba(255,255,255,0.4); font-size:0.82rem;">Downloadable summary</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)