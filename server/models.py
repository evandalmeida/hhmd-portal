from sqlalchemy_serializer import SerializerMixin
from config import db
from flask_sqlalchemy import SQLAlchemy;
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin;
from datetime import datetime
from config import db, metadata


db = SQLAlchemy(metadata=metadata)


class User(db.Model, SerializerMixin):
    __tablename__ ='users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    serialize_rules = ('-password_hash', '-email')

class Clinic(db.Model):
    __tablename__ = 'clinics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)

    providers = relationship('Provider', back_populates='clinics')
    patients = relationship('Patient', secondary='patient_clinics', back_populates='clinics')

class Provider(db.Model, SerializerMixin):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    provider_type = db.Column(db.String, nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'))

    clinic = relationship('Clinic', back_populates='providers')
    appointments = relationship('Appointment', back_populates='provider')

    serialize_rules = ('-clinic',)

class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'))

    patient = relationship('Patient', back_populates='appointments')
    provider = relationship('Provider')

    serialize_rules = ('-patient.DL_image',)

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.String, nullable=False)
    DL_image = db.Column(db.LargeBinary)
    rx = db.Column(db.String)

    appointments = relationship('Appointment', back_populates='patient')
    clinics = relationship('Clinic', secondary='patient_clinics',back_populates='patients')

class Form(db.Model):
    __tablename__ = 'forms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    document_type = db.Column(db.String)

    signature = relationship('FormSignature', back_populates='forms')

class PatientClinc(db.Model):
    __tablename__ = 'patient_clinics'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'))

class PatientForm(db.Model):
    __tablename__ = 'patient_forms'

    id = db.Column(db.Integer, primary_key=True)
    patient_id= db.Column(db.Integer, db.ForeignKey('patients.id'))
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'))

class FormSignature(db.Model):
    __tablename__ = 'form_signatures'

    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    envelope_id = db.Column(db.String)
    signature_id = db.Column(db.String)
    signed_status = db.Column(db.String)

    form = relationship('Form', back_populates='signatures')
    patient = relationship('Patient', back_populates='signatures')

    serialize_rules = ('-form', '-patient')

class DocumentFile(db.Model):
    __tablename__ = 'document_files'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'))
    form_signature_id = db.Column(db.Integer, db.ForeignKey('form_signatures.id'))

    serialize_rules = ('-form_signature',)