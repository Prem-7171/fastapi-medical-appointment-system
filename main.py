from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
import math

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
    senior_citizen : bool = Field(default=False)
    
# Pydantic model for new Doctor
# Q11
class NewDoctor(BaseModel):
    name : str = Field(..., min_length=2)
    specialization : str = Field(..., min_length=2)
    fee : int = Field(..., gt=0)
    experience_years : int = Field(..., gt=0)
    is_available : bool = Field(default=True)
    
# Appointment Records
appointments = []
appt_counter = 1


# Helper Functions
# Q7    
def find_doctor(doctor_id):
    '''Finds a doctor by ID'''
    for d in doctors:
        if d['id'] == doctor_id:
            return d
    return None
        
def calculate_fee(base_fee, appointment_type, senior_citizen ):
    
    if appointment_type == 'video':
        fee = int(0.8*base_fee)
    elif appointment_type == 'in-person':
        fee = base_fee
    elif appointment_type == 'emergency':
        fee = int(1.5*base_fee)
    else:
        return None
    
    discounted_fee = fee
    if senior_citizen:
        discounted_fee = int(fee - (0.15*fee))
    
    return fee, discounted_fee
    
# Q10 - Filtering Helper Function
def filter_doctors_logic(specialization, max_fee, min_experience, is_available):
    
    result = doctors.copy()
   
    if specialization is not None:
        result = [d for d in result if d['specialization'].lower() == specialization.lower()]
       
    if max_fee is not None:
        result = [d for d in result if d['fee'] <= max_fee]
        
    if min_experience is not None:
        result = [d for d in result if d['experience_years'] >= min_experience]
        
    if is_available is not None:
        result = [d for d in result if d['is_available'] == is_available]
        
    return result

# Finding Appointment Helper function
def find_appointment(appointment_id):
    '''Finds an appointment by ID'''
    for a in appointments:
        if a['appointment_id'] == appointment_id:
            return a
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

# Q10
@app.get('/doctors/filter')
def filter_doctors(
    specialization : str = Query(default=None, description="Enter the Specialization of the doctor"),
    max_fee : int = Query(default=None, description="Enter the maximum fee of the doctor"),
    min_experience : int = Query(default=None, description="Enter the minimum experience of the doctor"),
    is_available : bool = Query(default=None, description="Enter the availability of the doctor")
):
    
    result = filter_doctors_logic(specialization, max_fee, min_experience, is_available)
    
    return {'doctors': result, 'total': len(result)}

# Q16 - Searching
@app.get('/doctors/search')
def search_doctors(keyword : str = Query(...)):
    searched = [d for d in doctors if keyword.lower() in d['name'].lower() or keyword.lower() in d['specialization'].lower()]
    if not searched:
        raise HTTPException( status_code=404, detail= "no results found on given keyword")
    return {'total_found': len(searched), 'results':searched}

# Q17 - Sorting
@app.get('/doctors/sort')
def sort_by(sort_by : str = Query(default="fee"),
            order : str = Query(default="asc")):
    if sort_by not in ['fee', 'name', 'experience_years']:
        raise HTTPException( status_code=400, detail="sort_by must be one of fee, name and experience_years")
    reverse = False if order == "asc" else True 
    sorted_list = sorted(doctors, key = lambda doc : doc[sort_by], reverse=reverse)
    return {'sort_by':sort_by, 'order':order, 'total':len(sorted_list),'doctors': sorted_list}

# Q18 - Pagination
@app.get('/doctors/page')
def paging_doctors(page : int = Query(default=1, gt=0),
                   limit : int = Query(default=3, gt=0)):
    total_pages = math.ceil(len(doctors)/limit)
    if page > total_pages:
        raise HTTPException(status_code=400, detail="Invalid Page number")
    start = (page-1)*limit
    end = start+ limit
    
    
    return {'page':page, 'limit':limit, 'doctors': doctors[start:end], 'total_pages':total_pages, 'total_items':len(doctors )}

# Q20 - Browse Doctors
@app.get('/doctors/browse')
def browse_doctors(keyword : str = Query(default=None),
                   sort_by : str = Query(default="fee"),
                   order : str = Query(default="asc"),
                   page : int = Query(default=1, gt=0),
                   limit : int = Query(default=4, gt=0)
                   ):
     
    # Sort_by Validation
    if sort_by not in ['fee', 'experience_years']:
        raise HTTPException(status_code=400, detail="sort_by must be one of fee and experience_years")
    
    results = doctors.copy()
    
    # 1 - Filtering by search keyword
    if keyword is not None:
        results = [d for d in doctors if keyword.lower() in d['name'].lower() or keyword.lower() in d['specialization'].lower()]

    if not results:
        return {'message':'No results found for the given keyword'}
    
     # Page validation 
    total_pages = math.ceil(len(doctors)/limit)
    if page > total_pages:
        raise HTTPException( status_code=400, detail="Invalid page number entered")
    
    # 2 - Filtering By sorting and order
    reverse = False if order == "asc" else True
    results = sorted(results, key = lambda r : r[sort_by], reverse=reverse)
    
    # 3 - Pagination for the filtered data
    start = (page - 1)*limit
    end = start + limit
    
    return {'keyword':keyword, 'sort_by':sort_by, 'order':order, 'page':page, 'limit':limit, 'total':len(results), 'total_pages':total_pages, 'doctors':results[start:end]}
    
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

# Q8, Q9
@app.post('/appointments')
def get_appointment(appointment : AppointmentRequest):
    global appt_counter
    doctor = find_doctor(appointment.doctor_id)
    if not doctor:
        raise HTTPException( status_code=404, detail="doctor not found")
    if not doctor['is_available']:
        raise HTTPException( status_code=400, detail="doctor is not available")
    
    original_fee, discounted_fee = calculate_fee(doctor['fee'], appointment.appointment_type, appointment.senior_citizen)
    appt = {'appointment_id':appt_counter, 
            'patient':appointment.patient_name,
            'doctor_id': doctor['id'], 
            'doctor_name':doctor['name'],
            'reason': appointment.reason,
            'date':appointment.date,
            'type':appointment.appointment_type,
            'original_fee': original_fee,
            'discounted_fee' : discounted_fee,
            'status':'scheduled'
            }
    appointments.append(appt)
    appt_counter += 1
    return appt
    
# Q11 - New Doctor Endpoint
@app.post('/doctors', status_code= status.HTTP_201_CREATED)
def add_new_doctor(new_doctor : NewDoctor):
    for d in doctors:
        if d['name'].lower() == new_doctor.name.lower():
            raise HTTPException( status_code= 409, detail="Doctor with this name already exists")
    
    new_doc = {
                "id": len(doctors) + 1,
                "name": new_doctor.name,
                "specialization": new_doctor.specialization,
                "fee": new_doctor.fee,
                "experience_years": new_doctor.experience_years,
                "is_available": new_doctor.is_available
    }
    
    doctors.append(new_doc)
    return {'new_doctor': new_doc}

# Q12 -  To update existing doctors Endpoint
@app.put('/doctors/{doctor_id}') 
def update_doctor(doctor_id : int,
                  fee : int = Query(default=None, gt=0),
                  is_available : bool = Query(default=None)
                  ):
    doc = find_doctor(doctor_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    if fee is not None:
        doc['fee'] = fee
    if is_available is not None:
        doc['is_available'] = is_available
    return {'updated_doctor': doc}
    
    
# Q13 -  To Delete existing doctors with no appointments Endpoint
@app.delete('/doctors/{doctor_id}') 
def delete_doctor(doctor_id : int):
    doc = find_doctor(doctor_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    for appoint in appointments:
        if appoint['status'] == 'scheduled' and appoint['doctor_name'] == doc['name']:
            raise HTTPException(status_code=409, detail= "The doctor already has scheduled appointments")
        
    doctors.remove(doc)
    return {'message': 'doctor deleted sucessfully', 'deleted_doctor': doc}
    
# Q15 - Display Active Appointments
@app.get('/appointments/active')
def active_appointments():
    active_appointments = [a for a in appointments if a['status'] in ['scheduled', 'confirmed']]
    return {'active_appointments': active_appointments}    
    
# Q14 - confirm appointment
@app.post('/appointments/{appointment_id}/confirm')
def confirm_appointment(appointment_id: int):
    appoint = find_appointment(appointment_id)
    
    if appoint is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appoint['status'] == 'cancelled':
        raise HTTPException(status_code=409, detail= "The appointment has been already cancelled")
    
    appoint['status'] = 'confirmed'
    return {'message':'appointment status confirmed', 'appointment':appoint}

# Q14 - Cancle appointment
@app.post('/appointments/{appointment_id}/cancel')
def cancle_appointment(appointment_id: int):
    appoint = find_appointment(appointment_id)
    
    if appoint is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appoint['status'] = 'cancelled'
    
    doc = find_doctor(appoint['doctor_id'])
    doc['is_available'] = True
    
    return {'message':'appointment cancelled', 'appointment':appoint}

# Q15 - Display Appointments by-doctor
@app.get('/appointments/by-doctor/{doctor_id}')
def by_doctor_appointments(doctor_id : int):
     by_doctor_appointments = [a for a in appointments if a['doctor_id'] == doctor_id]
     return {'total': len(by_doctor_appointments), 'appointments': by_doctor_appointments}

# Q15 - Complete appointment
@app.post('/appointments/{appointment_id}/complete')
def complete_appointment(appointment_id: int):
    appoint = find_appointment(appointment_id)
    
    if appoint is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appoint['status'] == 'cancelled':
        raise HTTPException(status_code=409, detail= "The appointment has been already cancelled")
    
    appoint['status'] = 'completed'
    return {'message':'appointment completed', 'appointment':appoint}

# Q19 - Searching Appointment
@app.get('/appointments/search')
def search_appointments(patient_name : str = Query(...)):
    searched = [a for a in appointments if patient_name.lower() in a['patient'].lower()]
    if not searched:
        raise HTTPException( status_code=404, detail= "no results found on given patient_name")
    return {'total_found': len(searched), 'results':searched}

# Q19 - Sorting Appointment
@app.get('/appointments/sort')
def sort_by(sort_by : str = Query(default="fee"),
            order : str = Query(default="asc")):
    if sort_by not in ['discounted_fee', 'date']:
        raise HTTPException( status_code=400, detail="sort_by must be one of fee and date")
    reverse = False if order == "asc" else True 
    sorted_list = sorted(appointments, key = lambda appoint : appoint[sort_by], reverse=reverse)
    return {'sort_by':sort_by, 'order':order, 'total':len(sorted_list),'appointments': sorted_list}

# Q19 - Appointment Pagination
@app.get('/appointments/page')
def paging_appointment(page : int = Query(default=1, gt=0),
                   limit : int = Query(default=3, gt=0)):
    total_pages = math.ceil(len(appointments)/limit)
    if page > total_pages:
        raise HTTPException(status_code=400, detail="Invalid Page number")
    start = (page-1)*limit
    end = start+ limit
    
    
    return {'page':page, 'limit':limit, 'appointments': appointments[start:end], 'total_pages':total_pages, 'total_items':len(appointments )}


    
    