# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:36:41 2025

@author: WoojaeYang
"""

#%% ########################## slack ##########################

import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 메시지를 보내는 부분. 함수 안 argument 순서 :
# token : Slack Bot의 토큰
# channel : 메시지를 보낼 채널 
# text : Slack Bot 이 보낼 텍스트 메시지. 마크다운 형식이 지원된다.
# attachments : 첨부파일. 텍스트 이외에 이미지등을 첨부할 수 있다.

def notice_message(token, channel, attachments):
    attachments = json.dumps(attachments) # 리스트는 Json 으로 덤핑 시켜야 Slack한테 제대로 간다.
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,  "attachments": attachments}) # 봇 메세지 외부 내용

#env_path = os.path.join(os.path.dirname(__file__), 'slack_tokens.env') # __file__ 기준으로 slack_tokens.env 경로 지정
load_dotenv(dotenv_path="/home/ywj/venv-auto/slack_tokens.env") # 절대경로 지정

# Token 변수 할당
my_workspace_tkn = os.getenv("MY_WORKSPACE_TOKEN")
des_workspace_tkn = os.getenv("DES_WORKSPACE_TOKEN")

#print("MY_WORKSPACE_TOKEN:", os.getenv("MY_WORKSPACE_TOKEN"))
#print("DES_WORKSPACE_TOKEN:", os.getenv("DES_WORKSPACE_TOKEN"))

if not my_workspace_tkn or not des_workspace_tkn:
    raise EnvironmentError("Slack 토큰이 환경변수에서 불러와지지 않았습니다. .env 파일과 load_dotenv() 호출을 확인하세요.")

#### Slack 관련 정보 입력

# 사용하는 APP Token 입력 : 토요일 (weekday == 5) 일 때만 공용 워크스페이스의 채널에 메세지 전송
today = datetime.today()
if today.weekday() in (5, 6):    
    token = des_workspace_tkn
else:
    token = my_workspace_tkn

title = "Market Interlligence ETF Data Update Test" 
content = "Test Done"
channel = "qa-bot-channel"



#%% ########################## Chrome_webdriver ##########################

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager # Chrome driver 자동 업데이트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import random as rd
import time


#기본 설정
#result_path = 'C:/Users/WoojaeYang/Desktop/auto/result/'

rdint = rd.randint(2,5)
options = Options()
url = 'https://mi-etf.banksalad.com/login'

# headless 옵션 설정
options.add_argument('headless')
options.add_argument("no-sandbox")

# 브라우저 윈도우 사이즈
#options.add_argument('window-size=1920x1080')

# 불필요한 에러메시지 노출 방지
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 사람처럼 보이게 하는 옵션들
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

# 크롬드라이버 자동 업데이트
service = Service(executable_path=ChromeDriverManager().install())

# 드라이버 위치 경로 입력
driver = webdriver.Chrome(service = service, options = options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)


def log_in():

    id = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/form/div[1]/input') 
    id.send_keys('qa@desilo.ai')

    pw = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/form/div[2]/input')
    pw.click()
    pw.send_keys('desilo2024@!')

    login_btn = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/form/button')
    login_btn.click()

    # 기다려
    time.sleep(rdint)  

 
#%%  ########################## Page 1 ##########################
#import pyautogui

new_result = []

def last_saturday():
    today = datetime.today()
    days_since_saturday = (today.weekday() - 5) % 7  # 5(Saturday) 기준으로 차이 계산
    last_saturday = today - timedelta(days=days_since_saturday)
    return last_saturday.date().strftime('%Y.%m.%d')


def check_page1(last_sat):
    updated_date = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div[1]/div[2]/div/div[1]').text.split()[-1]
    #new_result.append(updated_date)
    
    return 'Page 1 OK' if updated_date == last_sat else 'Page 1 NG'
    time.sleep(3)

def check_page1_graph():
    #pyautogui.moveTo(1747, 1116)
    
    driver.execute_script(f"""
        let element = document.elementFromPoint(1747, 1116);
        if (element) {{
            element.dispatchEvent(new MouseEvent('mouseover', {{ bubbles: true }}));
            element.dispatchEvent(new MouseEvent('mousemove', {{ bubbles: true }}));
        }}
        console.log("Mouse event triggered at (1747, 1116)");
    """)

    time.sleep(3)
    
    # JavaScript를 실행하여 툴팁 요소 찾기    
    try:
        tooltip_text = driver.execute_script("""
            let tooltips = document.querySelectorAll('div[style*="position: absolute"][style*="display: block"]');
            return tooltips.length > 0 ? tooltips[0].innerText : "";
        """)
        return tooltip_text[:10]
    except TimeoutException:
        return " "


#%%  ########################## Page 2 ##########################

def check_page2_1():
    page2_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]')
    page2_btn.click()
    page2_1_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/a[1]')
    page2_1_btn.click()
    
    try:
        buy_user_count = wait.until(EC.presence_of_element_located((
            By.XPATH,  '/html/body/div[2]/main/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[4]'
            ))) # [매수 현황 바 차트] > 1위 항목 > 매수 고객 수
        return 'Page 2-1 OK'
    except TimeoutException:
        return 'Page 2-1 NG'


def check_page2_2():
    page2_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]')
    page2_btn.click()
    
    page2_2_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/a[2]')
    page2_2_btn.click()
    
    try:
        jasa_investor_cnt = wait.until(EC.presence_of_element_located((
            By.XPATH,  '/html/body/div[2]/main/div/div[3]/div/div[1]/div[1]/div/div[3]/div[1]/div[3]'
            ))) # 자사 단일 매수 고객 수 
        return 'Page 2-2 OK' 
    except TimeoutException:
        return 'Page 2-2 NG'


def check_page2_3():
    page2_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]')
    page2_btn.click()
    
    page2_1_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/a[3]')
    page2_1_btn.click()
    
    try:
        etf_top10 = wait.until(EC.presence_of_element_located((
            By.XPATH,  '/html/body/div[2]/main/div/div[3]/div[1]/div[1]/div/div[2]/div[2]/div[10]'
            ))) #top10 리스트
        return 'Page 2-3 OK' 
    except TimeoutException:
        return 'Page 2-3 NG'


#%%  ########################## Page 4 ##########################

def check_page4_1():
    page4_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]')
    page4_btn.click()
    
    page4_1_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/a[1]')
    page4_1_btn.click()
    
    try:
        persona1_tab = wait.until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/div[1]/div/div[1]'
        )))  #페르소나1 탭
        return 'Page 4-1 OK'
    except Exception as e:
        return f'Page 4-1 NG : {e}'


def check_page4_2():
    page4_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]')
    page4_btn.click()
    
    page4_2_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/a[2]')
    page4_2_btn.click()
    
    try:
        persona1_tab_tasa = wait.until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]'
        )))    #타사 페르소나1 탭
        return 'Page 4-2 OK'
    except Exception as e:
        return f'Page 4-2 NG : {e}'
    

#%%  ########################## Page 0 ##########################

def check_page_0():
    page0_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/a[2]')
    page0_btn.click()
    
    try:
        etf_value = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[2]/main/div/div[2]/div[1]/div/div[1]')))
        # ETF 상품 보유 규모
        return "Page 0 OK"
    except Exception as e:
        return f'Page 0 NG : {e}'
    


#%%  ########################## logging ##########################

import sys
import logging

log_path = '/home/ywj/venv-auto/mi_e2e/logs/'  

# 로그 파일 경로 설정
LOG_FILE = f"{log_path}MI_etf_slack_notice_log.txt"
STDOUT_FILE =  f"{log_path}MI_etf_slack_notice_stdout.txt"
STDERR_FILE =  f"{log_path}MI_etf_slack_notice_stderr.txt"

# 기존 핸들러 제거 (중복 설정 방지)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# 로그 설정 (파일로 저장)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# 표준 출력 및 에러도 로그에 기록
sys.stdout = open(STDOUT_FILE, "w", encoding="utf-8")
sys.stderr = open(STDERR_FILE, "w", encoding="utf-8")

def log_message(level, message):
    """로그 메시지를 남기는 함수"""
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)


#%%  ########################## main ##########################

def main():
    log_message("info", "=========== [MI_etf_slack_notice START] ===========")
    
    try:
        
        driver.get(url) # 접속
        log_message("info", "접속 완료")
        
        log_in()
        log_message("info", "로그인 완료")
        
        last_sat = last_saturday()
        log_message("info", f"토요일 날짜 {last_sat}")
        
        result_page1 = check_page1(last_sat)
        log_message("info", f" PAGE 1 {result_page1}")
        
        recent_update_date = check_page1_graph()
        #print(recent_update_date)
        log_message("info", f" PAGE 1 RECENT UPDATE {recent_update_date}")
        
        result_page0 = check_page_0()
        log_message("info", f" PAGE 0 {result_page0}")
        
        result_page2_1 = check_page2_1()
        log_message("info", f" PAGE 2_1 {result_page2_1}")
        
        result_page2_2 = check_page2_2()
        log_message("info", f" PAGE 2_2 {result_page2_2}")
        
        result_page2_3 = check_page2_3()
        log_message("info", f" PAGE 2_3 {result_page2_3}")
        
        
        result_page4_1 = check_page4_1()
        log_message("info", f" PAGE 4_1 {result_page4_1}")
        
        result_page4_2 = check_page4_2()
        log_message("info", f" PAGE 4_2 {result_page4_2}")
        
        # 봇 메세지에 출력할 날짜
        now = datetime.now()
        now_date = now.strftime('%Y.%m.%d')
        now_time = now.strftime('%H:%M:%S')
        
        # 봇 메세지 내부 내용
        attach_dict = {
            'color' : '#ff0000',
            'author_name' : 'Slack Bot Notice',
            'title' : title,
            'text' : f"""{now_date} {now_time} ```
        == [Page 1] ==============
        {result_page1}  {recent_update_date}
        == [Page 0] ==============
        {result_page0}
        == [Page 2] ==============
        {result_page2_1}
        {result_page2_2}
        {result_page2_3}
        == [Page 4] ==============
        {result_page4_1}
        {result_page4_2} ``` """
            }
            
        attach_list = [attach_dict]

        notice_message(token, channel, attach_list)
        log_message("info", "Slack 메세지 전송 완료")
    
    except Exception as e:
        log_message("error", f"오류 발생: {e}")
    
    finally:
        driver.quit()
        log_message("info", "=========== [MI_slack_notice END] ===========")



#%%

if __name__ =="__main__":
    main()





