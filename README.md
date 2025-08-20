# python 后端

[![zh](https://img.shields.io/badge/lang-zh-blue.svg)](./README.md)[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.en.md)

运行service文件夹下的app.py文件即可启动后台服务，如果发生报错可能是因为没有导入一些必要的库文件，可以查看requirements.txt文件，里面列出了一些必要的安装库以及对应的版本。

如果执行 ```from flask_mongoengine import Document``` 时报错 ```cannot import name 'JSONEncoder' from 'flask.json'```，则在终端执行```pip install flask==2.2.5 ```



进行调试之前你需要新建一个你的api，可以参考eeg_controller.py文件内的下面这段代码，首先定义一个新的路径，方法选择POST，然后定义一个函数，这里你需要定义你接受到的数据的格式，以及你需要的输出。参考文件的写法之后创建你的函数。

![api](./Img/api.png)

在上面这段代码中黄色的框中调用了eeg_service，eeg_service中定义了一个函数，用来接受数据，并输出模型的结果，请参考这里的写法定义你的函数。模型定义在eeg_depression_model.py文件中，请参考这里的写法之后新建你的模型文件。

调试时候使用的是postman软件，新建请求，请求类型选择post，这里的api是事先定义好的，中间这个方框内输入测试数据，你需要选择对应的数据格式，比如我这里选择是json格式，运行app.py之后，点击send按钮，结果就会出现在下方的方框内。

![postman](./Img/postman.png)



