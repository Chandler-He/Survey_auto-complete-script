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
        driver.get('https://pitt.co1.qualtrics.com/jfe/form/SV_8k5RaMpakDSkeOO')
        print("Survey page loaded.")
        time.sleep(3)  # Wait for the page to load

        while True:  # Loop to handle multiple pages in the survey
            # Wait for all questions to load
            questions = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.QuestionOuter'))
            )
            print(f"Found {len(questions)} questions on the current page.")

            # Loop through each question and answer it
            for i, question in enumerate(questions, start=1):
                try:
                    # Find radio button or checkbox options within each question
                    options = question.find_elements(By.CSS_SELECTOR, 'input[type="radio"], input[type="checkbox"]')

                    if options:
                        if len(options) > 1:  # Handle multi-select questions
                            num_choices = random.randint(1, len(options))
                            selected_options = random.sample(options, num_choices)
                            for selected_option in selected_options:
                                label = question.find_element(By.CSS_SELECTOR, f'label[for="{selected_option.get_attribute("id")}"]')
                                driver.execute_script("arguments[0].click();", label)
                                print(f"Answered question {i} by clicking label for multi-select option: {selected_option.get_attribute('value')}")
                        else:  # Handle single-choice questions
                            selected_option = random.choice(options)
                            label = question.find_element(By.CSS_SELECTOR, f'label[for="{selected_option.get_attribute("id")}"]')
                            driver.execute_script("arguments[0].click();", label)
                            print(f"Answered question {i} by clicking label for option: {selected_option.get_attribute('value')}")
                    else:
                        print(f"No options found for question {i}. Skipping.")
                except Exception as question_exception:
                    print(f"Error answering question {i}: {question_exception}")

            # Ensure all questions have been answered before proceeding
            unanswered_questions = [q for q in questions if not q.find_elements(By.CSS_SELECTOR, 'input:checked')]
            if unanswered_questions:
                print(f"Unanswered questions found: {len(unanswered_questions)}. Retrying.")
                continue  # Retry the page if any questions are still unanswered

            # Wait for the "Next" or "Submit" button
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, 'NextButton'))
                )
                next_button.click()
                print("Clicked 'Next' to proceed to the next page.")
                time.sleep(3)  # Allow next page to load
            except Exception as e:
                print(f"No 'Next' button found, assuming this is the last page: {e}")
                try:
                    # Attempt to find and click "Submit" button if it's the last page
                    submit_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Submit") or contains(text(),"submit")]'))
                    )
                    submit_button.click()
                    print("Survey submitted successfully.")
                except Exception as submit_exception:
                    print(f"Failed to submit survey: {submit_exception}")
                break  # Exit the loop if "Next" and "Submit" buttons are not found

    except Exception as e:
        print(f"An error occurred during the survey process: {e}")

# Repeat the survey filling process for the desired number of iterations
for _ in range(130):
    fill_survey()

# Close the browser after all submissions
driver.quit()
