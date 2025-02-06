Complete Steps for running the project on the local browser:-

1) Clone the "MediGenie" Repo in any folder in your system.
2) Download the weights of the pre-trained model from "https://drive.google.com/file/d/1WsT8_uhmoSEihpFgTQ9KFyidKIgl5LHl/view?usp=sharing" and paste them into the MediGenie Repo in your system. (File too big for Github)
3) Open the MediGenie folder in the vs code, open the manage.py file and then open a new terminal.
4) Then create a python virtual environment, using "python -m venv test" , test is the name of the virtual env.
5) Once created acticvate it by the command, "test\Scripts\activate".
6) After activation install the following dependencies in it one by one, for e.g. pip install django<br>
   6.1) django<br>
   6.2) torch<br>
   6.3) torchvision<br>
   6.4) requests<br>
7) After installing all the dependencies , run this command to open it in the browser "python manage.py runserver".
8) Once you get this ctrl+click on the 'http://127.0.0.1:8000/'
   
![image](https://github.com/user-attachments/assets/22e4a8fe-4dbf-4163-8ad8-1121459b05d1)

Choose images from the demo images given in the MediGenie repo itself.<br>
Accuracy - 86.7% (after fine tuning hyper parameters)
