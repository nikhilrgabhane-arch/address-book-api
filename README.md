# Address Book API

A production-ready address book REST API built with Python 3, FastAPI, and SQLAlchemy.

## Features
- **Validation**: Strict boundary checks for geographical coordinates via Pydantic.
- **Geocoding**: Distance searches via Geopy (Vincenty geodesic algorithm).
- **Architecture**: Modular layout with Dependency Injection.
- **Logging**: Dedicated standard logging structure.

---

## Quick Start (Local Setup)

1. **Clone the repository** (if applicable) and switch to the project root:
   ```bash
   cd Project
   ```

2. **Create a virtual environment & Install Dependencies**:
   ```bash
   python -m venv .venv
   
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Run the API**:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Explore the Docs & Test the API**:
   Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) in your browser. This built-in Swagger UI allows you to interact with the API directly.

---

## 🎯 Testing Examples (Swagger UI / cURL)

To verify the distance functionality, you can use these examples in the Swagger UI (`/docs`):

**Step 1: Create an Address**
*(POST `/addresses/`)*
```json
{
  "name": "Cubbon Park",
  "street": "Kasturba Road",
  "city": "Bengaluru",
  "state": "Karnataka",
  "country": "India",
  "latitude": 12.9779,
  "longitude": 77.5952
}
```

**Step 2: Search Nearby Addresses**
*(GET `/addresses/nearby`)*
Input the following query parameters to find the address you just created:
- `latitude`: `12.9716`
- `longitude`: `77.5946`
- `distance_km`: `5`

---

##  Running Tests

Ensure your virtual environment is activated, then run:

```bash
pytest tests/
```

This will run the integration test suite validating REST endpoints, edge case calculations, and error handling.
