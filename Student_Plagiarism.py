def Plagiarism(model, start=0, list=[], end=None, account=None, password=None):
    import requests
    from bs4 import BeautifulSoup

    url = 'https://datacode.wndc.nkust.edu.tw/Identity/Account/Login'
    headers = {
        "User-Agent": '"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/49.0.2623.13 Safari/537.36'}
    s = requests.Session()
    g = s.get(url)
    token = BeautifulSoup(g.text, 'html.parser').find('input', {'name': '__RequestVerificationToken'})['value']
    payload = {'Input.Email': account, 'Input.Password': password, 'Input.RememberMe': 'false',
               '__RequestVerificationToken': token}
    s.post(url, data=payload)
    content_dict = {}
    if model == 1:
        r = s.get('https://datacode.wndc.nkust.edu.tw/Exercise/Score/' + str(start))
        table = BeautifulSoup(r.text, 'html.parser').select('tr > td')
        content_dict[str(start)] = {}
        for i in range(0, len(table), 2):
            content_dict[str(start)][table[i].text.strip()] = table[i + 1].text.strip()
    elif model == 2:
        for num in list:
            r = s.get('https://datacode.wndc.nkust.edu.tw/Exercise/Score/' + str(num))
            table = BeautifulSoup(r.text, 'html.parser').select('tr > td')
            content_dict[str(num)] = {}
            for i in range(0, len(table), 2):
                content_dict[str(num)][table[i].text.strip()] = table[i + 1].text.strip()
    elif model == 3:
        for num in range(start, end + 1):
            r = s.get('https://datacode.wndc.nkust.edu.tw/Exercise/Score/' + str(num))
            table = BeautifulSoup(r.text, 'html.parser').select('tr > td')
            content_dict[str(num)] = {}
            for i in range(0, len(table), 2):
                content_dict[str(num)][table[i].text.strip()] = table[i + 1].text.strip()

    return content_dict


import pandas as pd

login = input("請輸入帳號密碼(用空格隔開，按下Enter為預設):")
while 1:
    model = int(input("請輸入要抓取模式的數字(1) 單題 (2)跳題 (3) 連續題:"))
    if model in [1, 2, 3]:
        break
start_number = input("請輸入題號(用空格隔開，如為連續題號請直接輸入開始及結束題號):").split(" ")
if model == 1:
    content_dict = Plagiarism(1, start=int(start_number[0]), account=login[0], password=login[1])
elif model == 2:
    content_dict = Plagiarism(2, list=start_number, account=login[0], password=login[1])
elif model == 3:
    content_dict = Plagiarism(3, start=int(start_number[0]), end=int(start_number[1]), account=login[0],
                              password=login[1])
data = pd.DataFrame(content_dict)
# print(data)
data.to_excel('Student_Plagiarism.xlsx', sheet_name='sheet1', na_rep='--')
print('抓取完畢~~平安喜樂~~')
msg=r"""
                                                          _ooOoo_
                                                         o8888888o
                                                         88" . "88
                                                         (| -_- |)
                                                          O\ = /O
                                                      ____/`---'\____
                                                    .   ' \\| |// `.
                                                     / \\||| : |||// \
                                                   / _||||| -:- |||||- \
                                                     | | \\\ - /// | |
                                                   | \_| ''\---/'' | |
                                                    \ .-\__ `-` ___/-. /
                                                 ___`. .' /--.--\ `. . __
                                              ."" '< `.___\_<|>_/___.' >'"".
                                             | | : `- \`.;`\ _ /`;.`/ - ` : | |
                                               \ \ `-. \_ __\ /__ _/ .-` / /
                                       ======`-.____`-.___\_____/___.-`____.-'======
                                                          `=---='
                                       .............................................
                                              媛嬤保佑             永無BUG
                                       .............................................
   
"""
print(msg)
import os
os.system('pause')

