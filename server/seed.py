from sqlalchemy.exc import IntegrityError
from faker import Faker 
from config import db
from models import User, Clinic, Provider, Appointment, Patient, Form, PatientClinic, PatientForm, FormSignature, DocumentFile

fake = Faker()

num_users = 10
num_clinics = 5
num_providers = 20 
num_patients = 50
num_forms = 10
num_appointments = 100

def main():

  db.drop_all()
  db.create_all()

  # Create users
  users = []
  for _ in range(num_users):
    user = User(
      username=fake.user_name(),
      password_hash=fake.password(),
      role=fake.random_element(elements=["admin", "doctor", "patient"]),
      email=fake.email() 
    )
    users.append(user)

  try:
    db.session.add_all(users)
    db.session.commit()
  except IntegrityError:
    db.session.rollback()

  # Create clinics
  clinics = []
  for _ in range(num_clinics):
    clinic = Clinic(
      name=fake.company(),
      address=fake.address(),
      city=fake.city(),
      zip_code=fake.zipcode()
    )
    clinics.append(clinic)

  try:
    db.session.add_all(clinics)
    db.session.commit()
  except IntegrityError:
    db.session.rollback()

  # Create providers
  providers = []
  for _ in range(num_providers):
    provider = Provider(
      first_name=fake.first_name(),
      last_name=fake.last_name(),
      provider_type=fake.random_element(elements=["GP", "Dentist", "Surgeon"]), 
      clinic_id=fake.random_element(elements=clinics).id  
    )
    providers.append(provider)

  try:
    db.session.add_all(providers)
    db.session.commit() 
  except IntegrityError:
    db.session.rollback()

  # Create patients
  patients = []
  for _ in range(num_patients):
    patient = Patient(
      first_name=fake.first_name(),
      last_name=fake.last_name(),
      dob=fake.date_of_birth(minimum_age=18, maximum_age=80),
      address=fake.address(),
      DL_image=None,
      rx=fake.sentence() 
    )
    patients.append(patient)

  try:
    db.session.add_all(patients)
    db.session.commit()
  except IntegrityError: 
    db.session.rollback()

  # Create forms
  forms = []
  for _ in range(num_forms):
    form = Form(
      name=fake.word(),
      document_type=fake.random_element(elements=["Medical", "Dental", "Surgical"])
    )
    forms.append(form)

  try:
    db.session.add_all(forms)
    db.session.commit()
  except IntegrityError:
    db.session.rollback()

  # Add relationships
  for patient in patients:
    # Assign clinics
    num_clinics = fake.random_int(min=1, max=len(clinics)) 
    patient_clinics = random.sample(clinics, num_clinics)
    for clinic in patient_clinics:
      db.session.add(PatientClinic(
        patient_id=patient.id,
        clinic_id=clinic.id  
      ))

    # Assign forms 
    num_forms = fake.random_int(min=1, max=len(forms))
    patient_forms = random.sample(forms, num_forms)
    for form in patient_forms:
      db.session.add(PatientForm(
        patient_id=patient.id,
        form_id=form.id
      ))

  for provider in providers:
    # Assign clinic
    provider.clinic_id = fake.random_element(elements=clinics).id

  for appointment in appointments: 
    # Assign patient and provider
    appointment.patient_id = fake.random_element(elements=patients).id
    appointment.provider_id = fake.random_element(elements=providers).id

  try:
    db.session.commit()
  except IntegrityError: 
    db.session.rollback()

if __name__ == '__main__':
  main()