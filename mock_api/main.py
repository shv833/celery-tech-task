from fastapi import FastAPI
from faker import Faker

app = FastAPI()
fake = Faker()


@app.get("/users", response_model=list[dict])
async def get_users(limit: int = 10):
    users = []
    for _ in range(limit):
        users.append(
            {
                "uid": fake.uuid4(),
                "name": fake.name(),
                "username": fake.user_name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "website": fake.domain_name(),
                "company": fake.company(),
            }
        )
    return users


@app.get("/credit_cards", response_model=list[dict])
async def get_credit_cards(limit: int = 1):
    cards = []
    for _ in range(limit):
        cards.append(
            {
                "uid": fake.uuid4(),
                "credit_card_number": fake.credit_card_number(),
                "credit_card_expiry_date": fake.credit_card_expire(),
                "credit_card_type": fake.credit_card_provider(),
            }
        )
    return cards


@app.get("/addresses", response_model=list[dict])
async def get_addresses(limit: int = 1):
    addresses = []
    for _ in range(limit):
        addresses.append(
            {
                "uid": fake.uuid4(),
                "city": fake.city(),
                "street_name": fake.street_name(),
                "street_address": fake.street_address(),
                "zip_code": fake.zipcode(),
                "country": fake.country(),
            }
        )
    return addresses
