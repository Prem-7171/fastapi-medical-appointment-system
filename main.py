from fastapi import FastAPI

app = FastAPI()

# Q1
@app.get('/')
def home():
    return {'message': 'Welcome to SmartCare Clinic'}