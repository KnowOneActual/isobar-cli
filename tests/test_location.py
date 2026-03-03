from isobar_cli.location import get_auto_location


def test_get_auto_location_success(requests_mock):
    mock_response = {
        "success": True,
        "city": "Chicago",
        "region": "Illinois",
        "country": "United States",
    }
    requests_mock.get("https://ipwho.is/", json=mock_response)

    city = get_auto_location()
    assert city == "Chicago"


def test_get_auto_location_fail(requests_mock):
    requests_mock.get("https://ipwho.is/", json={"success": False})

    city = get_auto_location()
    assert city is None


def test_get_auto_location_timeout(requests_mock):
    requests_mock.get("https://ipwho.is/", exc=Exception("Timeout"))

    city = get_auto_location()
    assert city is None
