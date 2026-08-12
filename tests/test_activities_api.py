import asyncio
from copy import deepcopy

import pytest
from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient

from src.app import app, activities

ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def reset_activities():
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))


def test_get_activities_returns_catalog(reset_activities):
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


@pytest.mark.asyncio
async def test_signup_rejects_duplicate_email_under_concurrency(reset_activities):
    # Arrange
    email = "new.student@mergington.edu"
    activity_name = "Chess Club"
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Act
        responses = await asyncio.gather(
            client.post(f"/activities/{activity_name}/signup", params={"email": email}),
            client.post(f"/activities/{activity_name}/signup", params={"email": email}),
        )

    # Assert
    assert sum(response.status_code == 200 for response in responses) == 1
    assert sum(response.status_code == 400 for response in responses) == 1
    assert activities[activity_name]["participants"].count(email) == 1
