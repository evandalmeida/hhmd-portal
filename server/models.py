

# Import necessary libraries and modules
from datetime import datetime
from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

# Define the User model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)  
    role = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    # Define a one-to-one relationship with Clinic
    clinic = db.relationship('Clinic', back_populates='user', uselist=False, primaryjoin="User.id == Clinic.user_id")
    patient = db.relationship('Patient', back_populates='user', uselist=False)

    @classmethod
    def create(self, username, hashed_password):
        user = self(username=username, password_hash=hashed_password.decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return user


    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'email': self.email
        }







# Define the Clinic model
class Clinic(db.Model, SerializerMixin):
    __tablename__ = 'clinics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='clinic', uselist=False)

    # Define a many-to-many relationship with Patient
    patients = db.relationship('Patient', secondary='patient_clinics', back_populates='clinics')
    patients_proxy = association_proxy('patients', 'id')  # Proxy for patient IDs

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'state': self.state,
            'zip_code': self.zip_code
        }

# Define the Provider model
class Provider(db.Model, SerializerMixin):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    provider_type = db.Column(db.String, nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'))

    # Define a one-to-many relationship with Appointment
    appointments = db.relationship('Appointment', back_populates='provider')

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'provider_type': self.provider_type
        }

# Define the Appointment model
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

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),  # Convert to ISO format for serialization
            'time': self.time.strftime('%H:%M:%S')  # Convert to string in HH:MM:SS format
        }


# Define the Patient model
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

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob.isoformat(),  # Convert to ISO format for serialization
            'street_address': self.street_address,
            'state': self.state,
            'zip_code': self.zip_code
        }

# Define the many-to-many relationship table for patients and clinics
patient_clinics = db.Table('patient_clinics',
    db.Column('patient_id', db.Integer, db.ForeignKey('patients.id'), primary_key=True),
    db.Column('clinic_id', db.Integer, db.ForeignKey('clinics.id'), primary_key=True)
)