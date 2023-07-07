import random
import string
import requests
import time
import tempfile
import sys
import os
from progress.bar import Bar
from colorama import Fore, init
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException

def generate_codes(num_codes):
    generated_links = []

    for _ in range(num_codes):
        while True:
            code = "".join(random.choices(string.ascii_letters + string.digits, k=10))
            if code not in generated_links:
                generated_links.append(code)
                break

    with open("generated_codes.txt", "w") as file:
        for link in generated_links:
            file.write(link + "\n")

    print(Fore.LIGHTGREEN_EX+"Generated links have been saved to generated_codes.txt.")

def check_codes(file_path):

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print(Fore.RED + "Invalid file path or empty file.")
        return
    
    with open(file_path, 'r') as f, open("good_output.txt", "w", encoding="utf-8") as file:
        lines = f.readlines()
        total = len(lines)
        good = 0

        for i, line in enumerate(lines):
            line = line.strip()
            url = f"https://anonfiles.com/{line}"
            req = requests.get(url)

            if req.status_code == 200:
                good += 1
                content = extract_content(url)
                file.write(f"{url}/{content}\n")
                print("\n" + Fore.LIGHTGREEN_EX + "[+] " + Fore.MAGENTA + ">>" + Fore.LIGHTGREEN_EX + " " + f"{url}/{content}" + "\n")

            print(f"Checked: {i+1}/{total}", end="\r")
            time.sleep(0.7)

        if good == 0:
            print("No good links found.")
        else:
            print(Fore.LIGHTMAGENTA_EX + f"\n{good} links found and saved to good_output.txt.")

def extract_content(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    content = tree.xpath('/html/body/div/div[4]/div[2]/h1/text()')
    if content:
        return content[0]
    return ""


def scrape_links_with_domain(url, domain, num_pages):
    log_file_path = "webdriver.log"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-logging')
    options.add_argument(f'--log-path={log_file_path}')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    temp_stderr = tempfile.TemporaryFile()
    sys.stderr = temp_stderr

    wait = WebDriverWait(driver, 10)

    all_links = []

    print(Fore.YELLOW + "\nEstablishing the connection, please wait...\n", end='', flush=True)

    driver.get(url)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
    page_links = extract_links(driver, domain)
    all_links.extend(page_links)
    
    print("\n" + Fore.LIGHTGREEN_EX + "[+] " + Fore.MAGENTA + ">>" + Fore.LIGHTGREEN_EX + " Connexion Established !! " + "\n")

    print(Fore.LIGHTCYAN_EX + "\nSorting order ?\n\n[1] Oldest to Newest\n[2] Newest to Oldest\n[3] Default (by URL)\n")
    sort_option = input("\n> ")
    while sort_option not in ['1', '2', '3']:
        print(Fore.RED + "Incorrect value.")
        sort_option = input("\n> ")

    if sort_option == '1':
        date_sort_button = driver.find_element(By.XPATH, '//*[@id="resultsUrl"]/thead/tr/th[3]')
        date_sort_button.click()
        try:
            wait.until(EC.staleness_of(date_sort_button))
        except TimeoutException:
            pass
    elif sort_option == '2':
        date_sort_button = driver.find_element(By.XPATH, '//*[@id="resultsUrl"]/thead/tr/th[3]')
        date_sort_button.click()
        date_sort_button.click()
        try:
            wait.until(EC.staleness_of(date_sort_button))
        except TimeoutException:
            pass
    elif sort_option == '3':
        pass

    current_page = 0
    progress_bar = Bar(Fore.LIGHTCYAN_EX + 'Scraping Progress', max=num_pages)

    while has_next_page(driver) and current_page < num_pages:
        next_button = driver.find_element(By.XPATH, '//*[@id="resultsUrl_next"]/a')
        next_button.click()
        wait.until(EC.staleness_of(next_button))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        page_links = extract_links(driver, domain)
        all_links.extend(page_links)
        current_page += 1
        progress_bar.next()

    progress_bar.finish()
    driver.quit()

    sys.stderr = sys.__stderr__
    temp_stderr.close()

    filtered_links = filter_links(all_links)
    write_to_file(filtered_links)
    print(Fore.LIGHTMAGENTA_EX + "Saved to file\n")

def extract_links(driver, domain):
    links = driver.find_elements(By.TAG_NAME, 'a')
    page_links = []
    for link in links:
        href = link.get_attribute('href')
        if href and domain in href:
            page_links.append(href)
    return page_links

def has_next_page(driver):
    try:
        next_button = driver.find_element(By.XPATH, '//*[@id="resultsUrl_next"]/a')
        return next_button.is_enabled() and next_button.is_displayed()
    except NoSuchElementException:
        return False


def filter_links(links):
    unique_codes = set()
    filtered_links = []
    for link in links:
        start_index = link.find(domain) + len(domain) + 1
        end_index = link.find('/', start_index)
        if end_index != -1 and end_index - start_index == 10:
            code = link[start_index:end_index]
            if code not in unique_codes:
                unique_codes.add(code)
                filtered_links.append(code)
    return filtered_links


def write_to_file(links):
    with open('anony_output.txt', 'w') as file:
        for link in links:
            file.write(link + '\n')

init(autoreset=True)

print(Fore.CYAN + '''
                      _   _  ____  _   ___     __
                /\   | \ | |/ __ \| \ | \ \   / /
               /  \  |  \| | |  | |  \| |\ \_/ / 
              / /\ \ | . ` | |  | | . ` | \   /  
             / ____ \| |\  | |__| | |\  |  | |   
            /_/    \_\_| \_|\____/|_| \_|  |_|   

                      Anonfiles tools - by Sla0ui                                                                          
                                     t.me/slesl23            
                                                                    
                       ''')

while True:
    

    print(Fore.WHITE + "\nMenu:")
    print("[1] " + Fore.YELLOW + "Generate random codes")
    print("[2] " + Fore.YELLOW + "Check codes")
    print("[3] " + Fore.YELLOW + "Scrape codes from the internet")
    print("[4] " + Fore.YELLOW + "Exit")
    while True:
        try:
            choice = int(input("\n> "))
            if 1 <= choice <= 4:
                break
            else:
                print(Fore.RED + "Invalid input.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid number.")
        

    if choice == 1:
        print(Fore.CYAN + "Enter the number of codes you want to generate: ")
        while True:
            try:
                num_codes = int(input("\n> "))
                if 1 <= num_codes:
                    generate_codes(num_codes)
                    break
                else:
                    print(Fore.RED + "Invalid input.")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a valid number.")
    elif choice == 2:
        file_path = input(Fore.CYAN + "Enter the file path: "+ Fore.RESET )
        check_codes(file_path)
    elif choice == 3:
        url = 'https://web.archive.org/web/*/anonfiles.com/*'
        domain = 'anonfiles.com'
        num_pages = int(input(Fore.CYAN + "Enter the number of pages to scrape: "))
        scrape_links_with_domain(url, domain, num_pages)
    elif choice == 4:
        break
    else:
        print(Fore.RED + "Invalid choice. Please try again.")

print(Fore.GREEN + "Program exited.")
