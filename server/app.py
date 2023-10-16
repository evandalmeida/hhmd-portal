from flask import request, jsonify 
from models import db, User, Clinic, Patient, Appointment
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from config import app, db, bcrypt


@app.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  
  if 'clinic_name' in data:
    user = User(
      email=data['email'],
      password=bcrypt.generate_password_hash(data['password']),
      role='clinic_admin'
    )
    clinic = Clinic(name=data['clinic_name'], admin_id=user.id)

  else:
    user = User(
      email=data['email'],  
      password=bcrypt.generate_password_hash(data['password']),
      role='patient'
    )
    
    user.clinic_id = data['clinic_id']

  db.session.add(user)
  db.session.add(clinic) if 'clinic_name' in data else None
  db.session.commit()

  return jsonify(user)


@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  user = User.query.filter_by(email=data['email']).first()

  if user and bcrypt.check_password_hash(user.password, data['password']):
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

  return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/users')
@jwt_required()
def get_users():
  curr_user = get_jwt_identity()
  clinic = Clinic.query.get(curr_user.clinic_id)

  if not clinic or clinic.admin_id != curr_user.id:
    return jsonify({'error': 'Unauthorized'}), 401
  
  users = User.query.all()
  return jsonify(users)


@app.route('/appointments')
@jwt_required()
def get_appointments():
  curr_user = get_jwt_identity()

  if curr_user.role == 'clinic_admin':
    clinic = Clinic.query.get(curr_user.clinic_id)
    appointments = Appointment.query.filter_by(clinic_id=clinic.id)

  elif curr_user.role == 'patient':  
    appointments = Appointment.query.filter_by(patient_id=curr_user.id)

  else:
    return jsonify({'error': 'Unauthorized'}), 401

  return jsonify(appointments)


@app.route('/patients')
@jwt_required()
def get_patients():
  # Validate clinic admin
  curr_user = get_jwt_identity()
  clinic = Clinic.query.get(curr_user.clinic_id)

  if not clinic or clinic.admin_id != curr_user.id:
    return jsonify({'error': 'Unauthorized'}), 401

  patients = Patient.query.filter_by(clinic_id=clinic.id)

  return jsonify(patients)


@app.route('/create_appointment', methods=['POST']) 
@jwt_required()
def create_appointment():
  data = request.get_json()
  curr_user = get_jwt_identity()

  if curr_user.role == 'clinic_admin':
    pass 
  elif curr_user.role == 'provider':
    if curr_user.id != data['provider_id']:
      return jsonify({'error': 'Unauthorized'}), 401
  else:
    return jsonify({'error': 'Unauthorized'}), 401

  apt = Appointment(
    patient_id=data['patient_id'],
    provider_id=data['provider_id'], 
    date=data['date'],
    time=data['time']
  )

  db.session.add(apt)
  db.session.commit()

  return jsonify(apt)



if __name__ == '__main__':
    db.create_all() 
    app.run(port=5555, debug=True)