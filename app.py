import requests
from flask import Flask, request

# 抖音爬虫地址 https://blog.csdn.net/qq470603823/article/details/109242222
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/94.0.4606.71 Safari/537.36 "}


def douyin(url=''):
    # 参考 https://blog.csdn.net/m0_46521785/article/details/109684811
    # 获取抖音用户信息 （sec_uid咋生成的？？）
    # https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=MS4wLjABAAAAsRIQ9howZwtPIsFFZhkMS6q2KIc4wLs5q7LlExJqUNA
    # 获取抖音用户下的所有视频  （max_cursor 是否可以滑动，_signature咋来的？？）
    # https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAsRIQ9howZwtPIsFFZhkMS6q2KIc4wLs5q7LlExJqUNA&count=21&max_cursor=0&_signature=5ifCTAAAhPBHTuX.S4ev0uYnwl
    resp = requests.get(url).url  # 获取url的重定向地址
    print(resp)
    real_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + resp.replace(
        "https://www.douyin.com/video/", "")
    response = requests.get(real_url, headers=headers)
    json_response = response.json()
    print(json_response)
    video_url = json_response['item_list'][0]['video']['play_addr']['url_list'][0]
    return str(video_url).replace("playwm", "play")


def douyin_user_info(url=''):
    # 参考 https://blog.csdn.net/m0_46521785/article/details/109684811
    # 获取抖音用户信息 （sec_uid就是重定向地址后面的值）
    # https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=MS4wLjABAAAAsRIQ9howZwtPIsFFZhkMS6q2KIc4wLs5q7LlExJqUNA
    # 获取抖音用户下的所有视频  （max_cursor 是否可以滑动，_signature难分析）
    # https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAsRIQ9howZwtPIsFFZhkMS6q2KIc4wLs5q7LlExJqUNA&count=21&max_cursor=0&_signature=5ifCTAAAhPBHTuX.S4ev0uYnwl
    resp = requests.get(url).url  # 获取url的重定向地址
    print(resp)
    real_url = "https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=" + resp.replace(
        "https://www.douyin.com/user/", "")
    response = requests.get(real_url, headers=headers)
    json_response = response.json()
    print(json_response)
    return json_response


def analyse_url(url=''):
    if len(url) == 0:
        return "url是空的"
    else:
        if not url.startswith("https"):
            print(url)
            url_1 = url[url.rfind('https'):]
            print(url_1)
            url = url_1[0:url_1.rfind('/')]
    try:
        return douyin(url)
    except (RuntimeError, TypeError, NameError):
        return "系统出现异常，url解析失败"


app = Flask(__name__)


# 获取真实的下载地址
@app.route("/douyin", methods=['GET'])
def dy_url():
    url = request.args.get('url')
    return analyse_url(url=url)


# 获取用户信息
@app.route("/user", methods=['GET'])
def dy_user_info():
    url = request.args.get('url')
    return douyin_user_info(url=url)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
