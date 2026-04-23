# 💊 SmartCare – Medical Appointment & Management System

<img width="1536" height="1024" alt="Cover Photo Final 1" src="https://github.com/user-attachments/assets/9016c897-c506-4ca0-8434-e088d9c5a98c" />


---

> > 🚀 Built from scratch using FastAPI — a complete backend system with 20+ APIs, real-world workflows, and advanced data operations.

---

## 🚀 Project Overview

SmartCare is a backend system for managing doctors, scheduling appointments, and tracking consultations. It covers everything from basic GET routes to advanced search, sorting, and pagination — all tested via Swagger UI.

---

## ⚙️ Features Implemented

- **GET APIs** — Home route, list all doctors/appointments, get by ID, summary stats
- **POST APIs** — Book appointments with full Pydantic validation
- **Helper Functions** — `find_doctor()`, `calculate_fee()`, `filter_doctors_logic()`
- **CRUD Operations** — Create, Read, Update, Delete for doctors
- **Appointment Workflow** — Schedule → Confirm → Complete / Cancel
- **Fee Calculation** — In-person, video, emergency + senior citizen discount
- **Filtering** — Filter doctors by specialization, fee, experience, availability
- **Search** — Case-insensitive keyword search across name and specialization
- **Sorting** — Sort by fee, name, or experience (ascending/descending)
- **Pagination** — Page-based navigation for doctors and appointments
- **Combined Browse** — Filter + Sort + Paginate in one endpoint (`/doctors/browse`)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core language |
| FastAPI | Web framework |
| Pydantic | Request validation |
| Uvicorn | ASGI server |
| Swagger UI | API testing |

---

## 📁 Project Structure

```
fastapi-medical-appointment-system/
│
├── main.py               # All routes, models, and helper functions
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── screenshots/          # Swagger UI screenshots for all 20 tasks
    ├── cover.png
    ├── Q1_home_route.png
    ├── Q2_get_all_doctors.png
    ├── Q3_get_doctor_by_id.png
    ├── Q4_get_appointments.png
    ├── Q5_doctors_summary.png
    ├── Q6_pydantic_validation.png
    ├── Q7_helper_functions.png
    ├── Q8_post_appointment.png
    ├── Q9_senior_citizen_discount.png
    ├── Q10_filter_doctors.png
    ├── Q11_add_doctor.png
    ├── Q12_update_doctor.png
    ├── Q13_delete_doctor.png
    ├── Q14_confirm_cancel_appointment.png
    ├── Q15_complete_active_appointments.png
    ├── Q16_search_doctors.png
    ├── Q17_sort_doctors.png
    ├── Q18_paginate_doctors.png
    ├── Q19_appointments_search_sort_page.png
    └── Q20_combined_browse.png
```

---

## 📋 API Endpoints

### Doctors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/doctors` | Get all doctors |
| GET | `/doctors/summary` | Stats — total, available, specializations |
| GET | `/doctors/filter` | Filter by specialization, fee, experience |
| GET | `/doctors/search` | Keyword search across name & specialization |
| GET | `/doctors/sort` | Sort by fee, name, or experience |
| GET | `/doctors/page` | Paginated doctor list |
| GET | `/doctors/browse` | Combined search + sort + pagination |
| GET | `/doctors/{doctor_id}` | Get doctor by ID |
| POST | `/doctors` | Add a new doctor |
| PUT | `/doctors/{doctor_id}` | Update doctor fee or availability |
| DELETE | `/doctors/{doctor_id}` | Delete doctor (if no active appointments) |

### Appointments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/appointments` | Get all appointments |
| GET | `/appointments/active` | Get scheduled + confirmed appointments |
| GET | `/appointments/search` | Search by patient name |
| GET | `/appointments/sort` | Sort by fee or date |
| GET | `/appointments/page` | Paginated appointment list |
| GET | `/appointments/by-doctor/{doctor_id}` | Appointments by doctor |
| POST | `/appointments` | Book a new appointment |
| POST | `/appointments/{id}/confirm` | Confirm an appointment |
| POST | `/appointments/{id}/cancel` | Cancel an appointment |
| POST | `/appointments/{id}/complete` | Mark appointment as completed |

---

## 🏃 How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Prem-7171/fastapi-medical-appointment-system.git
cd fastapi-medical-appointment-system
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the server**
```bash
uvicorn main:app --reload
```

**5. Open Swagger UI**
```
http://127.0.0.1:8000/docs
```

---

## 📸 Swagger UI Preview

<img width="1023" height="953" alt="Swagger_Overview" src="https://github.com/user-attachments/assets/30445a5d-4c7f-411c-9750-eaea1fa73799" />


---

## 👨‍💻 Author

**Prem Palkar**
B.Tech CSE (AI & ML) | Innomatics Research Labs Intern

[![GitHub](https://img.shields.io/badge/GitHub-Prem--7171-black?logo=github)](https://github.com/Prem-7171)

---

## 🏢 Internship

Built as the **Final Project** for the FastAPI Internship at **Innomatics Research Labs**.

> *"Not just coding, but thinking like a developer."*
