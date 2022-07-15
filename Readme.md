<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [短视频爬虫](#%E7%9F%AD%E8%A7%86%E9%A2%91%E7%88%AC%E8%99%AB)
  - [需要的库](#%E9%9C%80%E8%A6%81%E7%9A%84%E5%BA%93)
  - [接口](#%E6%8E%A5%E5%8F%A3)
    - [单个视频](#%E5%8D%95%E4%B8%AA%E8%A7%86%E9%A2%91)
    - [多个视频](#%E5%A4%9A%E4%B8%AA%E8%A7%86%E9%A2%91)
    - [用户信息](#%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 短视频爬虫
使用Python来爬取短视频链接，目前只抓了抖音的，用Flask生成了Api接口,

## 需要的库
  + Flask~=2.1.2
  + requests
  + pyOpenSSL

## 接口
### 单个视频
  + 本地地址：http://192.168.30.56:8080/douyin/single?url=https://v.douyin.com/2jA2dGq/&is_origin=0
    ```
    参数说明：
    url：分享的短视频链接,可以直接使用复制内容，会解析里面的链接
    is_origin: 是否需要原始返回数据（0为需要，1为不需要）
    返回数据（is_origin为0）：
    {
    "code": 200,
    "video_url": "https://aweme.snssdk.com/aweme/v1/play?video_id=v0200fg10000cb6l3ojc77u09nmstov0&ratio=720p&line=0"
    }
    返回数据（is_origin为1）：
    {
    "code": 200,
    "extra": {
        "logid": "202207151459210102080660730D0001F0",
        "now": 1657868362000
    },
    "filter_list": [],
    "item_list": [
        {
            "author": {
                "avatar_larger": {
                    "uri": "1080x1080/aweme-avatar/mosaic-legacy_c150001e6de3d8e4e65",
                    "url_list": [
                        ......
                    ]
                },
                "avatar_medium": {
                    "uri": "720x720/aweme-avatar/mosaic-legacy_c150001e6de3d8e4e65",
                    "url_list": [
                        ......
                    ]
                },
                "avatar_thumb": {
                    "uri": "100x100/aweme-avatar/mosaic-legacy_c150001e6de3d8e4e65",
                    "url_list": [
                        .....
                    ]
                },
                "card_entries": null,
                "follow_status": 0,
                "followers_detail": null,
                "geofencing": null,
                "mix_info": null,
                "nickname": "陈翔六点半",
                "platform_sync_info": null,
                "policy_version": null,
                "short_id": "3559807",
                "signature": "7月15日13:00 来我们直播间一起摸鱼？\n陈翔导演作品！\n商务合作邮箱：sw@cxldb.com",
                "type_label": null,
                "uid": "6556303280",
                "unique_id": "cxldb001"
            },
            "author_user_id": 6556303280,
            "aweme_id": "7119437431757229320",
            "aweme_type": 4,
            "category": 0,
            "cha_list": [
                {
                    "cha_name": "陈翔六点半",
                    "cid": "1585033776113694",
                    "connect_music": null,
                    "cover_item": {
                        "uri": "compass/RfupYzYBDKSUTF",
                        "url_list": [
                            ......
                        ]
                    },
                    "desc": "",
                    "hash_tag_profile": "compass/RfupYzYBDKSUTF",
                    "is_commerce": false,
                    "type": 1,
                    "user_count": 0,
                    "view_count": 0
                }
            ],
            "comment_list": null,
            "create_time": 1657623223,
            "desc": "这个世界难道真的没有人能阻挡卷王了吗？#陈翔六点半  #公司日常 ",
            "duration": 294618,
            "forward_id": "0",
            "geofencing": null,
            "group_id": 7119437431757229000,
            "group_id_str": "7119437431757229320",
            "image_infos": null,
            "images": null,
            "is_live_replay": false,
            "is_preview": 0,
            "label_top_text": null,
            "long_video": null,
            "music": {
                "author": "陈翔六点半",
                "cover_hd": {
                    "uri": "1080x1080/aweme-avatar/mosaic-legacy_c150001e6de3d8e4e65",
                    "url_list": [
                        .....
                    ]
                },
                "cover_large": {
                    "uri": "1080x1080/aweme-avatar/mosaic-legacy_c150001e6de3d8e4e65",
                    "url_list": [
                        .....
                    ]
                },
                "cover_medium": {
                    "uri": "720x720/aweme-avatar/mosaic-legacy_c150001e6de3d8e4e65",
                    "url_list": [
                        .....
                    ]
                },
                "cover_thumb": {
                    "uri": "168x168/aweme-avatar/mosaic-legacy_c150001e6de3d8e4e65",
                    "url_list": [
                        .....
                    ]
                },
                "duration": 294,
                "id": 7119437660095385000,
                "mid": "7119437660095384334",
                "play_url": {
                    "uri": "https://sf6-cdn-tos.douyinstatic.com/obj/ies-music/7119437658728008461.mp3",
                    "url_list": [
                        "https://sf6-cdn-tos.douyinstatic.com/obj/ies-music/7119437658728008461.mp3",
                        "https://sf3-cdn-tos.douyinstatic.com/obj/ies-music/7119437658728008461.mp3"
                    ]
                },
                "position": null,
                "status": 1,
                "title": "@陈翔六点半创作的原声一陈翔六点半（原声中的歌曲：B-Life-C MUSIC Professional Library）"
            },
            "promotions": null,
            "risk_infos": {
                "content": "",
                "reflow_unplayable": 0,
                "type": 0,
                "warn": false
            },
            "share_info": {
                "share_desc": "在抖音，记录美好生活",
                "share_title": "这个世界难道真的没有人能阻挡卷王了吗？#陈翔六点半  #公司日常 ",
                "share_weibo_desc": "#在抖音，记录美好生活#这个世界难道真的没有人能阻挡卷王了吗？#陈翔六点半  #公司日常 "
            },
            "share_url": "https://www.iesdouyin.com/share/video/7119437431757229320/?region=&mid=7119437660095384334&u_code=0&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ&with_sec_did=1&titleType=title",
            "statistics": {
                "aweme_id": "7119437431757229320",
                "comment_count": 19411,
                "digg_count": 729690,
                "play_count": 0,
                "share_count": 42101
            },
            "text_extra": [
                {
                    "end": 25,
                    "hashtag_id": 1585033776113694,
                    "hashtag_name": "陈翔六点半",
                    "start": 19,
                    "type": 1
                },
                {
                    "end": 32,
                    "hashtag_id": 1591267371655182,
                    "hashtag_name": "公司日常",
                    "start": 27,
                    "type": 1
                }
            ],
            "video": {
                "bit_rate": null,
                "cover": {
                    "uri": "tos-cn-i-dy/b3cc0713ff7c4ad58e989ad4b8fde693",
                    "url_list": [
                        .....
                    ]
                },
                "duration": 294618,
                "dynamic_cover": {
                    "uri": "tos-cn-i-dy/b3cc0713ff7c4ad58e989ad4b8fde693",
                    "url_list": [
                        .....
                    ]
                },
                "has_watermark": true,
                "height": 1080,
                "is_long_video": 1,
                "origin_cover": {
                    "uri": "tos-cn-p-0015/c28d7b873ca045a3ac18aa6a867104d7_1657623227",
                    "url_list": [
                        .....
                    ]
                },
                "play_addr": {
                    "uri": "v0200fg10000cb6l3ojc77u09nmstov0",
                    "url_list": [
                        "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200fg10000cb6l3ojc77u09nmstov0&ratio=720p&line=0"
                    ]
                },
                "ratio": "540p",
                "vid": "v0200fg10000cb6l3ojc77u09nmstov0",
                "width": 1920
            },
            "video_labels": null,
            "video_text": null
        }
    ],
    "status_code": 0   } ```

### 多个视频
   + 本地地址：http://192.168.30.56:8080/douyin/list?url=https://v.douyin.com/2YVVPR7/&is_origin=0&max_cursor=0
     ```
     参数说明：（一次最多返回20条数据）
     url：分享的用户主页链接,可以直接使用复制内容，会解析里面的链接
     is_origin: 是否需要原始返回数据（0为需要，1为不需要）
     max_cursor：第一次为0，返回会有hasmore来确定是否有更多数据，设置返回的max_cursor到下次的请求参数来请求下次的数据

     请求的数据太多，自己进行测试。
     ```

### 用户信息
   + 用户信息：http://192.168.30.56:8080/douyin/user?url=https://v.douyin.com/2YVVPR7/
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
       }}       ```
