from flask import Flask
from flask import request, logging, make_response, jsonify
from utils.download import download_image_as_jpeg
from utils.crack_qq import qq_mark_detect, get_track
import os
import uuid

app = Flask(__name__)
logger = logging.create_logger(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/tx/image', methods=['POST'])
def image():
    json = request.get_json()
    url = json['url']
    # 1.下载图片
    # 2.识别图片
    app.logger.debug(url)
    file = os.path.join(os.path.dirname(__file__), "tmp", str(uuid.uuid4()) + "_captcha.jpg")
    print(file)
    download_image_as_jpeg(url, "./tmp/a.jpg")
    res = qq_mark_detect("./tmp/a.jpg")
    dis = res.x.values[0]
    tacks = get_track(dis)
    print("解析成功：", dis)
    try:
        os.remove(file)
    except EnvironmentError as e:
        print("e：", e)
    return make_response(jsonify({'message': "解析成功", 'data': {'x': dis, 'list': tacks, 'url': url}}), 200)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
