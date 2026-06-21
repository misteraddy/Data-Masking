from faker import Faker
from faker.providers import BaseProvider
import random
import string

fake = Faker("en_US")


class PresidioProvider(BaseProvider):

    def us_driver_license(self):
        # Example: D1234567
        return random.choice(string.ascii_uppercase) + ''.join(
            random.choices(string.digits, k=7)
        )

    def us_bank_account(self):
        return ''.join(random.choices(string.digits, k=12))

    def us_medicare_id(self):
        # Medicare Beneficiary Identifier (MBI)
        chars = "ACDEFGHJKMNPQRTUVWXY"
        return (
            random.choice(string.digits)
            + random.choice(chars)
            + random.choice(chars)
            + random.choice(string.digits)
            + random.choice(chars)
            + random.choice(string.digits)
            + random.choice(chars)
            + random.choice(chars)
            + random.choice(string.digits)
            + random.choice(string.digits)
            + random.choice(chars)
        )

    def us_itin_custom(self):
        return (
            "9"
            + ''.join(random.choices(string.digits, k=2))
            + "-"
            + ''.join(random.choices(string.digits, k=2))
            + "-"
            + ''.join(random.choices(string.digits, k=4))
        )

    def political_group(self):
        return random.choice([
            "Independent",
            "Republican",
            "Democrat"
        ])

    def nationality(self):
        return random.choice([
            "American",
            "Canadian",
            "Mexican"
        ])

    def religion(self):
        return random.choice([
            "Christian",
            "Jewish",
            "Muslim",
            "Hindu",
            "Buddhist"
        ])


fake.add_provider(PresidioProvider)


# PII_GENERATORS = {
#     "PERSON": fake.name,
#     "EMAIL_ADDRESS": fake.email,
#     "PHONE_NUMBER": fake.phone_number,
#     "CREDIT_CARD": fake.credit_card_number,
#     "US_SSN": fake.ssn,
#     "US_ITIN": fake.us_itin_custom,
#     "US_PASSPORT": fake.passport_number,
#     "US_DRIVER_LICENSE": fake.us_driver_license,
#     "US_BANK_NUMBER": fake.us_bank_account,
#     "US_MEDICARE_BENEFICIARY_ID": fake.us_medicare_id,
#     "IBAN_CODE": fake.iban,
#     "IP_ADDRESS": fake.ipv4,
#     "URL": fake.url,
#     "LOCATION": fake.address,
#     "DATE_TIME": fake.date_time,
#     "CRYPTO": fake.cryptocurrency_address,
# }


# CUSTOM_MAPPINGS = {
#     "VIN": lambda: fake.vin(),
#     "LICENSE_PLATE": lambda: fake.license_plate(),
#     "POLICY_NUMBER": lambda: fake.bothify("POL-########"),
#     "CLAIM_NUMBER": lambda: fake.bothify("CLM-########"),
#     "ACCOUNT_NUMBER": lambda: fake.bban(),
#     "ROUTING_NUMBER": lambda: ''.join(fake.random_choices(elements='0123456789', length=9)),
#     "IMEI": lambda: fake.numerify("###############"),
#     "MEMBER_ID": lambda: fake.bothify("MEM-########"),
# }


# nationality_provider = DynamicProvider(
#     provider_name="nationality",
#     elements=[
#         "American",
#         "Canadian",
#         "Mexican",
#         "British",
#         "French",
#         "German",
#         "Italian",
#         "Japanese",
#         "Chinese",
#         "Indian"
#     ]
# )

# fake.add_provider(nationality_provider)