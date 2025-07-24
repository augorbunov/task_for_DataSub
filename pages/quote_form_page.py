class QuoteFormPage:
    def __init__(self, page):
        self.page = page
        self.name_input = page.locator('#name')
        self.email_input = page.locator('#email')
        self.service_select = page.locator('#service')
        self.purpose_business_radio = page.locator('#purposeBusiness')
        self.purpose_personal_radio = page.locator('#purposePersonal')
        self.withdraw_cash_radio = page.locator('#withdrawCash')
        self.withdraw_card_radio = page.locator('#withdrawCard')
        self.withdraw_crypto_radio = page.locator('#withdrawCrypto')
        self.message_input = page.locator('#message')
        self.submit_button = page.locator('button.btn-dark')
        self.status_div = page.locator('#formStatus')

    def goto(self):
        self.page.goto("https://qatest.datasub.com/quote.html")

    def fill_name(self, name):
        self.name_input.fill(name)

    def fill_email(self, email):
        self.email_input.fill(email)

    def select_service(self, value):
        self.service_select.select_option(value)

    def select_purpose(self, purpose="business"):
        if purpose == "business":
            self.purpose_business_radio.check()
        else:
            self.purpose_personal_radio.check()

    def select_withdrawal(self, option="cash"):
        if option == "cash":
            self.withdraw_cash_radio.check()
        elif option == "card":
            self.withdraw_card_radio.check()
        else:
            self.withdraw_crypto_radio.check()

    def fill_message(self, message):
        self.message_input.fill(message)

    def submit(self):
        self.submit_button.click()

    def wait_for_status(self):
        self.status_div.wait_for(state='visible')

    def get_status_text(self):
        return self.status_div.inner_text()

    def get_name_class(self):
        return self.name_input.get_attribute('class')

    def get_message_class(self):
        return self.message_input.get_attribute('class') 