from selenium import webdriver
import pandas as pd
import os
import xlrd,xlwt
from xlutils.copy import copy
import time

base_url = 'http://webapi.cninfo.com.cn/#/dataBrowse'

def Spider():
    code_list = ['002671']  # , '002671', '300813', '688100'  # 股票代码列表
    jianchen_list = []
    hangye_list = []

    # 读取文件股票代码
    # df = pd.read_excel(r'zichanfuzhai.xls', converters={u'股票代码': str})
    # df_li = df.values.tolist()
    # for s_li in df_li:
    #     code_list.append(s_li[0])
    #     jianchen_list.append(s_li[3])
    #     hangye_list.append(s_li[4])
    # print(code_list)
    for code in code_list:
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(base_url)
        driver.find_element_by_xpath('//*[@id="commnHeader"]/div[2]/div[1]/div/div[1]/ul/li[7]/a').click() # 点击财务指标
        driver.find_element_by_xpath('//*[@id="commnHeader"]/div[2]/div[2]/div/div[1]/ul[4]/li[1]/a').click() # 点击报告期
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="commnHeader"]/div[2]/div[3]/div/div[1]/ul[1]/li[1]/a').click() # 点击资产负债
        driver.find_element_by_xpath('//*[@id="input_code"]').send_keys(code)  # 输入股票名称

        driver.find_element_by_xpath('//*[@id="se1_sele"]').send_keys('0')

        # driver.find_element_by_xpath('//*[@id="se1_sele"]').send_keys('2019')
        #
        # driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div/div/div[1]/div/div[4]/div[2]/select').click() # 点击季报下拉框
        # driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div/div/div[1]/div/div[4]/div[2]/select/option[3]').click() # 选择三季报
        # driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div/div/div[1]/div/button').click()
        time.sleep(5)

Spider()



