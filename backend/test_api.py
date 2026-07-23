from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

from backend.main import app
import pytest

client = TestClient(app)

def test_extract_rules_endpoint():
    """
    Tests the /extract-rules endpoint.
    Requires GOOGLE_API_KEY to be set in the environment.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        pytest.skip("GOOGLE_API_KEY environment variable is not set. Skipping real API test.")
        
    file_path = os.path.join(os.path.dirname(__file__), "..", "test", "20_resolucao_no_09.2024_-_consuni_0.pdf")
    assert os.path.exists(file_path), f"Test document not found at {file_path}"
    
    with open(file_path, "rb") as f:
        # We send the request just as the frontend would via FormData
        response = client.post(
            "/api/v1/extract-rules",
            files={"document": ("document.pdf", f, "application/pdf")}
        )
    
    # Assert successful response
    if response.status_code != 200:
        print(f"Error from server: {response.text}")
    assert response.status_code == 200
    
    # Assert structure of the response
    data = response.json()
    assert "rules" in data
    assert isinstance(data["rules"], list)
    
    print(f"Extracted {len(data['rules'])} rules successfully.")
    for rule in data["rules"]:
        assert "title" in rule
        assert "description" in rule
        assert "id" in rule
