"""
Training data for clinical note classification.
Each tuple contains: (note_text, category)
"""

TRAINING_NOTES = [
    # Emergency notes
    ("Patient arrives with severe chest pain and shortness of breath", "Emergency"),
    ("Acute headache with vision problems and dizziness", "Emergency"),
    ("Patient collapsed, unconscious, needs immediate attention", "Emergency"),
    ("Severe bleeding from wound, patient in distress", "Emergency"),
    ("High fever 104F with confusion and rapid heartbeat", "Emergency"),
    ("Difficulty breathing, oxygen saturation dropping rapidly", "Emergency"),
    ("Suspected heart attack, crushing chest pain radiating to arm", "Emergency"),
    ("Severe allergic reaction, throat swelling", "Emergency"),
    ("Head injury from fall, loss of consciousness", "Emergency"),
    ("Severe abdominal pain, possible appendicitis", "Emergency"),

    # Follow-up notes
    ("Follow-up visit for blood pressure medication adjustment", "Follow-up"),
    ("Checking progress on diabetes management plan", "Follow-up"),
    ("Patient returns for wound healing assessment", "Follow-up"),
    ("Follow-up on previous lab results discussion", "Follow-up"),
    ("Monitoring response to new medication regimen", "Follow-up"),
    ("Post-surgery check-up, incision healing well", "Follow-up"),
    ("Review of treatment plan effectiveness", "Follow-up"),
    ("Patient reports improvement in symptoms since last visit", "Follow-up"),
    ("Follow-up on referral to specialist", "Follow-up"),
    ("Checking blood sugar levels after medication change", "Follow-up"),

    # Routine checkup notes
    ("Annual physical examination completed", "Routine"),
    ("Routine blood work and vitals check", "Routine"),
    ("General health screening, all normal", "Routine"),
    ("Routine vaccination administration", "Routine"),
    ("Yearly wellness visit, no complaints", "Routine"),
    ("Preventive care visit, health education provided", "Routine"),
    ("Routine cholesterol and blood pressure screening", "Routine"),
    ("Well-child visit, growth and development normal", "Routine"),
    ("Routine eye and ear examination", "Routine"),
    ("Periodic health assessment, patient feeling well", "Routine"),

    # Initial consultation notes
    ("New patient intake and medical history review", "Initial Consultation"),
    ("First visit for persistent cough and fatigue", "Initial Consultation"),
    ("Patient presents with new onset back pain", "Initial Consultation"),
    ("Initial assessment for skin rash concern", "Initial Consultation"),
    ("New patient complains of sleep disturbances", "Initial Consultation"),
    ("First consultation regarding weight management", "Initial Consultation"),
    ("Patient seeks help for stress and anxiety", "Initial Consultation"),
    ("Initial visit for migraine headaches", "Initial Consultation"),
    ("New patient with joint pain and stiffness", "Initial Consultation"),
    ("First appointment to discuss digestive issues", "Initial Consultation"),

    # Blood Pressure related
    ("Patient comes with headache and high blood pressure", "Follow-up"),
    ("Blood pressure reading 140/90, slightly elevated", "Routine"),
    ("Patient says high BP is controlled, 120/80 in general", "Follow-up"),
    ("Severe hypertensive crisis, BP 200/120", "Emergency"),
    ("Routine blood pressure check, within normal range", "Routine"),

    # Headache related
    ("Patient complains of a strong headache on the back of neck", "Follow-up"),
    ("Mild headache, probable tension type", "Routine"),
    ("Patient feels general improvement and no more headaches", "Follow-up"),
    ("Sudden severe headache, worst ever experienced", "Emergency"),

    # Medication related
    ("Patient is taking medicines to control blood pressure", "Follow-up"),
    ("Patient is taking Losartan 50mg to control blood pressure", "Follow-up"),
    ("Prescription refill for chronic condition management", "Routine"),
    ("Adverse reaction to new medication", "Emergency"),
    ("Patient compliant with medication regimen", "Follow-up"),

    # Add more varied examples
    ("Routine dental cleaning and check-up", "Routine"),
    ("Patient reports no issues, just routine visit", "Routine"),
    ("Minor cut requiring stitches", "Routine"),
    ("Sprained ankle from sports injury", "Routine"),
    ("Regular immunization for travel", "Routine"),
    ("Patient doing well on current treatment plan", "Follow-up"),
    ("Adjusting insulin dosage based on recent readings", "Follow-up"),
    ("Chronic pain management discussion", "Follow-up"),
    ("Reviewing test results from specialist", "Follow-up"),
    ("Severe asthma attack, struggling to breathe", "Emergency"),
    ("Possible stroke symptoms, facial drooping", "Emergency"),
    ("Diabetic emergency, blood sugar critically low", "Emergency"),
]

