import os

import requests

url_pre="https://ikcdn01.ikzybf.com"
url="https://ikcdn01.ikzybf.com/20240525/4dRMUEBw/2000kb/hls/index.m3u8"
save_path="D:/download/"
file_path="D:/download/index_file.txt"
resp=requests.get(url)


for filename in os.listdir(save_path):
    if filename.endswith(f".ts"):
        os.remove(os.path.join(save_path, filename))
    if filename.endswith(f".txt"):
        os.remove(os.path.join(save_path, filename))
result=resp.text.split("\n")
print(len(result))
index = 1
for r in result:
    if(r.endswith(".ts")):
        print(r)
        all_url=url_pre+r
        re=requests.get(all_url);
        if index<10:
            name="000"+str(index)+".ts"
        elif index <100:
            name="00"+str(index)+".ts"
        elif index < 1000:
            name = "0" + str(index) + ".ts"
        else:
            name = str(index) + ".ts"
        with open(save_path+name,'wb') as f:
            f.write(re.content)
        with open(file_path,'a') as f:
            f.write(f"file '{name}'\n")
        index=index+1

