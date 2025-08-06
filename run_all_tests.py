# -*- coding: utf-8 -*-
"""
Created on Fri May 16 08:34:38 2025

@author: WoojaeYang
"""

from driver_setup import create_driver
from admin_page import Admin_Page
from project_page import Project_Page
from provider_page import Provider_Page
import time
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# # 기본 탭 (provider)
# provider_tab = driver.current_window_handle

# # 추가 탭 (admin, project)
# driver.execute_script("window.open('');")
# admin_tab = driver.window_handles[1]

# driver.execute_script("window.open('');")
# project_tab = driver.window_handles[2]


# # 클래스 인스턴스 생성 시 driver, wait, tab 모두 넘김
# provider = Provider_Page(driver, wait, provider_tab)
# admin = Admin_Page(driver, wait, admin_tab)
# project = Project_Page(driver, wait, project_tab)

today = datetime.today()
today_date = today.strftime('%y%m%d_%H%M')
today_date 

#%%  ########################## logging ##########################

import sys
import logging

log_path = '/home/ywj/venv-auto/dcr_e2e/logs/'  

# 로그 파일 경로 설정
LOG_FILE = f"{log_path}dcr_e2e_logs.txt"
STDOUT_FILE =  f"{log_path}dcr_e2e_stdout.txt"
STDERR_FILE =  f"{log_path}dcr_e2e_stderr.txt"

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

   
    
#%%  ########################## SCENARIO #01 ##########################

def scene_01(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no01'
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div/table/tbody/tr/td'
    print(f"▶ {scene_num} 시작 ===========================================")

    log_message('info', 'DCR_scenario_#1_Start -----')
    da_name_01 = f'AUTO_{today_date}_hospital_{scene_num}'
    query_01 = f'SELECT COUNT(*) \nFROM provider1.{da_name_01}'
    

    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#1 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_01, today_date)
        provider.upload_file()
        provider.register()
    
    finally:
        log_message('info', 'DCR_scenario_#1 - Data-registry Done ===========================================')
    
    # Admin
    try:
        log_message('info', 'DCR_scenario_#1 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.move_to_dat_space()
        admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
    finally:
        log_message('info', 'DCR_scenario_#1 - Admin Done ===========================================')
    
    # Asker
    try:
        log_message('info', 'DCR_scenario_#1 - Asker Start ===========================================')
        print('  Asker Start -----')
        time.sleep(2)
        project.create_project(today_date, scene_num)
        project.create_workflow(today_date, scene_num)
        project.input_query(query_01)
        project.start_workflow()
        
        #쿼리 결과 확인
        result = project.cehck_query_result(result_xpath)
        log_message('info', f'Query_Result : {result}')
        
    finally:
        log_message('info', 'DCR_scenario_#1 - Asker Done ===========================================')
    
    return f'Query_Result : {result}'


#%%  ########################## SCENARIO #02 ##########################

def scene_02(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no02'
    result_xpath02 = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div/table/tbody/tr/td'
    print(f"▶ {scene_num} 시작 ===========================================")
    
    log_message('info', 'DCR_scenario_#2_Start ===========================================')
    da_name_02 = f'AUTO_{today_date}_hospital_{scene_num}'
    query_02 = f'SELECT COUNT(*) \nFROM provider1.{da_name_02}'

    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#2 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_02, today_date)
        # 시나리오2 에서는 데이터 등록 자동승인 OFF
        provider.click_approval_box()
        provider.upload_file()
        provider.register()
        
    finally:
        log_message('info', 'DCR_scenario_#2 - Data-registry Done ===========================================')
    
    # Admin
    try:
        log_message('info', 'DCR_scenario_#2 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.move_to_dat_space()
        admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
    finally:
        log_message('info', 'DCR_scenario_#2 - Admin Done ===========================================')
        
    # Asker
    try:
        log_message('info', 'DCR_scenario_#2 - Asker Start ===========================================')
        print('  Asker Start -----')
        project.create_project(today_date, scene_num)
        project.create_workflow(today_date, scene_num)
        project.input_query(query_02)
        project.start_workflow()
        time.sleep(3)  
    
    finally:
        log_message('info', 'DCR_scenario_#2 - Asker Done ===========================================')
        
    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#2 - Query Approval Start ===========================================')
        print('  Query Approval task -----')
        provider.enter_query_approval(da_name_02)
        provider.approve_query()
    
    finally:
        log_message('info', 'DCR_scenario_#2 - Query Approval Done ===========================================')
    
    # Asker
    try:
        log_message('info', 'DCR_scenario_#2 - Asker02 Start ===========================================')
        print('  Asker02 Start -----')
        result = project.cehck_query_result(result_xpath02)
        log_message('info',  f'Query_Result : {result}')
    finally:
        log_message('info', 'DCR_scenario_#2 - Asker02 Done ===========================================')
        
    return f'Query_Result : {result}'

    time.sleep(1)
        
        
#%%  ########################## SCENARIO #03 ########################## ANOVA

def scene_03(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no03'
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div[1]/table/tbody/tr/td[2]/div'
    print(f"▶ {scene_num} 시작 ===========================================")
    
    log_message('info', 'DCR_scenario_#3_Start ===========================================')
    da_name_03 = f'AUTO_{today_date}_hospital_{scene_num}'

    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#3 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_03, today_date)
        provider.upload_file()
        provider.register()

    finally:
        log_message('info', 'DCR_scenario_#3 - Data-registry Done ===========================================')

    # Admin
    try:
        log_message('info', 'DCR_scenario_#3 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.move_to_dat_space()
        admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
    finally:
        log_message('info', 'DCR_scenario_#3 - Admin Done ===========================================')

    # Asker
    try:
        log_message('info', 'DCR_scenario_#3 - Asker Start ===========================================')
        print('  Asker Start -----')
        time.sleep(2)
        project.create_project(today_date, scene_num)
        project.create_workflow(today_date, scene_num)
        
        #아노바 분석 설정
        project.set_anova(da_name_03)
        project.start_workflow()
                
        #쿼리 결과 확인
        result = project.cehck_query_result(result_xpath)
        log_message('info',  f'ANOVA_P-value : {result}')
        
    finally:
        log_message('info', 'DCR_scenario_#3 - Asker Done ===========================================')
    
    return f'ANOVA_P-value : {result}'

    time.sleep(1)
        
        
#%%  ########################## SCENARIO #04 ##########################  Linear Regression

def scene_04(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no04'
    print(f"▶ {scene_num} 시작 ===========================================")
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div[1]/table/tbody/tr[2]/td[2]/div'
    log_message('info', 'DCR_scenario_#4_Start ===========================================')
    da_name_04 = f'AUTO_{today_date}_hospital_{scene_num}'
    

    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#4 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_04, today_date)
        provider.upload_file()
        provider.register()

    finally:
        log_message('info', 'DCR_scenario_#4 - Data-registry Done ===========================================')

    # Admin
    try:
        log_message('info', 'DCR_scenario_#4 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.move_to_dat_space()
        admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
    finally:
        log_message('info', 'DCR_scenario_#4 - Admin Done ===========================================')

    # Asker
    try:
        log_message('info', 'DCR_scenario_#4 - Asker Start ===========================================')
        print('  Asker Start -----')
        time.sleep(2)
        project.create_project(today_date, scene_num)
        project.create_workflow(today_date, scene_num)
        
        # Linear Rgression 설정
        project.set_linear(da_name_04)
        project.start_workflow()
                
        #쿼리 결과 확인
        result = project.cehck_query_result(result_xpath)
        log_message('info',  f'R-Squared_Result : {result}')
        
    finally:
        log_message('info', 'DCR_scenario_#4 - Asker Done ===========================================')


    return f'ANOVA_P-value : {result}'

    time.sleep(1)


#%%  ########################## SCENARIO #05 ##########################

def scene_05(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no05'
    print(f"▶ {scene_num} 시작 ===========================================")
    
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div/table/tbody/tr/td'
    log_message('info', 'DCR_scenario_#5_Start ===========================================')
    da_name_05 = f'AUTO_{today_date}_hospital_{scene_num}'
    query_05 = f'SELECT SUM(provider1.{da_name_05}.나이) \nFROM provider1.{da_name_05}'

    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#5 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_05, today_date)
        provider.upload_file()
        provider.register()

    finally:
        log_message('info', 'DCR_scenario_#5 - Data-registry Done ===========================================')

    # Admin
    try:
        log_message('info', 'DCR_scenario_#5 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.move_to_dat_space()
        admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
    finally:
        log_message('info', 'DCR_scenario_#5 - Admin Done ===========================================')


    # Asker
    try:
        log_message('info', 'DCR_scenario_#5 - Asker Start ===========================================')
        print('  Asker Start -----')
        time.sleep(2)
        project.create_project(today_date, scene_num)
        project.create_workflow(today_date, scene_num)
        project.input_query(query_05)
        project.start_workflow()
                
        #쿼리 결과 확인
        result = project.cehck_query_result(result_xpath)
        log_message('info',  f'Query_Result : {result}')

    finally:
        log_message('info', 'DCR_scenario_#5 - Asker Done ===========================================')

    return f'ANOVA_P-value : {result}'


#%%  ########################## SCENARIO #06 ##########################

def scene_06(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no06'
    print(f"▶ {scene_num} 시작 ===========================================")
    
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div/table/tbody/tr/td'
    log_message('info', 'DCR_scenario_#6_Start')
    da_name_06 = f'AUTO_{today_date}_hospital_{scene_num}'
    query_06 = f'SELECT COUNT(*) \nFROM provider1.{da_name_06}'

    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#6 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_06, today_date)
        provider.upload_file()
        provider.register()

    finally:
        log_message('info', 'DCR_scenario_#6 - Data-registry Done ===========================================')

    # Admin
    try:
        log_message('info', 'DCR_scenario_#6 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.move_to_dat_space()
        admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
    finally:
        log_message('info', 'DCR_scenario_#6 - Admin Done ===========================================')


    # Asker
    try:
        log_message('info', 'DCR_scenario_#6 - Asker Start ===========================================')
        print('  Asker Start -----')
        time.sleep(2)
        project.create_project(today_date, scene_num)
        project.create_workflow(today_date, scene_num)
        project.input_query(query_06)
        project.start_workflow()
                
        #쿼리 결과 확인
        result = project.cehck_query_result(result_xpath)
        log_message('info',  f'Query_Result : {result}')

    finally:
        log_message('info', 'DCR_scenario_#6 - Asker Done ===========================================')

    # Admin --  가비지 컬렉션
    now_time = today.strftime('%Y-%m-%d %H:%M')
    try:
        log_message('info', 'DCR_scenario_#6 - Garbage-collection Start ===========================================')
        print('  Garbage-collection Start -----')
        status, end_time = admin.run_garbage_collection(now_time)
        log_message('info', f'Garbage Collection status : {status}')
        log_message('info', f'Garbage Collection end : {end_time}')
        
    except Exception as e:
        log_message('info', f'Workflow Running NG : {e}')
    
    finally:
        log_message('info', 'DCR_scenario_#6 - Garbage-collection Done ===========================================')

    return f'Query_Result : {result}'

    time.sleep(1)
    
    
#%%  ########################## SCENARIO #07 ##########################

def scene_07(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no07'
    print(f"▶ {scene_num} 시작 ===========================================")
    
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div/table/tbody/tr/td'
    log_message('info', 'DCR_scenario_#7_Start ===========================================')
    da_name_07 = f'AUTO_{today_date}_hospital_{scene_num}'
    query_07 = f'SELECT COUNT(*) \nFROM provider1.{da_name_07}'
    
    
    # Admin
    try:
        log_message('info', 'DCR_scenario_#7 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.key_gen()
    finally:
        log_message('info', 'DCR_scenario_#7 - Admin Done ===========================================')
    
    # Data-registy
    try:
        log_message('info', 'DCR_scenario_#7 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_07, today_date)
        provider.upload_file()
        provider.register()

    finally:
        log_message('info', 'DCR_scenario_#7 - Data-registry Done ===========================================')
        
    # Admin
    try:
        log_message('info', 'DCR_scenario_#7 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.move_to_dat_space()
        admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
    finally:
        log_message('info', 'DCR_scenario_#7 - Admin Done ===========================================')
    
    
    # Asker
    try:
        log_message('info', 'DCR_scenario_#7 - Asker Start ===========================================')
        print('  Asker Start -----')
        time.sleep(2)
        project.create_project(today_date, scene_num)
        project.create_workflow(today_date, scene_num)
        project.input_query(query_07)
        project.start_workflow()
                
        #쿼리 결과 확인
        result = project.cehck_query_result(result_xpath)
        log_message('info',  f'Query_Result : {result}')
    
    finally:
        log_message('info', 'DCR_scenario_#7 - Asker Done ===========================================')
    
    # Admin --  가비지 컬렉션
    now_time = today.strftime('%Y-%m-%d %H:%M')
    try:
        log_message('info', 'DCR_scenario_#7 - Garbage-collection Start ===========================================')
        print('  Garbage-collection Start -----')
        status, end_time = admin.run_garbage_collection(now_time)
        log_message('info', f'Garbage Collection status : {status}')
        log_message('info', f'Garbage Collection end : {end_time}')
        
    except Exception as e:
        log_message('info', f'Workflow Running NG : {e}')
    
    finally:
        log_message('info', 'DCR_scenario_#7 - Garbage-collection Done ===========================================')
    
    return f'Query_Result : {result}'
    
    time.sleep(1)


#%%  ########################## SCENARIO #08 ##########################

def scene_08(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no08'
    print(f"▶ {scene_num} 시작 ===========================================")
    
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div[2]/div'
    log_message('info', 'DCR_scenario_#8_Start ===========================================')
    da_name_08 = f'AUTO_{today_date}_hospital_{scene_num}'
    query_08 = f'SELECT COUNT(*) \nFROM provider1.{da_name_08}'
            
    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#8 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_08, today_date)
        # 시나리오8 에서는 데이터 등록 자동승인 OFF
        provider.click_approval_box()
        provider.upload_file()
        provider.register()
        
    finally:
        log_message('info', 'DCR_scenario_#8 - Data-registry Done ===========================================')
    
    # Admin
    try:
        log_message('info', 'DCR_scenario_#8 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.move_to_dat_space()
        admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
    finally:
        log_message('info', 'DCR_scenario_#8 - Admin Done ===========================================')
        
    # Asker
    try:
        log_message('info', 'DCR_scenario_#8 - Asker Start ===========================================')
        print('  Asker Start -----')
        project.create_project(today_date, scene_num)
        project.create_workflow(today_date, scene_num)
        project.input_query(query_08)
        project.start_workflow()
        time.sleep(3)  
    
    finally:
        log_message('info', 'DCR_scenario_#8 - Asker Done ===========================================')
        
    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#8 - Query Approval Start ===========================================')
        print('  Query Approval Start -----')
        provider.enter_query_approval(da_name_08)
        provider.reject_query()
    
    finally:
        log_message('info', 'DCR_scenario_#8 - Query Approval Done ===========================================')
    
    # Asker
    try:
        log_message('info', 'DCR_scenario_#8 - Asker02 Start ===========================================')
        print('  Asker02 Start -----')
        result = project.cehck_query_result(result_xpath)
        log_message('info',  f'Query_Result : {result}')
    finally:
        log_message('info', 'DCR_scenario_#8 - Asker02 Done ===========================================')
        
    return result

    time.sleep(1)


#%%  ########################## SCENARIO #09 ##########################

def scene_09(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no09'
    print(f"▶ {scene_num} 시작 ===========================================")
    
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div[2]/div'
    log_message('info', 'DCR_scenario_#9_Start ===========================================')
    da_name_09 = f'AUTO_{today_date}_main4_{scene_num}-'
            

    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#9 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_09, today_date)
        provider.upload_file_main4()
        provider.register()

    finally:
        log_message('info', 'DCR_scenario_#9 - Data-registry Done ===========================================')

    # Admin
    try:
        log_message('info', 'DCR_scenario_#9 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.move_to_dat_space()
        admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
    finally:
        log_message('info', 'DCR_scenario_#9 - Admin Done ===========================================')


    # Asker
    try:
        log_message('info', 'DCR_scenario_#9 - Asker Start ===========================================')
        print('  Asker Start -----')
        time.sleep(2)
        project.create_project(today_date, scene_num)
        project.create_workflow(today_date, scene_num)
        
        # Kaplan-Meier
        project.set_kpe(da_name_09)
        project.start_workflow()
        
        time.sleep(120)        
        #쿼리 결과 확인
        try:
            kpe_result = wait.until(EC.presence_of_element_located(( By.XPATH,  result_xpath)))
            log_message('info',  'KPE Graph OK')
            return 'KPE Graph OK'
        except TimeoutException:
            return 'KPE Graph NG'

    finally:
        log_message('info', 'DCR_scenario_#9 - Asker Done ===========================================')


#%%  ########################## SCENARIO #10 ##########################

def scene_10(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no10'
    print(f"▶ {scene_num} 시작 ===========================================")
    
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div[2]/div'
    log_message('info', 'DCR_scenario_#10_Start ===========================================')
    da_name_10 = f'AUTO_{today_date}_main4_{scene_num}'

    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#10 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_10, today_date)
        provider.upload_file_main4()
        provider.register()

    finally:
        log_message('info', 'DCR_scenario_#10 - Data-registry Done ===========================================')

    # Admin
    try:
        log_message('info', 'DCR_scenario_#10 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(2)
        admin.move_to_dat_space()
        admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
    finally:
        log_message('info', 'DCR_scenario_#10 - Admin Done ===========================================')


    # Asker
    try:
        log_message('info', 'DCR_scenario_#10 - Asker Start ===========================================')
        print('  Asker Start -----')
        time.sleep(2)
        project.create_project(today_date, scene_num)
        project.create_workflow(today_date, scene_num)
        
        # Kaplan-Meier
        project.set_cox(da_name_10)
        project.start_workflow()
        
        time.sleep(120)        
        #쿼리 결과 확인
        try:
            kpe_result = wait.until(EC.presence_of_element_located(( By.XPATH,  result_xpath)))
            return 'Cox OK'
        except TimeoutException:
            return 'Cox NG'

    finally:
        log_message('info', 'DCR_scenario_#10 - Asker Done ===========================================')
    

#%%  ########################## SCENARIO #11 ##########################

def scene_11(driver, wait, provider, admin, project):
    time.sleep(2)
    scene_num = 'no11'
    print(f"▶ {scene_num} 시작 ===========================================")
    
    result_xpath = '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/div[2]/div[2]/div'
    log_message('info', 'DCR_scenario_#11_Start ===========================================')
    da_name_11 = f'AUTO_{today_date}_main4_{scene_num}'
    results = []
    
    # Data-registry
    try:
        log_message('info', 'DCR_scenario_#11 - Data-registry Start ===========================================')
        print('  Data-registry Start -----')
        time.sleep(2)
        provider.move_to_data_registration()
        provider.data_registration(da_name_11, today_date)
        provider.upload_file_main4()
        provider.register()
        
        time.sleep(2)
        
        # Data Asset Delete
        da_del_time = provider.del_da(da_name_11)
        da_del_created_time, da_del_event_detail = admin.check_log()
        
        # 문자열을 datetime으로 변환
        fmt = "%Y-%m-%d %H:%M:%S"  # 로그 형식에 맞게 조정
        da_del_time_dt = datetime.strptime(da_del_time, fmt)
        da_del_created_time_dt = datetime.strptime(da_del_created_time, fmt)
        
        da_diff = abs(da_del_time_dt - da_del_created_time_dt)
        
        if da_diff.total_seconds() <= 5 and da_del_event_detail == '데이터 에셋 삭제 (성공)':
            log_message('info','Data Asset Delete OK')
            results.append('Data Asset Delete OK')
        else:
            log_message('info', f'da_del_created_time : {da_del_created_time} // da_del_time : {da_del_time}')
            results.append(f'da_del_created_time : {da_del_created_time} // da_del_time : {da_del_time}')

    finally:
        log_message('info', 'DCR_scenario_#11 - Data-registry Done ===========================================')

    # Admin
    try:
        log_message('info', 'DCR_scenario_#11 - Admin Start ===========================================')
        print('  Admin Start -----')
        time.sleep(1)
        admin.move_to_dat_space()
        ds_name_11 = admin.add_ds(today_date, scene_num)
        admin.assign(today_date)
        admin.add_da(scene_num)
        admin.add_analyst()
        
        time.sleep(2)
        
        # Data Space Delete
        ds_del_time = admin.del_ds(ds_name_11)
        ds_del_created_time, ds_del_event_detail = admin.check_log()
        
        # 문자열을 datetime으로 변환
        fmt = "%Y-%m-%d %H:%M:%S"  # 로그 형식에 맞게 조정
        ds_del_time_dt = datetime.strptime(ds_del_time, fmt)
        ds_del_created_time_dt = datetime.strptime(ds_del_created_time, fmt)
        
        ds_diff = abs(ds_del_time_dt - ds_del_created_time_dt)
        
        if ds_diff.total_seconds() <= 5 and ds_del_event_detail == '데이터 스페이스 삭제 (성공)':
            log_message('info', 'Data Space Delete OK')
            results.append('\t\t\t Data Space Delete OK')
        else:
            log_message('info', f'ds_del_created_time : {ds_del_created_time} // ds_del_time : {ds_del_time}')
            results.append(f'\t\t ds_del_created_time : {ds_del_created_time} \n ds_del_time : {ds_del_time}\n')
    finally:
        log_message('info', 'DCR_scenario_#11 - Admin Done ===========================================')


    # Asker
    try:
        log_message('info', 'DCR_scenario_#11 - Asker Start ===========================================')
        print('  Asker Start -----')
        time.sleep(1)
        proj_name_11 = project.create_project(today_date, scene_num) 

        # Project Delete
        proj_del_time = project.del_proj(proj_name_11)
        proj_del_created_time, proj_del_event_detail = admin.check_log()
       
        # 문자열을 datetime으로 변환
        fmt = "%Y-%m-%d %H:%M:%S"  # 로그 형식에 맞게 조정
        proj_del_time_dt = datetime.strptime(proj_del_time, fmt)
        proj_del_created_time_dt = datetime.strptime(proj_del_created_time, fmt)
        
        proj_diff = abs(proj_del_time_dt - proj_del_created_time_dt)
        
        if proj_diff.total_seconds() <= 5 and proj_del_event_detail == '프로젝트 삭제 (성공)':
            log_message('info', 'Project Delete OK')
            results.append('\t\t\t Project Delete OK')
        else:
            log_message('info', f'proj_del_created_time : {proj_del_created_time} // proj_del_time : {proj_del_time}')
            results.append(f'\t\t proj_del_created_time : {proj_del_created_time} \n proj_del_time : {proj_del_time}')

    finally:
        log_message('info', 'DCR_scenario_#11 - Asker Done ===========================================')

    return "\n".join(results)

#%% ########################## slack ##########################


import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# 메시지를 보내는 부분. 함수 안 argument 순서
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

# 사용하는 APP Token 입력 : 토요일/일요일 (weekday in (5,6) ) 일 때 공용 워크스페이스의 채널에 메세지 전송
today = datetime.today()
if today.weekday() in (5, 6):    
    token = my_workspace_tkn
else:
    token = des_workspace_tkn

title = "DCR E2E Automation Test" 
content = "Test Done"
channel = "qa-bot-channel"


#%%   ########################## MAIN ##########################


def main():
    
    # 봇 메세지에 출력할 날짜
    now = datetime.now()
    now_date = now.strftime('%Y.%m.%d')
    now_time = now.strftime('%H:%M:%S')
    
    print(f'main START {now_date} {now_time}')
    log_message('info', 'main START')
    driver, wait = create_driver()
    
    driver.execute_script("window.open('');")
    time.sleep(1)
    driver.execute_script("window.open('');")
    time.sleep(1)

    handles = driver.window_handles
    #print(f"탭 확인: {handles}")

    provider_tab = handles[0]
    admin_tab = handles[1]
    project_tab = handles[2]

    provider = Provider_Page(driver, wait, provider_tab)
    admin = Admin_Page(driver, wait, admin_tab)
    project = Project_Page(driver, wait, project_tab)
    
    admin_url = 'https://dcr-operator-admin.qa.desilo.co/audit-logs'
    admin_email = 'admin1@desilo.ai'
    admin_pw = 'desilo00@!'

    provider_url = 'https://dcr-provider-dataregistry.qa.desilo.pro/data-assets'
    provider_email = 'provider1@desilo.ai'
    provider_pw = 'desilo00@!'
    
    project_url = 'https://dcr-operator-asker.qa.desilo.co/projects'
    project_email = 'analyst6@desilo.ai'
    project_pw = 'desilo00@!'
    
        
    log_message("info", "====================================================== [DCR_E2E_automation_test START] ======================================================")
    
    try:
        log_message("info", "로그인 시작")
        admin.admin_login(admin_url, admin_email, admin_pw)
        provider.provider_login(provider_url, provider_email, provider_pw)
        project.project_login(project_url, project_email, project_pw)
        log_message("info", "로그인 완료")
        
        log_message("info", "시나리오1 시작")
        result01 = scene_01(driver, wait, provider, admin, project)
        log_message("info", "시나리오1 완료")

        log_message("info", "시나리오2 시작")
        result02 = scene_02(driver, wait, provider, admin, project)
        log_message("info", "시나리오2 완료")
        
        log_message("info", "시나리오3 시작")
        result03 = scene_03(driver, wait, provider, admin, project)
        log_message("info", "시나리오3 완료")
        
        log_message("info", "시나리오4 시작")
        result04 = scene_04(driver, wait, provider, admin, project)
        log_message("info", "시나리오4 완료")
        
        log_message("info", "시나리오5 시작")
        result05 = scene_05(driver, wait, provider, admin, project)
        log_message("info", "시나리오5 완료")
        
        log_message("info", "시나리오6 시작")
        result06 = scene_06(driver, wait, provider, admin, project)
        log_message("info", "시나리오6 완료")
        
        log_message("info", "시나리오7 시작")
        result07 = scene_07(driver, wait, provider, admin, project)
        log_message("info", "시나리오7 완료")
        
        log_message("info", "시나리오8 시작")
        result08 = scene_08(driver, wait, provider, admin, project)
        log_message("info", "시나리오8 완료")
        
        log_message("info", "시나리오9 시작")
        result09 = scene_09(driver, wait, provider, admin, project)
        log_message("info", "시나리오9 완료")
        
        # log_message("info", "시나리오10 시작")
        # result10 = scene_10(driver, wait, provider, admin, project)
        # log_message("info", "시나리오10 완료")
        
        log_message("info", "시나리오11 시작")
        result11 = scene_11(driver, wait, provider, admin, project)
        log_message("info", "시나리오11 완료")
        

        # 봇 메세지 내부 내용
        attach_dict = {
            'color' : '#ff0000',
            'author_name' : 'Slack Bot Notice',
            'title' : title,
            'text' : f"""{now_date} {now_time} ```
        == [Scenario_#1] ==============
            {result01}
        == [Scenario_#2] ==============
            {result02}
        == [Scenario_#3] ==============
            {result03}
        == [Scenario_#4] ==============
            {result04}
        == [Scenario_#5] ==============
            {result05}
        == [Scenario_#6] ==============
            {result06}
        == [Scenario_#7] ==============
            {result07}
        == [Scenario_#8] ==============
            {result08}
        == [Scenario_#9] ==============
            {result09} 
        == [Scenario_#11] ==============
            {result11}     
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
        log_message("info", "====================================================== [DCR_E2E_automation_test END] ======================================================")


#%%
if __name__ == "__main__":
    main()
    
    
    
