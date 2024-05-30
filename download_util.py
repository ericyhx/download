import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import time
import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

Tss_file = 'D:/download/temp_ts/'
contact_mp4 = 'D:/download/'
# 保存的ts文件列表
file_name_list=[]
#ts文件的url下载列表
download_list=[]
no_url_list=[]

# 下载文件函数
def Down_file(download, file_name):
    urllib.request.urlretrieve(download, file_name)

# 保存txt文件
def Save_file_list():
    Ts_named()
    with open(Tss_file + 'ts_list.txt', 'w', encoding='utf-8') as F:  # 指定保存txt文件的地址
        for file in file_name_list:
            F.write(f"file '{file}'\n")  # 把所有ts名称写如txt文件 格式：file '***.ts'

#下载开始之前清理文件夹函数
def Clear_txt():
    if not os.path.exists(Tss_file):
        os.makedirs(Tss_file,exist_ok=True)
    for filename in os.listdir(Tss_file):
        if filename.endswith(f".ts"):
            os.remove(os.path.join(Tss_file, filename))
        if filename.endswith(f".txt"):
            os.remove(os.path.join(Tss_file, filename))

 #合并ts文件并保存函数
def Contact_ts(mp4_name):
    tss_list_file = Tss_file + 'ts_list.txt'
    concat_mp4 = fr' {contact_mp4}{mp4_name}.mp4'
    cmd_code = f'ffmpeg -f concat -safe 0 -y -i {tss_list_file} -c copy -strict -2 {concat_mp4}'
    os.system(cmd_code)
#构造规则的ts文件名
def Ts_named():
    for i in range(len(download_list)):
        if i < 10:
            name = "000" + str(i) + '.ts'
        elif i < 100:
            name = "00" + str(i) + '.ts'
        elif i < 1000:
            name = "0" + str(i) + '.ts'
        else:
            name = str(i) + '.ts'
        file_name_list.append(Tss_file + name)

#构建线程池并提交任务函数
def Thread_pool_start():
    # 开设线程多少
    task_list = []
    n_threads = 50  # 越大越快？
    with ThreadPoolExecutor(max_workers=n_threads) as pool:
        for i in range(len(download_list)):
            task_list.append(pool.submit(Down_file, download_list[i], file_name_list[i]))
        # 判断所有下载线程是否全部结束
        first_time = time.time()
        while True:
            if len(task_list) == 0:
                pool.shutdown(wait=False)
                print('下载完成！正在转码保存')
                break
            for i in task_list:
                if i.done():
                    task_list.remove(i)
            second_time = time.time()
            if second_time - first_time > 1:
                j = 100 * (len(download_list) - len(task_list)) / len(download_list)
                print(str(round(j, 2)) + "%")
                first_time = second_time


#获取所有ts文件url
def Get_ts_url(no,url):
    print(f"正在下载：{no}，url:{url}")
    resp = requests.get(url)
    result = resp.text.split("\n")
    strs = url.split("/")
    uri=strs[0]+"//"+strs[2]
    for r in result:
        if (r.endswith(".ts")):
            download_list.append(uri + r)
#获取剧集和其url
def Parse_number_url(p,base_url,url):
    # 获取a标签的href
    temp = p.get('href').split('/')[3]
    res2 = requests.get(url + "/" + temp)
    soup2 = BeautifulSoup(res2.text, 'html.parser')
    soup2 = soup2.find(id='cms_play')
    script_tags = soup2.find_all('script')
    script_content = str(script_tags[0])
    match = re.search(r'var cmsPlayer = (\{.*?\});', script_content, re.DOTALL)
    if match:
        json_str = match.group(1)
        # 解析JSON文本
        json_data = json.loads(json_str)
        full_url = base_url + json_data.get('url')
        # 分解URL
        parsed_url = urlparse(full_url)

        # 解析查询字符串
        query_params = parse_qs(parsed_url.query)

        # 获取url参数的值
        url_value = query_params['url'][0]

        no = query_params['no'][0]
        res3 = requests.get(url_value)
        strs = url_value.split("/")
        uri = strs[0] + "//" + strs[2]
        ts_url = uri + res3.text.split("\n")[2]
        print(f"正在解析：{no}，url:{ts_url}")
        return no,ts_url


def download(url,base_url):
    response = requests.get(url)
    if response.status_code == 200:  # 检查请求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')  # 使用BeautifulSoup解析HTML
        # 现在你可以使用BeautifulSoup的方法来查找和操作HTML元素
        # 例如，找到所有的段落标签
        soup = soup.find(id='con_playlist_1')
        paragraphs = soup.find_all('a')
        for p in paragraphs:
            no_url_list.append(Parse_number_url(p,base_url,url))

if __name__ == '__main__':
    base_url = "https://www.cxhrgd.com"
    url="https://www.cxhrgd.com/xsj/137742"
    download(url,base_url)
    print(no_url_list)
    for no_url in no_url_list:
        Clear_txt()
        Get_ts_url(no_url[0],no_url[1])
        Save_file_list()
        Thread_pool_start()
        Contact_ts(no_url[0])
        print(no_url)