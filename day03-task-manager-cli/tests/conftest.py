"""
Pytest configuration and fixtures
"""

import pytest


@pytest.fixture
def sample_data():
    """Sample test data"""
    return {
        'test_item_1': 'value1',
        'test_item_2': 'value2',
        'test_list': [1, 2, 3, 4, 5]
    }


@pytest.fixture
def temp_file(tmp_path):
    """Create temporary file for testing"""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    return file_path


# Add more fixtures as needed for specific tests
