from isobar_cli.location import get_auto_location


def test_get_auto_location_success(requests_mock):
    mock_response = {
        "status": "success",
        "city": "Chicago",
        "regionName": "Illinois",
        "country": "United States",
    }
    requests_mock.get("http://ip-api.com/json/", json=mock_response)

    city = get_auto_location()
    assert city == "Chicago"


def test_get_auto_location_fail(requests_mock):
    requests_mock.get("http://ip-api.com/json/", json={"status": "fail"})

    city = get_auto_location()
    assert city is None


def test_get_auto_location_timeout(requests_mock):
    requests_mock.get("http://ip-api.com/json/", exc=Exception("Timeout"))

    city = get_auto_location()
    assert city is None
