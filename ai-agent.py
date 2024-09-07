from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# Define your WebDriver path and initialize it using Service
driver_path = 'chromedriver-mac-arm64/chromedriver'  # Replace with your actual path to ChromeDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Function to randomly fill the survey
def fill_survey():
    try:
        # Open the survey link
        driver.get('your_survey_url')
        print("Survey page loaded.")
        time.sleep(3)  # Wait for the page to load

        # Find all question containers
        questions = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.QuestionOuter'))
        )
        print(f"Found {len(questions)} questions on the page.")

        for i, question in enumerate(questions, start=1):
            try:
                # Find radio button or checkbox options within each question
                options = question.find_elements(By.CSS_SELECTOR, 'input[type="radio"], input[type="checkbox"]')
                
                if options:
                    if i in range(10, 13):  # For questions 10 to 12 (multi-select questions)
                        num_choices = random.randint(1, len(options))  # Randomly select 1 to all options
                        selected_options = random.sample(options, num_choices)  # Randomly select multiple options
                        for selected_option in selected_options:
                            label = question.find_element(By.CSS_SELECTOR, f'label[for="{selected_option.get_attribute("id")}"]')
                            driver.execute_script("arguments[0].click();", label)
                            print(f"Answered question {i} by clicking label for multi-select option: {selected_option.get_attribute('value')}")
                    else:
                        # Single choice question handling
                        selected_option = random.choice(options)
                        label = question.find_element(By.CSS_SELECTOR, f'label[for="{selected_option.get_attribute("id")}"]')
                        driver.execute_script("arguments[0].click();", label)
                        print(f"Answered question {i} by clicking label for option: {selected_option.get_attribute('value')}")
                
                else:
                    print(f"No options found for question {i}.")
            except Exception as question_exception:
                print(f"Error answering question {i}: {question_exception}")

        # Retry mechanism to find and click the "Next" button using its ID
        button_clicked = False
        for attempt in range(3):  # Retry up to 3 times
            try:
                # Try to click the "Next" button using its unique ID
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, 'NextButton'))
                )
                next_button.click()
                print("Clicked 'Next' to proceed to the next page.")
                button_clicked = True
                break  # Exit loop if button click is successful
            except Exception as next_exception:
                print(f"Attempt {attempt + 1}: No 'Next' button found or could not be clicked: {next_exception}")

            try:
                # Try to click "Submit" button if it's the last page (adjust this if there's a unique ID for Submit)
                submit_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Submit") or contains(text(),"submit")]'))
                )
                submit_button.click()
                print("Survey submitted successfully.")
                button_clicked = True
                break  # Exit loop if button click is successful
            except Exception as submit_exception:
                print(f"Attempt {attempt + 1}: Submit button not found or could not be clicked: {submit_exception}")

            time.sleep(2)  # Wait briefly before retrying

        if not button_clicked:
            print("Failed to find and click either 'Next' or 'Submit' button after multiple attempts.")

        # Wait before closing to ensure submission is completed
        time.sleep(2)

    except Exception as e:
        print(f"An error occurred during the survey process: {e}")

# Repeat the survey filling process for the desired number of iterations
for _ in range(50):
    fill_survey()

# Close the browser after all submissions
driver.quit()
