# models/gpss_client.py
import requests
import pandas as pd
from config import API_URL
from playwright.sync_api import sync_playwright
import re
import base64
import os

class GPSSClient:
    """負責與 GPSS API 進行通訊的客戶端類別"""
    
    def __init__(self, browser):
        # 啟動瀏覽器並存入 self
        self.home_url = "https://tiponet.tipo.gov.tw/gpss2/gpsskmc/gpssbkm"
        self.url_prefix = "https://tiponet.tipo.gov.tw"
        self.context = browser.new_context()
        self.page = self.context.new_page()
        self.page.goto(self.home_url)
        self.login_url = self.url_prefix + self.page.locator("a:has(span[title='登入'])").get_attribute("href")

    def login(self):
        self.page.goto(self.login_url)

        self.page.locator("input[name='email']").fill("")
        self.page.locator("input[type='PASSWORD']").fill("")

        self.page.wait_for_url(lambda url: url != self.login_url, timeout=0)

        self.home_url = self.url_prefix + self.page.locator(".navbar-header > a").get_attribute("href")
    
    def fetch_data(self, query):
        self.search(query)
        self.page.locator("input[value='家族去重']").click()        
        self.page.wait_for_load_state()
        self.page.locator("input[value='檢索去重']").click()        
        self.page.wait_for_load_state()
        self.fetch_diagrams()

    def search(self, query):
        self.page.goto(self.home_url)
        curr_url = self.page.url
        self.page.get_by_role("textbox").fill(query)
        self.page.locator("input[src*='search_btn.png']").click()
        self.page.wait_for_load_state()
        return self.page.url
    
    def fetch_diagrams(self):
        with self.context.expect_page() as new_page_info:
            self.page.locator("div.show_chart").click()     
        new_page = new_page_info.value
        new_page.wait_for_load_state()
        new_page.wait_for_timeout(5000)
        buttons = new_page.query_selector_all("a.chdw")


        new_page.locator("select[name='fld4']").select_option("YP_0")
        new_page.locator("select[name='limit4']").select_option("4")
        new_page.locator("select[name='fld2']").select_option("IP3")
        new_page.locator("select[name='limit2']").select_option("30")


        for i in range(3):
            with new_page.expect_download() as download_info:
                buttons[i].click()
                new_page.wait_for_load_state()
            download = download_info.value
            file_name = f"diagram_{i+1}.html"
            destination_path = os.path.join(os.getcwd() + "/.data", file_name)
            download.save_as(destination_path)
        
        new_page.locator("select[name='fld2']").select_option("AY")
        with new_page.expect_download() as download_info:
            buttons[2].click()
        download = download_info.value
        file_name = f"diagram_{4}.html"
        destination_path = os.path.join(os.getcwd() + "/.data", file_name)
        download.save_as(destination_path)

        new_page.close()