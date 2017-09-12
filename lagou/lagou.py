import requests
from bs4 import BeautifulSoup
import traceback
import re
import time

def getHtmlText(url):
    try:
        r = requests.get(url,headers = {'user-agent':'*'})
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("请求页面失败")
        return ""

def getPythonList(lst, PythonURL):
	#定义爬取的页数，最多为30页,n的取值为从1到30
	n = 1
    for i in range(n):
        url = PythonURL + str(i+1) + '/?filterOption=2'
        html = getHtmlText(url)
        if (html == ""):
            print("请求超链接列表跪了...")
            continue
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find_all('a')
        for j in a:
            try:
                if j.attrs['class'] == ['position_link']:
                    href = j.attrs['href']
                    lst.append(href)
            except:
                continue
        print(lst)
    return ""

def getPythonInfo(lst, PythonURL, fpath):
    #string = []
    for url in lst:
		#设定爬取一次后短暂睡眠7秒钟，请求频率过高会导致请求html页面失败，目前正在寻找其他方法
        time.sleep(7)
        try:
            html = getHtmlText(url)
            if (html == ""):
                print("请求具体信息跪了...")
            continue
            #提取python岗位要求...
            soup = BeautifulSoup(html, 'html.parser')
            description = soup.find('dd', attrs={'class':'job_bt'})
            detail = description.find_all('p')
            with open (fpath, 'a', encoding = 'utf-8') as f:
                for i in detail:
                    f.write(i.text+"\n")
        except:
            continue
    
def main():
    python_list_url = 'https://www.lagou.com/zhaopin/Python/'
    python_info_url = 'https://www.lagou.com/jobs/'
    output_path = 'D:/LagouPythonInfo.txt'
    
    slist = []
    getPythonList(slist, python_list_url)
    getPythonInfo(slist, python_info_url, output_path)

main()
