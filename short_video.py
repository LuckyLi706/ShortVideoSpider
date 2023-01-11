"""
针对短视频处理类
目前支持抖音单个视频和多个视频的获取
"""
# -- coding: utf-8 --
import re

import requests
from short_video_type import ShortVideoType

__REQUEST_HEADER = {"user-agent": "Mozilla/5.0 (Linux; Android 9.0; SAMSUNG SM-F900U Build/PPR1.180610.011) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36",
                    "Cookie": '__ac_nonce=063be2be9000260c8616a; '
                              '__ac_signature=_02B4Z6wo00f01JsPGiwAAIDB48HxKq6aRUCbPx6AAEWC1JgK5i1XnxhYZV6bhMSHVm'
                              '-1W6RcC3PEi2bOQdXX29GERz3AInNnZOhvZh2hegmceqyKB0TU5HPHRbttds2l6uRn0CnLF79DSemN1c; '
                              's_v_web_id=verify_lcr3lkk4_nm3BMcfw_JZYJ_4FIi_B1UL_JgpgXNzIntoy; '
                              '_tea_utm_cache_2018=undefined; '
                              'ttwid=1%7CZmEFW4YDG2mZjAvxfCC3j3CZSeyDKE8CIIm6PYQ6m6U%7C1673407477'
                              '%7Cea8e988f50ea4864f0acbca30ddba9dd8f54993d0dc8c60f2577cda95e12f6b1; '
                              'msToken=22L7umFLAPPCYQD65Kxwh6EUaertkP4LBccYZmT_fOaVWt-tR6'
                              '-a4OOwgsn_1FATJFF1vWU7BoWLo259q7eCS_geGDsJsW9dpknp1vMtpaAx3QvbJT43ofY1IzNYsg==; '
                              'msToken=8ouSxeM_B5BbUPovBKKz5cYpukRhzu3iFdOPKLlmN54NQm_lj4NTQC'
                              '-sZXkjAgO_dFMQe3Js5cEDc3zmFG5wyMNphesCiAuDWaRenuPPHy0GWDNZ5iqcOzuW0fUung==; '
                              'ttcid=4169d143891843c49965001fc2b97b7c52; '
                              'tt_scid=8O6F4JHvGPbnTJvkAOKUPdXuqoWdVIuCxHhSWlsBdXlZ4bVswKLfwe2WyqRUi5Ns731f'}
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
        params = {'item_ids': get_items_ids(resp)}
        response = requests.get(__DOUYIN_SINGLE_BASE_URL, params=params, headers=__REQUEST_HEADER)
        json_response = response.json()
        if json_response['status_code'] != 0:
            json_error = {'code': 500, 'des': f'地址解析失败，复制地址重试'}
            return json_error
        if is_origin != 0:
            json_response['code'] = 200
            return json_response
        elif resp.__contains__('note'):  # 解析全是图片的
            image_list = json_response['item_list'][0]['images']
            image_url_list = []
            image_desc = json_response['item_list'][0]['desc']
            for index in range(len(image_list)):
                image_url_list.append(image_list[index]['url_list'][3])
            return {'image_url_list': image_url_list, 'code': 200, 'image_desc': image_desc}
        else:  # 解析视频信息
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
