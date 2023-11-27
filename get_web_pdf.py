from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def get_pdf_from_web(url, geckodriver_path):
    try:
        options = Options()
        options.headless = False
        profile_options = FirefoxProfile()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0'
        profile_options.set_preference('profile_options = FirefoxProfile()', user_agent)
        profile_options.set_preference("print_printer", "Mozilla Save to PDF")
        profile_options.set_preference("print.always_print_silent", True)
        profile_options.set_preference("print.show_print_progress", False)
        profile_options.set_preference('print.save_as_pdf.links.enabled', True)
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_file", True)
        profile_options.set_preference("print.more-settings.open", True);
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_ignore_unwriteable_margins", True);
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_margin_bottom", "0");
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_margin_left", "0");
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_margin_right", "0");
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_margin_top", "0");
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_shrink_to_fit", True);
        profile_options.set_preference("print_printer", "Mozilla Save to PDF");
        profile_options.set_preference('print.printer_Mozilla_Save_to_PDF.print_to_filename',
                                       "out.pdf")

        driver = webdriver.Firefox(executable_path=geckodriver_path, options=options, firefox_profile=profile_options)
        driver.get(url)
        sleep(1)

        driver.execute_script('window.print()')
        sleep(5)

        driver.quit()
        

        
    except Exception as e:
        print(f"An error occurred: {e}")

url_to_scrape = "http://127.0.0.1:8000/resume_1.html"

geckodriver_path = "../geckodriver"  
get_pdf_from_web(url_to_scrape, geckodriver_path)

