import os

import pytest
import selenium.webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

CANDIDATE_DETAILS = {
    "first_name": "Pallabi",
    "last_name": "Goswami",
    "email": "pallabi.goswami@gmail.com",
    "phone": "+4901707391617",
    "resume": "PallabiGoswamiResume-v1.pdf",
    "github": "https://github.com/pallabig4787/staffbase_assignment",
}


class TestStaffBaseApplication:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        options = selenium.webdriver.ChromeOptions()
        self.driver = selenium.webdriver.Chrome(service=Service("/Users/palla/Downloads/chromedriver.exe"), options=options)

        self.wait = WebDriverWait(self.driver, 20)
        yield
        self.driver.close()

    def test_qa_engineer_application(self):
        # Apply for QA Engineer Position
        self.driver.get("https://staffbase.com/jobs/quality-assurance-engineer-2021_1730")
        self.driver.maximize_window()

        # Reject cookies
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-reject-all-handler"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Apply']"))).click()
        self.wait.until(EC.url_contains("apply"))
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[id='grnhse_iframe'][title='Greenhouse Job Board']")
            )
        )
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#application_form")))

        # Enter required information in the application form
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#first_name"))).send_keys(
            CANDIDATE_DETAILS["first_name"])
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#last_name"))).send_keys(
            CANDIDATE_DETAILS["last_name"])
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#email"))).send_keys(
            CANDIDATE_DETAILS["email"])
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#phone"))).send_keys(
            CANDIDATE_DETAILS["phone"])
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form[id='s3_upload_for_resume'] input[type='file']"))
        ).send_keys("C:/Users/palla/PycharmProjects/Meisterwerk/Staffbase/PallabiGoswamiResume-v1.pdf")
        assert self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#resume_filename"), CANDIDATE_DETAILS["resume"]))

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class = 'select2-chosen']"))).click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#select2-result-label-3"))).click()

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#job_application_answers_attributes_2_text_value"))
        ).send_keys(CANDIDATE_DETAILS["github"])

        # Submit application
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit_app"))).click()

        # asserting the application
        assert self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Thank you for applying.']")))
