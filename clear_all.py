# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 09:20:12 2025

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


#%%
def main():
    
    # 봇 메세지에 출력할 날짜
    now = datetime.now()
    now_date = now.strftime('%Y.%m.%d')
    now_time = now.strftime('%H:%M:%S')
    
    print(f'Clear START {now_date} {now_time}')
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

    admin.admin_login(admin_url, admin_email, admin_pw)
    provider.provider_login(provider_url, provider_email, provider_pw)
    project.project_login(project_url, project_email, project_pw)
    
    provider.clear()
    time.sleep(3)
    
    admin.clear()
    time.sleep(3)
    
    project.clear()
    time.sleep(3)
    
#%%
if __name__ == "__main__":
    main()
    
    