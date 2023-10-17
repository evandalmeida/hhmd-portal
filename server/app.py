


from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Clinic, Patient, Appointment, Provider
from flask import request, jsonify
from config import app, db, bcrypt

@app.route('/users')
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    clinic = Clinic.query.get(current_user.clinic_id)

    if not clinic or clinic.admin_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 401

    users = User.query.all()

    user_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]

    return jsonify(user_data)

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({'error': 'User not found'}), 401

    if not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid password'}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify(access_token=access_token)

# Clinic registration route
@app.route('/clinic_register', methods=['POST'])
def clinic_register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    clinic_name = data.get('clinic_name')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 400

    new_user = User(
        username=username,
        password=bcrypt.generate_password_hash(password),
        email=email,
        role='clinic',
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

@app.route('/patient_register', methods=['POST'])
def patient_register():
    data = request.get_json()

    # Check if all required fields are present
    required_fields = ['username', 'password', 'email', 'first_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    username = data['username']
    password = data['password']
    email = data['email']
    first_name = data['first_name']

    # Check if a user with the same email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 409  # Use 409 for conflict

    # Hash the password using Flask-Bcrypt
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new User and Patient
    new_user = User(
        username=username,
        password_hash=password_hash,
        email=email,
        role='patient',
    )

    new_patient = Patient(
        first_name=first_name,
        user=new_user,
        last_name=data.get('last_name'),  # You can adjust these as needed
        dob=data.get('dob'),
        street_address=data.get('street_address'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
    )

    # Commit the changes to the database
    db.session.add(new_user)
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'Patient registered successfully'})












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

@app.route('/create_appointment', methods=['POST'])
@jwt_required()
def create_appointment():
    current_user = get_jwt_identity()
    data = request.get_json()

    if current_user.role == 'clinic_admin':
        provider_id = data.get('provider_id')
        patient_id = data.get('patient_id')
        date = data.get('date')
        time = data.get('time')

        if not provider_id or not patient_id or not date or not time:
            return jsonify({'error': 'Invalid appointment data'}), 400

        appointment = Appointment(
            provider_id=provider_id,
            patient_id=patient_id,
            date=date,
            time=time
        )
        db.session.add(appointment)
        db.session.commit()

        return jsonify({'message': 'Appointment created'})

    elif current_user.role == 'provider':
        provider_id = current_user.id
        patient_id = data.get('patient_id')
        date = data.get('date')
        time = data.get('time')

        if not patient_id or not date or not time:
            return jsonify({'error': 'Invalid appointment data'}), 400

        appointment = Appointment(
            provider_id=provider_id,
            patient_id=patient_id,
            date=date,
            time=time
        )
        db.session.add(appointment)
        db.session.commit()

        return jsonify({'message': 'Appointment created'})

    else:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/add_provider', methods=['POST'])
@jwt_required()
def add_provider():
    if get_jwt_identity().role != 'clinic_admin':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()

    if 'first_name' not in data or 'last_name' not in data or 'provider_type' not in data:
        return jsonify({'error': 'Missing data'}), 400

    new_provider = Provider(
        first_name=data['first_name'],
        last_name=data['last_name'],
        provider_type=data['provider_type'],
        clinic_id=get_jwt_identity().clinic_id
    )

    db.session.add(new_provider)
    db.session.commit()

    return jsonify({'message': 'Provider added successfully'})

@app.route('/remove_provider/<int:provider_id>', methods=['DELETE'])
@jwt_required()
def remove_provider(provider_id):
    if get_jwt_identity().role != 'clinic_admin':
        return jsonify({'error': 'Unauthorized'}), 401

    provider = Provider.query.get(provider_id)

    if not provider:
        return jsonify({'error': 'Provider not found'}), 404
    
    db.session.delete(provider)
    db.session.commit()

    return jsonify({'message': 'Provider removed successfully'})

@app.route('/add_appointment', methods=['POST'])
@jwt_required()
def add_appointment():
    if get_jwt_identity().role != 'clinic_admin':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()

    patient_id = data.get('patient_id')
    provider_id = data.get('provider_id')
    date = data.get('date')
    time = data.get('time')

    if not all([patient_id, provider_id, date, time]):
        return jsonify({'error': 'Missing required fields'}), 400

    appointment = Appointment(
        patient_id=patient_id,
        provider_id=provider_id,
        date=date,
        time=time
    )

    db.session.add(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment added successfully'})

@app.route('/remove_appointment/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def remove_appointment(appointment_id):
    if get_jwt_identity().role != 'clinic_admin':
        return jsonify({'error': 'Unauthorized'}), 401

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    if appointment.provider.clinic_id != get_jwt_identity().clinic_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # Delete the appointment
    db.session.delete(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment removed successfully'})

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

@app.route('/add_patient_appointment', methods=['POST'])
@jwt_required()
def add_patient_appointment():
    if get_jwt_identity().role != 'patient':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()

    date = data.get('date')
    time = data.get('time')

    if not date or not time:
        return jsonify({'error': 'Invalid appointment details'}), 400

    appointment = Appointment(
        patient_id=get_jwt_identity().id,
        provider_id=data.get('provider_id'),
        date=date,
        time=time
    )

    db.session.add(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment added successfully'})

@app.route('/remove_patient_appointment/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def remove_patient_appointment(appointment_id):
    current_user = get_jwt_identity()

    if current_user.role != 'patient':
        return jsonify({'error': 'Unauthorized'}), 401

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    if appointment.patient_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 401

    db.session.delete(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment removed successfully'})

if __name__ == '__main__':
    db.create_all() 
    app.run(port=5555, debug=True)