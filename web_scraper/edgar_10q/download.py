from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DownloadFilings:

    def __init__(self, ticker, start_date, dest_dir, driver_path):
        self.ticker = ticker
        self.start_date = start_date
        self.dest_dir = dest_dir
        self.driver = webdriver.Chrome(service=Service(executable_path=driver_path))
        self.wait = WebDriverWait(self.driver, 10)
     
         
    def create_folders(self):
        dest_dir = Path(self.dest_dir)
        dir = dest_dir / "raw_html" / f"{self.ticker}"
        dir.mkdir(parents=True, exist_ok=True)
        return dir


    def element_exists(self, by, value):
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False 
    
    
    def get_main_html(self):
        driver =  self.driver.maximize_window
        driver.get("https://www.sec.gov/edgar/searchedgar/companysearch.html")
        # Validate success? 
    
    def get_ticker_html(self):
        actions = actionChains(self.driver)
        input= self.driver.find_element("id", "edgar-company-person")  
        actions.move_to_element(input).click().send_keys(self.ticker, Keys.ENTER).perform()
        # validate? 
        
    def select_10k_and_10q_buttons(self):
        xpath_10k_and_10q = r'//*[@id="filingsStart"]/div[2]/div[3]/h5'
        self.wait.until(EC.element_to_be_clickable(("xpath", xpath_10k_and_10q))).click()
        xpath_view_all_10k_and_10q =  r'//*[@id="filingsStart"]/div[2]/div[3]/div/button[1]'
        self.wait.until(EC.element_to_be_clickable(("xpath",xpath_view_all_10k_and_10q))).click()
    
    def fill_searchbox(self):
        self.driver.find_element("id", "searchbox").send_keys("10-Q")
        self.driver.find_element("id", "filingDateFrom").clear()
        time.sleep(2)
        actions = ActionChains(self.driver)
        input = self.wait.until(EC.element_to_be_clickable((By.ID, "filingDateFrom")))
        actions.move_to_element(input).click().send_keys(self.start_date, Keys.ENTER).perform()

    def click_form_link(self, i):
        xml_form_link = f'//*[@id="filingsTable"]/tbody/tr[{i}]/td[2]/div/a[1]'
        form = self.wait.until(EC.element_to_be_clickable((By.XPATH, xml_form_link))) 
        form = self.driver.execute_script("arguments[0].click();", form)
        self.wait.until(EC.number_of_windows_to_be(2))
        self.driver.switch_to.window(self.driver.window_handles[1])
    

    def get_ixvFrame_html(self):
        self.driver.switch_to.frame(self.driver.find_element(By.ID, "ixvFrame"))
        self.wait.until(EC.element_to_be_clickable((By.ID, "menu-dropdown-link"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "form-information-html"))).click()
        self.wait.until(EC.number_of_windows_to_be(3))
        time.sleep(1)

    def get_txt(self):
        q10_table = self.driver.find_element(By.XPATH, """//*[@id="formDiv"]/div/table/tbody""")
        for row in q10_table.find_elements(By.CSS_SELECTOR,"tr"):
            for cell in row.find_elements(By.TAG_NAME, "td"):
                if '.txt' in cell.text:
                    link = cell.find_element(By.TAG_NAME, "a")
                    self.wait.until(EC.element_to_be_clickable(link)).click()
                    time.sleep(1)
                    break


    def save_file_close_windows(self, form_type, filing_date):
        raw_dir = Path(self.dest_dir) / "raw_html" / f"{self.ticker}"
        raw_dir.mkdir(parents=True, exist_ok=True)  
        with open(f"{raw_dir}/{self.ticker}_{form_type}_filing_{filing_date}.html", "w", encoding='utf-8') as f:
                f.write(self.driver.page_source)
        
        while len(self.driver.window_handles) > 1:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
        
    
    def download_all(self):
        self.get_main_html()
        self.get_ticker_html()
        self.select_10k_and_10q_buttons()
        self.fill_searchbox()

        form_count = len(self.driver.find_element(By.ID, "filingsTable").find_elements(By.TAG_NAME, "tr"))
        for i in range(1, form_count + 1):
            form_type = self.driver.find_element(By.XPATH, f'//*[@id="filingsTable"]/tbody/tr[{i}]/td[1]')
            filing_date = self.driver.find_element(By.XPATH, f'//*[@id="filingsTable"]/tbody/tr[{i}]/td[3]').text

            if form_type.text == '10-Q':
                self.click_form_link(i)

                if self.element_exists(By.ID, "ixvFrame"):
                    self.get_ixvFrame_html(self)
                    self.save_file_close_windows(form_type, filing_date)

                elif self.element_exists(By.ID, "formHeader"):
                    self.get_txt(self)
                    self.save_file_close_windows(form_type, filing_date)

                else: 
                    self.element_exists(By.ID, "formHeader")
                    self.save_file_close_windows(form_type, filing_date)
      


# Next steps
    # Add error handling  
    # Add logging 