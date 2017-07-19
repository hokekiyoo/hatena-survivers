from argparse import ArgumentParser
from urllib import request 
from urllib import error
from bs4 import BeautifulSoup
import os
import csv
import json


def crawler(args):
    url = "http://staff.hatenablog.com/"
    flag = True
    ismax = False
    with open("blog_url.csv","w") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(["url"])
        while flag:
            bloggers = [url]
            crawled = []
            past = len(bloggers)
            for url in bloggers:
                if ismax:
                    break
                if url in crawled:
                    continue
                try:
                    html = request.urlopen(url)
                except error.HTTPError as e: 
                    # HTTPレスポンスのステータスコードが404, 403, 401などの例外処理
                    print(e.reason)
                    continue
                except error.URLError as e: 
                    # アクセスしようとしたurlが無効なときの例外処理
                    print(e.reason)
                    continue
                except ValueError:
                    continue
                soup = BeautifulSoup(html, "html.parser")
                url_top = soup.html.get("data-blog-uri")
                try:
                    html = request.urlopen("{}/about".format(url_top))
                except error.HTTPError as e: 
                    # HTTPレスポンスのステータスコードが404, 403, 401などの例外処理
                    print(e.reason)
                    continue
                except error.URLError as e: 
                    # アクセスしようとしたurlが無効なときの例外処理
                    print(e.reason)
                    continue
                except ValueError:
                    continue
                soup = BeautifulSoup(html, "html.parser")
                subscribers_page = soup.find_all("a", class_="subscriber")
                for subscribe_page in subscribers_page:
                    subscriber = subscribe_page.get("href")
                    if subscriber not in bloggers:
                        bloggers.append(subscriber)
                        writer.writerow([subscriber])
                        print("Now:",len(bloggers))
                        if len(bloggers) > min(args.maxnum,50000):
                            ismax = True
                            flag = False
                            break
            crawled.append(url)
            now = len(bloggers)
            # flag = (past < now)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-m", "--maxnum", type=int, default=1000,help="input maximum number of blogger")
    args = parser.parse_args()
    crawler(args)