from datetime import datetime


# ─── INPUT ───────────────────────────────────────────────────────────────────

def get_input():
    print("=" * 55)
    print("   CHILD HEALTH ANALYZER")
    print("=" * 55)
    print("Hello!! I will help you understand your child's health.\n")
    try:
        name   = input("What is your child's name? ").strip().title()
        age    = int(input("What is your child's age (in years)? "))
        weight = float(input("What is the weight of your child (in kg)? "))
        height = float(input("What is the height of your child (in cm)? "))
    except:
        print("Invalid input. Please restart.")
        exit()

    gender   = input("What is your child's gender? (male/female): ").lower()
    activity = input("How active is your child? (low/medium/high): ").lower()
    diet     = input("How is your child's diet? (healthy/junk/mix): ").lower()
    sleep    = input("Does your child sleep at least 7 hours? (yes/no/sometimes): ").lower()
    screen   = input("How is your child's screen time? (low/high): ").lower()
    stress   = input("Is your child under stress? (yes/no): ").lower()

    print("\nWhat does your child usually eat? (select all that apply)")
    print("Options: dairy, fruits, vegetables, meat, grains, legumes, junk, sweets, eggs, fish")
    food_raw   = input("Enter foods (comma separated): ").lower()
    food_items = [f.strip() for f in food_raw.split(",") if f.strip()]

    return name, age, gender, activity, diet, sleep, screen, stress, weight, height, food_items


# ─── HEALTH SCORE ────────────────────────────────────────────────────────────

def calculate_score(activity, diet, sleep, screen, stress):
    score = 100
    if activity == "low":
        score -= 20
    elif activity == "medium":
        score -= 10
    if diet == "junk":
        score -= 20
    elif diet == "mix":
        score -= 10
    if sleep == "no":
        score -= 15
    elif sleep == "sometimes":
        score -= 10
    if screen == "high":
        score -= 15
    if stress == "yes":
        score -= 15
    return score


def get_risk(score):
    if score >= 75:
        return "Low Risk"
    elif score >= 50:
        return "Moderate Risk"
    else:
        return "High Risk"


# ─── BMI & DISEASE PREDICTION ────────────────────────────────────────────────

def calculate_bmi(weight, height):
    return round(weight * 10000 / (height * height), 2)


def get_bmi_category_for_age(bmi, age):
    if age <= 5:
        if bmi < 14:      return "Underweight"
        elif bmi <= 17:   return "Normal"
        elif bmi <= 18.5: return "Overweight"
        else:             return "Obese"
    elif age <= 10:
        if bmi < 14.5:  return "Underweight"
        elif bmi <= 19: return "Normal"
        elif bmi <= 21: return "Overweight"
        else:           return "Obese"
    elif age <= 14:
        if bmi < 15.5:    return "Underweight"
        elif bmi <= 21.5: return "Normal"
        elif bmi <= 24:   return "Overweight"
        else:             return "Obese"
    else:
        if bmi < 16.5:  return "Underweight"
        elif bmi <= 23: return "Normal"
        elif bmi <= 26: return "Overweight"
        else:           return "Obese"


def diseasepredict(age, activity, diet, sleep, screen, stress, weight, height):
    bmi         = calculate_bmi(weight, height)
    bmi_cat     = get_bmi_category_for_age(bmi, age)
    obesity     = "Low"
    underweight = "Low"

    if activity == "low" and diet == "junk" and bmi_cat == "Obese":
        obesity = "High"
    elif (activity == "low" or diet == "junk" or screen == "high") and bmi_cat in ["Overweight", "Obese"]:
        obesity = "Moderate"

    if diet == "junk" and stress == "yes" and bmi_cat == "Underweight":
        underweight = "High"
    elif bmi_cat == "Underweight":
        underweight = "Moderate"

    return obesity, underweight, bmi, bmi_cat


# ─── REASONS & LIFESTYLE ─────────────────────────────────────────────────────

def get_reasons(activity, diet, sleep, screen, stress):
    reasons = []
    if activity == "low":
        reasons.append("Low physical activity")
    if diet == "junk":
        reasons.append("Unhealthy eating habits (junk food)")
    if diet == "mix":
        reasons.append("Diet could be improved (currently mixed)")
    if sleep == "no":
        reasons.append("Insufficient sleep")
    if screen == "high":
        reasons.append("Excessive screen time")
    if stress == "yes":
        reasons.append("Child is under stress")
    return reasons


def lifestyle_advice(activity, diet, sleep, screen, stress):
    advice = []
    if activity == "low":
        advice.append("Encourage at least 60 minutes of outdoor play daily")
    if diet == "junk":
        advice.append("Reduce junk food and include more fruits and home-cooked meals")
    if diet == "mix":
        advice.append("Gradually shift toward more whole foods and home-cooked meals")
    if sleep == "no":
        advice.append("Ensure the child gets 7-9 hours of proper sleep")
    if screen == "high":
        advice.append("Limit screen time and promote physical or creative activities")
    if stress == "yes":
        advice.append("Talk to the child and create a supportive environment")
    return advice


# ─── DAILY CALORIE NEEDS ─────────────────────────────────────────────────────

def calculate_calorie_needs(age, weight, height, gender, activity):
    # Schofield equation (WHO recommended) for BMR
    if gender == "male":
        if age < 3:    bmr = 59.512 * weight - 30.4
        elif age < 10: bmr = 22.706 * weight + 504.3
        elif age < 18: bmr = 17.686 * weight + 658.2
        else:          bmr = 15.057 * weight + 692.2
    else:
        if age < 3:    bmr = 58.317 * weight - 31.1
        elif age < 10: bmr = 20.315 * weight + 485.9
        elif age < 18: bmr = 13.384 * weight + 692.6
        else:          bmr = 14.818 * weight + 486.6

    multipliers = {"low": 1.40, "medium": 1.65, "high": 1.82}
    multiplier  = multipliers.get(activity, 1.55)
    tdee        = round(bmr * multiplier)

    carbs   = round((tdee * 0.50) / 4)
    protein = round((tdee * 0.25) / 4)
    fats    = round((tdee * 0.25) / 9)

    return tdee, carbs, protein, fats


# ─── NUTRITIONAL DEFICIENCY FLAGS ────────────────────────────────────────────

def check_nutritional_deficiencies(food_items, age, diet):
    nutrient_sources = {
        "Calcium":     ["dairy", "fish", "legumes", "vegetables"],
        "Iron":        ["meat", "legumes", "eggs", "fish", "vegetables"],
        "Vitamin C":   ["fruits", "vegetables"],
        "Vitamin D":   ["dairy", "fish", "eggs"],
        "Vitamin A":   ["dairy", "eggs", "fruits", "vegetables"],
        "Vitamin B12": ["meat", "fish", "eggs", "dairy"],
        "Zinc":        ["meat", "legumes", "grains", "eggs"],
        "Omega-3":     ["fish"],
        "Fiber":       ["fruits", "vegetables", "grains", "legumes"],
        "Protein":     ["meat", "eggs", "dairy", "legumes", "fish"],
        "Folate":      ["vegetables", "legumes", "fruits", "grains"],
        "Magnesium":   ["grains", "legumes", "vegetables", "fruits"],
    }

    deficiency_advice = {
        "Calcium":     "Add milk, yogurt, cheese, or leafy greens to diet.",
        "Iron":        "Include spinach, lentils, red meat, or fortified cereals.",
        "Vitamin C":   "Add oranges, guava, tomatoes, or bell peppers.",
        "Vitamin D":   "Include eggs, fish, fortified milk. Ensure sunlight exposure.",
        "Vitamin A":   "Add carrots, sweet potato, eggs, or leafy greens.",
        "Vitamin B12": "Include eggs, dairy, fish, or meat.",
        "Zinc":        "Add lentils, chickpeas, meat, or pumpkin seeds.",
        "Omega-3":     "Include fish (salmon, sardines) or flaxseed/walnuts.",
        "Fiber":       "Add whole grains, fruits, vegetables, and legumes.",
        "Protein":     "Include eggs, dal, paneer, chicken, or legumes.",
        "Folate":      "Add leafy greens, beans, lentils, or fortified grains.",
        "Magnesium":   "Include nuts, seeds, whole grains, or leafy vegetables.",
    }

    deficiencies = []
    for nutrient, sources in nutrient_sources.items():
        covered = any(food in food_items for food in sources)
        if not covered:
            deficiencies.append({"nutrient": nutrient, "advice": deficiency_advice[nutrient]})

    extra_warnings = []
    if diet == "junk":
        extra_warnings.append("High junk food intake raises risk of excess sodium, sugar, and trans fats.")
    if "sweets" in food_items:
        extra_warnings.append("High sugar intake detected – risk of dental cavities and energy crashes.")

    return deficiencies, extra_warnings


# ─── ALERT FLAG SYSTEM ───────────────────────────────────────────────────────

def get_alert_flags(score, bmi_cat, obesity, underweight, stress, sleep, best_disease):
    flags = []

    # RED – emergency
    if bmi_cat == "Obese" and obesity == "High":
        flags.append(("RED", "Severe obesity risk detected. Consult a pediatric nutritionist immediately."))
    if underweight == "High":
        flags.append(("RED", "Severe underweight risk. Seek immediate medical evaluation."))
    if best_disease in ["Pneumonia", "Malaria", "Dengue", "Typhoid", "Measles"]:
        flags.append(("RED", f"{best_disease} suspected – requires immediate medical attention."))
    if score < 40:
        flags.append(("RED", "Very low health score. Multiple risk factors present. See a doctor urgently."))

    # YELLOW – visit doctor soon
    if bmi_cat == "Overweight" or obesity == "Moderate":
        flags.append(("YELLOW", "Child is overweight. Schedule a checkup with a pediatrician."))
    if underweight == "Moderate":
        flags.append(("YELLOW", "Child may be underweight for their age. Consult a doctor."))
    if stress == "yes" and sleep == "no":
        flags.append(("YELLOW", "Stress combined with poor sleep can harm development. Seek guidance."))
    if best_disease in ["Asthma", "Anemia", "Ear Infection", "Bronchitis", "Conjunctivitis", "Allergies"]:
        flags.append(("YELLOW", f"{best_disease} detected – visit a doctor within 1-2 days."))
    if 40 <= score < 55:
        flags.append(("YELLOW", "Low health score. Lifestyle improvements and a doctor visit are recommended."))

    # GREEN – monitor at home
    if not flags:
        flags.append(("GREEN", "No immediate medical concern. Continue healthy habits and monitor regularly."))

    return flags


def print_flags(flags):
    colors = {
        "RED":    "\033[91m",
        "YELLOW": "\033[93m",
        "GREEN":  "\033[92m",
        "RESET":  "\033[0m",
    }
    print("\n" + "=" * 55)
    print("  ALERT FLAGS")
    print("=" * 55)
    for level, message in flags:
        icon  = {"RED": "[!!! RED   ]", "YELLOW": "[!!  YELLOW]", "GREEN": "[OK  GREEN ]"}[level]
        color = colors.get(level, "")
        reset = colors["RESET"]
        print(f"{color}{icon} {message}{reset}")
    print("=" * 55)


# ─── SYMPTOM & DISEASE ───────────────────────────────────────────────────────

def symptomdisease():
    raw = input("\nDoes your child have any symptoms? (comma separated, or 'no'): ").strip().lower()
    if raw == "no" or raw == "":
        return None

    symptoms = [s.strip() for s in raw.split(",") if s.strip()]
    if not symptoms:
        return None

    diseases = {
        "Common Cold":       ["runny nose", "sneezing", "mild fever", "cough", "sore throat"],
        "Flu":               ["high fever", "body aches", "fatigue", "dry cough"],
        "Stomach Infection": ["diarrhea", "vomiting", "stomach pain"],
        "Malaria":           ["high fever", "chills", "sweating"],
        "Pneumonia":         ["cough", "difficulty breathing", "chest pain"],
        "Dengue":            ["high fever", "joint pain", "rash"],
        "Typhoid":           ["prolonged fever", "weakness", "stomach pain"],
        "Asthma":            ["wheezing", "shortness of breath", "chest tightness"],
        "Chickenpox":        ["itchy rash", "blisters", "fever", "fatigue", "loss of appetite"],
        "Ear Infection":     ["ear pain", "fever", "irritability", "difficulty hearing", "fluid from ear"],
        "Allergies":         ["sneezing", "itchy eyes", "runny nose", "skin rash", "swelling"],
        "Bronchitis":        ["persistent cough", "mucus", "fatigue", "chest discomfort", "mild fever"],
        "Teething":          ["drooling", "gum swelling", "irritability", "chewing objects", "mild fever"],
        "Measles":           ["high fever", "red rash", "runny nose", "cough", "red eyes"],
        "Food Poisoning":    ["vomiting", "diarrhea", "stomach cramps", "nausea", "fever"],
        "HFMD":              ["mouth sores", "rash on hands", "rash on feet", "fever", "loss of appetite"],
        "Conjunctivitis":    ["red eyes", "itchy eyes", "eye discharge", "watery eyes", "swelling"],
        "Anemia":            ["fatigue", "pale skin", "weakness", "dizziness", "shortness of breath"],
    }

    best       = ""
    best_score = 0

    for disease, sym_list in diseases.items():
        matches = 0
        for user_sym in symptoms:
            for disease_sym in sym_list:
                if user_sym == disease_sym or user_sym in disease_sym.split() or disease_sym == user_sym:
                    matches += 1
                    break
        if matches > best_score:
            best       = disease
            best_score = matches

    confidence = round((best_score / max(len(symptoms), 1)) * 100)

    if best:
        print(f"\nYour child may have: {best}  (Symptom match: {confidence}%)")
    else:
        print("\nNo specific disease detected based on the symptoms entered.")

    return best if best else None


def disease_advice(best):
    advice_map = {
        "common cold":       "Give fluids, rest, steam inhalation, and light food.",
        "flu":               "Give fluids, rest, and control fever. See a doctor if fever is very high.",
        "stomach infection": "Give ORS, fluids, light diet, and maintain hygiene.",
        "malaria":           "Consult a doctor immediately and ensure full treatment.",
        "pneumonia":         "Serious condition. Seek medical help immediately.",
        "dengue":            "Give fluids, avoid ibuprofen, and monitor platelet count closely.",
        "typhoid":           "Antibiotics required. Visit a doctor promptly.",
        "asthma":            "Use the prescribed inhaler and identify and avoid triggers.",
        "chickenpox":        "Keep nails trimmed, apply calamine lotion, avoid scratching. Consult a doctor.",
        "ear infection":     "See a doctor. Keep the ear dry and avoid inserting anything into it.",
        "allergies":         "Identify and avoid the trigger. Antihistamines may help — consult a doctor.",
        "bronchitis":        "Rest, fluids, and steam. See a doctor if symptoms persist beyond a week.",
        "teething":          "Use a chilled teething ring. Consult a doctor if fever is high.",
        "measles":           "Isolate the child, ensure rest and fluids. Seek medical guidance.",
        "food poisoning":    "Give ORS and bland food. See a doctor if vomiting or diarrhoea persists.",
        "hfmd":              "Keep the child home; it is contagious. Ensure rest and fluids. Consult a doctor.",
        "conjunctivitis":    "Clean eyes gently with a damp cloth. See a doctor for appropriate eye drops.",
        "anemia":            "Include iron-rich foods (spinach, lentils, meat). Consult a doctor for supplements.",
    }
    key = best.lower()
    if key in advice_map:
        print(f"\nAdvice for {best}: {advice_map[key]}")
    else:
        print("\nPlease consult a doctor for specific advice.")


def disease_medicines(best):
    medicines_map = {
        "Common Cold": {
            "OTC Medicines": [
                "Paracetamol (Calpol) – for fever and discomfort",
                "Cetirizine (Zyrtec) – for runny nose and sneezing",
                "Dextromethorphan syrup – for cough relief",
            ],
            "Home Remedies": [
                "Honey + warm water (for children over 1 year)",
                "Steam inhalation with eucalyptus oil",
                "Warm turmeric milk",
            ],
            "Note": "Avoid antibiotics – colds are viral. Consult a doctor if symptoms last over 7 days.",
        },
        "Flu": {
            "OTC Medicines": [
                "Paracetamol (Calpol/Tylenol) – for fever and body ache",
                "Oseltamivir (Tamiflu) – antiviral, requires prescription",
                "Ibuprofen (Advil) – for pain and fever (avoid in dengue)",
            ],
            "Home Remedies": [
                "Warm chicken soup or broth",
                "Ginger tea with honey",
                "Adequate rest and hydration",
            ],
            "Note": "See a doctor if fever exceeds 103 F or breathing is labored.",
        },
        "Stomach Infection": {
            "OTC Medicines": [
                "ORS (Oral Rehydration Salts) – to prevent dehydration",
                "Zinc supplements – helps reduce diarrhea duration in children",
                "Probiotics (Lactobacillus) – to restore gut flora",
            ],
            "Home Remedies": [
                "Rice water (kanji) to soothe the stomach",
                "Banana and plain toast (BRAT diet)",
                "Coconut water for electrolytes",
            ],
            "Note": "Avoid anti-diarrheal drugs without a doctor's advice in young children.",
        },
        "Malaria": {
            "OTC Medicines": [
                "Paracetamol – for fever management only",
            ],
            "Prescription Required": [
                "Artemether-Lumefantrine (Coartem) – first-line antimalarial",
                "Chloroquine – for chloroquine-sensitive strains",
                "Primaquine – to prevent relapse (doctor supervised)",
            ],
            "Note": "ALWAYS consult a doctor. Do not self-medicate for malaria.",
        },
        "Pneumonia": {
            "OTC Medicines": [
                "Paracetamol – for fever relief",
            ],
            "Prescription Required": [
                "Amoxicillin – first-line antibiotic for bacterial pneumonia",
                "Azithromycin – for atypical pneumonia",
                "Oxygen therapy – in hospital settings if SpO2 is low",
            ],
            "Note": "Pneumonia is serious. Immediate medical attention is mandatory.",
        },
        "Dengue": {
            "OTC Medicines": [
                "Paracetamol (Calpol) – ONLY for fever. DO NOT use Ibuprofen or Aspirin.",
                "ORS – for hydration",
            ],
            "Home Remedies": [
                "Papaya leaf extract – may help raise platelet count",
                "Plenty of fluids: coconut water, juice, water",
            ],
            "Note": "Monitor platelet count daily. Seek emergency care if platelet count drops below 50,000.",
        },
        "Typhoid": {
            "Prescription Required": [
                "Azithromycin – preferred first-line for children",
                "Cefixime – oral antibiotic for typhoid",
                "Ceftriaxone – for severe cases (IV, hospital)",
            ],
            "Home Remedies": [
                "High-calorie soft diet (mashed potatoes, rice, bananas)",
                "Plenty of fluids and rest",
            ],
            "Note": "Full antibiotic course must be completed. Do not stop early.",
        },
        "Asthma": {
            "OTC Medicines": [
                "Salbutamol inhaler (Ventolin) – quick relief during attacks",
            ],
            "Prescription Required": [
                "Budesonide inhaler – daily controller medication",
                "Montelukast (Singulair) – reduces inflammation and triggers",
                "Prednisolone – for acute severe attacks (short course)",
            ],
            "Home Remedies": [
                "Keep the child away from dust, smoke, and pet dander",
                "Steam inhalation for mild congestion",
            ],
            "Note": "Always carry the relief inhaler. Have an asthma action plan from your doctor.",
        },
        "Chickenpox": {
            "OTC Medicines": [
                "Paracetamol – for fever (NOT Aspirin – risk of Reye's syndrome)",
                "Calamine lotion – for itch relief on skin",
                "Cetirizine (antihistamine) – to reduce itching",
            ],
            "Prescription Required": [
                "Acyclovir – antiviral, reduces severity if started early",
            ],
            "Home Remedies": [
                "Oatmeal bath to soothe itching",
                "Trim child's nails to prevent scratching and infection",
                "Loose, cotton clothing",
            ],
            "Note": "Keep child isolated until all blisters crust over (~7 days).",
        },
        "Ear Infection": {
            "OTC Medicines": [
                "Paracetamol or Ibuprofen – for pain and fever",
            ],
            "Prescription Required": [
                "Amoxicillin – antibiotic for bacterial ear infection",
                "Ear drops (Ciprofloxacin) – for outer ear infections",
            ],
            "Home Remedies": [
                "Warm compress on the ear to ease pain",
                "Keep ear dry – avoid swimming",
            ],
            "Note": "Do not insert anything into the ear. See a doctor if pain is severe.",
        },
        "Allergies": {
            "OTC Medicines": [
                "Cetirizine (Zyrtec) – for sneezing, runny nose, itchy eyes",
                "Loratadine (Claritin) – non-drowsy antihistamine",
                "Hydrocortisone cream – for mild skin rash/itching",
            ],
            "Prescription Required": [
                "Fluticasone nasal spray – for nasal allergies",
                "Epinephrine auto-injector (EpiPen) – for severe allergic reactions",
            ],
            "Note": "Identify and avoid allergen triggers. Carry antihistamines when outdoors.",
        },
        "Bronchitis": {
            "OTC Medicines": [
                "Paracetamol – for fever and discomfort",
                "Guaifenesin (expectorant syrup) – loosens mucus",
                "Salbutamol inhaler – if wheezing is present",
            ],
            "Home Remedies": [
                "Steam inhalation 2-3 times a day",
                "Honey in warm water for cough",
                "Plenty of fluids and rest",
            ],
            "Note": "Antibiotics are NOT needed for viral bronchitis. See doctor if symptoms persist over 10 days.",
        },
        "Teething": {
            "OTC Medicines": [
                "Paracetamol (Calpol) – for mild fever and pain relief",
                "Ibuprofen – for children over 6 months if pain is significant",
            ],
            "Home Remedies": [
                "Chilled (not frozen) teething ring",
                "Gently rub gums with a clean finger",
                "Cold cucumber or carrot stick (supervised)",
            ],
            "Note": "Avoid teething gels with benzocaine for young children. Consult a pediatrician.",
        },
        "Measles": {
            "OTC Medicines": [
                "Paracetamol – for fever",
                "Vitamin A supplements – reduces severity (doctor recommended)",
            ],
            "Home Remedies": [
                "Rest in a dim-lit room (light sensitivity is common)",
                "Warm fluids and soft foods",
                "Lukewarm sponge baths for high fever",
            ],
            "Note": "Measles is highly contagious. Isolate the child and contact a doctor immediately.",
        },
        "Food Poisoning": {
            "OTC Medicines": [
                "ORS – to prevent and treat dehydration",
                "Domperidone – for nausea/vomiting (pediatric dose)",
                "Zinc – for diarrhea in children",
            ],
            "Home Remedies": [
                "BRAT diet: Banana, Rice, Applesauce, Toast",
                "Coconut water or rice water",
                "Avoid dairy and fatty foods until recovery",
            ],
            "Note": "Seek medical help if vomiting is persistent or child shows signs of dehydration.",
        },
        "HFMD": {
            "OTC Medicines": [
                "Paracetamol or Ibuprofen – for fever and mouth pain",
                "Mouth rinse with warm salt water – for mouth sores",
            ],
            "Home Remedies": [
                "Cold foods like yogurt or ice pops to soothe mouth sores",
                "Soft, bland diet – avoid acidic or spicy foods",
            ],
            "Note": "HFMD is contagious. Keep child home for at least 7-10 days. No specific antiviral exists.",
        },
        "Conjunctivitis": {
            "OTC Medicines": [
                "Lubricant eye drops (artificial tears) – for irritation",
            ],
            "Prescription Required": [
                "Chloramphenicol eye drops – for bacterial conjunctivitis",
                "Antihistamine eye drops – for allergic conjunctivitis",
            ],
            "Home Remedies": [
                "Clean eye discharge with a warm, damp cloth (wipe outward)",
                "Avoid touching or rubbing the eye",
            ],
            "Note": "Wash hands frequently. Do not share towels or pillowcases.",
        },
        "Anemia": {
            "OTC Medicines": [
                "Ferrous sulfate (iron syrup) – for iron-deficiency anemia",
                "Folic acid supplements – for folate-deficiency anemia",
                "Vitamin C – enhances iron absorption (give alongside iron)",
            ],
            "Dietary Sources": [
                "Spinach, lentils, beans, tofu",
                "Red meat, chicken, fish",
                "Fortified cereals and dates",
            ],
            "Note": "Iron supplements should be taken on an empty stomach if tolerated. Follow doctor's dosage.",
        },
    }

    key = best.strip().title()
    if key in medicines_map:
        print(f"\nMedicines & Remedies for {key}:")
        print("-" * 45)
        for category, items in medicines_map[key].items():
            print(f"\n  [{category}]")
            if isinstance(items, list):
                for item in items:
                    print(f"    - {item}")
            else:
                print(f"    {items}")
        print("-" * 45)
    else:
        print(f"\nNo medicine data available for '{best}'. Please consult a pediatrician.")


# ─── DOCTOR SUMMARY REPORT ───────────────────────────────────────────────────

def print_doctor_summary(name, age, gender, weight, height, bmi, bmi_cat,
                          score, risk, obesity, underweight,
                          reasons, flags, deficiencies, extra_warnings,
                          tdee, carbs, protein, fats, best_disease):

    sep  = "=" * 55
    date = datetime.now().strftime("%d %B %Y, %I:%M %p")

    lines = []
    lines.append(sep)
    lines.append("       CHILD HEALTH REPORT – FOR DOCTOR")
    lines.append(f"       Generated on: {date}")
    lines.append(sep)

    lines.append("\n[CHILD INFORMATION]")
    lines.append(f"  Name   : {name}")
    lines.append(f"  Age    : {age} years")
    lines.append(f"  Gender : {gender.title()}")
    lines.append(f"  Weight : {weight} kg")
    lines.append(f"  Height : {height} cm")
    lines.append(f"  BMI    : {bmi}  ({bmi_cat})")

    lines.append("\n[HEALTH SCORE]")
    lines.append(f"  Score  : {score} / 100")
    lines.append(f"  Risk   : {risk}")

    lines.append("\n[OBESITY / UNDERWEIGHT PREDICTION]")
    lines.append(f"  Obesity Risk     : {obesity}")
    lines.append(f"  Underweight Risk : {underweight}")

    lines.append("\n[ALERT FLAGS]")
    for level, message in flags:
        icon = {"RED": "[!!! RED   ]", "YELLOW": "[!!  YELLOW]", "GREEN": "[OK  GREEN ]"}[level]
        lines.append(f"  {icon} {message}")

    lines.append("\n[RISK FACTORS IDENTIFIED]")
    if reasons:
        for r in reasons:
            lines.append(f"  - {r}")
    else:
        lines.append("  None identified.")

    lines.append("\n[SUSPECTED ILLNESS (based on symptoms)]")
    lines.append(f"  {best_disease}" if best_disease else "  No specific illness detected.")

    lines.append("\n[NUTRITIONAL DEFICIENCY FLAGS]")
    if deficiencies:
        for d in deficiencies:
            lines.append(f"  - Possible {d['nutrient']} deficiency")
            lines.append(f"    Advice: {d['advice']}")
    else:
        lines.append("  No major nutritional deficiencies detected.")

    if extra_warnings:
        lines.append("\n[DIETARY WARNINGS]")
        for w in extra_warnings:
            lines.append(f"  ! {w}")

    lines.append("\n[ESTIMATED DAILY CALORIE NEEDS]")
    lines.append(f"  Total Calories : {tdee} kcal/day")
    lines.append(f"  Carbohydrates  : {carbs} g/day")
    lines.append(f"  Protein        : {protein} g/day")
    lines.append(f"  Fats           : {fats} g/day")

    lines.append("\n" + sep)
    lines.append("  NOTE: This report is generated by a health analyzer")
    lines.append("  tool and is NOT a substitute for professional medical")
    lines.append("  diagnosis. Please consult a qualified pediatrician.")
    lines.append(sep)

    report_text = "\n".join(lines)
    print("\n" + report_text)

    filename = f"health_report_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(filename, "w") as f:
        f.write(report_text)
    print(f"\n  Report saved as: {filename}")


# ─── MAIN PROGRAM ────────────────────────────────────────────────────────────

name, age, gender, activity, diet, sleep, screen, stress, weight, height, food_items = get_input()

print("\nAnalyzing your child's health...\n")

score                              = calculate_score(activity, diet, sleep, screen, stress)
risk                               = get_risk(score)
obesity, underweight, bmi, bmi_cat = diseasepredict(age, activity, diet, sleep, screen, stress, weight, height)
reasons                            = get_reasons(activity, diet, sleep, screen, stress)
advice                             = lifestyle_advice(activity, diet, sleep, screen, stress)
tdee, carbs, protein, fats         = calculate_calorie_needs(age, weight, height, gender, activity)
deficiencies, extra_warnings       = check_nutritional_deficiencies(food_items, age, diet)

# ── Basic Results ──
print("=" * 55)
print(f"  HEALTH ANALYSIS FOR: {name.upper()}")
print("=" * 55)
print(f"  BMI          : {bmi}  ({bmi_cat})")
print(f"  Health Score : {score} / 100")
print(f"  Overall Risk : {risk}")
print(f"  Obesity Risk : {obesity}")
print(f"  Underweight  : {underweight}")

# ── Calorie Needs ──
print("\n[DAILY CALORIE NEEDS]")
print(f"  Total     : {tdee} kcal/day")
print(f"  Carbs     : {carbs} g  |  Protein : {protein} g  |  Fats : {fats} g")

# ── Nutritional Deficiencies ──
print("\n[NUTRITIONAL DEFICIENCY FLAGS]")
if deficiencies:
    for d in deficiencies:
        print(f"  - Possible {d['nutrient']} deficiency")
        print(f"    -> {d['advice']}")
else:
    print("  No major nutritional deficiencies detected.")

if extra_warnings:
    print("\n[DIETARY WARNINGS]")
    for w in extra_warnings:
        print(f"  ! {w}")

# ── Reasons ──
print("\n[RISK FACTORS]")
if reasons:
    for r in reasons:
        print(f"  - {r}")
else:
    print("  No major issues detected.")

# ── Lifestyle Advice ──
print("\n[LIFESTYLE ADVICE]")
if advice:
    for a in advice:
        print(f"  - {a}")
else:
    print("  Keep maintaining healthy habits!")

# ── Symptom Check ──
best = symptomdisease()

# ── Alert Flags ──
flags = get_alert_flags(score, bmi_cat, obesity, underweight, stress, sleep, best if best else "")
print_flags(flags)

# ── Disease Advice & Medicines ──
if best:
    choice = input("\nDo you need disease-specific advice? (yes/no): ").lower()
    if choice == "yes":
        disease_advice(best)

    med_choice = input("\nDo you want medicine recommendations? (yes/no): ").lower()
    if med_choice == "yes":
        disease_medicines(best)

# ── Doctor Summary ──
summary_choice = input("\nPrint a summary report for the doctor? (yes/no): ").lower()
if summary_choice == "yes":
    print_doctor_summary(
        name, age, gender, weight, height, bmi, bmi_cat,
        score, risk, obesity, underweight,
        reasons, flags, deficiencies, extra_warnings,
        tdee, carbs, protein, fats, best if best else None
    )

print("\nThank you! Take care of your child's health.")
