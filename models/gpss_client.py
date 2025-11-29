# models/gpss_client.py
from playwright.sync_api import sync_playwright
import os
import json

class GPSSClient:
    """負責與 GPSS API 進行通訊的客戶端類別"""
    
    def __init__(self, browser):
        # 啟動瀏覽器並存入 self
        self.context = browser.new_context()
        self.page = self.context.new_page()
        self.home_url = "https://tiponet.tipo.gov.tw/gpss2/gpsskmc/gpssbkm"
        self.page.goto(self.home_url)
        self.page.wait_for_load_state()
        self.page2 = None
    
    def fetch_data(self, query):
        self.login()
        self.search(query)
        self.dedup_by_family()
        self.dedup_by_search()
        self.fetch_diagrams()
        self.add_to_list()
        self.fetch_names_and_contents()
        self.add_to_matrix()
        self.go_to_matrix()

    def login(self):
        curr_url = "https://tiponet.tipo.gov.tw" + self.page.locator("a:has(span[title='登入'])").get_attribute("href")
        self.page.goto(curr_url)
        self.page.wait_for_load_state()
        self.page.locator("input[name='email']").fill("")
        self.page.locator("input[type='PASSWORD']").fill("")
        self.page.wait_for_url(lambda url: url != curr_url, timeout=0)
        self.page.wait_for_load_state()
        self.home_url = "https://tiponet.tipo.gov.tw" + self.page.locator(".navbar-header > a").get_attribute("href")
    
    def search(self, query):
        self.page.goto(self.home_url)
        self.page.wait_for_load_state()
        curr_url = self.page.url
        self.page.get_by_role("textbox").fill(query)
        self.page.locator("input[src*='search_btn.png']").click()
        self.page.wait_for_load_state()
        return self.page.url
    
    def dedup_by_family(self):
        self.page.locator("input[value='家族去重']").click(timeout = 0)        
    
    def dedup_by_search(self):
        self.page.locator("input[value='檢索去重']").click(timeout = 0)        
    
    def add_to_list(self):
        self.page.locator("input[title='本次全選']").click()
        self.page.wait_for_load_state()
        self.page.locator("input[title='加入標記清單']").click()
        self.page.wait_for_load_state()

    def fetch_diagrams(self):
        with self.context.expect_page(timeout=0) as new_page_info:
            self.page.locator("div.show_chart").click(timeout=0)     
        self.page2 = new_page_info.value
        self.page2.wait_for_selector("a.chdw", timeout = 0)
        buttons = self.page2.locator("a.chdw", has_text="資料表下載").all()

        self.page2.locator("select[name='fld4']").select_option("YP_0")
        self.page2.locator("select[name='limit4']").select_option("4")
        with self.page2.expect_download() as download_info:
            buttons[1].click()
            self.page2.wait_for_load_state()
        download = download_info.value
        file_name = f"diagram_{1}.html"
        destination_path = os.path.join(os.getcwd() + "/.data", file_name)
        download.save_as(destination_path)

        self.page2.locator("select[name='limit2']").select_option("30")
        self.page2.locator("select[name='fld2']").select_option("AX")
        with self.page2.expect_download() as download_info:
            buttons[2].click()
        download = download_info.value
        file_name = f"diagram_{2}.html"
        destination_path = os.path.join(os.getcwd() + "/.data", file_name)
        download.save_as(destination_path)

        self.page2.locator("select[name='limit2']").select_option("30")
        self.page2.locator("select[name='fld2']").select_option("AY")
        with self.page2.expect_download() as download_info:
            buttons[2].click()
        download = download_info.value
        file_name = f"diagram_{3}.html"
        destination_path = os.path.join(os.getcwd() + "/.data", file_name)
        download.save_as(destination_path)

        self.page2.locator("select[name='limit2']").select_option("30")
        self.page2.locator("select[name='fld2']").select_option("IP3")
        with self.page2.expect_download() as download_info:
            buttons[2].click()
        download = download_info.value
        file_name = f"diagram_{4}.html"
        destination_path = os.path.join(os.getcwd() + "/.data", file_name)
        download.save_as(destination_path)


        self.page2.close()

    def fetch_names_and_contents(self):
        curr_url = "https://tiponet.tipo.gov.tw" + self.page.locator("a:has-text('標記清單')").get_attribute("href")
        self.page2 = self.context.new_page()
        self.page2.goto(curr_url)
        self.page2.wait_for_load_state()
        self.page2.locator("input[title='下載全選']").click()

        self.page2.locator("span[data-target='#outpop']").click()
        modal = self.page2.locator("div[id='outpop']")
        modal.locator("input[value='全不選']").click()
        modal.locator("input[name='_9_11_S_TI']").click()
        modal.locator("input[name='_9_11_S_AB']").click()

        with self.page2.expect_download(timeout = 0) as download_info:
            modal.locator("input[title='執行輸出']").click(timeout = 0)
        download = download_info.value
        file_name = f"contents.xls"
        destination_path = os.path.join(os.getcwd() + "/.data", file_name)
        download.save_as(destination_path)
        
        modal.locator("span[class='modal_close']").click()

        self.page2.close()

    def add_to_matrix(self):
        button = self.page.locator("input[title='檢索歸類']")
        button.evaluate("element => element.click()")
        self.page.wait_for_selector("div[class='msgfmt']", timeout = 0)

    def go_to_matrix(self):
        with self.context.expect_page() as new_page_info:
            self.page.locator("div[class='msgfmt'] a[target='_proj']").click()
        self.page2 = new_page_info.value
        self.page2.wait_for_load_state()
        with self.context.expect_page() as new_page_info:
            self.page2.locator("span[title='Matrix']").click()
        self.page2.close()
        self.page2 = new_page_info.value

    def fill_matrix_form(self, json_data):
        """
        將 JSON 資料填入技術功效矩陣表單
        :param json_data: 包含 technologies 和 efficacies 的字典
        """
        technologies = json_data.get("technologies", [])
        efficacies = json_data.get("efficacies", [])
        for _ in range(len(technologies) - 3):
            self.page2.locator("span[id='tech_add']").click()
        for i in range(len(efficacies) - 3):
            self.page2.locator("span[id='func_add']").click()

        # 1. 填寫【技術名稱】與【技術檢索條件】 (橫向 X 軸)
        # HTML name 格式: mtr/tech/name01, mtr/tech/term01 ... 到 06
        for i, tech in enumerate(technologies):
            # 索引從 0 開始，但 HTML name 是從 01 開始，所以要 i+1
            index_str = f"{i+1:02d}" # 格式化成 "01", "02"...
            
            # 填寫技術名稱 (Label)
            self.page2.locator(f"textarea[name='mtr/tech/name{index_str}']").fill(tech["label"])
            
            # 填寫技術檢索條件 (Boolean)
            self.page2.locator(f"textarea[name='mtr/tech/term{index_str}']").fill(tech["boolean"])

        # 2. 填寫【功效名稱】與【功效檢索條件】 (縱向 Y 軸)
        # HTML name 格式: mtr/func/name01, mtr/func/term01 ... 到 06
        for i, eff in enumerate(efficacies):
            index_str = f"{i+1:02d}"
            
            # 填寫功效名稱 (Label)
            self.page2.locator(f"textarea[name='mtr/func/name{index_str}']").fill(eff["label"])
            
            # 填寫功效檢索條件 (Boolean)
            self.page2.locator(f"textarea[name='mtr/func/term{index_str}']").fill(eff["boolean"])

        self.page2.locator("body").click()
        self.page2.locator("input[value='進行分析']").click()
        self.page2.locator("select[name='exp_format']").select_option("EXCEL")

        with self.page2.expect_download(timeout = 0) as download_info:
            self.page2.locator("input[title='Export']").click(timeout = 0)
        download = download_info.value
        file_name = f"matrix_form.xls"
        destination_path = os.path.join(os.getcwd() + "/.data", file_name)
        download.save_as(destination_path)