from playwright.sync_api import sync_playwright
import http.client as httplib

mslink = "https://forms.office.com/Pages/DesignPageV2.aspx?" + \
         "origin=NeoPortalPage&subpage=design&id=hGiVYK0Q-" + \
         "kCGPU8yweOjemYNbVVriiJHgFdevpzMcOZUNDMwWVlPTkdYOD" + \
         "A1RFRUMUs4VkFTRTgwSSQlQCN0PWcu&analysis=true"
cookies = None

def check_connection():
    '''
    This function checks for a network connection.

    Returns:
        True if a successful network connection is
        established, False otherwise.
    '''
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
    '''
    This function navigates the page to the
    Microsoft Forms result page.

    Parameters:
        - page: playwright.sync_api.Page
            The page used to navigate to the results.
    '''
    page.goto(mslink)
    page.locator("//html/body/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/button").click()

def get_survey(page, ssid, save_path, *, new_navigation = False, prev_ssids = [3]):
    '''
    This function searches up a Scheduling Survey
    via the provided Scheduling Survey ID (ssid),
    and saves the page as a PDF at the path given.

    Parameters:
        - page: playwright.sync_api.Page
            The page which is navigated to the
            results page of the MS Form.
        - ssid: int
            The Scheduling Survey ID to look up.
        - save_path: str
            The path to save the PDF to.
        - new_navigation: bool
            True if this is the first search
            completed on the passed page, False
            otherwise.
        - prev_ssids: List[int]
            The list of ssids searched up. Defaults
            to the initial search ID, which is 3.
    '''
    if new_navigation:
        page.fill(f"input[value='{prev_ssids[0]}']", f"{ssid}")
    else:
        page.fill(f"input[value='{prev_ssids[-1]}']", f"{ssid}")
    page.wait_for_timeout(600)
    prev_ssids.append(ssid)
    page.pdf(path=save_path)