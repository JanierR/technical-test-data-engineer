import pytest
import requests
from unittest.mock import patch, MagicMock
import os
import csv
from data_pipeline import fetch_data, save_to_csv

# Mock de datos para los tests
MOCK_TRACKS_DATA = {
    "items": [
        {"id": 1, "name": "Song A", "artist": "Artist A"},
        {"id": 2, "name": "Song B", "artist": "Artist B"}
    ]
}

MOCK_USERS_DATA = {
    "items": [
        {"id": 1, "username": "User1"},
        {"id": 2, "username": "User2"}
    ]
}

MOCK_LISTEN_HISTORY_DATA = {
    "items": [
        {"user_id": 1, "track_id": 1, "timestamp": "2025-01-21T10:00:00Z"},
        {"user_id": 2, "track_id": 2, "timestamp": "2025-01-21T11:00:00Z"}
    ]
}

OUTPUT_DIR = "output_data"

@pytest.fixture
def mock_requests_get():
    """
    Mock para requests.get que devuelve diferentes respuestas según el endpoint.
    """
    with patch("requests.get") as mock_get:
        def mock_response(url, *args, **kwargs):
            if "tracks" in url:
                return MagicMock(status_code=200, json=lambda: MOCK_TRACKS_DATA)
            elif "users" in url:
                return MagicMock(status_code=200, json=lambda: MOCK_USERS_DATA)
            elif "listen_history" in url:
                return MagicMock(status_code=200, json=lambda: MOCK_LISTEN_HISTORY_DATA)
            return MagicMock(status_code=404)
        mock_get.side_effect = mock_response
        yield mock_get

def test_fetch_data(mock_requests_get):
    """
    Test para verificar que fetch_data retorna los datos esperados.
    """
    tracks = fetch_data("http://127.0.0.1:8000/tracks")
    assert len(tracks) == 2
    assert tracks[0]["name"] == "Song A"

    users = fetch_data("http://127.0.0.1:8000/users")
    assert len(users) == 2
    assert users[1]["username"] == "User2"

    listen_history = fetch_data("http://127.0.0.1:8000/listen_history")
    assert len(listen_history) == 2
    assert listen_history[0]["user_id"] == 1

def test_save_to_csv():
    """
    Test para verificar que save_to_csv guarda correctamente los datos.
    """
    filepath = os.path.join(OUTPUT_DIR, "test_tracks.csv")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    save_to_csv(MOCK_TRACKS_DATA["items"], "test_tracks.csv")

    assert os.path.exists(filepath)

    # Leer y verificar contenido del archivo CSV
    with open(filepath, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["name"] == "Song A"
        assert rows[1]["artist"] == "Artist B"

    # Eliminar el archivo de prueba
    os.remove(filepath)
