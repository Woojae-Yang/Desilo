# -*- coding: utf-8 -*-
"""
Created on Fri May  9 15:07:11 2025

@author: WoojaeYang
"""


##### Admin 페이지

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime


class Admin_Page:
    def __init__(self, driver, wait, tab):
        self.driver = driver
        self.wait = wait
        self.tab = tab
    
    def switch_tab(self):
        self.driver.switch_to.window(self.tab)

    def admin_login(self, url, email, password):
        self.switch_tab()
        self.driver.switch_to.window(self.tab)
        self.driver.get(url)
        time.sleep(2)

        id = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/form/div[1]/div[2]/div/input') 
        id.send_keys(email)
        time.sleep(2)

        pw = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/form/div[2]/div[2]/div/input')
        pw.click()
        pw.send_keys(password)
        time.sleep(2)

        login_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/form/div[3]/div/button')
        login_btn.click()
        time.sleep(3)
        
        # 한국어 설정
        setting_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[2]/button')
        setting_btn.click()
        time.sleep(3)
        
        ko_elem = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div/div[2]/div/div[1]')
        ko_elem.click()
        time.sleep(3)


    #데이터 스페이스로 이동
    def move_to_dat_space(self):
        self.switch_tab()   
        ds_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[2]')))
        ds_btn.click()
        time.sleep(1)
        
        
    # 데이터 스페이스 추가     
    def add_ds(self, today_date, scene_num):
        self.switch_tab()
        add_ds_btn = self.wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div[1]/div[2]/div/div/button')))
        add_ds_btn.click()
        time.sleep(3)
        
        # 데이터 스페이스 이름 입력
        global ds_name
        ds_name = f'AUTO[{scene_num}]_{today_date}'
        ds_name_input = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div[2]/div/input')
        ds_name_input.click()
        ds_name_input.send_keys(ds_name)
        
        # 추가 버튼 클릭
        add_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div/div[3]/div/div[2]/button')
        add_btn.click()
        
        time.sleep(3)
        
        return ds_name
        
        
    #데이터 제공자 배정
    def assign(self, today_date):
        self.switch_tab()
        time.sleep(2)
        
        # 데이터 스페이스 선택
        ds_btn = self.driver.find_element(By.XPATH, f'//div[contains(text(), "{ds_name}")]')
        ds_btn.click()
        time.sleep(2)
        
        # 데이터 제공자 배정
        try:
            assign_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button')))
            assign_btn.click()
            time.sleep(3)
            
            # provider1  선택
            provider1 = self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div')))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", provider1)
            provider1.click()
            time.sleep(3)
            #print('provider1 선택')
            
            # 배정 버튼 클릭
            final_assign_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[3]/div[2]/div[2]/button')))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", final_assign_btn)
            final_assign_btn.click()
            time.sleep(3)
            #print('배정 버튼 클릭')
        
        except TimeoutException:
            print("[INFO] 데이터 제공자 배정 타임아웃 : 생략")
            try:
                total_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.set_window_size(1920, total_height)
                self.driver.save_screenshot(f'assign_timeout_debug_{today_date}.png')
                print("[DEBUG] Timeout fullpage screenshot saved")
            except Exception as e:
                print("[ERROR] Screenshot failed:", e)
        
        except Exception as e:
            print(f"[ERROR] Unexpected exception: {e}")
            self.driver.save_screenshot(f'assign_exception_debug_{today_date}.png')
            print("[DEBUG] Exception screenshot saved")
        
        time.sleep(2)


    # 데이터 에셋 추가
    def add_da(self, scene_num):
        self.switch_tab()
        time.sleep(2)
        
        # 데이터 에셋 리스트
        ds_list = self.driver.find_element(By.XPATH ,'/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]')
        ds_list.click()
        
        # 데이터 에셋 추가 버튼
        add_da_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[2]/div[3]/button')))
        add_da_btn.click()
        time.sleep(3)
        
        # 추가할 데이터 에셋
        scene_num = str(scene_num).strip()
        da_select = self.wait.until(EC.element_to_be_clickable((By.XPATH, '( /html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/* )[last()]')))
        self.driver.execute_script("arguments[0].click();", da_select)
        #da_select.click()
        time.sleep(3)
        
        # 추가 버튼 클릭
        ds_add_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[3]/div/div[2]/button')
        ds_add_btn.click()
        time.sleep(3)
    
    
    # 분석가 추가
    def add_analyst(self):
        self.switch_tab()
        time.sleep(2)
        
        # 분석가 리스트
        analyst_list = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[2]')
        analyst_list.click()
        
        # 분석가 목록 탭
        analyst_list = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[2]')))
        analyst_list.click()
        time.sleep(3)
        
        # 분석가 추가 버튼
        add_analyst_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[2]/div[3]/button')
        add_analyst_btn.click()
        time.sleep(3)
        
        # 분석가 추가
        try:
            analyst = self.driver.find_element(By.XPATH, '//span[contains(text(), "analyst6@desilo.ai")]')
            analyst.click()
            time.sleep(3)
            
            # 추가 버튼
            anal_add_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[3]/div/div[2]/button')
            anal_add_btn.click()
            
        except Exception as e:
            print('[INFO] 분석가 배정 생략 ')
            cancel_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[3]/div/div[1]/button')
            cancel_btn.click()
        
      
    # 가비지 컬렉션
    def run_garbage_collection(self, now_time):
        self.switch_tab()
        time.sleep(2)
        
        # 가비지 컬렉션 진입
        garbage_collection_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[5]')
        garbage_collection_btn.click()
        time.sleep(3)
        
        # 실행 버튼
        run_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[1]/div[2]/div/div/button')
        run_btn.click()
        
        time.sleep(3)

        status = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div[3]').text
        self.wait.until(lambda d: d.find_element(By.XPATH,
            '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div[3]'
            ).text.strip() == "DONE")
        
        end_time = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div[5]').text
        
        return status, end_time
        
    # 암호화 키
    def key_gen(self):
        self.switch_tab()
        time.sleep(2)
        
        # 암호화 키 관리 진입
        key_management_tab = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[4]')))
        key_management_tab.click()
        time.sleep(2)
        
        # 키 생성
        create_key_btn  = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div/div[2]/button')
        create_key_btn.click()
        time.sleep(3)
        create_key_btn.click()  # 키 하나 더 생성
        time.sleep(10)
        
        refresh = 0
        
        while refresh < 20:
            try:
                status = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/table/tbody[1]/tr/td[4]/div').text.strip()
                if status == '사용 중' or 'Active':
                    break
                else:
                    self.driver.refresh()
                    time.sleep(10)
                    refresh += 1
            except Exception as e:
                print(f" 상태 확인 중 예외 발생: {e} — 새로고침")
                self.driver.refresh()
                time.sleep(5)
                refresh += 1
        
        else:
            raise TimeoutError("상태 전환 미응답")

        action02_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/table/tbody[2]/tr/td[4]/div/button')))
        action02_btn.click()
        
        
    # 데이터 스페이스 제거
    def del_ds(self, ds_name):
        self.switch_tab()
        time.sleep(2)
        
        # 데이터 스페이스 진입
        ds_tab = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[2]')))
        ds_tab.click()
        time.sleep(3)
        
        #
        ds_to_del = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "{ds_name}")]')))
        ds_to_del.click()
        time.sleep(3)
        
        del_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/button')
        del_btn.click()
        time.sleep(3)
        
        ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[3]/div/div[2]/button')
        ds_del_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ok_btn.click()
        time.sleep(3)
        
        return ds_del_time
            
    
    # 감사 로그 확인
    def check_log(self):
        self.switch_tab()
        time.sleep(2)
        
        # 감사 로그 탭 진입
        log_tab = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[6]')
        log_tab.click()
        time.sleep(3)
        
        # 로그 생성 시간
        created_time = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[1]').text
                                                          
        # 로그 내용
        event_detail = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/div[2]').text
        
        return created_time, event_detail
        
    #CLEAR    
    def clear(self):
        self.switch_tab()
        time.sleep(2)
        print("Admin Clearing")
        
        # 데이터 스페이스 진입
        ds_tab = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[2]')))
        ds_tab.click()
        time.sleep(3)
        
        # 데이터 스페이스 목록
        ds_list = '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div[2]'
        ds_elem = self.driver.find_elements(By.XPATH, ds_list + '/button')
        
        for num in range(len(ds_elem), 0, -1):
            ds_btn = self.driver.find_element(By.XPATH, f'/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div[2]/button[{num}]/div/div/div/div')
            ds_name = ds_btn.text.strip()
            
            if 'AUTO' in ds_name:
                
                ds_btn.click()
                time.sleep(2)
                
                del_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/button')
                del_btn.click()
                time.sleep(2)
                
                del_btn_modal = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[3]/div/div[2]/button')
                del_btn_modal.click()
                time.sleep(2)
                print(f'{ds_name} 삭제 완료')
                

   
        
        
        
