from faker import Faker

fake = Faker("en_US")

PII_MAPPINGS = {
    "PERSON": fake.name,
    "EMAIL_ADDRESS": fake.email,
    "PHONE_NUMBER": fake.phone_number,
    "CREDIT_CARD": fake.credit_card_number,
    "US_SSN": fake.ssn,
    "US_ITIN": fake.itin,
    "US_PASSPORT": fake.passport_number,
    "IP_ADDRESS": fake.ipv4,
    "URL": fake.url,
    "LOCATION": fake.address,
    "DATE_TIME": fake.date_time,
    "CRYPTO": fake.cryptocurrency_address,
}