from flask import Flask
from flask import request, logging, make_response, jsonify
from utils.download import download_image_as_jpeg
import utils.crack_qq as crack_qq
import os
import uuid

app = Flask(__name__)
logger = logging.create_logger(app)


@app.route('/')
def root():
    return 'godtoy\'s python api , Use WeChat：zhaojunlike to contact me'


@app.route('/tx/image', methods=['POST'])
def image():
    try:
        json = request.get_json()
        url = json['url']
        # 1.下载图片
        file = os.path.join(os.path.dirname(__file__), "tmp", str(uuid.uuid4()) + "_captcha.jpg")
        _, code = download_image_as_jpeg(url, file)
        if not code == 200:
            return make_response(jsonify({'message': "解析失败Code:" + code}), 400)
        # 2.识别图片
        res = crack_qq.qq_mark_pos(file)
        dis = res.x.values[0]
        tacks = crack_qq.get_track_list(dis)  # 模拟加速度
        app.logger.debug("解析成功,需要移动距离:{},点数:{}".format(dis, len(tacks)))
        os.remove(file)  # 解析后删除文件就可以了
        return make_response(jsonify({'message': "解析成功", 'data': {'x': dis, 'list': tacks, 'url': url}}), 200)
    except Exception as e:
        print("e：", e)
        return make_response(jsonify({'message': "解析失败,请重新尝试"}), 400)


if __name__ == '__main__':
    app.run()
