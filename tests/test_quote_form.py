import pytest
import allure
from pages.quote_form_page import QuoteFormPage

def test_form_submission_with_one_withdrawal_option_positive(page):
    form = QuoteFormPage(page)
    form.goto()
    form.fill_name("Test user")
    form.fill_email("test@mail.com")
    form.select_service('B Service')
    form.select_purpose("business")
    form.select_withdrawal("cash")
    form.fill_message("Test message")
    form.submit()
    form.wait_for_status()
    assert form.get_status_text() == "Форма отправлена."

@pytest.mark.parametrize("service_value", [
    "A Service",
    "B Service",
    "C Service",
    "D Service"
])
def test_form_submission_with_each_of_services_positive(page, service_value):
    form = QuoteFormPage(page)
    form.goto()
    form.fill_name("Test user")
    form.fill_email("test@mail.com")
    form.select_service(service_value)
    form.select_purpose("business")
    form.select_withdrawal("cash")
    form.fill_message("Test message")
    form.submit()
    form.wait_for_status()
    assert form.get_status_text() == "Форма отправлена."

def test_form_submission_with_one_symbol_name_negative(page):
    form = QuoteFormPage(page)
    form.goto()
    form.fill_name("A")
    input_class = form.get_name_class()
    assert 'is-invalid' in input_class

def test_form_submission_without_message_negative(page):
    form = QuoteFormPage(page)
    form.goto()
    form.fill_message("asdf")
    input_class = form.get_message_class()
    assert 'is-invalid' in input_class