import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import time

import requests

Tss_file = f'D:/download/temp_ts/'
ts_file='ts_list.txt'
contact_mp4 = f'D:/download/'
url_pre="https://ikcdn01.ikzybf.com"
url="https://ikcdn01.ikzybf.com/20240527/GOwzb8C3/2000kb/hls/index.m3u8"





# 下载文件函数
def Down_file(download, file_name):
    urllib.request.urlretrieve(download, file_name)


# 保存txt文件
def Save_file_list(file_list):
    with open(Tss_file + ts_file, 'w', encoding='utf-8') as F:  # 指定保存txt文件的地址
        for file in file_list:
            F.write(f"file '{file}'\n")  # 把所有ts名称写如txt文件 格式：file '***.ts'

def clear_txt():
    for filename in os.listdir(Tss_file):
        if filename.endswith(f".ts"):
            os.remove(os.path.join(Tss_file, filename))
        if filename.endswith(f".txt"):
            os.remove(os.path.join(Tss_file, filename))
A = 21
start_time = time.time()
for filename in os.listdir(Tss_file):
    if filename.endswith(f".ts"):
        os.remove(os.path.join(Tss_file, filename))
    if filename.endswith(f".txt"):
        os.remove(os.path.join(Tss_file, filename))

resp=requests.get(url)
result=resp.text.split("\n")
download_list=[]
for r in result:
    if(r.endswith(".ts")):
        download_list.append(url_pre+r)
# 保存的文件列表
file_name_list=[]
for i in range(len(download_list)):
    if i<10:
        name="000"+str(i)+'.ts'
    elif i < 100:
        name = "00" + str(i) + '.ts'
    elif i < 1000:
        name = "0" + str(i) + '.ts'
    else:
        name = str(i) + '.ts'
    file_name_list.append(Tss_file+name)
# file_name_list = [Tss_file + str(i) + '.ts' for i in range(len(download_list))]
Save_file_list(file_name_list)
# 线程池的创立
flag = True
download_flag = True
if flag:
    # 开设线程多少
    task_list = []
    n_threads = 50  # 越大越快？
    with ThreadPoolExecutor(max_workers=n_threads) as pool:
        for i in range(len(download_list)):
            task_list.append(pool.submit(Down_file, download_list[i], file_name_list[i]))
        # 判断所有下载线程是否全部结束
        first_time = time.time()
        flag_time = time.time()
        # flag_A = len(task_list)
        while download_flag:
            second_time = time.time()
            if len(task_list) == 0:
                # download_flag = False
                print('结束')
                pool.shutdown(wait=False)
                print('下载完成！正在转码保存')
                break
            for i in task_list:
                if i.done():
                    task_list.remove(i)
            second_time = time.time()
            if second_time - first_time > 1:
                j = 100 * (len(download_list) - len(task_list)) / len(download_list)
                print(str(round(j,2)) + "%")
                first_time = second_time
            # if second_time - flag_time > 30:
            #     flag_time = second_time
            #     if 0 == len(task_list):
            #         download_flag = False
            #         print('结束')
            #         pool.shutdown(wait=False)
                # else:
                #     flag_A = len(task_list)
print(download_flag)
# if download_flag:
# 合并保存
tss_list_file = Tss_file+ts_file
concat_mp4 = fr' {contact_mp4}21.mp4'
cmd_code =f'ffmpeg -f concat -safe 0 -y -i {tss_list_file} -c copy -strict -2 {concat_mp4}'
os.system(cmd_code)
end_time = time.time()
print(f'结束，运行时间为{round(end_time - start_time,2)}s')
# else:
#     print('下载失败')

def contact():
    tss_list_file = Tss_file + ts_file
    concat_mp4 = fr' {contact_mp4}21.mp4'
    cmd_code = f'ffmpeg -f concat -safe 0 -y -i {tss_list_file} -c copy -strict -2 {concat_mp4}'
    os.system(cmd_code)