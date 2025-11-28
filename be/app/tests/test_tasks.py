from unittest.mock import patch

import respx
from httpx import Response

from db.models import Address, User
from worker.tasks import MOCK_API_URL, enrich_address_task, fetch_users_task


@respx.mock
def test_fetch_users_task(db_session):
    """
    Test that users are fetched from API and saved to DB.
    """
    mock_users = [
        {
            "uid": "u1",
            "name": "Alice",
            "username": "alice1",
            "email": "alice@test.com",
            "phone": "123",
            "website": "test.com",
            "company": "Corp",
        }
    ]
    respx.get(f"{MOCK_API_URL}/users?limit=5").mock(return_value=Response(200, json=mock_users))

    with patch("worker.tasks.SessionLocal") as mock_session_cls:
        mock_session_cls.return_value.__enter__.return_value = db_session

        result = fetch_users_task.delay().get()

        assert "Saved 1 new users" in result

        user = db_session.query(User).filter(User.email == "alice@test.com").first()
        assert user is not None
        assert user.name == "Alice"


@respx.mock
def test_enrich_address_task(db_session):
    """
    Test that addresses are fetched and linked to users.
    """
    user = User(name="Bob", username="bobby", email="bob@test.com", uid="u2")
    db_session.add(user)
    db_session.commit()

    mock_address = [
        {
            "uid": "a1",
            "city": "Lviv",
            "street_name": "Market Sq",
            "street_address": "1",
            "zip_code": "79000",
            "country": "Ukraine",
            "state": "Lviv",
        }
    ]
    respx.get(f"{MOCK_API_URL}/addresses?limit=1").mock(
        return_value=Response(200, json=mock_address)
    )

    with patch("worker.tasks.SessionLocal") as mock_session_cls:
        mock_session_cls.return_value.__enter__.return_value = db_session

        result = enrich_address_task.delay().get()

        assert "Enriched 1 users" in result

        address = db_session.query(Address).filter(Address.user_id == user.id).first()
        assert address is not None
        assert address.city == "Lviv"
