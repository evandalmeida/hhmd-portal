from random import randint, choice as rc

from faker import Faker 

from app import app

from models import db, User, Clinic, Provider, Patient, Appointment

if __name__ == '__main__':

    fake = Faker()

    with app.app_context():
       
        print('Deleting tables...')
        db.drop_all()
        
        print('Creating tables...')
        db.create_all()

        print("Adding users...")
        for i in range(3):
            user = User(
                username=fake.user_name(),
                password_hash=fake.password(),
                role='admin',
                email=fake.email()
            )
            db.session.add(user)

        print("Adding clinics...")
        for i in range(3):
            clinic = Clinic(
               name=fake.company(),
               address=fake.street_address(),
               city=fake.city(),
               zip_code=fake.postcode()
            )
            db.session.add(clinic)

        print("Adding providers...")
        for i in range(5):
            provider = Provider(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                provider_type=rc(['Nurse', 'Doctor']),
                clinic_id=rc([1, 2, 3]) 
            )
            db.session.add(provider)

        print("Adding patients...")
        for i in range(10):
            patient = Patient(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                dob=fake.date_between(start_date='-65y', end_date='-18y'),
                address=fake.street_address(),
                DL_image=fake.binary(length=128),
                rx=fake.text(max_nb_chars=40)
            )
            db.session.add(patient)

        print("Adding appointments...")
        for i in range(15):
            appointment = Appointment(
                date=fake.date_between(start_date='-1y', end_date='+1y'),
                time=fake.time(),
                patient_id=rc(range(1, 11)),
                provider_id=rc(range(1, 6)),
                clinic_id=rc([1, 2, 3])
            )
            db.session.add(appointment)

        print("Committing changes...")
        db.session.commit()

        print("Done!")
