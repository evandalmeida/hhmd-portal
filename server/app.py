
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Clinic, Appointment, Patient
from flask import request, jsonify, session
from config import app, db, bcrypt


# SHARED ROUTES
@app.get('/check_session')
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        return user.to_dict(), 200
    else:
        return {}, 401
    

    
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 401

        if not bcrypt.check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid password'}), 401

        access_token = create_access_token(identity=user.id)

        return jsonify(access_token=access_token, role=user.role)
    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.delete('/logout')
def logout():
    session.pop('user_id')
    return {}, 204

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        hashed_pw = bcrypt.generate_password_hash(data["password"].encode('utf-8'), 10)

        # Creating the new user
        new_user = User.create(username=data['username'], hashed_password=hashed_pw)

        # Committing the user to the database
        db.session.commit()

        session['user_id'] = new_user.id
        return new_user.to_dict(), 201
    except Exception as e:
        print(e)  # Log the error for debugging
        db.session.rollback()
        return {'error': str(e)}, 500
    



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

@app.route('/clinic_admin-registration', methods=['POST', 'OPTIONS'])
def clinic_register():
    if request.method == 'OPTIONS':
        # This is an OPTIONS request, respond with 200 OK.
        return '', 200

    try:
        data = request.get_json()

        # Extract data and validate it
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        clinic_name = data.get('clinic_name')

        if not all([username, password, email, clinic_name]):
            return jsonify({'error': 'All fields are required'}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409  # 409 for conflict

        # Hash the password before creating the user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create and add a new user and clinic
        new_user = User(
            username=username,
            password_hash=hashed_password,  # Use the hashed password
            email=email,
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
        app.logger.error(f"Error during clinic registration: {str(e)}")
        return jsonify({'error': 'An error occurred during registration'}), 500


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