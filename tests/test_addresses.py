import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Verify application boots correctly."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app_name": "Address Book API"}

def test_create_address():
    """Create a standard address."""
    payload = {
        "name": "Home",
        "street": "1600 Pennsylvania Avenue NW",
        "city": "Washington",
        "state": "DC",
        "country": "USA",
        "latitude": 38.8977,
        "longitude": -77.0365
    }
    response = client.post("/addresses/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Home"
    assert "id" in data

def test_create_address_invalid_coordinates():
    """Verify Pydantic boundaries refuse invalid latitudes/longitudes."""
    payload = {
        "name": "Invalid Place",
        "street": "123 Error St",
        "city": "Nowhere",
        "state": "NW",
        "country": "USA",
        "latitude": 95.0,  # Invalid: > 90
        "longitude": -185.0  # Invalid: < -180
    }
    response = client.post("/addresses/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_get_nearby_addresses():
    """Verify the distance calculation and filtering."""
    # First, insert another point around 3.5km away
    payload = {
        "name": "Lincoln Memorial",
        "street": "2 Lincoln Memorial Cir NW",
        "city": "Washington",
        "state": "DC",
        "country": "USA",
        "latitude": 38.8893,
        "longitude": -77.0502
    }
    client.post("/addresses/", json=payload)

    # Note: distance from Whitehouse to Lincoln memorial is roughly 1.5 - 2km.
    
    # Query within 500km
    response = client.get("/addresses/nearby?latitude=38.8977&longitude=-77.0365&distance_km=500.0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # White House and Lincoln Memorial

    # Query within 0.1km
    response = client.get("/addresses/nearby?latitude=38.8977&longitude=-77.0365&distance_km=0.1")
    assert response.status_code == 200
    data = response.json()
    # Lincoln is ~1.5km away, so it shouldn't show up. Only WhiteHouse.
    assert len(data) == 1
    assert data[0]["name"] == "Home"
