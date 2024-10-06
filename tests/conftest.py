import pytest
from unittest.mock import AsyncMock



@pytest.fixture
def mock_db_session(mocker):
    mock_session = AsyncMock()

    mock_context_manager = mocker.patch('warehous_manager.db.db.db_session',
                                        return_value=AsyncMock()
                                        )
    mock_context_manager.__aenter__.return_value = mock_session
    mock_context_manager.__aexit__.return_value = AsyncMock()

    return mock_session

