from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains


def display_author_info(driver):
    """
    Function to display author information using an alert popup.
    """
    author_info = """
    作者：zy
    联系邮箱：zy1280@163.com  
    项目网址：zy66.online
    仅作为学习参考使用，禁止用于破坏公平性活动，如若侵权请及时联系删除
    """
    script = f"""
    alert(`{author_info}`);
    """
    driver.execute_script(script)

    # 等待用户手动关闭弹出框
    while True:
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text  # 读取弹出框的文本，确保弹出框仍然存在
            time.sleep(0.5)  # 稍微等待，避免无限循环占用CPU资源
        except:
            break  # 如果没有弹出框，跳出循环，继续执行后续代码


def read_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        config = {}
        for line in lines:
            key, value = line.strip().split('=')
            config[key.strip()] = value.strip()
        return config

def scroll_element(driver, element_xpath, distance):
    """
    Function to scroll a specified element horizontally by a certain distance.
    """
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        driver.execute_script("arguments[0].scrollIntoView();", element)
        actions = ActionChains(driver)
        actions.click_and_hold(element).move_by_offset(distance, 0).release().perform()
        print(f"Scrolled element at {element_xpath} by {distance} pixels.")
    except Exception as e:
        print(f"Exception occurred while trying to scroll element: {str(e)}")

def click_seat(driver, time_choice, selected_seat_index):
    """
    Function to attempt to click a seat.
    """
    time.sleep(0.2)
    try:
        seat_xpath = f'/html/body/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/div[{time_choice - 6}]/div[{selected_seat_index}]/div'
        seat_element = driver.find_element(By.XPATH, seat_xpath)
        if "unselected-seat" in seat_element.get_attribute("class"):
            next_div_element = seat_element.find_element(By.XPATH, './div')
            next_div_element.click()
            print(f"Clicked seat at time_choice {time_choice} and selected_seat_index {selected_seat_index}")
            return True
        else:
            print(f"Seat at time_choice {time_choice} and selected_seat_index {selected_seat_index} is not available")
            return False
    except Exception as e:
        print(f"Exception occurred while trying to click seat: {str(e)}")
        return False

def additional_clicks(driver):
    """
    Function to perform additional clicks after a seat is successfully clicked.
    """
    try:
        next_button_xpath = '/html/body/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[3]/button'
        next_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
        next_button.click()
        print("Clicked next button")

        checkbox_xpath = '/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div[1]/label/span[1]/span'
        checkbox = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
        checkbox.click()
        print("Clicked checkbox")

        confirm_button_xpath = '/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div[2]/button[2]'
        confirm_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, confirm_button_xpath)))
        confirm_button.click()
        print("Clicked confirm button")

    except Exception as e:
        print(f"Exception occurred during additional clicks: {str(e)}")

def basic_info_input(driver_path, url_input, sleep_time,
                     password_path,
                     sports_type, complexes_name, date_data,
                     time_threshold, time_choice, selected_seat_index,
                     response_time, chrome_path,
                     selected_seat_index_alt, time_choice_limit,
                     zy_mode):
    origin_time = time.time()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_path

    service = Service(driver_path)
    service.start()
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url_input)
    time.sleep(sleep_time)
    display_author_info(driver)
    time.sleep(sleep_time)

    login_button = driver.find_element(By.XPATH, '//button[@class="el-button el-button--primary"]/span[text()="登 录"]')
    login_button.click()
    time.sleep(sleep_time)

    with open(password_path, 'r') as f:
        student_id = f.readline().strip()
        student_password = f.readline().strip()
    username_input = driver.find_element(By.ID, 'j_username')
    username_input.send_keys(student_id)
    password_input = driver.find_element(By.ID, 'j_password')
    password_input.send_keys(student_password)

    submit_button = driver.find_element(By.ID, 'loginButton')
    submit_button.click()
    time.sleep(sleep_time)

    sports_type_xpath_expression = f'//li[p[text()="{sports_type}"]]'
    sports_type_item = driver.find_element(By.XPATH, sports_type_xpath_expression)
    sports_type_item.click()
    time.sleep(sleep_time)

    complexes_xpath_expression = f"//div[@class='cardP15']/h3[text()='{complexes_name}']"
    element = driver.find_element(By.XPATH, complexes_xpath_expression)
    element.click()
    time.sleep(sleep_time)

    start_time = time.time()

    date_xpath_expression = f'//div[contains(@id, "tab-{date_data}")]'

    current_time = datetime.now().strftime('%H:%M:%S.%f')
    refresh_count = 0
    while current_time < time_threshold:
        try:
            date_element = WebDriverWait(driver, 0.4).until(
                EC.element_to_be_clickable((By.XPATH, date_xpath_expression)))
            date_element.click()
            print(f"找到元素并点击成功，当前时间：{current_time}")
            break
        except:
            refresh_count += 1
            print(f"未找到元素，刷新网页。当前刷新次数：{refresh_count}, 当前时间：{current_time}")
            driver.refresh()
        finally:
            current_time = datetime.now().strftime('%H:%M:%S.%f')
    if current_time >= time_threshold:
        print("已达到时间阈值，停止刷新")

    current_time = datetime.now().strftime('%H:%M:%S.%f')
    refresh_count = 0
    element_clicked = False

    while current_time < time_threshold and not element_clicked:
        try:
            element_present = WebDriverWait(driver, 0.8).until(
                EC.presence_of_element_located((By.XPATH, date_xpath_expression)))
            if element_present:
                date_element = WebDriverWait(driver, 0.5).until(
                    EC.element_to_be_clickable((By.XPATH, date_xpath_expression)))
                date_element.click()
                print(f"找到元素并点击成功，当前时间：{current_time}")
                element_clicked = True
        except:
            refresh_count += 1
            print(f"未找到元素，刷新网页。当前刷新次数：{refresh_count}, 当前时间：{current_time}")
            driver.refresh()
            time.sleep(response_time)
        finally:
            current_time = datetime.now().strftime('%H:%M:%S.%f')

    if current_time >= time_threshold and not element_clicked:
        print("已达到时间阈值，停止刷新")
    time.sleep(response_time)

    seat_clicked = click_seat(driver, time_choice, selected_seat_index)

    if not seat_clicked:
        for seat_index in selected_seat_index_alt:
            seat_clicked = click_seat(driver, time_choice, seat_index)
            if seat_clicked:
                break

    if not seat_clicked:
        for new_time_choice in range(time_choice + 1, time_choice_limit + 1):
            for seat_index in selected_seat_index_alt:
                seat_clicked = click_seat(driver, new_time_choice, seat_index)
                if seat_clicked:
                    break
            if seat_clicked:
                break

    if not seat_clicked:
        print("未能成功点击任何座位")
        time.sleep(600)
    else:
        print("成功点击座位")
        time.sleep(response_time)
        additional_clicks(driver)
        if zy_mode:
            while True:
                time.sleep(0.5)
                scroll_element(driver, "/html/body/div/div[2]/div[7]/div/div[2]/div/div[2]/div/div", 265)
                element_exists = driver.find_elements(By.XPATH, "/html/body/div/div[2]/div[7]/div/div[2]/div/div[2]/span")
                if not element_exists:
                    break

        time.sleep(600)


if __name__ == "__main__":
    # Read configuration from config.txt
    config = read_config('config.txt')

    # Convert necessary items to their appropriate types
    selected_seat_index_alt = [int(x) for x in config['selected_seat_index_alt'].strip('[]').split(',')]
    time_choice_limit = int(config['time_choice_limit'])
    time_choice = int(config['time_choice'])
    selected_seat_index = int(config['selected_seat_index'])
    response_time = float(config['response_time'])
    zy_mode = config['zy_mode'].lower() == 'true'

    # Call the function with the parsed config
    basic_info_input(
        driver_path=config['driver_path'],
        url_input=config['url_input'],
        sleep_time=int(config['sleep_time']),
        password_path=config['password_path'],
        sports_type=config['sports_type'],
        complexes_name=config['complexes_name'],
        date_data=config['date_data'],
        time_threshold=config['time_threshold'],
        time_choice=time_choice,
        selected_seat_index=selected_seat_index,
        response_time=response_time,
        chrome_path=config['chrome_path'],
        selected_seat_index_alt=selected_seat_index_alt,
        time_choice_limit=time_choice_limit,
        zy_mode=zy_mode
    )