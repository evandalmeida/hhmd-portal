from models import User, Clinic, Patient, Appointment, Provider
from flask import request, jsonify, session
from config import app, db, bcrypt

app.secret_key = b'u\xd2\xdc\xe82\xa3\xc0\xca\xe7H\xd03oi\xd1\x95\xcc\x7f'

URL = '/api/v1'

# HELPER METHODS
def current_user():
    print(f"\nuser id: {session.get('user_id')}\n")
    return User.query.filter(User.id == session.get('user_id')).first()

# CLINIC 
@app.post(URL + '/clinic_admin-registration')
def clinic_register():
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
        role='clinic_admin'
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
    
    session['user_id'] = new_user.id

    return jsonify(new_user.to_dict()), 201


#LOGIN/LOGOUT and CHECK SESSION
@app.post(URL + '/login')
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        session['user_id'] = user.id
        return jsonify(user.to_dict()), 202
    else:
        return jsonify({"message": "Invalid username or password"}), 401
    
@app.get(URL + '/check_session')
def check_session():
    user = current_user()
    if user:
        return jsonify({'user_id': user.id, 'role': user.role}), 200
    else: 
        return {}, 401
    
@app.delete(URL + '/logout')
def logout():
    session['user_id'] = None
    return {}, 204


# PATIENT
@app.post(URL + '/patient-registration')
def patient_register():
    # Get the registration data from the request
    data = request.get_json()

    # Extract the required fields from the request data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    street_address = data.get('street_address')
    state = data.get('state')
    zip_code = data.get('zip_code')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if all required fields are provided
    if not all([first_name, last_name, dob, street_address, state, zip_code, username, email, password]):
        return jsonify({'error': 'All fields are required'}), 400

    # Check if a user with the same email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 409

    # Hash the password
    password_hash = bcrypt.generate_password_hash(password.encode('utf-8'), 10)

    # Create a new User and Patient
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash.decode('utf-8'),
        role='patient'
    )

    new_patient = Patient(
        first_name=first_name,
        last_name=last_name,
        dob=dob,
        street_address=street_address,
        state=state,
        zip_code=zip_code,
        user=new_user
    )

    # Add the new User and Patient to the database
    db.session.add(new_user)
    db.session.add(new_patient)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

# CLINIC INFO
@app.route(URL + '/clinic_info')
def clinic_info():
  if current_user().role == 'clinic_admin':
    clinic = current_user().clinic

    if not clinic:
      return jsonify({'error': 'Information not found'}), 404
    
    return jsonify(clinic.to_dict())

  else:
    return jsonify({'error': 'Unauthorized'}), 401
  

# GET PATIENTS
@app.route(URL + '/patients')
def get_patients():
    if current_user().role == 'clinic_admin':
        clinic = Clinic.query.get(current_user().clinic.id)
        if not clinic:
            return jsonify({'error': 'Clinic not found'}), 404
        patients = clinic.patients

        return jsonify([patient.to_dict() for patient in patients ])

    else:
        return jsonify({'error': 'Unauthorized'}), 401



# APPOINTMENTS FOR CLINICS
@app.route(URL + '/providers')
def get_appointments():
    if current_user().role == 'clinic_admin':

        providers = Provider.query.filter_by(clinic_id=current_user().clinic.id)
    
        return jsonify([provider.to_dict() for provider in providers])


    else:
        return jsonify({'error': 'Unauthorized'}), 401



    
    # elif current_user().role == 'patient':
    #     appointments = Appointment.query.filter_by(patient_id=current_user().patient.id)

    #     return jsonify([appointment.to_dict() for appointment in appointments])
    # appointment_list = [{"id": appointment.id, "date": appointment.date.isoformat(), "time": appointment.time.strftime('%H:%M:%S')} for appointment in appointments]

    # return jsonify(appointment_list)



if __name__ == '__main__':
    db.create_all() 
    app.run(port=5555, debug=True)