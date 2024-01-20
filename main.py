from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import ElementClickInterceptedException


TARGET_ACCOUNT = "paperbee.giftshop"
USERNAME = "gifteryland"
PASSWORD = "Doblo5052-5252"


class InstaFollower:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=self.chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com/")
        time.sleep(2)
        username = self.driver.find_element(By.NAME, "username")
        username.send_keys(USERNAME)
        time.sleep(2)
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(PASSWORD, Keys.ENTER)
        time.sleep(7)

        # Click "Not now" and ignore Save-login info prompt
        save_login_prompt = self.driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Şimdi değil')]")
        if save_login_prompt:
            save_login_prompt.click()
        time.sleep(2)

        # Click "not now" on notifications prompt
        notifications_prompt = self.driver.find_element(by=By.XPATH, value="// button[contains(text(), 'Şimdi Değil')]")
        if notifications_prompt:
            notifications_prompt.click()

    def find_followers(self):
        # Show followers of the selected account.
        self.driver.get(f"https://www.instagram.com/{TARGET_ACCOUNT}/followers")
        time.sleep(7)

        # The xpath  of the modal that shows the followers will change over time. Update yours accordingly.
        modal_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]"
        modal = self.driver.find_element(by=By.XPATH, value=modal_xpath)
        for i in range(15):
            # In this case we're executing some Javascript, that's what the execute_script() method does.
            # The method can accept the script as well as an HTML element.
            # The modal in this case, becomes the arguments[0] in the script.
            # Then we're using Javascript to say: "scroll the top of the modal (popup) element by the height of the modal (popup)"
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def follow(self):
        # Check and update the (CSS) Selector for the "Follow" buttons as required.
        all_buttons = self.driver.find_elements(By.CSS_SELECTOR, value='._aano button')

        for button in all_buttons:
            try:
                button.click()
                time.sleep(1.1)
            # Clicking button for someone who is already being followed will trigger dialog to Unfollow/Cancel
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'İptal')]")
                cancel_button.click()





operation = InstaFollower()
operation.login()
time.sleep(3)
operation.find_followers()
operation.follow()