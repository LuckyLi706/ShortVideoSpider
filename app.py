from flask import Flask, request
from flask_apscheduler import APScheduler
import short_video as video


def is_number(value: str):
    for c in value:
        if '0' <= c <= '9':
            continue
        else:
            return False
    return True


ip_rules = {}
black_ips = []


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
def dy_single_video():
    if ip_black_rules(request.remote_addr):
        return f"当前ip：{request.remote_addr},访问次数过多，被加入黑名单，请告知原因予以解封"
    url = request.args.get('url')
    is_origin = request.args.get('is_origin')
    if is_origin is None:
        is_origin = 0
    return video.douyin_single(url=url, is_origin=int(is_origin))


# 获取当前用户下的抖音列表
@app.route('/douyin/list', methods=['GET'])
def dy_user_video_list():
    if ip_black_rules(request.remote_addr):
        return f"当前ip：{request.remote_addr},访问次数过多，被加入黑名单，请告知原因予以解封"
    url = request.args.get('url')
    max_cursor = request.args.get('max_cursor')
    is_origin = request.args.get('is_origin')
    if max_cursor is None or not is_number(max_cursor):
        max_cursor = 0
    if is_origin is None:
        is_origin = 0
    return video.douyin_list(url=url, max_cursor=int(max_cursor), is_origin=int(is_origin))


# 获取单个抖音的真实下载地址
@app.route('/tiktok/single', methods=['GET'])
def tt_single_video():
    if ip_black_rules(request.remote_addr):
        return f"当前ip：{request.remote_addr},访问次数过多，被加入黑名单，请告知原因予以解封"
    url = request.args.get('url')
    is_origin = request.args.get('is_origin')
    if is_origin is None:
        is_origin = 0
    return video.tiktok_single(url=url, is_origin=int(is_origin))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
