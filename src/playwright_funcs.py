from playwright.sync_api import sync_playwright
import http.client as httplib

mslink = "https://forms.office.com/Pages/DesignPageV2.aspx?" + \
         "origin=NeoPortalPage&subpage=design&id=hGiVYK0Q-" + \
         "kCGPU8yweOjemYNbVVriiJHgFdevpzMcOZUNDMwWVlPTkdYOD" + \
         "A1RFRUMUs4VkFTRTgwSSQlQCN0PWcu&analysis=true"
cookies = None
new_navigation = True

def check_connection():
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except:
        return False
    finally:
        conn.close()

def get_login():
    '''
    This function gets the login cookies for the MS
    page needed to run the rest of the playwright
    functions, which are used to grab and download
    the PDFs of the Scheduling Surveys.
    '''
    global cookies
    try:
        with sync_playwright() as pw:
            login_browser = pw.chromium.launch(headless=False)
            p = login_browser.new_page()
            p.goto(mslink)
            p.wait_for_event('load')
            while p.url != mslink:
                p.wait_for_timeout(5000)
            cookies = p.context.cookies()
            login_browser.close()
            return cookies
    except:
        return None

def navigate_to_results(page):
    page.goto(mslink)
    page.locator("//html/body/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/button").click()

def get_survey(page, ssid, save_path, *, new_navigation = False, prev_ssids = [3]):
    if new_navigation:
        page.fill(f"input[value='{prev_ssids[0]}']", f"{ssid}")
    else:
        page.fill(f"input[value='{prev_ssids[-1]}']", f"{ssid}")
    page.wait_for_timeout(600)
    prev_ssids.append(ssid)
    page.pdf(path=save_path)