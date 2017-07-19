import pandas as pd
from urllib import request 
from urllib import error
from bs4 import BeautifulSoup
import csv

# status 0:まだ 1:始めた 2:やめてる 3:死亡
def get_status(url):
    years = range(2012,2018)
    months = range(1,13)
    status = 0
    vacation = 0
    count = 0
    # 保存しておく箱
    dates = []
    events = []
    counts = []
    print(url+"  ",end="",flush=True)
    article_num = 0
    for year in years:
        if year == 2017:
            months = range(1,8)
        for month in months:
            try:
                html = request.urlopen("{}/archive/{}/{}".format(url,year,month))
            except error.HTTPError as e: 
                # HTTPレスポンスのステータスコードが404, 403, 401などの例外処理
                print(e.reason)
                break
            except error.URLError as e: 
                # アクセスしようとしたurlが無効なときの例外処理
                print(e.reason)
                break
            except:
                break
            soup = BeautifulSoup(html, "html.parser")
            articles = soup.find_all("a", class_="entry-title-link")
            # 状態遷移
            # 活動開始
            article_num += len(articles)
            if status == 0 and len(articles) > 0:
                status = 1
                events.append("start")
                dates.append(str(year)+"-"+str(month))
                counts.append(count)
            # 活動→休止
            elif status == 1 and len(articles) == 0:
                status = 2
                vacation += 1
                events.append("pause")
                dates.append(str(year)+"-"+str(month))
                counts.append(count)
            # 休止中
            elif status == 2 and len(articles) == 0:
                # 休止が3ヶ月以内なら休止中
                if vacation < 3:
                    vacation += 1
                # 休止が3ヶ月以上なら死亡
                else:
                    status = 3
                    events.append("dead")
                    dates.append(str(year)+"-"+str(month))
                    counts.append(count)

            # 休止→活動
            elif status == 2 and len(articles) > 0:
                status = 1
                vacation = 0
                events.append("resume")
                dates.append(str(year)+"-"+str(month))
                counts.append(count)
            # 死亡
            elif status == 3:
                break
            count += 1
            print(".", end="",flush=True)
        if status == 3:
            break
    events.append("now")
    dates.append("2017"+"-"+"7")
    counts.append(count)
    return events, dates, counts, article_num

def checker(events,dates,counts):
    if "start" not in events:
        print("Not started")
        return ["Yet","",""]
    if "dead" in events:
        ind_start = events.index("start")
        ind_dead = events.index("dead")
        duration = -counts[ind_start]+counts[ind_dead-1]
        print("Inactive. Duration: {} month".format(duration))
        return ["Inactive", dates[ind_start], duration]
    else:
        ind_start = events.index("start")
        duration = counts[-1]-counts[ind_start]
        print("Active. Duration: {}month".format(duration))
        return ["Active", dates[ind_start], duration]

def subscribers(url_top):
    # 読者数
    try:
        html = request.urlopen("{}/about".format(url_top))
        soup = BeautifulSoup(html, "html.parser")
        num = soup.find("span",class_="about-subscription-count").text
    except error.HTTPError as e: 
        # HTTPレスポンスのステータスコードが404, 403, 401などの例外処理
        print(e.reason)
    except error.URLError as e: 
        # アクセスしようとしたurlが無効なときの例外処理
        print(e.reason)
        return None
    except:
        print("Error")
        return None
    return int(num.replace(" ","").replace("人","").replace("\n",""))

def main():
    with open("blog_info.csv","w") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(["state", "start", "duration", "url", "article num","subscribers"])
    df = pd.read_csv("blog_url.csv")
    l = len(df)
    for count, url in enumerate(df.values):
        print("{}/{}: ".format(count,l),end="")
        try:
            html = request.urlopen(url[0])
        except error.HTTPError as e: 
            # HTTPレスポンスのステータスコードが404, 403, 401などの例外処理
            print(e.reason)
            continue
        except error.URLError as e: 
            # アクセスしようとしたurlが無効なときの例外処理
            print(e.reason)
            continue
        except:
            continue
        
        soup = BeautifulSoup(html, "html.parser")
        try:
            url_top = soup.html.get("data-blog-uri")
            events,dates,counts,atricle_num = get_status(url_top)
            result = checker(events, dates, counts)
            result.append(url)
            result.append(atricle_num)
            if result[0] == "Yet":
                num = 0
            else:    
                num = subscribers(url_top)
            result.append(num)
            print(result)
            with open("blog_info.csv","a") as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(result)
        except:
            continue

if __name__ == '__main__':
    main()