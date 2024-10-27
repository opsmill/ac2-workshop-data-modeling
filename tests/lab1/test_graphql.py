from fastapi.testclient import TestClient

QUERY_DEVICES = """
query {
    devices {
        name
        site {
            name
        }
    }
}
"""


def test_read_main(client: TestClient, device_data):
    response = client.post("/graphql", json={"query": QUERY_DEVICES})

    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "devices": [
                {
                    "name": "device1",
                    "site": {
                        "name": "atl1",
                    },
                },
                {
                    "name": "device2",
                    "site": {
                        "name": "den1",
                    },
                },
            ],
        },
    }
