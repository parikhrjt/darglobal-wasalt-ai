"""
End-to-End Application Health & Verification Suite
"""

import sys
import httpx
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_endpoints():
    print("Testing GET /health...")
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health_data = res.json()
    print("Health Data:", health_data)
    assert health_data["status"] == "healthy"
    assert health_data["properties_indexed"] > 0

    print("\nTesting GET / (Frontend Single Page App)...")
    res = client.get("/")
    assert res.status_code == 200
    assert "DarGlobal" in res.text or "DAR" in res.text
    print("Frontend successfully served!")

    print("\nTesting GET /api/properties...")
    res = client.get("/api/properties?limit=5")
    assert res.status_code == 200
    props = res.json()
    print(f"Retrieved {props['count']} properties.")
    assert props["count"] > 0

    print("\nTesting POST /api/chat (Property Discovery)...")
    chat_res = client.post("/api/chat", json={
        "message": "Show me luxury developments in Dubai with Pagani and Trump"
    })
    assert chat_res.status_code == 200, f"Chat failed: {chat_res.text}"
    data = chat_res.json()
    print(f"Chat Response Engine: {data['engine']}")
    print(f"Property cards attached: {len(data['cards'])}")
    print(f"Tools executed: {[t.get('tool') for t in data['tools_executed']]}")
    assert len(data["cards"]) > 0

    print("\nTesting POST /api/chat (Financial Mortgage & ROI Model)...")
    mortgage_res = client.post("/api/chat", json={
        "message": "Calculate mortgage for $3,000,000 property with 8% ROI"
    })
    assert mortgage_res.status_code == 200
    m_data = mortgage_res.json()
    print("Mortgage Analysis Tools:", [t.get('tool') for t in m_data['tools_executed']])
    assert any(t.get('tool') == 'calculate_mortgage_and_roi' for t in m_data['tools_executed'])

    print("\nTesting POST /api/consultation (Lead Capture)...")
    lead_res = client.post("/api/consultation", json={
        "client_name": "Hamad Al-Subaie",
        "email": "hamad@investor.sa",
        "phone": "+966505554321",
        "property_name": "Da Vinci Tower by Pagani",
        "notes": "Interested in penthouse collection."
    })
    assert lead_res.status_code == 200
    lead_data = lead_res.json()
    print("Booking confirmed:", lead_data["booking"]["booking_reference"])

    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY! 🚀")

if __name__ == "__main__":
    test_endpoints()
