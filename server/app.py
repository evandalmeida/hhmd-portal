
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from models import User, Clinic, Appointment, Patient
from flask import request, jsonify, session
from config import app, db, bcrypt
from datetime import timedelta 

from dotenv import load_dotenv
import os

load_dotenv()

app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1) 

jwt = JWTManager(app)


# SHARED ROUTES
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data["password"].encode('utf-8')):
        access_token = create_access_token(identity=user.serialize())
        return jsonify({"access_token": access_token, "user": user.serialize()})

    return jsonify(message="Invalid username or password"), 401




## CLINIC
@app.route('/clinic_info')
@jwt_required()
def clinic_info():
    if get_jwt_identity().role != 'clinic_admin':
        return jsonify({'error': 'Unauthorized'}), 401

    curr_user = get_jwt_identity()
    clinic = Clinic.query.get(curr_user.clinic_id)

    if clinic is None:
        return jsonify({'error': 'Clinic not found'}), 404

    clinic_info = {
        'id': clinic.id,
        'name': clinic.name,
        'address': clinic.address,
        'state': clinic.state,
        'zip_code': clinic.zip_code
    }

    return jsonify(clinic_info)



@app.route('/clinic_admin-registration', methods=['POST'])
def clinic_register():
    try:
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')  
        clinic_name = data.get('clinic_name')

        if not all([username, password, email, clinic_name]):
            return jsonify({'error': 'All fields are required'}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409

        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'), 10)

        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash.decode('utf-8'),  
            role='clinic_admin',
        )

        new_clinic = Clinic(
            name=clinic_name,
            user=new_user,
            address=data.get('clinic_address'),
            state=data.get('clinic_state'),
            zip_code=data.get('clinic_zip_code'),
        )

        db.session.add(new_user)
        db.session.add(new_clinic)
        db.session.commit()

        return jsonify({'message': 'Clinic registered successfully'})

    except Exception as e:
        return jsonify({'error': 'An error occurred during registration', 'error_message': str(e)}), 500



@app.route('/patients')
@jwt_required()
def get_patients():
    current_user = get_jwt_identity()

    if current_user.role == 'clinic_admin':
        clinic = Clinic.query.get(current_user.clinic_id)
        if not clinic:
            return jsonify({'error': 'Clinic not found'}), 404
        patients = clinic.patients
    elif current_user.role == 'provider':
        return jsonify({'error': 'Unauthorized'}), 401
    elif current_user.role == 'patient':
        patient = Patient.query.get(current_user.patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        patients = [patient]
    else:
        return jsonify({'error': 'Unauthorized'}), 401

    serialized_patients = [{'id': patient.id, 'first_name': patient.first_name, 'last_name': patient.last_name} for patient in patients]

    return jsonify({'patients': serialized_patients})



## APPOINTMENTS FOR CLINCS
@app.route('/appointments')
@jwt_required()
def get_appointments():
    curr_user = get_jwt_identity()

    if curr_user.role == 'clinic_admin':
        appointments = Appointment.query.filter_by(clinic_id=curr_user.clinic_id)

    elif curr_user.role == 'patient':
        appointments = Appointment.query.filter_by(patient_id=curr_user.id)

    else:
        return jsonify({'error': 'Unauthorized'}), 401

    appointment_list = [{"id": appointment.id, "date": appointment.date, "time": appointment.time} for appointment in appointments]

    return jsonify(appointment_list)



if __name__ == '__main__':
    db.create_all() 
    app.run(port=5555, debug=True)