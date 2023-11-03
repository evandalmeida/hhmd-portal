from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)  
    role = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    # Define a one-to-one relationship with Clinic
    clinic = db.relationship('Clinic', back_populates='user', uselist=False) 
    patient = db.relationship('Patient', back_populates='user', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'email': self.email
        }

class Clinic(db.Model, SerializerMixin):
    __tablename__ = 'clinics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='clinic', uselist=False)
    

    # M2M relationship with Patient
    patients = db.relationship('Patient', secondary='patient_clinics', back_populates='clinics')
    patients_proxy = association_proxy('patients', 'id') 

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'state': self.state,
            'zip_code': self.zip_code
        }
    
class Provider(db.Model, SerializerMixin):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    provider_type = db.Column(db.String, nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'))

    # O2M relationship with Appointment
    appointments = db.relationship('Appointment', back_populates='provider')

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'provider_type': self.provider_type
        }

class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'))

    # M2O relationship with Patient
    patient = db.relationship('Patient', back_populates='appointments')

    # M2o relationship with Provider
    provider = db.relationship('Provider', back_populates='appointments')

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'time': self.time.strftime('%H:%M:%S')
        }


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

    # O2O relationship with User
    user = db.relationship('User', back_populates='patient', uselist=False)

    # M2M relationship with Clinic
    clinics = db.relationship('Clinic', secondary='patient_clinics', back_populates='patients')
    clinics_proxy = association_proxy('clinics', 'id')

    # O2M relationship with Appointment
    appointments = db.relationship('Appointment', back_populates='patient')

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob.isoformat(),
            'street_address': self.street_address,
            'state': self.state,
            'zip_code': self.zip_code
        }

# M2M relationship table for patients and clinics
patient_clinics = db.Table('patient_clinics',
    db.Column('patient_id', db.Integer, db.ForeignKey('patients.id'), primary_key=True),
    db.Column('clinic_id', db.Integer, db.ForeignKey('clinics.id'), primary_key=True)
)


