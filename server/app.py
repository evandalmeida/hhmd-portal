# Remote library imports
from flask import request, session, jsonify



from models import db, User, Patient, Appointment

from datetime import datetime

from config import app, db, bcrypt


# # HELPER METHODS
# def current_user():
#     return User.query.filter(User.id == session.get('user_id')).first()

# def check_admin():
#     return current_user() and current_user().username == "chett2"



# HOME 
@app.route('/')
def index():
    return '<h1>Project Server</h1>'



# # USER SIGN UP
# @app.route('/users', methods=['POST'])
# def create_user():
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({"message": "Invalid input data"}), 400

#         username = data.get("username")
#         password = data.get("password")

#         if not username or not password:
#             return jsonify({"message": "Username and password are required"}), 400

#         # Check if the username already exists
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             return jsonify({"message": "Username already taken"}), 400

#         # Hash the password
#         password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

#         # Create a new user
#         new_user = User(username=username, password_hash=password_hash)
#         db.session.add(new_user)
#         db.session.commit()

#         # Generate a JWT for the new user
#         access_token = create_access_token(identity=new_user.id)
#         return jsonify({"access_token": access_token, "user": new_user.to_dict()}), 201

#     except Exception as e:
#         return jsonify({'error': str(e)}, 500)



# # USER LOGIN and LOGOUT
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data:
#         return jsonify({"message": "Invalid input data"}), 400

#     username = data.get("username")
#     password = data.get("password")

#     if not username or not password:
#         return jsonify({"message": "Username and password are required"}), 400

#     user = User.query.filter_by(username=username).first()

#     if user and bcrypt.check_password_hash(user.password_hash, password):
#         # User is authenticated, generate a JWT
#         access_token = create_access_token(identity=user.id)
#         return jsonify({"access_token": access_token, "user": user.to_dict()}), 200
#     else:
#         return jsonify({"message": "Invalid username or password"}), 401

    

# @app.route('/check_session', methods=['GET'])

# def check_session():
#     current_user = get_jwt_identity()
#     user = User.query.get(current_user)
#     if user:
#         return jsonify(user.to_dict()), 200
#     else:
#         return jsonify({"message": "User not found"}), 404


    
# @app.route('/logout', methods=['DELETE'])
# def logout_user():
#     # User is authenticated if they reached this route
#     # The token is invalidated upon expiration
#     return jsonify({"message": "Logged out"}), 200



# # PATIENT ROUTES
# @app.route('/api/patient', methods=['GET'])
# def get_patient_info():
#     try:
#         user = current_user()

#         if not user:
#             return jsonify({'message': 'User not found'}), 404

#         patient = Patient.query.filter_by(id=user.id).first()

#         if not patient:
#             return jsonify({'message': 'Patient information not found'}), 404

#         patient_info = {
#             'id': patient.id,
#             'first_name': patient.first_name,
#             'last_name': patient.last_name,
#             'dob': patient.dob.strftime('%Y-%m-%d'),  # Serialize the date as a string
#             'address': patient.address,
#             'DL_image': patient.DL_image.decode('utf-8') if patient.DL_image else None,  # Serialize DL_image if it exists
#             'rx': patient.rx
#         }

#         return jsonify({'patient_info': patient_info}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}, 500)


# @app.route('/api/patient/update', methods=['PUT'])
# def update_patient_info():
#     current_user_id = get_jwt_identity()

#     if not current_user_id:
#         return jsonify({'message': 'User not found'}), 404

#     patient = Patient.query.filter(Patient.id == current_user_id).first()

#     if not patient:
#         return jsonify({'message': 'Patient information not found'}), 404

#     try:
#         json = request.json

#         if 'first_name' in json:
#             patient.first_name = json['first_name']
#         if 'last_name' in json:
#             patient.last_name = json['last_name']
#         if 'dob' in json:
#             patient.dob = datetime.strptime(json['dob'], '%Y-%m-%d')
#         if 'address' in json:
#             patient.address = json['address']
#         if 'DL_image' in json:
#             patient.DL_image = json['DL_image'].encode('utf-8')
#         if 'rx' in json:
#             patient.rx = json['rx']

#         db.session.commit()

#         return jsonify({'message': 'Patient information updated'}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 406



# # CLINIC (ADMIN) ROUTES
# @app.route('/api/clinic', methods=['GET'])
# def get_clinic_info():
#     current_user_id = get_jwt_identity()

#     if not current_user_id:
#         return jsonify({'message': 'User not found'}), 404

#     user = User.query.get(current_user_id)

#     if user and user.clinic:
#         clinic = user.clinic
#         clinic_info = {
#             'id': clinic.id,
#             'name': clinic.name,
#             'address': clinic.address,
#             'city': clinic.city,
#             'zip_code': clinic.zip_code,
#         }
#         return jsonify(clinic_info), 200
#     else:
#         return jsonify({'message': 'Clinic information not found'}), 404


# # APPOINTMENTS
# @app.route('/api/clinic/appointments', methods=['GET'])
# def list_clinic_appointments():
#     clinic_id = request.args.get('clinic_id')
    
#     if clinic_id is None:
#         return jsonify({'message': 'Clinic ID is required'}), 400

#     appointments = Appointment.query.filter_by(clinic_id=clinic_id).all()

#     appointment_list = []
#     for appointment in appointments:
#         appointment_data = {
#             'id': appointment.id,
#             'date': appointment.date.strftime('%Y-%m-%d'),
#             'time': appointment.time.strftime('%H:%M:%S'),
#             'patient_id': appointment.patient_id,
#             'provider_id': appointment.provider_id
#         }
#         appointment_list.append(appointment_data)

#     return jsonify(appointment_list), 200

# @app.route('/api/clinic/appointments/add', methods=['POST'])
# def add_clinic_appointment():
#     try:
#         data = request.json
#         clinic_id = data.get('clinic_id')

#         if not clinic_id:
#             return jsonify({'message': 'Clinic ID is required'}), 400

#         appointment = Appointment(
#             date=data['date'],
#             time=data['time'],
#             patient_id=data['patient_id'],
#             provider_id=data['provider_id'],
#             clinic_id=clinic_id
#         )

#         db.session.add(appointment)
#         db.session.commit()

#         return jsonify({'message': 'Appointment added to the clinic'}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
# @app.route('/api/clinic/appointments/update', methods=['PUT'])
# def update_clinic_appointment():
#     try:
#         data = request.json
#         appointment_id = data.get('id')

#         if not appointment_id:
#             return jsonify({'message': 'Appointment ID is required'}), 400

#         appointment = Appointment.query.get(appointment_id)

#         if not appointment:
#             return jsonify({'message': 'Appointment not found'}), 404

#         appointment.date = data.get('date', appointment.date)
#         appointment.time = data.get('time', appointment.time)
#         appointment.patient_id = data.get('patient_id', appointment.patient_id)
#         appointment.provider_id = data.get('provider_id', appointment.provider_id)

#         db.session.commit()

#         return jsonify({'message': 'Appointment information updated'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/clinic/appointments/delete', methods=['DELETE'])
# def delete_clinic_appointment():
#     try:
#         appointment_id = request.args.get('appointment_id')

#         if not appointment_id:
#             return jsonify({'message': 'Appointment ID is required'}), 400

#         appointment = Appointment.query.get(appointment_id)

#         if not appointment:
#             return jsonify({'message': 'Appointment not found'}), 404

#         db.session.delete(appointment)
#         db.session.commit()

#         return jsonify({'message': 'Appointment deleted from the clinic'}), 204
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# # ERROR METHODS
# @app.errorhandler(404)
# def page_not_found(e):
#     return jsonify({'message':'Resource not found'}), 404

# @app.errorhandler(500)
# def internal_server_error(e):
#     return jsonify({'message':'Internal server error'}), 500 


if __name__ == '__main__':
    db.create_all() 
    app.run(port=5555, debug=True)