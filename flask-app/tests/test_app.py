import pytest
from .. import flask_app

MOCK_ENCODING = "mock-encoding"

class MockEncodingResponse:
    def __init__(self):
        self.headers = {"Content-Encoding": MOCK_ENCODING}


def _mock_get(url):
    assert url == "https://www.quasicoherentlabs.com"
    return MockEncodingResponse()

'''overrides requests.get to mocked get function'''
@pytest.fixture
def mock_encoding_request(monkeypatch):
    monkeypatch.setattr("requests.get", _mock_get)


@pytest.fixture
def app():
    return flask_app.app


@pytest.fixture
def test_client(app):
    return app.test_client()


def test_hello(test_client):
    """
    GIVEN: A flask hello app
    WHEN: I GET the /hello route
    THEN: The response should be "Hello World!"
    """
    response = test_client.get("/hello")
    assert response.data.decode("utf-8") == "Hello World!"

def test_encoding_header(test_client, mock_encoding_request):
    """
    GIVEN: A flask hello app
           A mock request handler
    WHEN: I GET the /get_webpage route
    THEN: The response should be the expected Content-Encoding
    """
    response = test_client.get("/get_webpage")
    assert response.data.decode("utf-8") == MOCK_ENCODING
