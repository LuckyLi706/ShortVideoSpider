import requests
from flask import Flask, request

# 抖音爬虫地址 https://blog.csdn.net/qq470603823/article/details/109242222
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/94.0.4606.71 Safari/537.36 "}


def single_video_douyin(url='', is_origin=0):
    try:
        url = analyse_url(url)
        # 参考 https://blog.csdn.net/m0_46521785/article/details/109684811
        resp = requests.get(url).url  # 获取url的重定向地址
        item_ids = remove_url_before(resp, "https://www.douyin.com/video/")
        real_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_ids}'
        response = requests.get(real_url, headers=headers)
        json_response = response.json()
        if json_response['status_code'] != 0:
            json_error = {'code': 500, 'des': f'地址解析失败，复制地址重试'}
            return json_error
        if is_origin != 0:
            json_response['code'] = 200
            return json_response
        else:
            video_url = json_response['item_list'][0]['video']['play_addr']['url_list'][0]
            origin_cover_imager_url = json_response['item_list'][0]['video']['origin_cover']['url_list'][0]
            return {'video_url': str(video_url).replace('playwm', 'play'), 'code': 200,
                    'cover_image_url': origin_cover_imager_url}
    except Exception as result:
        json_error = {'code': 500, 'des': f'系统内部出现异常，{result}'}
        return json_error


def douyin_user_info(url=''):
    try:
        # 获取抖音用户信息 （sec_uid就是重定向地址后面的值）
        # https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid
        url = analyse_url(url)
        resp = requests.get(url).url  # 获取url的重定向地址
        sec_uid = remove_url_before(resp)
        real_url = f'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={sec_uid}'
        response = requests.get(real_url, headers=headers)
        json_response = response.json()
        if json_response['status_code'] != 0:
            json_error = {'code': 500, 'des': f'地址解析失败，复制地址重试'}
            return json_error
        json_response['code'] = 200
        return json_response
    except Exception as result:
        json_error = {'code': 500, 'des': f'系统内部出现异常，{result}'}
        return json_error


def list_video_douyin(url='', max_cursor=0, is_origin=0):
    try:
        url = analyse_url(url)
        resp = requests.get(url).url  # 获取url的重定向地址
        sec_uid = remove_url_before(resp)
        # 获取抖音用户下的所有视频  （max_cursor 是否可以滑动，_signature难分析）
        # https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAsRIQ9howZwtPIsFFZhkMS6q2KIc4wLs5q7LlExJqUNA&count=21&max_cursor=0&_signature=5ifCTAAAhPBHTuX.S4ev0uYnwl
        real_url = f'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={sec_uid}&count=21&max_cursor={max_cursor}'
        response = requests.get(real_url, headers=headers)
        json_response = response.json()
        if json_response['status_code'] != 0:
            json_error = {'code': 500, 'des': f'地址解析失败，复制地址重试'}
            return json_error
        if is_origin != 0:
            json_response['code'] = 200
            return json_response
        else:
            video_url_list = []
            cover_image_url_list = []
            aweme_list = json_response['aweme_list']
            max_cursor = json_response['max_cursor']
            has_more = json_response['has_more']
            for key in aweme_list:
                video_url = key['video']['download_addr']['url_list'][0]
                video_url_list.append(video_url.replace('watermark=1', 'watermark=0'))
                cover_image_url_list.append(key['video']['origin_cover']['url_list'][0])
            return {'code': 200, 'max_cursor': max_cursor, 'has_more': has_more, 'video_url_list': video_url_list,
                    'cover_image_url_list': cover_image_url_list, 'des': ''}
    except Exception as result:
        json_error = {'code': 500, 'des': f'系统内部出现异常，{result}'}
        return json_error


def remove_url_before(resp, value='https://www.douyin.com/user/'):
    return resp.replace(
        value, "")


def analyse_url(url=''):
    if not url.startswith('https'):
        text_list = url.split(" ")
        for i in range(len(text_list)):
            if text_list[i].startswith("https") & text_list[i].__contains__("douyin.com"):
                return text_list[i]
    return url


app = Flask(__name__)

dy_video_number = 0
dy_user_info_number = 0
dy_user_video_list_number = 0


# 获取单个抖音的真实下载地址
@app.route('/douyin/single', methods=['GET'])
def dy_video_url():
    global dy_video_number
    dy_video_number = dy_video_number + 1
    print(f"dy_video_url:{dy_video_number}")
    url = request.args.get('url')
    is_origin = request.args.get('is_origin')
    if is_origin is None:
        is_origin = 0
    return single_video_douyin(url=url, is_origin=int(is_origin))


# 获取用户信息
@app.route('/douyin/user', methods=['GET'])
def dy_user_info():
    global dy_user_info_number
    dy_user_info_number = dy_user_info_number + 1
    print(f"dy_user_info:{dy_user_info_number}")
    url = request.args.get('url')
    return douyin_user_info(url=url)


# 获取当前用户下的抖音列表
@app.route('/douyin/list', methods=['GET'])
def dy_user_video_list():
    global dy_user_video_list_number
    dy_user_video_list_number = dy_user_video_list_number + 1
    print(f"dy_user_video_list:{dy_user_video_list_number}")
    url = request.args.get('url')
    max_cursor = request.args.get('max_cursor')
    is_origin = request.args.get('is_origin')
    if max_cursor is None:
        max_cursor = 0
    if is_origin is None:
        is_origin = 0
    return list_video_douyin(url=url, max_cursor=int(max_cursor), is_origin=int(is_origin))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
