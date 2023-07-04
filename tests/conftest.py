import pytest
import json
import sys
import os


sys.path.append(f"{os.path.dirname(__file__)}/../src")


class MockData:
    mock_data: dict = {}
    base: str = "tests/unit_tests/mock_data/"

    @classmethod
    def get_mock_data(cls) -> dict:
        files = next(os.walk(cls.base))[2]
        files = list(filter(lambda filename: filename.endswith(".json"), files))
        files = list(map(lambda filename: filename[:-5], files))
        return {path: json.load(open(f"{cls.base}{path}.json")) for path in files}
    
    @classmethod
    def set_mock_data(cls) -> None:
        cls.mock_data = cls.get_mock_data()
    

@pytest.fixture
def mock_data(request):
    if not MockData.mock_data:
        MockData.set_mock_data()
    return MockData.mock_data