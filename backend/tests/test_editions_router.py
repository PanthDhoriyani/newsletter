import pytest

@pytest.mark.asyncio
async def test_health_check(client):
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_editions_list_empty(client):
    res = await client.get("/api/editions/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

@pytest.mark.asyncio
async def test_dashboard_endpoint(client):
    res = await client.get("/api/dashboard/")
    assert res.status_code == 200
    data = res.json()
    assert "breaking_news" in data
    assert "top_stories" in data
    assert "reading_progress" in data
