import allure
import pytest
import requests



@allure.feature('Test Booking')
@allure.story('Test create new booking')
def test_create_booking(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    with allure.step("Check create response"):
        response = api_client.create_booking(booking_data)

    with allure.step("Check fields"):
        booking = response["booking"]
        assert booking["firstname"] == booking_data["firstname"]
        assert booking["lastname"] == booking_data["lastname"]
        assert booking["totalprice"] == booking_data["totalprice"]
        assert booking["depositpaid"] == booking_data["depositpaid"]
        assert booking["bookingdates"] == booking_data["bookingdates"]
        assert booking["additionalneeds"] == booking_data["additionalneeds"]


