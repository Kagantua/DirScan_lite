from asyncio.windows_events import NULL
from fileinput import filename
import requests
from optparse import OptionParser
from fake_useragent import UserAgent
import queue
import threading
import sys
import calendar
import time

ts = calendar.timegm(time.gmtime())
filename = NULL

def main(url, threadNum):
    # 获取要爆破的路径
    path_queue = get_path(url)
    # 利用多线程进行url目录爆破
    threads = []
    for i in range(threadNum):
        t = threading.Thread(target=get_url, args=(path_queue, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# 目录爆破函数get_url()
def get_url(path_queue):
    while not path_queue.empty():
        try:
            url = path_queue.get()
            ua=UserAgent()
            response=requests.get(url,headers={'User-Agent': ua.random})
            if response.status_code != 404:
                sys.stdout.write("\033[32m [%d] = > %s \033[0m \n" %(response.status_code, url))
                result = open(str(ts)+'result.html', 'a+')
                result.write('<a href="' + url + '" target="_blank">' + url + '</a>' +"  "+ str(response.status_code))
                result.write('\r\n</br>')
                result.close()
            else:
                sys.stdout.write("[%d] = > %s \n" %(response.status_code, url))
        except:
            pass
    else:
        sys.exit()

# 路径获取函数get_path()
def get_path(url, file="dict.txt"):
    path_queue = queue.Queue()
    with open(file, "r", encoding="gbk") as f:
        for i in f.readlines():
            if i[0] == '/':
                i = i
            else:
                i = "/" + i
            path = url + i.strip()
            path_queue.put(path)
        return path_queue

if __name__ == "__main__":
    print(
        """
 /$$$$$$$  /$$$$$$ /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$  /$$   /$$
| $$__  $$|_  $$_/| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$| $$$ | $$
| $$  \ $$  | $$  | $$  \ $$| $$  \__/| $$  \__/| $$  \ $$| $$$$| $$
| $$  | $$  | $$  | $$$$$$$/|  $$$$$$ | $$      | $$$$$$$$| $$ $$ $$
| $$  | $$  | $$  | $$__  $$ \____  $$| $$      | $$__  $$| $$  $$$$
| $$  | $$  | $$  | $$  \ $$ /$$  \ $$| $$    $$| $$  | $$| $$\  $$$
| $$$$$$$/ /$$$$$$| $$  | $$|  $$$$$$/|  $$$$$$/| $$  | $$| $$ \  $$
|_______/ |______/|__/  |__/ \______/  \______/ |__/  |__/|__/  \__/
                                                                v 1.0    
                                                                    
                                                                    """
                                                                    )
    print("\n")
    print("\033[31m Start Brute \033[0m")
    parser = OptionParser('python DirScan.py -u <Target URL> -f <Dictionary file name> [-t <Thread_count>]')
    parser.add_option('-u', '--url', dest='url', type='string', help='target url for scan')
    parser.add_option('-f', '--file', dest='file_name',type='string', help='dictionary filename')
    parser.add_option('-t', '--thread', dest='count',type='int', default=10, help='scan thread count')
    (options, args) = parser.parse_args()
    if options.url and options.file_name:
        if options.url[-1] == '/':
            url = options.url[-1]
        else:
            url = options.url
        filename = options.file_name
        threadNum = options.count
        start = time.time()
        main(url, threadNum)
        end = time.time()
        print("总共耗时 %.2f" % (end-start))
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)

