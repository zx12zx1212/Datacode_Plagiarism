def Plagiarism(start=0, list=[], end=None, account=None, password=None):
    if end == None:
        end = start

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    from bs4 import BeautifulSoup

    chrome = webdriver.Chrome(ChromeDriverManager().install())
    chrome.get('https://datacode.wndc.nkust.edu.tw/Identity/Account/Login')
    chrome.find_element(By.ID, "Input_Email").send_keys(account)
    chrome.find_element(By.ID, "Input_Password").send_keys(password)
    chrome.find_element(By.CSS_SELECTOR, "button.btn").click()

    content_dict = {}
    if list != []:
        for num in list:
            chrome.get('https://datacode.wndc.nkust.edu.tw/Exercise/Score/' + str(num))
            soup = BeautifulSoup(chrome.page_source, 'html.parser')
            content = [td.text.replace('\n', '').replace(' ', '') for td in soup.find_all('td')]
            content_dict[str(num)] = {}
            for i in range(0, len(content), 2):
                content_dict[str(num)][content[i]] = content[i + 1]
    else:
        for num in range(start, end + 1):
            chrome.get('https://datacode.wndc.nkust.edu.tw/Exercise/Score/' + str(num))
            soup = BeautifulSoup(chrome.page_source, 'html.parser')
            content = [td.text.replace('\n', '').replace(' ', '') for td in soup.find_all('td')]
            content_dict[str(num)] = {}
            for i in range(0, len(content), 2):
                content_dict[str(num)][content[i]] = content[i + 1]

    chrome.quit()

    return content_dict


import pandas as pd

login = input("請輸入帳號密碼(用空格隔開，按下Enter為預設):")
start_number = input("請輸入題號(用空格隔開，如為連續題號請直接輸入開始及結束題號):").split(" ")
if len(start_number) == 2:
    content_dict = Plagiarism(start=int(start_number[0]), end=int(start_number[1]), account=login[0],
                              password=login[1])
elif len(start_number) > 2:
    content_dict = Plagiarism(list=start_number, account=login[0], password=login[1])
else:
    content_dict = Plagiarism(start=int(start_number[0]), account=login[0], password=login[1])
data = pd.DataFrame(content_dict)
print(data)
data.to_excel('Student_Plagiarism.xlsx', sheet_name='sheet1', na_rep='--')
