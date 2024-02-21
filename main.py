import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    user_data_dir = r'C:\Users\Allen\AppData\Local\Google\Chrome\User Data'
    profile_directory = 'Allen'
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"profile-directory={profile_directory}")
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)


def navigate_and_input_text(driver, url, input_text):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    textarea = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.lg\:w-\[88\%\]:nth-child(3) > textarea:nth-child(3)")))
    textarea.send_keys(input_text)
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#text-scan-desktop")))
    button.click()


def extract_data(driver, css_selector):
    extracted_data = {}
    index = 1
    while True:
        try:
            element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector.format(index))))
            impact = float(element.find_element(By.CSS_SELECTOR, "span:nth-child(3)").text)
            if impact != 0.00:
                extracted_data[element.find_element(By.CSS_SELECTOR, "div:nth-child(2) > p:nth-child(1)").text] = impact
            index += 1
        except selenium.common.exceptions.TimeoutException:
            break
    return extracted_data


def update_json(file_path, new_data):

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    data.update(new_data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)




if __name__ == "__main__":
    driver = initialize_driver()
    ai_new_data = {}
    hm_new_data = {}

    with open("json/input_text.json", 'r', encoding='utf-8') as file:
        newinputdata = json.load(file)

    for  newdate in newinputdata:
        print(newdate)
        navigate_and_input_text(driver, 'https://app.gptzero.me/app/welcome?tab=0&writing-feedback=false&inside-view=true',
                            newdate)

        ai_data = extract_data(driver, "ul.w-1\/2:nth-child(1) > div:nth-child({})")
        hm_data = extract_data(driver, "ul.w-1\/2:nth-child(2) > div:nth-child({})")

        ai_new_data.update(ai_data)
        hm_new_data.update(hm_data)





    update_json("json/ai_impact.json", ai_new_data)
    update_json("json/hm_impact.json", hm_new_data)

    print(ai_data)
    print(hm_data)

    input("Press Enter to quit...")
    driver.quit()
