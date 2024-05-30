import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

base_url = "https://www.cxhrgd.com"
url="https://www.cxhrgd.com/xsj/137742"
response = requests.get(url)
if response.status_code == 200:  # 检查请求是否成功
    soup = BeautifulSoup(response.text, 'html.parser')  # 使用BeautifulSoup解析HTML
    # 现在你可以使用BeautifulSoup的方法来查找和操作HTML元素
    # 例如，找到所有的段落标签
    soup=soup.find(id='con_playlist_1')
    paragraphs = soup.find_all('a')
    for p in paragraphs:
        #获取a标签的href
        temp=p.get('href').split('/')[3]
        res2=requests.get(url+"/"+temp)
        soup2 = BeautifulSoup(res2.text, 'html.parser')
        soup2 = soup2.find(id='cms_play')
        script_tags = soup2.find_all('script')
        script_content = str(script_tags[0])
        match = re.search(r'var cmsPlayer = (\{.*?\});', script_content, re.DOTALL)
        if match:
            json_str = match.group(1)
            # 解析JSON文本
            json_data = json.loads(json_str)
            full_url=base_url+json_data.get('url')
            # 分解URL
            parsed_url = urlparse(full_url)

            # 解析查询字符串
            query_params = parse_qs(parsed_url.query)

            # 获取url参数的值
            url_value = query_params['url'][0]

            no = query_params['no'][0]
            res3=requests.get(url_value)
            ts_url=base_url+res3.text.split("\n")[2]
            print(ts_url)
        else:
            print("No JSON data found in script tags.")

else:
    print(f"请求失败，状态码：{response.status_code}")
