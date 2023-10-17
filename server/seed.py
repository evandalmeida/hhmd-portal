# Import the necessary modules and classes
from config import db, app
from models import User, Clinic, Provider, Appointment, Patient, PatientClinic
from faker import Faker
from datetime import datetime, time, timedelta
import random

# Create a Faker instance
faker = Faker()

# Function to generate a random time between 9am and 5pm
def generate_weekday_time():
    return time(random.randint(9, 16), random.randint(0, 59), random.randint(0, 59))

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")
        print("Deleting old data...")

        db.drop_all()
        db.create_all()

        print("Seeding users...")

        users_list = []

        for _ in range(5):
            role = random.choice(["clinic", "patient"])
            first_name = faker.first_name()
            last_name = faker.last_name()
            user = User(
                username=f"{first_name} {last_name}",
                password_hash=faker.password(),
                role=role,
                email=faker.email(),
            )
            users_list.append(user)

        db.session.add_all(users_list)
        db.session.commit()

        print("Seeding clinics...")

        clinics_list = []

        for _ in range(5):
            clinic = Clinic(
                name=faker.company(),
                address=faker.street_address(),
                state=faker.state_abbr(),  # Add state information
                zip_code=faker.zipcode(),  # Add ZIP+4 codes as strings
            )
            clinics_list.append(clinic)

        db.session.add_all(clinics_list)
        db.session.commit()

        print("Seeding providers...")

        providers_list = []

        for _ in range(10):
            provider_type = random.choice(["NP", "DO", "MD", "PA"])
            first_name = faker.first_name()
            last_name = faker.last_name()

            provider = Provider(
                first_name=first_name,
                last_name=last_name,
                provider_type=provider_type,
                clinic_id=random.choice(clinics_list).id
            )
            providers_list.append(provider)

        db.session.add_all(providers_list)
        db.session.commit()

        print("Seeding patients...")

        patients_list = []

        for _ in range(10):
            first_name = faker.first_name()
            last_name = faker.last_name()
            dob = faker.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90)
            street_address = faker.street_address()
            zip_code = faker.zipcode()  # Add ZIP+4 codes as strings
            state = faker.state_abbr()  # Add state abbreviations
            user = random.choice(users_list)

            patient = Patient(
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                street_address=street_address,  # Update the address field name
                state=state,  # Assign state abbreviations
                zip_code=zip_code,  # Assign ZIP codes
                user=user,
            )
            patients_list.append(patient)

        db.session.add_all(patients_list)
        db.session.commit()

        print("Seeding patient-clinics...")

        patient_clinics_list = []

        for patient in patients_list:
            for _ in range(random.randint(1, 3)):
                clinic = random.choice(clinics_list)
                if clinic.id not in [pc.clinic_id for pc in patient_clinics_list]:
                    patient_clinic = PatientClinic(patient_id=patient.id, clinic_id=clinic.id)
                    patient_clinics_list.append(patient_clinic)

        db.session.add_all(patient_clinics_list)
        db.session.commit()

        print("Seeding appointments...")

        appointments_list = []

        for _ in range(20):
            appointment = Appointment(
                date=faker.date_between_dates(date_start=datetime.now() - timedelta(days=365), date_end=datetime.now()),
                time=generate_weekday_time(),
                patient=random.choice(patients_list),
                provider=random.choice(providers_list),
            )
            appointments_list.append(appointment)

        db.session.add_all(appointments_list)
        db.session.commit()

        print("Seeding complete!")