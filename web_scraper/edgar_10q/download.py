def download_files_10Q(ticker, start_date, dest_dir):
    '''
    Downlaods the ticker's raw 10-k files from SEC to destination folder.
    '''
    from pathlib import Path
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    def element_exists(by, value):
        from selenium.common.exceptions import NoSuchElementException 
        try:
            driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False 
            
    driver = webdriver.Chrome(service=Service(executable_path="/Users/acasariego/miniconda3/bin/chromedriver"))
    driver.maximize_window
    driver.get("https://www.sec.gov/edgar/searchedgar/companysearch.html")
    wait = WebDriverWait(driver, 10)

    # Search ticker
    actions = ActionChains(driver)
    input= driver.find_element("id", "edgar-company-person")  
    actions.move_to_element(input).click().send_keys(ticker, Keys.ENTER).perform()

    # Select 10-Q & 10-K buttons
    wait.until(EC.element_to_be_clickable(("xpath", r'//*[@id="filingsStart"]/div[2]/div[3]/h5'))
                                    ).click()

    wait.until(EC.element_to_be_clickable(("xpath", r'//*[@id="filingsStart"]/div[2]/div[3]/div/button[1]'))
                                    ).click()

    # Specify 10-Q and start_date in searchbox 
    driver.find_element("id", "searchbox").send_keys("10-Q")
    driver.find_element("id", "filingDateFrom").clear()
    time.sleep(2)
    actions = ActionChains(driver)
    input = wait.until(EC.element_to_be_clickable((By.ID, "filingDateFrom")))
    actions.move_to_element(input).click().send_keys(start_date, Keys.ENTER).perform()

    # Download forms
    raw_dir = dest_dir / f"{ticker}" / "raw_html"
    raw_dir.mkdir(exist_ok=True)

    i = 1
    form_count = len(driver.find_element("id", "filingsTable").find_elements(By.TAG_NAME, "tr"))
    while i < form_count:
        file_type = driver.find_element(By.XPATH, f'//*[@id="filingsTable"]/tbody/tr[{i}]/td[1]')
        date = driver.find_element(By.XPATH, f'//*[@id="filingsTable"]/tbody/tr[{i}]/td[3]').text
        if file_type.text == '10-Q':
            form = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="filingsTable"]/tbody/tr[{i}]/td[2]/div/a[1]'))) 
            form = driver.execute_script("arguments[0].click();", form)
            wait.until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[1])

            # If menu ribbon appears - select open as html
            if element_exists(By.ID, "ixvFrame"):
                driver.switch_to.frame(driver.find_element(By.ID, "ixvFrame"))
                wait.until(EC.element_to_be_clickable((By.ID, "menu-dropdown-link"))).click()
                wait.until(EC.element_to_be_clickable((By.ID, "form-information-html"))).click()

                # Save file 
                wait.until(EC.number_of_windows_to_be(3))
                driver.switch_to.window(driver.window_handles[2])
                time.sleep(1)
                with open(f"{raw_dir}/{ticker}_10-q_filing_{date}.html", "w", encoding='utf-8') as f:
                    f.write(driver.page_source)
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            # If table has html link with '.txt'
            elif element_exists(By.ID, "formHeader"):
                q10_table = driver.find_element(By.XPATH, """//*[@id="formDiv"]/div/table/tbody""")
                for row in q10_table.find_elements(By.CSS_SELECTOR,"tr"):
                    for cell in row.find_elements(By.TAG_NAME, "td"):
                        if '.txt' in cell.text:
                            link = cell.find_element(By.TAG_NAME, "a")
                            wait.until(EC.element_to_be_clickable(link)).click()
                            time.sleep(1)
                            
                            # Save file 
                            with open(f"{raw_dir}/{ticker}_10-q_filing_{date}.html", "w", encoding='utf-8') as f:
                                f.write(driver.page_source)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            break

            # Save file
            else:
                time.sleep(1)
                with open(f"{raw_dir}/{ticker}_10-q_filing_{date}.html", "w", encoding='utf-8') as f:
                    f.write(driver.page_source)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        i += 1