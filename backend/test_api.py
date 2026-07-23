from fastapi.testclient import TestClient
import os
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

from backend.main import app
from backend.services.evaluation_service import EvaluationService
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
        
    test_dir = os.path.join(os.path.dirname(__file__), "..", "test")
    pdf_files = [f for f in os.listdir(test_dir) if f.endswith(".pdf")]
    if not pdf_files:
        pytest.skip("No PDF files found in the test directory.")
    
    file_path = os.path.join(test_dir, pdf_files[0])
    assert os.path.exists(file_path), f"Test document not found at {file_path}"
    
    jwt_token = os.environ.get("JWT_TOKEN")
    if not jwt_token:
        pytest.skip("JWT_TOKEN environment variable is not set. Skipping test.")
        
    with open(file_path, "rb") as f:
        response = client.post(
            "/api/v1/extract-rules",
            headers={"Authorization": f"Bearer {jwt_token}"},
            files={"document": ("document.pdf", f, "application/pdf")}
        )
    
    if response.status_code != 200:
        print(f"Error from server: {response.text}")
    assert response.status_code == 200
    
    data = response.json()
    assert "rules" in data
    assert isinstance(data["rules"], list)
    
    extracted_rules = data["rules"]
    print(f"Extracted {len(extracted_rules)} rules successfully.")
    for rule in extracted_rules:
        assert "title" in rule
        assert "description" in rule
        assert "id" in rule

    # 1. Save extracted rules to /output/rules.json
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    rules_output_path = os.path.join(output_dir, "rules.json")
    
    with open(rules_output_path, "w", encoding="utf-8") as f:
        json.dump(extracted_rules, f, ensure_ascii=False, indent=4)
        
    # 2. Evaluate using Levenshtein distance
    eval_service = EvaluationService()
    resources_dir = os.path.join(os.path.dirname(__file__), "resources")
    os.makedirs(resources_dir, exist_ok=True)
    correct_rules_path = os.path.join(resources_dir, "rules.json")
    
    # Create empty rules.json if it doesn't exist
    if not os.path.exists(correct_rules_path):
        with open(correct_rules_path, "w", encoding="utf-8") as f:
            json.dump([], f)

    results_output_path = os.path.join(output_dir, "results.json")
    
    eval_result = eval_service.evaluate_and_save(
        extracted_rules=extracted_rules,
        correct_rules_path=correct_rules_path,
        output_path=results_output_path
    )
    
    print(f"Evaluation Complete! Semantic Similarity: {eval_result['percentual_similaridade_semantica']}%")
