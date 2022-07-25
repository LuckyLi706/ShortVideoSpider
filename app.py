import logging

import requests
from flask import Flask, request

# 抖音爬虫地址 https://blog.csdn.net/qq470603823/article/details/109242222
from flask_apscheduler import APScheduler


def is_number(value: str):
    for c in value:
        if '0' <= c <= '9':
            continue
        else:
            return False
    return True


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/94.0.4606.71 Safari/537.36 "}

ip_rules = {}
black_ips = []


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
            origin_cover_imager_url = json_response['item_list'][0]['video']['dynamic_cover']['url_list'][0]
            video_desc = json_response['item_list'][0]['desc'].replace(' ', '')
            return {'video_url': str(video_url).replace('playwm', 'play'), 'code': 200,
                    'cover_image_url': origin_cover_imager_url, 'video_desc': video_desc}
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
            video_desc_list = []
            aweme_list = json_response['aweme_list']
            max_cursor = json_response['max_cursor']
            has_more = json_response['has_more']
            for key in aweme_list:
                # 这边除了是视频还可能是音频，音频只有两项
                if len(key['video']['play_addr']['url_list']) == 2:
                    video_url = key['video']['play_addr']['url_list'][0]
                    cover_image_url_list.append(key['video']['cover']['url_list'][0])
                else:
                    video_url = key['video']['play_addr']['url_list'][2]
                    cover_image_url_list.append(key['video']['dynamic_cover']['url_list'][0])
                video_url_list.append(video_url.replace('watermark=1', 'watermark=0'))
                video_desc = key['desc'].replace(' ', '')
                video_desc_list.append(video_desc)
            return {'code': 200, 'max_cursor': max_cursor, 'has_more': has_more, 'video_url_list': video_url_list,
                    'cover_image_url_list': cover_image_url_list, 'des': '', 'video_desc_list': video_desc_list}
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


# 针对恶意ip加入黑名单处理
def ip_black_rules(ip):
    for i in range(len(black_ips)):
        if black_ips[i].replace('\n', '') == ip:
            app.logger.warn(f"IP:{ip},已经加入黑名单")
            return True
    times = ip_rules.get(ip)
    if times is None:
        ip_rules[ip] = 1
    else:
        ip_rules[ip] = times + 1
    app.logger.warn(f"IP:{ip},请求次数：{ip_rules[ip]}")
    return False


app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


# log = logging.getLogger('werkzeug')
# log.disabled = True


# 黑名单功能，一小时的定时任务
@scheduler.task('interval', id='1', seconds=1 * 60 * 60, misfire_grace_time=900)
def get_rules():
    global black_ips
    path = r'rules.txt'
    file = open(path, 'r')
    black_ips = file.readlines()
    app.logger.warn(f"黑名单：{black_ips}")
    file.close()  # 文件打开，使用完毕后需要关闭


get_rules()  # 启动之后执行一次


# 获取单个抖音的真实下载地址
@app.route('/douyin/single', methods=['GET'])
def dy_video_url():
    if ip_black_rules(request.remote_addr):
        return f"当前ip：{request.remote_addr},访问次数过多，被加入黑名单，请告知原因予以解封"
    url = request.args.get('url')
    is_origin = request.args.get('is_origin')
    if is_origin is None:
        is_origin = 0
    return single_video_douyin(url=url, is_origin=int(is_origin))


# 获取用户信息
@app.route('/douyin/user', methods=['GET'])
def dy_user_info():
    if ip_black_rules(request.remote_addr):
        return f"当前ip：{request.remote_addr},访问次数过多，被加入黑名单，请告知原因予以解封"
    url = request.args.get('url')
    return douyin_user_info(url=url)


# 获取当前用户下的抖音列表
@app.route('/douyin/list', methods=['GET'])
def dy_user_video_list():
    if ip_black_rules(request.remote_addr):
        return f"当前ip：{request.remote_addr},访问次数过多，被加入黑名单，请告知原因予以解封"
    url = request.args.get('url')
    max_cursor = request.args.get('max_cursor')
    is_origin = request.args.get('is_origin')
    if max_cursor is None:
        max_cursor = 0
    if not is_number(max_cursor):
        return {'code': 500, 'des': 'max_cursor必须是数字,请勿轻易改动默认值'}
    if is_origin is None:
        is_origin = 0
    return list_video_douyin(url=url, max_cursor=int(max_cursor), is_origin=int(is_origin))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
