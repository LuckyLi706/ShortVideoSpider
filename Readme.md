<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [短视频爬虫](#%E7%9F%AD%E8%A7%86%E9%A2%91%E7%88%AC%E8%99%AB)
    - [需要的库](#%E9%9C%80%E8%A6%81%E7%9A%84%E5%BA%93)
    - [接口](#%E6%8E%A5%E5%8F%A3)
        - [单个视频](#%E5%8D%95%E4%B8%AA%E8%A7%86%E9%A2%91)
        - [多个视频](#%E5%A4%9A%E4%B8%AA%E8%A7%86%E9%A2%91)
        - [用户信息](#%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF)
    - [免责声明](#%E5%85%8D%E8%B4%A3%E5%A3%B0%E6%98%8E)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 短视频爬虫

使用Python来爬取短视频链接，目前只抓了抖音的，用Flask生成了api接口，配套客户端详见[short_video_spider_client](https://github.com/LuckyLi706/short_video_spider_client)

## 需要的库

+ Flask~=2.1.2
+ requests
+ pyOpenSSL
+ Flask-APScheduler

## 运行

### 使用python运行

python app.py (此时会走main函数)

### 使用flask运行

flask run -p 8080 -h 0.0.0.0 （指定主机和端口，此时不会走main函数）

## 黑名单功能

将黑名单IP填入rules.txt,以换行符隔开

## 接口

### 单个视频

+ 本地地址：http://ip:port/douyin/single?url=https://v.douyin.com/2jA2dGq/&is_origin=0
+ 线上地址：http://81.68.122.109:8080/douyin/single?url=https://v.douyin.com/2jA2dGq/&is_origin=0
  ```
  参数说明：
  url：分享的短视频链接,可以直接使用复制内容，会解析里面的链接
  
  is_origin: 是否需要原始返回数据（0为不需要，1为需要）
  
  返回数据（is_origin为0）：
  {
  "code": 200,
  //cover_image_url 视频封面的图片地址
  "cover_image_url": "https://p3-sign.douyinpic.com/obj/tos-cn-i-dy/b3cc0713ff7c4ad58e989ad4b8fde693?x-expires=1659412800&x-signature=SxHpFcL6X9HpvAS005QMN%2BhPh2Q%3D&from=4257465056_large",
  //video_url 视频无水印地址
  "video_url": "https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200fg10000cb6l3ojc77u09nmstov0&ratio=720p&line=0"
  //video_desc 短视频的文案描述
  "video_desc":"..."
  }

  返回数据（is_origin为1）：
  抖音的详细数据，返回的数据太多，自己进行测试。
  
  ```

### 多个视频

+ 本地地址：http://ip:port/douyin/list?url=https://v.douyin.com/2YVVPR7/&is_origin=0&max_cursor=0
+ 线上地址：http://81.68.122.109:8080/douyin/list?url=https://v.douyin.com/2YVVPR7/&is_origin=0&max_cursor=0
  ```
  参数说明：（一次最多返回20条数据）
  url：分享的用户主页链接,可以直接使用复制内容，会解析里面的链接
  is_origin: 是否需要原始返回数据（0为不需要，1为需要）
  max_cursor：第一次为0，返回会有hasmore来确定是否有更多数据，设置返回的max_cursor到下次的请求参数来请求下次的数据
  返回数据（is_origin为0）：
  {
  "code": 200,
  //视频封面图片地址的列表
  "cover_image_url_list": [
     .....
  ],
  //描述信息
  "des": "",
  //是否有更多数据
  "has_more": true,
  //下次最大滑动距离
  "max_cursor": 1643624245000,
  //视频无水印地址列表
  "video_url_list": [
     .....
   ]
  //视频文案列表
  "video_desc_list":[
     .....
  ]
  }

  请求的数据太多，自己进行测试。
  ```

### 用户信息

+ 本地地址：http://ip:port/douyin/user?url=https://v.douyin.com/2YVVPR7/
+ 线上地址：http://81.68.122.109:8080/douyin/user?url=https://v.douyin.com/2YVVPR7/
  ```
  参数说明：
  url：分享的用户主页链接,可以直接使用复制内容，会解析里面的链接
  返回数据：
  { "code": 200,
    "extra": {
     "logid": "20220715151907010209168157440162C9",
     "now": 1657869547000 },
    "status_code": 0,
    "user_info": {
     "avatar_larger": {
         "uri": "aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9",
         "url_list": [
             "https://p3.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9.jpeg?from=2956013662",
             "https://p11.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9.jpeg?from=2956013662",
             "https://p26.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9.jpeg?from=2956013662"
         ]
     },
     "avatar_medium": {
         "uri": "aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9",
         "url_list": [
             "https://p3.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9.jpeg?from=2956013662",
             "https://p11.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9.jpeg?from=2956013662",
             "https://p26.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9.jpeg?from=2956013662"
         ]
     },
     "avatar_thumb": {
         "uri": "aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9",
         "url_list": [
             "https://p3.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9.jpeg?from=2956013662",
             "https://p11.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9.jpeg?from=2956013662",
             "https://p26.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i-0813_8b7da88366bc40bba58e2f8bce0255c9.jpeg?from=2956013662"
         ]
     },
     "aweme_count": 6,
     "card_entries": [],
     "custom_verify": "",
     "enterprise_verify_reason": "",
     "favoriting_count": 0,
     "follow_status": 0,
     "follower_count": 101,
     "followers_detail": null,
     "following_count": 239,
     "geofencing": null,
     "is_gov_media_vip": false,
     "is_mix_user": false,
     "mix_count": 0,
     "mix_info": null,
     "mplatform_followers_count": 101,
     "nickname": "十七😍",
     "original_musician": {
         "digg_count": 0,
         "music_count": 0,
         "music_used_count": 0
     },
     "platform_sync_info": [],
     "policy_version": null,
     "sec_uid": "MS4wLjABAAAAsRIQ9howZwtPIsFFZhkMS6q2KIc4wLs5q7LlExJqUNA",
     "secret": 0,
     "short_id": "0",
     "show_favorite_list": false,
     "signature": "互关咯\n#中二病 #熬夜冠军 #俄语废物",
     "total_favorited": "263",
     "type_label": null,
     "uid": "405060254438335",
     "unique_id": "xsy897256134",
     "verification_type": 0
    }}    
    ```

## 免责声明

本仓库只为学习研究，如涉及侵犯个人或者团体利益，请与我取得联系，我将主动删除一切相关资料，谢谢！
