from fastapi.testclient import TestClient


def test_read_main(client: TestClient, device_data):
    response = client.get("/api/devices")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "manufacturer": "Arista",
            "name": "device1",
            "status": "active",
        },
        {
            "id": 2,
            "manufacturer": "Nokia",
            "name": "device2",
            "status": "active",
        },
    ]
