# 后端启动流程

- 创建conda环境并切换环境(name为自己设的环境名称)
```
conda create -n name python=3.8
conda activate name
```

- 安装环境

```
pip install django==4.2.5
pip install pymysql
pip install django-crontab 
pip install opencv-python
pip install django-cors-headers
pip install cos-python-sdk-v5
pip install pillow
pip install cryptography
--------------------------------------------
另要深度学习框架包
```

- 添加日志文件夹

  在后端根目录下添加 logs文件夹存放日志

- MySql

  - 在mysql中创建数据库

  - 修改config/settings.py文件

  - 在开发环境数据库中修改代码

```
# 开发环境数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库名',
        'USER': '用户名',
        'PASSWORD': '密码',
        'HOST': '127.0.0.1', // 本地地址
        'PORT': '3306', // mysql端口
    }
}
```

- 尝试启动项目

```
// 终端运行
python manage.py runserver 127.0.0.1:8080  // 端口号要与前端调用接口端口一致

// 运行成功示例
Watching for file changes with StatReloader
Performing system checks...

Django version 3.2.16, using settings 'config.settings'
Starting development server at http://127.0.0.1:8080/
Quit the server with CTRL-BREAK.
```

- 终止服务

- 创建数据库表

```
python manage.py makemigrations  // 创建表结构
python manage.py migrate  // 创建数据库表
```

- 设置超级管理员

```
python manage.py createsuperuser 
```

- 收集Django自带界面静态资源

```
python manage.py collectstatic 
```

- 进入超级管理员界面 http://127.0.0.1:8080/admin/  
  - 超级管理员界面（Django自带），可以操作用户的权限，赋予标注人员和发布人员不同的操作数据库表的权力 
  - 需要添加手动组别 **requester**和**worker**，顺序不能反，代码中序号写死了
  - 组别权限规则
    - requester：可以操作自己创建的表的所有操作 add， change， view，delete
    - worker：对于任务和数据集任务，不能有add 和 delete 权限，其他随意

```
代码中，通过以下两个装饰器做权限管理
@permission_required('dataset.add_dataset')
@require_GET
```

- 联调前端，修改前端代码 utils/api.js

```
// let base = process.env.NODE_ENV === "production" ? "http://101.35.220.99/annotator-api" : "annotator-api-dev"; // 注释代码 
let base = "http://127.0.0.1:8080"; //端口与后端一致
```

# over！