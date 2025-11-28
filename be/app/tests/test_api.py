from db.models import Address, User


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "backend"}


def test_get_users_empty(client):
    """Test fetching users when DB is empty"""
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_get_users_with_data(client, db_session):
    """Test fetching users with nested address data"""
    user = User(name="John Doe", username="johnd", email="john@example.com", uid="123-456")
    db_session.add(user)
    db_session.flush()

    address = Address(city="Kyiv", street_name="Khreschatyk", country="Ukraine", user_id=user.id)
    db_session.add(address)
    db_session.commit()

    response = client.get("/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == "john@example.com"
    assert data[0]["address"]["city"] == "Kyiv"
    assert data[0]["credit_card"] is None
