import pytest
from datetime import datetime
from app.scheduler.checkpoint import get_or_create_state, advance_checkpoint, mark_generation_failed

@pytest.mark.asyncio
async def test_checkpoint_state_persistence(db_session):
    state = await get_or_create_state(db_session)
    assert state.id == 1
    assert state.is_running is False

    # Simulate success
    now = datetime.utcnow()
    await advance_checkpoint(db_session, now)
    state = await get_or_create_state(db_session)
    assert state.last_successful_cutoff == now
    assert state.last_status == "SUCCESS"

    # Simulate failure - cutoff must NOT advance
    await mark_generation_failed(db_session, "Temporary network timeout")
    state = await get_or_create_state(db_session)
    assert state.last_successful_cutoff == now  # Preserved!
    assert "FAILED" in state.last_status
    assert state.retry_count == 1
