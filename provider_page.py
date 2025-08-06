# -*- coding: utf-8 -*-
"""
Created on Fri May  9 16:23:13 2025

@author: WoojaeYang
"""


##### Provider 페이지

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime



class Provider_Page:
    def __init__(self, driver, wait, tab):
        self.driver = driver
        self.wait = wait
        self.tab = tab
        
    def switch_tab(self):
        self.driver.switch_to.window(self.tab)

    def provider_login(self, url, email, password):
        self.switch_tab()
        self.driver.get(url)

        id = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/form/div[1]/div[2]/div/input') 
        id.send_keys(email)

        pw = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/form/div[2]/div[2]/div/input')
        pw.click()
        pw.send_keys(password)

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

    
    # 데이터 등록 화면으로 이동
    def move_to_data_registration(self):
        self.switch_tab()
        time.sleep(3)
        
        lnb_data_asset = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[1]')
        lnb_data_asset.click()
        time.sleep(3)
        
        register_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[1]/div[2]/div/div/button')))
        register_btn.click()
        time.sleep(3)
    
    
    # 데이터 등록 화면
    def data_registration(self, da_name, today_date):
        self.switch_tab()
        time.sleep(2)

        # 데이터 에셋 이름
        data_asset_name = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div[1]/div[3]/div/input')))
        data_asset_name.click()
        data_asset_name.send_keys(f'{da_name}')
        
        # 데이터 에셋 설명
        da_discrip = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div[1]/textarea')
        da_discrip.click()
        da_discrip.send_keys(f'E2E_auto_test_{da_name}_{today_date}')
        time.sleep(3)
    
    
    # 자동 승인 체크박스
    def click_approval_box(self):
        time.sleep(2)
        
        approval_box = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div[1]')
        approval_box.click()
        time.sleep(3)
    
    
    # 파일 업로드 - hospital.csv
    def upload_file(self):
        self.switch_tab()
        time.sleep(2)
        
        upload_area = self.driver.find_element(By.CSS_SELECTOR, '#root > div.Layout_Container__Nzz07 > div.Layout_HeaderContentContainer__LMWZ7 > div.Layout_ContentContainer__FdIQP.Layout_Scrollable__Ti0QR > div > div > div.DataAssetUploadDragAndDrop_Container__ER86Q > div:nth-child(2) > input[type=file]')
        self.driver.execute_script("arguments[0].style.display = 'block';", upload_area)
        
        file_path = r'/home/ywj/venv-auto/dcr_e2e/hospital.csv'
        
        upload_area.send_keys(file_path)
      
        
    # 파일 업로드 - main4.csv  
    def upload_file_main4(self):
        self.switch_tab()
        time.sleep(2)
        
        upload_area = self.driver.find_element(By.CSS_SELECTOR, '#root > div.Layout_Container__Nzz07 > div.Layout_HeaderContentContainer__LMWZ7 > div.Layout_ContentContainer__FdIQP.Layout_Scrollable__Ti0QR > div > div > div.DataAssetUploadDragAndDrop_Container__ER86Q > div:nth-child(2) > input[type=file]')
        self.driver.execute_script("arguments[0].style.display = 'block';", upload_area)
        
        file_path = r'/home/ywj/venv-auto/dcr_e2e/main4.csv'
        
        upload_area.send_keys(file_path)
    
    
    # 등록
    def register(self):
        self.switch_tab()
        time.sleep(2)
        
        # 다음 버튼 클릭
        next_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[1]/div[3]/div/div/button')
        next_btn.click()
        time.sleep(2)
    
        # 등록 버튼 클릭
        register_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[1]/div[3]/div[2]/div/button')))
        register_btn.click()
        time.sleep(3)
        
        
    # 승인 확인 진입
    def enter_query_approval(self, da_name):
        self.switch_tab()
        time.sleep(2)
        
        # 쿼리 승인 관리 탭
        query_approval_management = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[2]')))
        query_approval_management.click()
        
        # 승인 대기
        peding_tab = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div/div[1]/div[1]')))
        peding_tab.click()
        time.sleep(3)
        
        # 데이터 에셋 클릭
        da_approval = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "{da_name}")]')))
        da_approval.click()
        time.sleep(5)
        
        
    # 쿼리 승인
    def approve_query(self):
        self.switch_tab()
        time.sleep(2)
        
        #쿼리 승인 버튼
        approve_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div[1]/div[3]/div[2]/div/button')))
        approve_btn.click()
        time.sleep(3)
        
        
    # 쿼리 거절
    def reject_query(self):
        self.switch_tab()
        time.sleep(2)         
        
        #거절 버튼
        approve_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[1]/div[3]/div[1]/div/button')
        approve_btn.click()
        time.sleep(3)
         
        reject_reason = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div/textarea')
        reject_reason.click()
        reject_reason.send_keys('Automation Test')
        time.sleep(3)
        
        # 완료 및 거절 버튼 클릭
        reject_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div/div/div[1]/div/div[3]/div/div[2]/button')
        reject_btn.click()
        time.sleep(3)
        
        
    # 데이터 에셋 삭제
    def del_da(self, da_name):
       self.switch_tab()
       time.sleep(2)
       
       # 데이터 에셋 탭
       da_tab = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[1]')
       da_tab.click()
       time.sleep(3)
        
       # 데이터 에셋 클릭
       da_to_del = self.driver.find_element(By.XPATH, f'//div[contains(text(), "{da_name}")]')    
       da_to_del.click()
       time.sleep(3)
       
       # 삭제 버튼
       del_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[1]/div[3]/div[1]/div/button')
       del_btn.click()
       time.sleep(3)
       
       # 확인 버튼
       ok_btn = self.driver.find_element(By.XPATH, '/html/body/div/div[4]/div/div[3]/div[2]/button')
       da_del_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       ok_btn.click()
       
       return da_del_time
        
        
    #CLEAR    
    def clear(self):
        self.switch_tab()
        time.sleep(2)
        print("Provider Clearing")
        
        # LNB 데이터 에셋 진입
        da_tab = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/button[1]')))
        da_tab.click()
        time.sleep(3)
        
        da_list = '/html/body/div/div[1]/div[3]/div[2]/div/div/div[3]'
        da_elem = self.driver.find_elements(By.XPATH, da_list + '/div')
        
        for num in range(len(da_elem), 0 ,-1):
            da_btn = self.driver.find_element(By.XPATH, f'/html/body/div/div[1]/div[3]/div[2]/div/div/div[3]/div[{num}]/div[1]')
            da_name = da_btn.text.strip()
            
            if 'AUTO' in da_name:
                
                da_btn.click()
                time.sleep(7)
                
                del_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[3]/div[1]/div[3]/div[1]/div/button')))
                del_btn.click()
                time.sleep(2)
                
                del_btn_modal = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[3]/div[2]/button')
                del_btn_modal.click()
                time.sleep(2)
                print(f'{da_name} 삭제 완료')

                
    

    
    