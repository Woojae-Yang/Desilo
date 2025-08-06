# -*- coding: utf-8 -*-
"""
Created on Fri May  9 16:37:11 2025

@author: WoojaeYang
"""


##### 분석가 페이지

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime


class Project_Page:
    
    
    def __init__(self, driver, wait, tab):
        self.driver = driver
        self.wait = wait
        self.tab = tab
    
    def switch_tab(self):
        self.driver.switch_to.window(self.tab)
    
    def project_login(self, url, email, password):
        self.switch_tab()
        self.driver.get(url)

        id = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/form/div[1]/div[2]/div/input') 
        id.send_keys(email)

        pw = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/form/div[2]/div[2]/div/input')
        pw.click()
        pw.send_keys(password)

        login_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/form/div[3]/div/button')
        login_btn.click()
        time.sleep(2)
        
        # 한국어 설정
        setting_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[2]/button')
        setting_btn.click()
        time.sleep(2)
        
        ko_elem = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div/div[2]/div/div[1]')
        ko_elem.click()
        time.sleep(2)
    
    
    # 프로젝트 생성
    def create_project(self, today_date, scene_num):
        self.switch_tab()
        time.sleep(2)
        
        # LNB 프로젝트 페이지
        lnb_project = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[1]')
        lnb_project.click()
        time.sleep(3)
        
        # 프로젝트 생성 버튼 클릭
        create_proj_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[1]/div[2]/div/div/button')
        create_proj_btn.click()
        time.sleep(3)
        
        # 프로젝트 이름 입력
        global proj_name
        proj_name = f'[AUTO]project{today_date}_{scene_num}'
        proj_name_input = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/input')
        proj_name_input.click()
        proj_name_input.send_keys(proj_name)
        
        # 생성 버튼 클릭
        create_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div[2]/button')))
        create_btn.click()
        time.sleep(3)
    
        return proj_name
    
    
    # 프로젝트 진입
    def enter_project(self, proj_name):
        self.switch_tab()
        time.sleep(2)
        
        # LNB 프로젝트 페이지
        proj_tab = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[1]')
        proj_tab.click()
        time.sleep(3)
        
        # 프로젝트 선택
        for num in range(1, 10):
            try:
                proj_elem =self.wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div/div[{num}]/div/div[1]/div[1]')))
                text = proj_elem.text.strip()
                print(f"[{num}] 찾은 프로젝트 이름: {text}")
                if text == proj_name:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", proj_elem)
                    time.sleep(0.5)
                    self.driver.find_element(By.XPATH, f'/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div/div[{num}]').click()
                    break
            except NoSuchElementException:
                print(f"[INFO] div[{num}] 요소가 존재하지 않아 종료합니다.")
                break
        time.sleep(3)        
    
    
    # 워크플로우 생성
    def create_workflow(self, today_date, scene_num):
        self.switch_tab()
        time.sleep(1)
        
        # 워크플로우 생성 버튼 클릭
        create_wf = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div[3]/div[2]/div/button')))
        create_wf.click()
        time.sleep(3)
        
        # 워크플로우 이름 입력
        wf_name = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/input')
        wf_name.click()
        wf_name.send_keys(f'workflow_{today_date}_{scene_num}')
        time.sleep(3)
        

    # 프로젝트 삭제
    def del_proj(self, proj_name):
        self.switch_tab()
        time.sleep(2)
        
        # 프로젝트 탭
        proj_tab = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[1]')
        proj_tab.click()
        time.sleep(3)
        
        # 삭제할 프로젝트 진입
        proj_to_del = self.driver.find_element(By.XPATH, f'//div[contains(text(), "{proj_name}")]')    
        proj_to_del.click()
        time.sleep(3)
        
        # 삭제 버튼
        del_btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div[2]/div[3]/button')
        del_btn.click()
        time.sleep(3)
        
        # 확인 버튼
        ok_btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[3]/div[2]/button')
        proj_del_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ok_btn.click()
        time.sleep(3)
        
        return proj_del_time  
    
    
    # 쿼리 입력
    def input_query(self, query):
        self.switch_tab()
        time.sleep(2)
        
        # Editor 형식으로 전환
        editor_tab = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]')))
        editor_tab.click()

    
        # 입력 영역
        text_area = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/textarea')))
        text_area.click()
        text_area.send_keys(query)
        time.sleep(3)
        
        
    # 워크플로우 실행
    def start_workflow(self):
        self.switch_tab()
        time.sleep(3)
        
        # 분석 실행 버튼
        start_wf = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[1]/div[3]/div/div/button')))
        start_wf.click()

        
    # 쿼리 결과 확인
    def cehck_query_result(self, result_xpath):
        self.switch_tab()
        time.sleep(3)
        try:
            result = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, result_xpath))).text
            return f' {result} : Workflow Running OK'
        except Exception as e:
            return f'Workflow Running NG : {e}'
        
        
    # Onw-way ANOVA 설정 
    def set_anova(self, da_name):
        self.switch_tab()
        time.sleep(2)
        
        # 드롭다운 선택
        dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div')))
        dropdown.click()
        
        # 아노바 선택
        anova = self.driver.find_element(By.XPATH, '//div[contains(text(), "ANOVA")]')
        anova.click()
        
        # from절
        from_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div')
        from_btn.click()
        time.sleep(2)
        
        provider1_btn = self.driver.find_element(By.XPATH, '//div[contains(text(),"provider1")]')
        provider1_btn.click()
        
        # 데이터 에셋 선택
        da_select = self.driver.find_element(By.XPATH, f'//div[contains(text(),"{da_name}")]')
        da_select.click()
        time.sleep(2)
        
        ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        ok_btn.click()
        
        
        # DEPENDENT VARIABLE
        variable = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div')
        variable.click()
        time.sleep(3)
        
        self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div').click()
        height_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "키")]')))
        height_btn.click()
        time.sleep(2)
        
        var_confirm_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        var_confirm_btn.click()
        time.sleep(3)
        
        #FACTOR
        factor = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div')
        factor.click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div').click()
        gender_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "성별")]')))
        gender_btn.click()
        time.sleep(3)
        
        factor_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        factor_ok_btn.click()
        time.sleep(2)
        
    # Linear Regression 설정 
    def set_linear(self, da_name):
        self.switch_tab()
        time.sleep(2)
        
        # 드롭다운 선택
        dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div')))
        dropdown.click()
        
        # 선형회귀 선택
        linear = self.driver.find_element(By.XPATH, '//div[contains(text(), "Linear")]')
        linear.click()
        
        # from절
        from_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[4]/div[2]/div')
        from_btn.click()
        time.sleep(3)
        
        provider1_btn = self.driver.find_element(By.XPATH, '//div[contains(text(),"provider1")]')
        provider1_btn.click()
        
        # 데이터 에셋 선택
        da_select = self.driver.find_element(By.XPATH, f'//div[contains(text(),"{da_name}")]')
        da_select.click()
        time.sleep(3)
        
        ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[4]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        ok_btn.click()
        time.sleep(3)
                                                     
        # 종속변수
        dependent = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div')
        dependent.click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div').click()
        weight_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "몸무게")]')))
        weight_btn.click()
        time.sleep(3)
        
        dependent_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        dependent_ok_btn.click()
        time.sleep(3)
        
        # 독립변수
        independent = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div')
        independent.click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div').click()
        height_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "키")]')))
        height_btn.click()
        time.sleep(3)
        
        independent_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        independent_ok_btn.click()
        time.sleep(2)
        
        # DUMMY
        dummy = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div')
        dummy.click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div').click()
        gender_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "성별")]')))
        gender_btn.click()
        time.sleep(2)
        
        dummy_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        dummy_ok_btn.click()
        time.sleep(3)
        
        
    # Kaplan-Meier 설정 
    def set_kpe(self, da_name):
        self.switch_tab()
        time.sleep(2)
        
        # 드롭다운 선택
        dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div')))
        dropdown.click()
        
        # Kaplan-Meier 선택
        kpe = self.driver.find_element(By.XPATH, '//div[contains(text(), "Kaplan-Meier")]')
        kpe.click()
        time.sleep(2)
        
        # from절
        from_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div')
        from_btn.click()
        time.sleep(3)
        
        provider1_btn = self.driver.find_element(By.XPATH, '//div[contains(text(),"provider1")]')
        provider1_btn.click()
        
        # 데이터 에셋 선택
        da_select = self.driver.find_element(By.XPATH, f'//div[contains(text(),"{da_name}")]')
        da_select.click()
        time.sleep(2)
        
        da_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        da_ok_btn.click()
        time.sleep(2)
        
        # Time 컬럼
        time_col = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div')
        time_col.click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, 
                                 '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div').click()    
        time_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "TIME")]')))
        time_elem.click()
        time.sleep(2)    
        
        time_elem_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        time_elem_ok_btn.click()
        time.sleep(2)
        
        # 코호트 컬럼 - STATIN
        cohort_col = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div')
        cohort_col.click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, 
                                 '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div').click()    
        cohort_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "STATIN")]')))
        cohort_elem.click()
        time.sleep(3)    
            
        cohort_elem_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        cohort_elem_ok_btn.click()
        time.sleep(2)
            
        
        # 이벤트 컬럼 - DTH 1
        event_col = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div')
        event_col.click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, 
                                 '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div').click()
        event_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "DTH")]')))
        event_elem.click()
        time.sleep(2)
        
        indicator = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[2]/div[3]/div[2]/div/div[2]')))
        indicator.click()
        time.sleep(2)
        
        event_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        event_ok_btn.click()
        time.sleep(2)
            
    
    def set_cox(self, da_name):
        self.switch_tab()
        time.sleep(2)
        
        # 드롭다운 선택
        dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div')))
        dropdown.click()
        time.sleep(2)
        
        # COX 선택
        kpe = self.driver.find_element(By.XPATH, '//div[contains(text(), "Cox")]')
        kpe.click()
        time.sleep(2)
        
        # from 절
        from_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div')
        from_btn.click()
        time.sleep(2)
        
        provider1_btn = self.driver.find_element(By.XPATH, '//div[contains(text(),"provider1")]')
        provider1_btn.click()
        time.sleep(2)
        
        # 데이터 에셋 선택
        da_select = self.driver.find_element(By.XPATH, f'//div[contains(text(),"{da_name}")]')
        da_select.click()
        time.sleep(2)
        
        da_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/div/div[3]/div/div[2]/button')
        da_ok_btn.click()
        time.sleep(2)
        
        # Time 컬럼
        time_col = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div')
        time_col.click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, 
                                 '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div').click()    
        time_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "TIME")]')))
        time_elem.click()
        time.sleep(2)    
        
        time_elem_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        time_elem_ok_btn.click()
        time.sleep(2)
        
        # 코호트 컬럼 - STATIN
        cohort_col = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div')
        cohort_col.click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, 
                                 '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div').click()    
        cohort_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "STATIN")]')))
        cohort_elem.click()
        time.sleep(2)    
            
        cohort_elem_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        cohort_elem_ok_btn.click()
        time.sleep(2)
            
        
        # 이벤트 컬럼 - DTH 1
        event_col = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div')
        event_col.click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, 
                                 '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div').click()
        event_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "DTH")]')))
        event_elem.click()
        time.sleep(2)
        
        indicator = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[2]/div[3]/div[2]/div/div[2]')))
        indicator.click()
        time.sleep(2)
        
        event_ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[3]/div/div[2]/button')
        event_ok_btn.click()
        time.sleep(2)
        
        
    #CLEAR    
    def clear(self):
        self.switch_tab()
        time.sleep(2)
        print("Project Clearing")
        
        # LNB 프로젝트 진입
        ds_tab = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[1]')))
        ds_tab.click()
        time.sleep(3)
        
        # 프로젝트 목록
        proj_list = '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div'
        proj_btns = self.driver.find_elements(By.XPATH, proj_list + '/div')
        print(len(proj_btns))
        
        for num in range(len(proj_btns), 0, -1):
            proj_btn = self.driver.find_element(By.XPATH, f'/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div/div[{num}]/div/div[1]/div[1]/div[2]')
            proj_name = proj_btn.text
            
            if 'AUTO' in proj_name:
                proj_btn.click()
                time.sleep(7)
                
                del_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div[2]/div[3]/button')))
                del_btn.click()
                time.sleep(2)
                
                del_btn_modal = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[3]/div[2]/button')
                del_btn_modal.click()
                time.sleep(2)
                print(f'{proj_name} 삭제 완료')

   
        

