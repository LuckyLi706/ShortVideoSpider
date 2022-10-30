"""
针对短视频处理类
目前支持抖音单个视频和多个视频的获取
"""
# -- coding: utf-8 --
import re

import requests
from short_video_type import ShortVideoType

__REQUEST_HEADER = {"user-agent": "Mozilla/5.0 (Linux; Android 9.0; SAMSUNG SM-F900U Build/PPR1.180610.011) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"}
# tiktok需要代理
__REQUEST_PROXIES = {"http": "http://127.0.0.1:7890", "https": "https://127.0.0.1:7890", }
__DOUYIN_SINGLE_BASE_URL = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/"
__DOUYIN_LIST_BASE_URL = "https://www.iesdouyin.com/web/api/v2/aweme/post/"
__DOUYIN_PREFIX_SINGLE_URL = "https://www.douyin.com/video/"
__DOUYIN_PREFIX_SINGLE_URL_NOTE = "https://www.douyin.com/note/"  # 这当前是图文信息
__DOUYIN_PREFIX_LIST_URL = "https://www.douyin.com/user/"

__TIKTOK_SINGLE_BASE_URL = "https://api.tiktokv.com/aweme/v1/aweme/detail/"


def format_url(video_type, url=''):
    if video_type == ShortVideoType.DOU_YIN:  # 抖音的处理
        if not url.startswith('https'):
            r = re.findall('https.*/', url)
            if len(r) > 0:
                return r[0]
    return url


def get_items_ids(url=''):
    items_ids = url.replace(__DOUYIN_PREFIX_SINGLE_URL, '').replace(__DOUYIN_PREFIX_SINGLE_URL_NOTE, '')
    if items_ids.__contains__('?'):
        return items_ids.split('?')[0]
    return items_ids


def douyin_single(url='', is_origin=0):
    try:
        url = format_url(ShortVideoType.DOU_YIN, url)
        resp = requests.get(url).url  # 获取url的重定向地址
        if resp.__contains__('note'):
            json_error = {'code': 500, 'des': f'目前只支持视频解析,暂时不支持图文解析'}
            return json_error
        params = {'item_ids': get_items_ids(resp)}
        response = requests.get(__DOUYIN_SINGLE_BASE_URL, params=params, headers=__REQUEST_HEADER)
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


def douyin_list(url='', max_cursor=0, is_origin=0):
    try:
        url = format_url(ShortVideoType.DOU_YIN, url)
        resp = requests.get(url).url  # 获取url的重定向地址
        sec_uid = resp.replace(__DOUYIN_PREFIX_LIST_URL, '')
        if sec_uid.__contains__('?'):
            sec_uid = sec_uid.split('?')[0]
        params = {'sec_uid': sec_uid, 'count': 21, 'max_cursor': max_cursor}
        print(params)
        response = requests.get(__DOUYIN_LIST_BASE_URL, params=params, headers=__REQUEST_HEADER)
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
                if len(key['video']['play_addr']['url_list']) <= 2:
                    video_url = key['video']['play_addr']['url_list'][0]
                    cover_image_url_list.append(key['video']['cover']['url_list'][0])
                else:
                    video_url = key['video']['play_addr']['url_list'][2]
                    cover_image_url_list.append(key['video']['dynamic_cover']['url_list'][0])
                video_url_list.append(video_url.replace('watermark=1', 'watermark=0'))
                video_desc = key['desc'].replace(' ', '')
                video_desc_list.append(video_desc)
            return {'code': 200, 'max_cursor': max_cursor, 'has_more': has_more, 'video_url_list': video_url_list,
                    'cover_image_url_list': cover_image_url_list, 'des': '', 'video_desc_list': video_desc_list,
                    "sec_uid": sec_uid}
    except Exception as result:
        json_error = {'code': 500, 'des': f'系统内部出现异常，{result}'}
        return json_error


def tiktok_single(url='', is_origin=0):
    try:
        url = format_url(ShortVideoType.TIK_TOK, url)
        aweme_id = re.findall('\\d{19}', url)
        params = {'aweme_id': aweme_id[0]}
        response = requests.get(__TIKTOK_SINGLE_BASE_URL, params=params, headers=__REQUEST_HEADER,
                                proxies=__REQUEST_PROXIES)
        json_response = response.json()
        if json_response['status_code'] != 0:
            json_error = {'code': 500, 'des': f'地址解析失败，复制地址重试'}
            return json_error
        if is_origin != 0:
            json_response['code'] = 200
            return json_response
        else:
            video_url = json_response["aweme_detail"]["video"]["play_addr"]["url_list"][0]
            origin_cover_imager_url = json_response['aweme_detail']['video']['dynamic_cover']['url_list'][0]
            video_desc = json_response['aweme_detail']['desc'].replace(' ', '')
            return {'video_url': video_url, 'code': 200,
                    'cover_image_url': origin_cover_imager_url, 'video_desc': video_desc}
    except Exception as result:
        json_error = {'code': 500, 'des': f'系统内部出现异常，{result}'}
        return json_error
