# -*- coding: utf-8 -*-
"""
Created on Thu May 29 13:45:26 2025

@author: WoojaeYang
"""

from driver_setup import create_driver
from admin_page import Admin_Page
from project_page import Project_Page
from provider_page import Provider_Page
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

today = datetime.today()
today_date = today.strftime('%y%m%d')
today_date 

#%%  ########################## logging ##########################

import sys
import logging

log_path = '/home/ywj/venv-auto/dcr_e2e/logs/'  

# 로그 파일 경로 설정
LOG_FILE = f"{log_path}[On-call]dcr_e2e_logs.txt"
STDOUT_FILE =  f"{log_path}[On-call]dcr_e2e_stdout.txt"
STDERR_FILE =  f"{log_path}[On-call]dcr_e2e_stderr.txt"

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
#sys.stdout = open(STDOUT_FILE, "w", encoding="utf-8")
sys.stderr = open(STDERR_FILE, "w", encoding="utf-8")

def log_message(level, message):
    """로그 메시지를 남기는 함수"""
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
        
        
#%% ########################## slack ##########################


import requests
import json
from datetime import datetime, timedelta
import os
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

# 사용하는 APP Token 입력 : 토요일/일요일 (weekday in (5,6) ) 일 때 만 내 워크스페이스의 채널에 메세지 전송
today = datetime.today()
if today.weekday() in (5, 6):    
    token = my_workspace_tkn
else:
    token = des_workspace_tkn
    

title = "DCR On-call Test" 
content = "Test Done"
channel = "qa-bot-channel"


#%%   ########################## DEF ##########################

def oncall_01(driver, wait, project):
    time.sleep(2)
    scene_num = 'On-call_01'
    print(f"▶ {scene_num} 시작")
    
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div/table/tbody/tr/td/div'
    log_message('info', 'On-call #01 START')
    query_01 = 'SELECT COUNT(*) \nFROM provider1.main4'
    proj_name = 'YWJ'

    # Asker
    try:
        log_message('info', 'DCR_scenario_#1 - Asker Start')
        time.sleep(2)
        
        # 정렬
        dropdown = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div[3]/div')
        dropdown.click()
        
        # 최신 업데이트 순
        recently_elem = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div[3]/div[2]/div[3]')
        recently_elem.click()
        time.sleep(1)
        
        # 프로젝트 진입
        project.enter_project(proj_name)
        
        # 워크플로우 생성 버튼 클릭
        create_wf = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div[3]/div[2]/div/button')))
        create_wf.click()
        time.sleep(3)
        # 워크플로우 이름 입력
        wf_name = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/input')
        wf_name.click()
        wf_name.send_keys(f'workflow_{today_date}_{scene_num}')
        time.sleep(2)
        
        # Editor 형식으로 전환
        editor_tab = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]')))
        editor_tab.click()
        # 입력 영역
        text_area = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div/div[1]/div/textarea')))
        text_area.click()
        text_area.send_keys(query_01)
        
        project.start_workflow()
        
        #쿼리 결과 확인
        result = project.cehck_query_result(result_xpath)
        log_message('info', f'Query_Result : {result}')
        
    finally:
        log_message('info', 'DCR_scenario_#1 - Asker Done')
    
    return f'Query_Result : {result}'

    time.sleep(1)


#%%   ########################## MAIN ##########################


def main():
    print('main START')
    log_message('info', 'main START')
    driver, wait = create_driver()

    handles = driver.window_handles
    #print(f"탭 확인: {handles}")
    driver.execute_script("window.open('');")
    time.sleep(1)
    driver.execute_script("window.open('');")
    time.sleep(1)
 
    handles = driver.window_handles
    #print(f"탭 확인: {handles}")
 
    provider_tab = handles[0]
    admin_tab = handles[1]
    project_tab = handles[2]

    project = Project_Page(driver, wait, project_tab)
    
    project_url = 'https://dcr-operator-asker.staging.desilo.co/projects'
    project_email = 'analyst1@gmail.com'
    project_pw = '1234'
    
    # 봇 메세지에 출력할 날짜
    now = datetime.now()
    now_date = now.strftime('%Y.%m.%d')
    now_time = now.strftime('%H:%M:%S')
        
    log_message("info", "=========== [DCR_On-calln_test START] ===========")
    
    try:
        log_message("info", "로그인 시작")
        project.project_login(project_url, project_email, project_pw)
        log_message("info", "로그인 완료")
        
        log_message("info", "On-call #01 시작")
        result01 = oncall_01(driver, wait, project)
        log_message("info", "On-call #01 완료")
        
        # 봇 메세지 내부 내용
        attach_dict = {
            'color' : '#ff0000',
            'author_name' : 'Slack Bot Notice',
            'title' : title,
            'text' : f"""{now_date} {now_time} ```
        == [On-calll_#1] ==============
        {result01}
            ``` """
            }
            
        attach_list = [attach_dict]

        notice_message(token, channel, attach_list)
        log_message("info", "Slack 메세지 전송 완료")
    
    except Exception as e:
        log_message("error", f"오류 발생: {e}")
    
    except Exception as e:
        log_message("error", f"오류 발생: {e}")
    
    finally:
        #driver.quit()
        log_message("info", "=========== [DCR_On-call_test END] ===========")    
        
        
#%%
if __name__ == "__main__":
    main()
    
    