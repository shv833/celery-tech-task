import os

import httpx

from db.database import SessionLocal
from db.models import Address, CreditCard, User
from worker.celery_app import celery_app

MOCK_API_URL = os.getenv("MOCK_API_URL", "http://mock_api:8001")


@celery_app.task(name="fetch_users_task")
def fetch_users_task():
    with SessionLocal() as db:
        try:
            response = httpx.get(f"{MOCK_API_URL}/users?limit=5")
            response.raise_for_status()
            users_data = response.json()
        except Exception as e:
            print(f"Error fetching users: {e}")
            return "Failed to fetch users"

        count = 0
        for u_data in users_data:
            exists = db.query(User).filter(User.email == u_data["email"]).first()
            if not exists:
                new_user = User(
                    name=u_data["name"],
                    username=u_data["username"],
                    email=u_data["email"],
                    uid=u_data["uid"],
                )
                db.add(new_user)
                count += 1

        db.commit()
        return f"Saved {count} new users."


@celery_app.task(name="enrich_address_task")
def enrich_address_task():
    with SessionLocal() as db:
        users_needing_address = (
            db.query(User).outerjoin(Address).filter(Address.id.is_(None)).limit(5).all()
        )

        if not users_needing_address:
            return "No users need addresses."

        count = len(users_needing_address)
        try:
            response = httpx.get(f"{MOCK_API_URL}/addresses?limit={count}")
            addr_data = response.json()
        except Exception as e:
            return f"Error fetching addresses: {e}"

        for user, addr in zip(users_needing_address, addr_data, strict=False):
            new_addr = Address(
                city=addr["city"],
                street_name=addr["street_name"],
                country=addr["country"],
                user_id=user.id,
            )
            db.add(new_addr)

        db.commit()
        return f"Enriched {count} users with addresses."


@celery_app.task(name="enrich_cc_task")
def enrich_cc_task():
    with SessionLocal() as db:
        users_needing_cc = (
            db.query(User).outerjoin(CreditCard).filter(CreditCard.id.is_(None)).limit(5).all()
        )

        if not users_needing_cc:
            return "No users need credit cards."

        count = len(users_needing_cc)
        try:
            response = httpx.get(f"{MOCK_API_URL}/credit_cards?limit={count}")
            cc_data = response.json()
        except Exception as e:
            return f"Error fetching CCs: {e}"

        for user, cc in zip(users_needing_cc, cc_data, strict=False):
            new_cc = CreditCard(
                cc_number=cc["cc_number"],
                cc_type=cc["cc_type"],
                cc_expiry=cc["cc_expiry"],
                user_id=user.id,
            )
            db.add(new_cc)

        db.commit()
        return f"Enriched {count} users with Credit Cards."
