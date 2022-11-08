import os

import pytest
import selenium.webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


class TestTaxdooBooking:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        options = selenium.webdriver.ChromeOptions()
        self.driver = selenium.webdriver.Chrome(
            service=Service("/Users/palla/Downloads/chromedriver.exe"), options=options
        )
        self.wait = WebDriverWait(self.driver, 20)
        yield
        self.driver.close()

    def test_booking_process(self):
        # Data Setup
        company_name = "Pallabi Test"
        username = "Pallabi Goswami"
        first, last = username.split()
        addr = "Valentinskamp 70, Hamburg, Germany"
        vat_id = "DE123456789"
        email = "pallabi.abc@kmail.com"
        telephone = "+4901231234567"

        # Get url
        self.driver.get("https://booking.test.env.taxdoo.com/")
        self.driver.maximize_window()

        # Reject cookies
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Reject All']"))).click()

        # Start Booking Process
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()=' 10.000 €']"))).click()
        self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='49 €']/following-sibling::div[text()='Choose']"))
            ).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Next']"))).click()

        #Add details
        add_company = self.wait.until(EC.visibility_of_element_located((By.NAME, "company")))
        add_company.send_keys(company_name)
        self.wait.until(EC.element_to_be_clickable((By.NAME, "salutation"))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//option[text()='Mrs']"))).click()
        first_name = self.wait.until(EC.element_to_be_clickable((By.NAME, "name")))
        first_name.send_keys(first)
        last_name = self.wait.until(EC.element_to_be_clickable((By.NAME, "surname")))
        last_name.send_keys(last)
        address = self.wait.until(EC.element_to_be_clickable((By.NAME, "address")))
        address.send_keys(addr)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[role='option']"))).click()
        vat = self.wait.until(EC.element_to_be_clickable((By.NAME, "vatNo")))
        vat.send_keys(vat_id)
        time.sleep(3)
        email_no = self.wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        email_no.send_keys(email)
        tel_no = self.wait.until(EC.element_to_be_clickable((By.NAME, "tel")))
        tel_no.send_keys(telephone)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Next']"))).click()

        # Next page for Booking Submission
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "label[for='accept']"))).click()
        self.driver.switch_to.window(self.driver.window_handles[0])
        checkmark = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div._circle_ovjji_62")))
        action = ActionChains(self.driver)
        action.move_to_element(checkmark)
        action.click().perform()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "// *[text() = 'Complete booking']"))).click()

        # Asserting that booking is successful
        assert self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Booking successful']")))
