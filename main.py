import os.path
import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
import functools
driver_path=r"C:\Users\yogesh\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
content_path=r"C:\Users\yogesh\OneDrive\Desktop\Linkedin_automated_posting\Content"

driver=webdriver.Chrome(driver_path)
driver.get("https://www.linkedin.com/login")


def load_cookies(driver,path='cookies.pkl'):
    try:
        with open(path,'rb') as cookies_file:
            cookies=pickle.load(cookies_file)
            for cookie in cookies:
                driver.add_cookie(cookie)
            print("Cookies loaded successfully!")
    except FileNotFoundError:
        print(f"File '{path}' not found.")
    except EOFError:
        print(f"Error: '{path}' does not contain valid pickle data.")
    except Exception as e:
        print(f"Exception occurred: {e}")


def save_cookies(driver,path='cookies.pkl'):
    with open(path,'wb') as fh:
        pickle.dump(driver.get_cookies(),fh)

load_cookies(driver)
driver.refresh()

if "login" in driver.current_url:
    input("enter after 2fa authorization")
    save_cookies(driver)

def get_next_file_to_post(posted_file):
    all_files=sorted(os.listdir(content_path))
    for file in all_files:
        if file not in posted_file:
            return os.path.join(content_path,file)

    print("all files have been posted")

posted_file_logs='posted_files_log.txt'
def get_posted_file():
    if os.path.exists(posted_file_logs):
        with open(posted_file_logs,'r') as log_file:
            return set(log_file.read().splitlines())
    return set()


posted_file=get_posted_file()
file_to_post= get_next_file_to_post(posted_file)
def log_posted_files(filename_to_log):
    with open(posted_file_logs,'a') as log_files:
        log_files.write(os.path.join(filename_to_log)+'\n')

def post_to_feed(driver,file_to_post):
    try:
        start_post = WebDriverWait(driver,60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "share-box-feed-entry__trigger"))
        )
        start_post.click()
        time.sleep(3)
        file_Extension=os.path.splitext(file_to_post)[1].lower()
        if file_Extension in ['.jpg','.png','.jpeg','.gif','.bmp']:
            Add_media=WebDriverWait(driver,60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "share-promoted-detour-button"))
            )
            Add_media.click()
            time.sleep(5)
            file_input = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div/div/div[1]/div/div[2]/input"))
            )
            file_input.send_keys(file_to_post)
            time.sleep(3)

            next_btn = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div/div/div[2]/div/button[2]"))
            )
            next_btn.click()
            time.sleep(3)
        elif file_Extension in [".txt"]:
            with open(file_to_post,'r') as txt_file:
                Text=txt_file.read()

                fle_input=WebDriverWait(driver,60).until(
                    EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div/div/div/div[1]"))
                )
                fle_input.send_keys(Text)
                time.sleep(5)
                post_button=WebDriverWait(driver,60).until(
                    EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/button"))
                )
                post_button.click()
                time.sleep(5)
                file_name_to_log=os.path.basename(file_to_post)
                print(file_name_to_log)
                log_posted_files(file_name_to_log)
                print("posted file logged succsessfully")



        else:
            add_button=WebDriverWait(driver,60).until(
                EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/section/div[2]/ul/li[5]/div/span/button"))
            )
            add_button.click()
            time.sleep(3)

            add_document_btn=WebDriverWait(driver,60).until(
                EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/section/div[2]/ul/li[7]/div/div/span/button"))
            )
            add_document_btn.click()
            time.sleep(3)

            file_input=WebDriverWait(driver,60).until(
                EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div/div[1]/div[1]/div/div/input"))
            )
            file_input.send_keys(file_to_post)
            document_title=os.path.basename(file_to_post)
            add_document_title=WebDriverWait(driver,60).until(
                EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div/div[1]/div[1]/input"))
            )
            add_document_title.send_keys(document_title)

            done_button=WebDriverWait(driver,60).until(
                EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div/div[2]/div/button[2]"))
            )
            done_button.click()
            time.sleep(3)

        post_btn=WebDriverWait(driver,60).until(
            EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div/div/div[2]/div[4]/div/div[2]/button"))
        )
        post_btn.click()

        log_posted_filename=os.path.basename(file_to_post)
        log_posted_files(log_posted_filename)
        time.sleep(10)
        driver.refresh()

    except Exception as e:
        print("error postng files: ",e)

schedule.every(1).hours.do(functools.partial( post_to_feed,driver,file_to_post))


if __name__=="__main__":
    post_to_feed(driver,file_to_post)

    while True:
        schedule.run_pending()
        time.sleep(3)
