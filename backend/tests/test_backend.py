import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import numpy as np
import sys

# Mock torch_directml if missing for tests
sys.modules['torch_directml'] = MagicMock()

from app.main import app

client = TestClient(app)

# Mock the entire HeartMuLaService pipeline to avoid loading 3B model during tests
@pytest.fixture
def mock_heartmula():
    with patch("app.engine.heartmula.HeartMuLaGenPipeline") as MockPipeline:
        # Check if pipeline called
        instance = MockPipeline.from_pretrained.return_value
        instance.return_value = None # pipeline() call returns nothing
        yield MockPipeline

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_generation_flow(mock_heartmula):
    # We mock the generate method of the SERVICE, or simpler:
    # mock the pipeline inside the service.
    
    # We also need to mock librosa.load since no file is actually created by the mock pipeline
    with patch("librosa.load") as mock_load:
        # Return 1 second of audio
        mock_load.return_value = (np.zeros(44100), 44100)
        
        payload = {
            "title": "Test Song",
            "bpm": 120,
            "genre": "Test",
            "structure": [{"type": "intro", "bars": 4}]
        }
        
        response = client.post("/api/v1/generate", json=payload)
        assert response.status_code == 200
        assert response.json()["status"] == "queued"
        
        # Note: Background tasks are not awaited by TestClient by default in this verification style
        # unless we explicitly run them. For API validity, this is enough.
