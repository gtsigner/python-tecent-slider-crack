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
```



``` shell script
uwsgi --ini /usr/local/nginx/html/myblog/uwsgiconfig.ini

#后台运行
uwsgi --ini /usr/local/nginx/html/myblog/uwsgiconfig.ini --daemonize /usr/local/nginx/html/myblog/myblog.out
``` 