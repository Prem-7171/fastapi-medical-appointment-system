from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

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

# Pydantic model for appointment 
# Q6
class AppointmentRequest(BaseModel):
    patient_name : str = Field(..., min_length=2)
    doctor_id : int = Field(..., gt=0)
    date : str =Field(..., min_length=8)
    reason : str = Field(..., min_length=5)
    appointment_type : str = Field(default='in-person')
    

# Appointment Records
appointments = []
appt_counter = 1


# Helper Functions
# Q7    
def find_doctor(doctor_id):
    for d in doctors:
        if d['id'] == doctor_id:
            return d
    return None
        
def calculate_fee(base_fee, appointment_type):
    if appointment_type == 'video':
        return int(0.8*base_fee)
    elif appointment_type == 'in-person':
        return base_fee
    elif appointment_type == 'emergency':
        return int(1.5*base_fee)
    else:
        return None
    

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

# Q8
@app.post('/appointments')
def get_appointment(appointment : AppointmentRequest):
    global appt_counter
    doctor = find_doctor(appointment.doctor_id)
    if not doctor:
        raise HTTPException( status_code=404, detail="doctor not found")
    if not doctor['is_available']:
        raise HTTPException( status_code=400, detail="doctor is not available")
    
    fee = calculate_fee(doctor['fee'], appointment.appointment_type)
    appt = {'appointment_id':appt_counter, 
            'patient':appointment.patient_name, 
            'doctor_name':doctor['name'],
            'reason': appointment.reason,
            'date':appointment.date,
            'type':appointment.appointment_type,
            'calculated_fee': fee,
            'status':'scheduled'
            }
    appointments.append(appt)
    appt_counter += 1
    return appt
    
    