# captcha_crack
验证码破解


## 安装
可参考：https://janikarhunen.fi/how-to-install-python-3-6-1-on-centos-7

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
pip install -r requirements.txt
```
## daemonize 

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


## 协议

授权协议：只允许研究、学习目的的分享、使用、修改，不允许任何商业用途。转载请注明出处，感谢。