from fastapi import FastAPI, HTTPException

app = FastAPI()

# Doctors List
doctors = [
            {
                "id": 1,
                "name": "Dr. Aisha Mehta",
                "specialization": "Cardiologist",
                "fee": 800,
                "experience_years": 12,
                "is_available": True
            },
            {
                "id": 2,
                "name": "Dr. Rohit Kulkarni",
                "specialization": "Dermatologist",
                "fee": 600,
                "experience_years": 8,
                "is_available": False
            },
            {
                "id": 3,
                "name": "Dr. Neha Patil",
                "specialization": "Pediatrician",
                "fee": 500,
                "experience_years": 6,
                "is_available": True
            },
            {
                "id": 4,
                "name": "Dr. Arjun Sharma",
                "specialization": "General",
                "fee": 400,
                "experience_years": 10,
                "is_available": True
            },
            {
                "id": 5,
                "name": "Dr. Sneha Joshi",
                "specialization": "Cardiologist",
                "fee": 900,
                "experience_years": 15,
                "is_available": False
            },
            {
                "id": 6,
                "name": "Dr. Karan Deshmukh",
                "specialization": "Dermatologist",
                "fee": 550,
                "experience_years": 5,
                "is_available": True
            }
            ]

# Appointment Records
appointments = []
appt_counter = 1

# Q1
@app.get('/')
def home():
    return {'message': 'Welcome to SmartCare Clinic'}

# Q2
@app.get('/doctors')
def get_doctors():
    available_count = sum(1 for d in doctors if d['is_available'])
    return {'doctors':doctors, 'total':len(doctors), 'available_count':available_count}

# Q5
@app.get('/doctors/summary')
def get_doctors_summary():
    available_count = sum(1 for d in doctors if d['is_available'])
    most_experienced_doctor = max(doctors, key = lambda d : d['experience_years'])
    cheapest_consultation_fee = min(doctors, key = lambda d : d['fee'])
    
    specialization = {}
    for d in doctors:
        if d['specialization'] in specialization:
            specialization[d["specialization"]] += 1
        else:
            specialization[d["specialization"]] = 1
    
    return {'total': len(doctors), 
            'available_count':available_count, 
            'most_experienced_doctor':most_experienced_doctor['name'], 
            'cheapest_consultation_fee': cheapest_consultation_fee['fee'],
            'specialization': specialization
            }

# Q3
@app.get('/doctors/{doctor_id}')
def get_doctor_id(doctor_id : int):
    for d in doctors:
        if d['id'] == doctor_id:
            return {'doctor': d}
        
    raise HTTPException(status_code=404, detail="Doctor not found !")

# Q4
@app.get('/appointments')
def get_appointments():
    return {'appointments':appointments, 'total':len(appointments)}

