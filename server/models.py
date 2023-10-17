

from datetime import datetime
from config import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define a one-to-one relationship with Clinic
    clinic = db.relationship('Clinic', back_populates='user', uselist=False, primaryjoin="User.id == Clinic.user_id")

    # Define a one-to-one relationship with Patient
    patient = db.relationship('Patient', back_populates='user', uselist=False)

class Clinic(db.Model, SerializerMixin):
    __tablename__ = 'clinics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='clinic', uselist=False)

    # Define a many-to-many relationship with Patient
    patients = db.relationship('Patient', secondary='patient_clinics', back_populates='clinics')
    patients_proxy = association_proxy('patients', 'id')  # Proxy for patient IDs

class Provider(db.Model, SerializerMixin):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    provider_type = db.Column(db.String, nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'))

    # Define a one-to-many relationship with Appointment
    appointments = db.relationship('Appointment', back_populates='provider')

class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'))

    # Define a many-to-one relationship with Patient
    patient = db.relationship('Patient', back_populates='appointments')

    # Define the many-to-one relationship with Provider
    provider = db.relationship('Provider', back_populates='appointments')


class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    street_address = db.Column(db.String, nullable=False)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Define a one-to-one relationship with User
    user = db.relationship('User', back_populates='patient', uselist=False)

    # Define a many-to-many relationship with Clinic
    clinics = db.relationship('Clinic', secondary='patient_clinics', back_populates='patients')
    clinics_proxy = association_proxy('clinics', 'id')  # Proxy for clinic IDs

    # Define the one-to-many relationship with Appointment
    appointments = db.relationship('Appointment', back_populates='patient')


class PatientClinic(db.Model, SerializerMixin):
    __tablename__ = 'patient_clinics'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'))
