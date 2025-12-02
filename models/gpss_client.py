# models/gpss_client.py
from playwright.sync_api import sync_playwright
import os
from services.captcha import CaptchaSolver
import re

class GPSSClient:
    
    def __init__(self, browser):
        self.context = browser.new_context()
        self.search_page = self.context.new_page()

        self.home_url = "https://tiponet.tipo.gov.tw/gpss2/gpsskmc/gpssbkm"
        self.login_url = "https://tiponet.tipo.gov.tw/gpss2/gpsskmc/gpssbkm"
        self.search_url = "https://tiponet.tipo.gov.tw/gpss2/gpsskmc/gpssbkm"
        self.list_url = "https://tiponet.tipo.gov.tw/gpss2/gpsskmc/gpssbkm"
        self.diagrams_url = "https://tiponet.tipo.gov.tw/gpss2/gpsskmc/gpssbkm"

        self.search_result = None
        self.dedup_result = None

    def download_data(self, filename, trigger, page):
        with page.expect_download(timeout = 0) as download_info:
            trigger.click(timeout = 0)
        download = download_info.value
        destination_path = os.path.join(os.getcwd() + "/.data", filename)
        download.save_as(destination_path)
    
    def open_new_page(self, trigger):
        with self.context.expect_page(timeout=0) as new_page_info:
            trigger.click(timeout=0)
        return new_page_info.value

    def get_num(self, trigger):
        text = trigger.text_content()
        text = re.sub(r'[^\d.]', '', text)
        return int(float(text))

    def login(self, account, password):
        page = self.context.new_page()
        page.goto(self.home_url)
        page.wait_for_load_state()
        self.login_url = "https://tiponet.tipo.gov.tw" + page.locator("a:has(span[title='登入'])").get_attribute("href")
        page.goto(self.login_url)
        page.wait_for_load_state()
        for _ in range(10):
            page.locator("input[name='email']").fill(account)
            page.locator("input[type='PASSWORD']").fill(password)

            auth = ""
            imgs = page.locator("table[class='rand'] img").all()
            for img in imgs:
                img_bytes = img.screenshot()            
                auth += CaptchaSolver.solve(img_bytes)

            page.locator("input[name='sys/00/rand']").fill(auth)
            page.locator("input[value='登入/Login']").click()
            page.wait_for_load_state("networkidle")
            if page.get_by_text("登出", exact=True).is_visible():
                self.home_url = "https://tiponet.tipo.gov.tw" + page.locator(".navbar-header > a").get_attribute("href")
                page.close()
                return True
        page.close()
        return False

    def fetch_data(self, query):
        self.search(query)
        self.fetch_diagrams()
    
    def search(self, query):
        self.search_page.goto(self.home_url)
        self.search_page.wait_for_load_state()

        self.search_page.get_by_role("textbox").fill(query)
        self.search_page.locator("input[src*='search_btn.png']").click()
        self.search_page.wait_for_load_state()

        self.search_page.locator("div[id='subdbdiv'] li").filter(has_text="全部").locator(":scope:not(.waiting)").locator("a").click(timeout=0)
        self.search_page.wait_for_load_state()
        self.search_result = self.get_num(self.search_page.locator("font[class='numfmt']").first)
        self.search_page.locator("input[value='家族去重']").click(timeout = 0)
        self.search_page.locator("input[value='檢索去重']").click(timeout = 0)    

        self.dedup_result = self.get_num(self.search_page.locator("font[class='numfmt']").first)

        self.search_url = self.search_page.url

    def fetch_diagrams(self):
        page = self.open_new_page(self.search_page.locator("div.show_chart"))

        self.diagrams_url = page.url

        page.wait_for_selector("a.chdw", timeout = 0)
        buttons = page.locator("a.chdw", has_text="資料表下載").all()

        page.locator("select[name='fld4']").select_option("YP_0")
        page.locator("select[name='limit4']").select_option("4")
        self.download_data("diagram_1.html", buttons[1], page)

        page.locator("select[name='limit2']").select_option("30")
        page.locator("select[name='fld2']").select_option("AX")
        self.download_data("diagram_2.html", buttons[2], page)

        page.locator("select[name='limit2']").select_option("30")
        page.locator("select[name='fld2']").select_option("AY")
        self.download_data("diagram_3.html", buttons[2], page)

        page.locator("select[name='limit2']").select_option("30")
        page.locator("select[name='fld2']").select_option("IP3")
        self.download_data("diagram_4.html", buttons[2], page)

        page.close()

    def fetch_names_and_contents(self):
        self.search_page.locator("input[title='本次全選']").click(timeout = 0)
        self.search_page.locator("input[title='加入標記清單']").click(timeout = 0)

        self.list_url = "https://tiponet.tipo.gov.tw" + self.search_page.locator("a:has-text('標記清單')").get_attribute("href")
        page = self.context.new_page()
        page.goto(self.list_url)
        page.wait_for_load_state()

        page.locator("input[title='下載全選']").click()
        page.locator("span[data-target='#outpop']").click()
        modal = page.locator("div[id='outpop']")
        modal.locator("input[value='全不選']").click()
        modal.locator("input[name='_9_11_S_TI']").click()
        modal.locator("input[name='_9_11_S_AB']").click()

        self.download_data("contents.xls", modal.locator("input[title='執行輸出']"), page)
        modal.locator("span[class='modal_close']").click()

        page.close()

    def fill_matrix_form(self, json_data):
        self.search_page.locator("input[title='本次全選']").click(timeout = 0)
        button = self.search_page.locator("input[title='檢索歸類']")
        button.evaluate("element => element.click()")
        self.search_page.wait_for_selector("div[class='msgfmt']", timeout = 0)

        page_temp = self.open_new_page(self.search_page.locator("div[class='msgfmt'] a[target='_proj']"))
        page = self.open_new_page(page_temp.locator("div[id='mtrdiv']"))
        page_temp.close()
        page.wait_for_selector("span[id='tech_add']", timeout = 0)

        technologies = json_data.get("technologies", [])
        efficacies = json_data.get("efficacies", [])

        for _ in range(len(technologies) - 3):
            page.locator("span[id='tech_add']").click()
        for i in range(len(efficacies) - 3):
            page.locator("span[id='func_add']").click()


        for i, tech in enumerate(technologies):
            index_str = f"{i+1:02d}"
            
            page.locator(f"textarea[name='mtr/tech/name{index_str}']").fill(tech["label"])
            page.locator(f"textarea[name='mtr/tech/term{index_str}']").fill(tech["boolean"])

        for i, eff in enumerate(efficacies):
            index_str = f"{i+1:02d}"
            
            page.locator(f"textarea[name='mtr/func/name{index_str}']").fill(eff["label"])            
            page.locator(f"textarea[name='mtr/func/term{index_str}']").fill(eff["boolean"])

        page.locator("body").click()
        page.locator("input[value='進行分析']").click()
        page.locator("select[name='exp_format']").select_option("EXCEL")

        self.download_data("matrix_form.xls", page.locator("input[title='Export']"), page)

        page.close()

    def get_results(self):
        return [self.search_result, self.dedup_result]