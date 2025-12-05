import allure
import pytest
import requests
from pydantic import ValidationError
from core.models.booking import BookingResponse



@allure.feature('Test Booking')
@allure.story('Positive: creating booking with random data')
def test_create_booking_with_custom_data(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    with allure.step("Check create response"):
        response = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValidationError(f"Response validation failed: {e}")

    with allure.step("Check fields"):
        booking = response["booking"]
        assert booking["firstname"] == booking_data["firstname"]
        assert booking["lastname"] == booking_data["lastname"]
        assert booking["totalprice"] == booking_data["totalprice"]
        assert booking["depositpaid"] == booking_data["depositpaid"]
        assert booking["bookingdates"]['checkin'] == booking_data["bookingdates"]['checkin']
        assert booking["bookingdates"]['checkout'] == booking_data["bookingdates"]['checkout']
        assert booking["additionalneeds"] == booking_data["additionalneeds"]


@allure.feature('Test Booking')
@allure.story('Negative: missing required field - firstname')
def test_create_booking_missing_required_field(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    del booking_data["firstname"]

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.create_booking(booking_data)

    status_code = exc_info.value.response.status_code
    assert status_code in [400, 500], f"Expected 400 or 500, got {status_code}"


@allure.feature('Test Booking') # БАГ ПРИХОДИТ 200 КОД
@allure.story('Negative: invalid field type — totalprice')
def test_create_booking_totalprice(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data.copy()
    booking_data["totalprice"] = "The one"

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.create_booking(booking_data)

    status_code = exc_info.value.response.status_code
    assert status_code in [400, 500], f"Expected 400 or 500, got {status_code}"


@allure.feature('Test Booking') # БАГ ПРИХОДИТ 200 КОД
@allure.story('Negative: empty firstname')
def test_create_booking_empty_firstname(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data.copy()
    booking_data["firstname"] = ""

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.create_booking(booking_data)

    status_code = exc_info.value.response.status_code
    assert status_code in [400, 500], f"Expected 400 or 500, got {status_code}"


@allure.feature('Test Booking')
@allure.story('Negative: invalid JSON')
def test_create_booking_invalid_json(api_client):
    invalid_json = '''{
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 100,
        "depositpaid": true,
        "bookingdates": {
            "checkin": "2025-12-01",
            "checkout": "2025-12-05"
        },
        "additionalneeds": "Breakfast",
    }'''

    response = requests.post(url=f"{api_client.base_url}/booking", data=invalid_json)

    assert response.status_code in [400, 500], f"Expected status 400 or 500 but got {response.status_code}"


@allure.feature('Test Booking')
@allure.story('Negative: create booking with invalid headers')
def test_create_booking_invalid_headers(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    response = requests.post(url=f"{api_client.base_url}/booking", json=booking_data, headers={"Content-Type": "application/xml"})

    assert response.status_code in [400, 500], f"Expected status 400 or 500 but got {response.status_code}"