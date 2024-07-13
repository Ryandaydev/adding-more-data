"""Testing the sdk"""
import pytest
from swcpy.swc_client import SWCClient

client = SWCClient(swc_base_url="http://0.0.0.0:8000")

def test_health_check():
    """Tests health check from SDK"""
    response = client.get_health_check()
    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}