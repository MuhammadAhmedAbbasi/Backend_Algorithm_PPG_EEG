# python service

[![zh](https://img.shields.io/badge/lang-zh-blue.svg)](./README.md)[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.en.md)

To start the background service, run the app.py file located in the service folder. If an error occurs, it maybe due to the absence of some necessary library files. You can refer to the requirements.txt file, which lists some essential libraries and their corresponding versions required for installation.

If you encounter the error "cannot import name 'JSONEncoder' from 'flask.json'" when executing "from flask_mongoengine import Document", then run "pip install flask==2.2.5" in the terminal. 



Before debugging, you need to create a new API for yourself. You can refer to the following code in the eeg_controller.py file. First, define a new path and set the method to POST, then define a function. Here you need to define the format of the data you receive, as well as the output you need. After referring to the writing style in the file, create your function. 

![api](./Img/api.png)

In the code above, eeg_service is called inside the yellow box. Within eeg_service, a function is defined to receive data and output the model's result. Please refer to the way it's written here to define your function. The model is defined in the eeg_depression_model.py file. Please refer to the way it's written here before creating your model file. 

When debugging, use the Postman software to create a new request. Choose 'post' as the request type. The API here is predefined. Enter the test data in the middle box. You need to select the corresponding data format; for instance, I have selected the JSON format. After running app.py, click the 'send' button, and the result will appear in the box below. 

![postman](./Img/postman.png)