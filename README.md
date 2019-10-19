## 腾讯滑块验证码识别

腾讯滑块验证码识别,识别凹槽的x轴位置，mock滑块的加速度。该项目公开API，提供识别和加速度模拟部分，第二部分模拟滑动进行识别返回数据请求

项目地址：https://github.com/zhaojunlike/python-tecent-slider-crack

原文地址：https://segmentfault.com/a/1190000020618430

参考项目：https://github.com/shuxue051/captcha_crack
## 安装python环境

参考：https://janikarhunen.fi/how-to-install-python-3-6-1-on-centos-7

``` shell script
sudo yum install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum install python36u
python3.6 -V
sudo yum install python36u-pip
sudo yum install python36u-devel
```

## 创建环境 Creating a virtualenv

``` shell script
python3.6 -m venv venv
. venv/bin/activate
pip install [package_name]
# 安装依赖
pip install -r requirements.txt 
```
## daemonize 运行

``` shell script
# 参考 https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
# Install the latest stable release:
pip install uwsgi
# ... or if you want to install the latest LTS (long term support) release,
pip install https://projects.unbit.it/downloads/uwsgi-lts.tar.gz

# 创建ln 
cp captcha.service /etc/systemd/system/captcha.service
systemctl enable captcha.service
systemctl start captcha.service
```



``` shell script
uwsgi --ini /usr/local/nginx/html/myblog/uwsgiconfig.ini

#后台运行
uwsgi --ini /usr/local/nginx/html/myblog/uwsgiconfig.ini --daemonize /usr/local/nginx/html/myblog/myblog.out

```

# 是用nginx做代理

在nginx部分做一个代理
``` text
        location /tx/ {
            add_header Access-Control-Allow-Origin *;
            include        uwsgi_params;
            uwsgi_pass     127.0.0.1:8008;
        }

``` 


## 访问api

请求图片识别和加速度模拟
``` text
http://127.0.0.1:5000/tx/image

POST /tx/image HTTP/1.1
Host:host
Content-Type: application/json
Accept: */*
Cache-Control: no-cache
Accept-Encoding: gzip, deflate
Content-Length: 1055
Connection: keep-alive
cache-control: no-cache

{
    "url": "图片的地址"
}

返回数据

{
    "data": {
        "list": [],//模拟的点
        "url": "",//图片地址
        "x": 515,// x轴的偏移量
    },
    "message": "解析成功"
}
```


## 模拟浏览器移动
``` javascript
            const slider = {width: 680, point: 0, move: 0, steps: 0, posX: 0};//原本的高度
            //开始计算移动的距离
            slider.point = bgSize.width / slider.width * x;
            slider.move = handle.x + slider.point - 5;
            slider.steps = Math.random() * 100 / 30 + 100;
            slider.posX = handle.x + handle.width / 2;

            logger.info(`开始识别和移动滑块`, slider);

            //滑块的位置
            await page.mouse.move(slider.posX, handle.y + handle.height / 3, {steps: slider.steps});
            await page.mouse.down();
            let val = handle.x;
            for (let i = 0; i < traces.length; i++) {
                val += bgSize.width / slider.width * (traces[i]);//缩放距离
                slider.move = val;
                if (val <= slider.posX) continue;
                await page.mouse.move(slider.move, handle.y + handle.height / 2 + 5);
            }
            await page.waitFor(100);
            await page.mouse.up();
```

验证码识别成功后悔返回验证识别结果的Ticket

![2019-10-08-22-59-04](https://blog-oeynet-com.oss-cn-chengdu.aliyuncs.com/69814559f61d45d8b7253b1439538407.png)

## 我的博客

https://blog.oeynet.com


## 协议

授权协议：只允许研究、学习目的的分享、使用、修改，不允许任何商业用途。转载请注明出处，感谢。
