# https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz
from   bs4       import BeautifulSoup
from   itertools import combinations
from   io        import BytesIO
import os
import requests
import sys
import tarfile
import subprocess

from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def check_gecko():
    file_path = f"{os.getcwd()}/geckodriver"

    if not os.path.exists(file_path):
        print(f"Gecko Driver NOT Found!")
        print(f"Downloading...")

        url = "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz"
        response = requests.get(url)

        if response.status_code == 200:
            content = BytesIO(response.content)

            with tarfile.open(fileobj=content, mode="r:gz") as tar:
                tar.extractall()
            print("Download and extraction of geckodriver successful.")
        else:
            Expected(f"Failed to download geckodriver file. Status code: {response.status_code}")
    else:
        print(f"Gecko Driver found, continuing!")



def generate_combos(header, strings, footer, amount):
    folder_path = "./combos"

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

    folder_path = "./texts"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

    if len(strings) < amount:
        print(f"Error: Input list must contain at least {amount} strings.")
        return

    folder_path = "./pdfs"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

    if len(strings) < amount:
        print(f"Error: Input list must contain at least {amount} strings.")
        return

    combined_sets = combinations(strings, amount)
    concatenated_combinations = [''.join(comb_set) for comb_set in combined_sets]

    i = 0
    for concatenated_combination in concatenated_combinations:
        output_file_path = os.path.join('./combos/', f'resume_{i}.html')
        text_output = os.path.join('./texts/', f'resume_{i}.txt')

        content = f"{header}{concatenated_combination}{footer}"
        soup = BeautifulSoup(content, 'html.parser')
        raw_text = soup.get_text()

        with open(output_file_path, 'w') as output_file:
            output_file.write(content)
        with open(text_output, 'w') as output_file:
            output_file.write(raw_text)

        print(f'Combination {i + 1} written to: {output_file_path}')
        i += 1
    return i

def parse_resume(input_file_path, amount):
    if not os.path.exists(input_file_path):
        Expected(f"Resume template not found, aborting...")

    with open(input_file_path, 'r') as input_file:
        html_content = input_file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    html_head = str(soup.head)
    html_header = f"<!DOCTYPE html> <html> <head>{html_head}</head><body> <div class=\"container mt-5\">"
    resume_header = f"{html_header}{soup.find('div', class_='resume-header')}"
    proj_combo_divs = soup.find_all('div', class_='proj-combo')
    resume_footer = f"{soup.find('div', class_='resume-footer')}</div></body> </html>"

    proj_combo_strs = []
    for proj_combo_div in proj_combo_divs:
        proj_combo_strs.append(f"{proj_combo_div}")
    return generate_combos(resume_header, proj_combo_strs, resume_footer, amount)


async def run_server():
    subprocess.run("python -m http.server", shell=True, capture_output=True)

def get_pdf_from_web(idx, geckodriver_path):
    try:
        options = Options()
        options.headless = True
        profile_options = FirefoxProfile()
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0"
        profile_options.set_preference("profile_options = FirefoxProfile()", user_agent)
        profile_options.set_preference("print_printer", "Mozilla Save to PDF")
        profile_options.set_preference("print.always_print_silent", True)
        profile_options.set_preference("print.show_print_progress", False)
        profile_options.set_preference("print.save_as_pdf.links.enabled", True)
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_file", True)
        profile_options.set_preference("print.more-settings.open", True);
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_ignore_unwriteable_margins", True);
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_margin_bottom", "0");
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_margin_left", "0");
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_margin_right", "0");
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_margin_top", "0");
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_shrink_to_fit", True);
        profile_options.set_preference("print_printer", "Mozilla Save to PDF");
        profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_filename",
                                       f"{os.getcwd()}/pdfs/resume_{idx}.pdf")

        driver = webdriver.Firefox(executable_path=geckodriver_path, options=options, firefox_profile=profile_options)
        driver.get(f"http://127.0.0.1:8000/combos/resume_{idx}.html")
        sleep(1)

        driver.execute_script("window.print()")
        sleep(1)

        driver.quit()
        
    except Exception as e:
        print(f"An error occurred: {e}")

def get_pdfs(size):
    for idx in range(0,size):
        print(f"Making pdf {idx}/{size}")
        get_pdf_from_web(idx, f"{os.getcwd()}/geckodriver")

check_gecko()
size = parse_resume("./resume_example.html", 4)
#run_server()
get_pdfs(size)
