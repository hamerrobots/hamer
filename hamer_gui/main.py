# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys, pyrebase, rospy, cv2, time, os, webbrowser, PyQt5, csv, subprocess, ntpath
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox,QFileDialog,QTextEdit,QVBoxLayout
from PyQt5.QtGui import QCursor
from sensor_msgs.msg import LaserScan
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QComboBox, QTextBrowser, QDoubleSpinBox, QSpinBox
from datetime import date, datetime
win = tk.
firebaseConfig = {'apiKey': "AIzaSyDviqsgHU1-p3q2LhehcUhGhtveR01eSrk",
                  'authDomain': "userinterface-74bf5.firebaseapp.com",
                  'databaseURL': "https://userinterface-74bf5.firebaseio.com",
                  'projectId': "userinterface-74bf5",
                  'storageBucket': "userinterface-74bf5.appspot.com",
                  'messagingSenderId': "717234517484",
                  'appId': "1:717234517484:web:3779cb277b9916c1dbfcc9",
                  'measurementId': "G-DNYHZQ6LG6",
                  'serviceAccount':"userinterface-74bf5-firebase-adminsdk-wipuk-8eb834d98d.json"}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
storage = firebase.storage()
number_of_experiments = 16





if not os.path.exists('documents'):
    os.makedirs('documents')
if not os.path.exists('assignments'):
    os.makedirs('assignments')

for i in  range(1,number_of_experiments+1):
    if not os.path.exists('assignments/experiment'+str(i)):
        os.makedirs('assignments/experiment'+str(i))


if not os.path.exists('solutions'):
    os.makedirs('solutions')


class first_screen(QMainWindow):
    def __init__(self):
        super(first_screen, self).__init__()
        loadUi("first_screen.ui", self)
        self.student_button.clicked.connect(self.student_login_scr)
        self.instructor_button.clicked.connect(self.instructor_login_scr)
        self.student_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.instructor_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    def student_login_scr(self):
        widget.setCurrentIndex(1)

    def instructor_login_scr(self):
        widget.setCurrentIndex(2)


class student_login(QDialog):
    def __init__(self):
        super(student_login, self).__init__()
        loadUi("student_login.ui", self)
        self.back_button.clicked.connect(self.goto_main_page)
        self.login_button.clicked.connect(self.std_login)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.create_account_button.clicked.connect(self.goto_create_acc)
        self.create_account_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.login_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.back_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        

    def goto_main_page(self):
        widget.setCurrentIndex(0)

    def goto_create_acc(self):
        widget.setCurrentIndex(3)

    def goto_std_main(self):
        widget.setCurrentIndex(5)

    def std_login(self):
        global email
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()
        try:
            login = auth.sign_in_with_email_and_password(email, password)
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], 'Logged in at', datetime.now()])
            storage.child('logfile.csv').put("logfile.csv")
            widget.setCurrentIndex(0)

            self.goto_std_main()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Log-in Failed!")
            msg.setText("Wrong email or password!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()


class student_create_account(QDialog):
    def __init__(self):
        super(student_create_account, self).__init__()
        loadUi("student_create_account.ui", self)
        self.back_button.clicked.connect(self.goto_main_page)
        self.login_button.clicked.connect(self.create_acc)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.back_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.login_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    def create_acc(self):
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()
        try:
            if self.lineEdit_2.text() == self.lineEdit_3.text():
                user = auth.create_user_with_email_and_password(email, password)
                self.goto_std_app()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Sign-up Failed!")
                msg.setText("Passwords do not match!")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Sign-up Failed!")
            msg.setText("The email adress is already in use!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def goto_main_page(self):
        widget.setCurrentIndex(1)

    def goto_std_app(self):
        widget.setCurrentIndex(4)


class student_create_acc_approved(QDialog):
    def __init__(self):
        super(student_create_acc_approved, self).__init__()
        loadUi("create_acc_approved.ui", self)
        self.login_button.clicked.connect(self.goto_main_page)
        self.login_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    def goto_main_page(self):
        widget.setCurrentIndex(0)


class instructor_login(QDialog):
    def __init__(self):
        super(instructor_login, self).__init__()
        loadUi("instructor_login.ui", self)
        self.back_button.clicked.connect(self.goto_main_page)
        self.login_button.clicked.connect(self.inst_login_func)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.back_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.login_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    def goto_main_page(self):
        widget.setCurrentIndex(0)

    def inst_login_func(self):
        ID = self.lineEdit.text()
        password = self.lineEdit_2.text()
        widget.setCurrentIndex(7)
        print("Succesfully logged in with", ID, " and password ", password)


class student_main(QMainWindow):
    def __init__(self):
        super(student_main, self).__init__()
        loadUi("student_main.ui", self)
        self.move_button.clicked.connect(self.move_forward)
        self.stop_button.clicked.connect(self.stop_robot)
        self.right_button.clicked.connect(self.turn_right)
        self.left_button.clicked.connect(self.turn_left)
        self.back_button.clicked.connect(self.go_back)
        self.increase_speed.clicked.connect(self.inc_speed)
        self.decrease_speed.clicked.connect(self.dec_speed)
        self.reset_speed.clicked.connect(self.res_speed)
        self.open_pdf_button.clicked.connect(self.download_pdf)
        self.open_IDE.clicked.connect(self.open_ide)
        self.hint_button.clicked.connect(self.show_hint)
        self.hamer_github.triggered.connect(self.goto_hamer)
        self.designer.triggered.connect(self.designer1)
        self.designer2.triggered.connect(self.goto_designer2)
        self.designer3.triggered.connect(self.goto_designer3)
        self.photo_button.clicked.connect(self.take_picture)
        rospy.Subscriber('/Realsense_Camera/RGB/image_raw', Image, self.camera_msg_callback)
        rospy.Subscriber('/hamer/odom', Odometry, self.show_odom)
        rospy.Subscriber('/scan', LaserScan, self.lidar_info)
        rospy.init_node('interface_node')
    
        
        self.fullscreen_button.clicked.connect(self.goto_camera)
        self.logout_button.clicked.connect(self.logout)
        self.upload_file.clicked.connect(self.warn_student)
        self.upload_file.clicked.connect(self.choose_file)
        
        self.bridge = CvBridge()
        self.terminal_on_tab()

        self.qTimer = QTimer()
        self.qTimer.setInterval(5)
        self.qTimer.timeout.connect(self.update)
        self.qTimer.start()
        self.timer = time.time()
        self.movie = QMovie('images/radar.gif')
        self.radar_label.setText("")
        self.radar_label.setMovie(self.movie)

        self.movie.start()


    def goto_hamer(self):
        webbrowser.open('https://github.com/Akerdogmus/hamer')
    def designer1(self):
        webbrowser.open('https://github.com/fatihvatansever')
    def goto_designer2(self):
        webbrowser.open('https://github.com/yagizumur')
    def goto_designer3(self):
        webbrowser.open('https://github.com/byariss')

    def open_ide(self):
        self.process2 = QProcess()
        self.process2.startDetached('idle')

    def show_hint(self):
        if self.experiment_comboBox.currentText() == 'Experiment 1':
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 1-Problem 1")
            msg.setText("To setup the ROS environment, the following line is written in the terminal.\n sudo apt install ros-melodic-desktop-full")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 1-Problem 2")
            msg.setText("After completing the setup of ROS, the setup of the environment is done with the following commands.\necho source /opt/ros/melodic/setup.bash\n~/.bashrc\nsource ~/.bashrc")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 1-Problem 3")
            msg.setText("Before using the ROS environment, rosdep must be initialized. rosdep enables users to easily setup system dependencies. To install rosdep, the following command is used. \nsudo apt install python-rosdep\nAfter the initialization, rosdep is ready to use. \nsudo rosdep init\nrosdep update")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 1-Problem 4")
            msg.setText("rqt_graph is a ROS package which is maintained by Michael Jeronimo and authored by Dirk Thomas that provides a visual plugin for computing graphs. It can be used with both rospy and roscpp.\nTo use the rqt_graph package, it must be first enabled with the following command.\n$ rosparam set enable_statistics true")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 1-Problem 5")
            msg.setText("rqt_plot is a ROS package which is used to visualize numerical values and plot a 2D graph using these numerical values. To use this package, it must be installed via the following code. \n$ sudo apt-get install ros-melodic-rqt \n$ sudo apt-get install ros-melodic-rqt-common-plugins")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 1-Problem 6")
            msg.setText("After the setup, the package must be used with a topic. To see the published topics which can be plotted numerically, the following command can be used. \n$ rostopic list \nNow a topic can be picked to be plotted. A simple example is given below. \n$ rqt_plot /turtle1/pose/x:y:z")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == 'Experiment 2':
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 2-Objectives")
            msg.setText("The main purpose of this experiment is to view the values on the sensors on the robot and to control the robot through the keyboard")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 2-Problem 1")
            msg.setText("Visualizing the Lidar Sensor\na) Change false as a true at <xacro:arg name=”laser_visual” default=”false”/> in document\nwhich is turtlebot3_waffle_pi.gazebo.xacro to visualize sensors.\nb) Open emptyworld from turtlebot3 maps and Check the functionality of the Lidar sensor.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 2-Problem 2")
            msg.setText("Visualizing the Sensor in Rviz\na) Run the turtlebot3_gazebo_rviz.launch file.\nb) Select the items you want to observe from the display screen on the left from the laserscan section.\nc) Add the odometry plugin from the display screen and observe the position vector of the robot.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 2-Problem 3")
            msg.setText("Keyboard Contol\na) Run turtlebot3_teleop_key.launch for keyboard control of the robot in a new terminal.\nb) Control the robot with the keyboard and observe the odometry value through rviz.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == "Experiment 3":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 3-Objectives")
            msg.setText("The main purpose of this experiment is to create a labyrinth environment in gazebo and add objects to the created environment.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 3-Problem 1")
            msg.setText("Open the empty world from the Turtlebot3 maps.\na) Click on the edit tab on the upper left of the Gazebo window and select the Building Editor.\nb) In the window that opens, the tab on the left shows the objects, colors and coatings we can\nuse. Add walls according to the labyrinth perimeter you want from the Create walls section.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 3-Problem 2")
            msg.setText("c) Add desired objects such as windows, doors and stairs from the Add Features section.\nd) You can see the drawing area on the right. The added objects are seen and edited in this\nsection. Clicking on an object can be moved to the right or left, new objects can be added and\nexisting objects can be removed. The scale of this area can be seen at the bottom left of the\ndrawing area. Adjust this scale to desired using the middle mouse button.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 3-Problem 3")
            msg.setText("To edit the created objects, right click on the object and select the edit object section and edit the dimensions of the walls from here.\nf) After the previously designed model is transferred to the Gazebo environment using the drawing area, exit from the drawing area from the file tab that appears at the top left of the screen, and the file is saved to turtlebot3_gazebo / models address.\ng) After this process is completed, the created model is ready for use. Try adding it to any project using the insert tab on Gazebo.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 4-Objectives")
            msg.setText("The main purpose of this experiment is to introduce the students to linear and angular movements in ROS environment.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == 'Experiment 4':
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 4-Problem 1")
            msg.setText("Create an empty Python script and name it as 1512xxxxxxxx_NameSurname.\na) Import the libraries rospy, Time and Twist.\nb) Initialize a new node. (Help: rospy.init_node(‘node_name’))")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 4-Problem 1")
            msg.setText("c) Publish the Twist message by creating a new publisher. (Help: rospy.Publisher(‘/cmd_vel’,Twist, queue_size=5).\nd) Define a new function to realize the movement.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 4-Problem 1")
            msg.setText("e) Using the Twist message and the formula ∆x = Vt[1], make the robot move a meter forward.( Help: You can use the function time.time() to define the time intervals.)\nf) To achieve a square movement, the robot is supposed to turn always to the same\ndirection.(Left or right).To achieve this, use the Twist message. Remember that to achieve a 90° turn, you must first convert the degree to radian.(rad = π × deg/180)[2]. \nRemember that rad = w × t")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 4-Problem 1")
            msg.setText("g) To make the robot move, the function Twist().linear.x(x is the direction) and Twist().angular.z functions must be used[3].\nh) Repeat the processes until the robot completes a full square.\ni) After completing the script, try it in the turtlebot3_empty_world.launch file.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == "Experiment 5":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 5-Objectives")
            msg.setText("The main purpose of this experiment is keeping the HAMER moving forward and backward steadily (patrolling).")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 5-Problem 1")
            msg.setText("a) Go to src folder and create a package.(Hint: cd ~/ , catkin_create_pkg 1512xxxxxxxx_NameSurname rospy geometry_msgs message_generation message_runtime).\nb) After creating package, make compilation for catkin).\nc) Add scripts folder to your package which will contain python code. (Hint: mkdir) ")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 5-Problem 1")
            msg.setText("d) Create a node for the mission[1].( Hint: nano code.py)The requirements for the code is following.\nd.1) YImport the necessary library: rospy ,[2] geometry_msgs.msg[Twist] , math[fabs].\nd.2)Define a function and name it as do_patrol.\nd.3)Start a node and publish the speed .(Hint1 : rospy.init_node(‘patrol’,anonymous=True Hint2:new_variable =rospy.Publisher….)\nd.4) Define a variable to hold Twist type variables.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 5-Problem 1")
            msg.setText("d.5)Define four variable for the robot’s speed,distance which robot move,number (how many times robot will go) and a counter to count patrol number.\nd.6)To calculate distance,hold the time  instantaneously with second and initialize it a variable(t0,t1) (Hint: t0 = rospy.Time.now().to_sec())\nd.7)When the operation is done,use shotdown command to close the loop and print it on terminal.(Hint: rospy.is_shutdown())\ne)Go to folder which contains the node and make it executable.(Hint: chmod)")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 5-Problem 2")
            msg.setText("Execute the empty_world.launch for the HAMER and execute the code.py on a new terminal.(The robot must patrol 5 times )")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()

        elif self.experiment_comboBox.currentText() == "Experiment 6":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 6-Objectives")
            msg.setText("The purpose of this experiments is to realize an object avoidance program for Turtlebot3 using Bug 0 Algorithm.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 6-Problem 1")
            msg.setText("Create an empty Python script and name it as 1512xxxxxxxx_NameSurname.\na) Import the necessary libraries rospy, time, Odometry, LaserScan, tf and Twist.\nb) alize the starting position and the goal of the robot. Along with these values, enter a yaw value and initialize it to 0.\nc)Define a new function scan_callback(scan_data). In this function, define the regions of the robot. (Help: fron_range=ranges[350:359]+ranges[0:20], right_range=ranges[80:90 and front_range=ranges[290:299]).")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 6-Problem 1")
            msg.setText("d) Define a new function pose_callback(pose_data), in this function define three global variables x_robot, y_robot and yaw. Also in this function, calculate the yaw value using the function tf.transformations.euler_from_quaternion.This function transforms a quaternion data system to Euler angles. The quaternion data system has four variables, (Help:data_name.pose.pose.orientation.x).")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 6-Problem 1")
            msg.setText("e) Define a new function rot_to_goal(). In the function, make the robot rotate towards the goal that is indicated. Use the atan2 function to get the angle value. Then, until the angle is equal to yaw value, rotate the robot.\nf)Define a new function wang (right). In the function, calculate the angle that the robot has with the closest obstacle. Compare every direction with the yaw value. Return , - or 0 according to the direction. The right variable indicates if there is an obstacle on the right side of the robot.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 6-Problem 1")
            msg.setText("g)Define a new function follow() to make the robot to move around the obstacle if any encountered. Use the wall_angle() function to obtain the angle that the robot has with the obstacle. Use the difference between this angle and the yaw value to set a boundary on the angle to rotate. Also, check if there is an obstacle in front of the robot. If there is not, move the robot forward in parallel with the wall(or obstacle).")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 6-Problem 1")
            msg.setText("h)In the main function,  initialize the node, subscribe to both LaserScan and Odometry. Also publish the cmd_vel message.\ni)Also in the main function, make the robot rotate and move towards the goal if there in no obstacle in front of it. Also if there in an obstacle in front, make the robot move around it. When the robot reaches the targeted location, stop the robot.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()

        elif self.experiment_comboBox.currentText() == "Experiment 7":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 7-Objectives")
            msg.setText("In this experiment, student will write a node for the TurtleBot3 Waffle Pi. The node must be designed as, the robot should follow the walls and the distance between wall and robot’s corners must be printed on terminal unless there is no interrupt on the program.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 7-Problem 1")
            msg.setText("a) Import the libraries which are used to get robot’s sensors information, move the robot, get time parameters, make transformation between time, make mathematical operations.\nb)Define a rotate function which contains the relative angle degree and angular velocity to turn the robot with wanted turning angle and angular velocity.In the function, define a global varibable move to use in the  function the movement will perform with Twist() function.Hold the time between function was called and was not called in seconds.Publish the move message to complete rotation. (Hint:rospy.Time.now().to_sec() )")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 7-Problem 1")
            msg.setText("c) Define a run function and create a loop for wall follower algorithm.You can help from Figure 2 Flowchart of Algortihm for algorithm.Print the distance between corners of the robot and walls.Run function contains the message.Message represents the corners of robot in angular form.(Hint:message.ranges[360]).\n d) Define an initial node for your script.(Hint:rospy.init_node())")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 7-Problem 1")
            msg.setText("e)Subscribe the sensors of robot where used in run function(Hint:rospy_Subscriber())\nf)Publish the Twist() function.(Hint:rospy.Publisher()).\ng)After completing the script, make the script executable.(Hint:chmod)\nh)Try your script on your maze which is made on Experiment3.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == "Experiment 8":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 8-Objectives")
            msg.setText("The main purpose of this experiment is creating a Python script to control the TurtleBot3 WafflePi with voice control.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 8-Problem 1")
            msg.setText("a) Install the following packages:SpeechRecognition (Hint: sudo pip3 install), PyAudio, PocketSphinx\nb)Write a Python script to control the robot with voice.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 8-Problem 1")
            msg.setText("b.1) Import libraries.(Hint:speech_recognition as sr,string,rospy.Twist etc..).\nb.2)Define a class and name as VoiceControl.\nb.3)Define a “__init__” function to hold initial variables and create initial node.Publish the words which will be used for controlling the robot.(Hint: rospy.init_node , rospy.Publishler()). ")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 8-Problem 1")
            msg.setText("b.4)Define a “get_params” function to get parameters and node names.(Hint:rospy.get_name() ).\nb.5)Define a “checkConfig” function to check the configuration of your voice is known or not from packages which is installed at part a).\nb.6)Define a  “recordAudio” function to control and print the voice is recorded or not.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 8-Problem 1")
            msg.setText("b.8)Define a “speechRecognition”function to write the word which is heard from receiver.In order to do that,define a variable and initialize it to zero.After assign it to heard word.\nb.9)Define a “getVoiceCommand”function to print heard word.\nb.10)Define three function to activate and deactivate for text,node and words.\nb.11)Define a “run” function to compare the heard voice is equal or not to command.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 8-Problem 2")
            msg.setText("Test the python script on simulation.\na)Run the empty_world launch file which is a map of turtlebot3..\nb)Run your python script from another terminal.\nc)Prompt the word command to the terminal what you said and test the program’s understandability.(Hint: rostopic echo)")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == "Experiment 9":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 9-Objectives")
            msg.setText("The main purpose of this experiment is ensuring autonomous movement of the robot by extracting the environment map with the gmapping package using the slam algorithm.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 9")
            msg.setText("1.a)Install the gmapping package on your system\n. $ sudo apt install ros-melodic-slam-gmapping\n. $sudo apt-get install ros-melodic-navigation")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 9")
            msg.setText("1.b)After these packages are installed, create a folder to be used in the package.\n1.c)After the package creation is completed, the compilation process is performed by going to the catkin workspace.\n1.d)After the gmapping package is installed, the mapping process can be started. Call the world where the mapping will be done.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 9")
            msg.setText("1.e)Call the gmapping package from the terminal.\n1.f)After the package is called, call the teleop file created for TurtleBot3 and control the TurtleBot3 with the keyboard.\n1.g)Save the navigated map\n$rosrun map_server map_saver -f /home/ubuntu/catkin_ws/src/nameofyourfile/map/my_world_map\n$rosrun map_server map_saver map:=nameofyourfile")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 9")
            msg.setText("1.h)Make the necessary changes in turtlebot3_navigation.launch file.\n1.i)After these operations are completed, open your map from gazebo and rviz.\nj)Target the robot with the 2D Nav Goal at the top of the rviz screen.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 9")
            msg.setText("2.a)Create a document with py extension and add the required libraries first\n2.b)Create the function we will do the necessary operations. First define the client into the functionand write the function that waits for the target point to arrive.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 9")
            msg.setText("2.c)Use MoveBaseGoal () message to set target point and make the robot turn on the map.\n2.d)Then let the service wait for the target to be sent to the action server and the action to be created.\n2.e)Issue an error message if the code block cannot wait, if it waits return the result of this service.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 9")
            msg.setText("2.f)Create a node and write a block indicating that if the result of the function just created is correct, the target point has been reached, if not, that it was not reached.\n2.g)As a final action, open a new terminal and run the node just created with the rosrun command.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()


        elif self.experiment_comboBox.currentText() == "Experiment 10":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 10")
            msg.setText("1)Install frontier_exploration package on your catkin folder.(Hint:sudo apt get)\n2)Open the map in Gazebo.(Hint:map.launch)\n3)Find slam file to operate the slam method as frontier exploration.The launch file should contain robot navigation and Rviz nodes.(Hint:turtlebot3_slam.launch slam_methods:=)")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 10")
            msg.setText("4)After the robot and it’s sensors seen on Rviz operate the exploration launch file.The exploration file allows to make plugins on Rviz surface\n5)In Rviz,find display panel and add marker on the list.In marker,select the marker topic and change it as /exploration_polygon_marker .In the same way add a map and change the topic as /exploration_server_node/explore_costmap/costmap.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 9")
            msg.setText("6)Select the area which is wanted surface to mapping by using Publish Point where at the top of the RvizAfter choosing a square shape which user wanted to explore,choose one more publish point in that square to start exploring.When the exploration is done, No valid points found, exploration complete can be seen on terminal.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == "Experiment 11":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 11-Objectives")
            msg.setText("The main purpose of this experiment is mapping with the map merge package.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 11")
            msg.setText("1.a)Run roscore.\n1.b)Open new terminal and run multi_turtlebot3.launch\n1.c)Open new terminal for each robot and run turtlebot3_gmapping.launch for each robot respectively.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 11")
            msg.setText("1.d)Open new terminal and launch merge file.\n1.e)Execute rviz terminal in new window.\n1.f)Control each robot with keyboard and explore their own areas with each robot.\n1.g)Save your map.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == "Experiment 12":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 12-Objectives")
            msg.setText("The main purpose of this experiment is to planning the shortest route for a robot to reach multiple points using Genetic Algorithm.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1)Create an empty Python script and name it as 1512xxxxxxxx_NameSurname.\n1.a)Import the necessary libraries rospy, actionlib, MoveBaseAction, MoveBaseGoal, copy and math.\n1.b)Define a new class State. In this class, use __init__ method to create a new child. And use __eq__ method to make sure each child is different than other. In this function, return True if self.route is equal to other.route.(Hint: def__init__(self,route[],distance=int==0),def__eq__(self,other)).")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1.c)Include def __lt__(self,other) function to compare the distances.\n1.d)Define a new class City to define the points that are needed to be visited. The class needs an index and distance variables. In the class, check if the point’s distance to the start point is less than the distances that other cities have to the starting point.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1.e)Define a new function create_population to create a new route. The route must include every point that is to be visited. (Hint: def create_population(matrix= [], home= int, city_indexes= [], size= int))")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1.f)Define a new function crossover to realize the first part of the Genetic Algorithm. In this function, a new child must be created using two separate parents. First, create two new temporary variables and copy the values that the parents have into these variables. Then create two empty arrays. Into these arrays, assign the parts that are randomly created from parents. At the end of the function, return the new state. (Hint: def crossover(matrix=[], home=int, parents=[]) where home is the starting position of the robot.)")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1.g)After completing the crossover section, define a new function to realize the mutation step. (Hint: def mutate(matrix= [ ], home= int, state= State, mutation_rate= float == 0.01)). In the function, generate a random number that is smaller than the mutation_rate variable. After that, create two different routes and converge them to create the mutated_state. Return this state at the end of the function.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1.h)Define a new function genetic_algorithm, to realize the last step of the algorithm. (Hint: def genetic_algorithm(matrix= [], home= int, population= [], keep= int, mutation_rate= float, generations= int) ). In the function, sort the populations that are created in the before functions. Then create an array children, and find the most optimized population. Return the shortest route.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1.i)Create a new function distance(a=[], b=[]) to calculate the distance between two points.(Hint: L = √(X B − X A ) 2 + (Y B − Y A ) 2 [4])")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1.j)Define a new function movebase_client() to realize the movement of the robot. In the function, define the points that are to be visited.(i.e. point1[0,0]) and choose one of these points as the starting point. The robot has to go back to the starting point after it finishes visiting all other points. Then, use distance(a=[], b=[]) function to calculate the distance between each point. Assign these distances into an n x n matrix. Use create_population function to create a new set of populations using the matrix created before.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1.k)Also in the function, create a new client using the actionlib library.(Hint:actionlib.SimpleActionClient('move_base',MoveBaseAction)[5]). Print the optimized route to inform the user.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1.l)Send the robot to the points one by one. Remember that the robot has to go back to the starting position after visiting all other points.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 12")
            msg.setText("1.m)After completing all steps, use if __name__ == ’__main__’ method to create the node for the script. End the application if all points are visited and the robot has returned to the starting position.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == "Experiment 13":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 13-Objectives")
            msg.setText("The main objective of this experiment is to understand the basics of the ROS package RTAB-Map.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 13")
            msg.setText("1)Use roslaunch to launch a previously created ROS world. Since Burger and Waffle Pi models of turtlebot3 do not provide any sensor to realize the visual mapping, do not forget to launch a TurtleBot3 Waffle model. (Hint: Write export TURTLEBOT3_MODEL=waffle in the terminal before launching the world.)")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 13")
            msg.setText("2)After launching the ROS world to be mapped, launch the demo_turtlebot3_navigation.launch file that is inside the rtabmap_ros package. Remember to export the TurtleBot3 model as waffle on this terminal as well.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 13")
            msg.setText("3)After launching both the map and the demo launch file, both rtabmapviz and rviz should open. In the rtabmapviz screen, you must see 3 screens. From right to left, these screens demonstrate the cost map(provided from RViz ), the 3D map of the environment and the camera output which is provided from /camera/rgb/image_raw node.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 13")
            msg.setText("4)Use the robot to travel through all map. This can be achieved by using the teleop launch file(roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch) or through RViz. You can use 2D navigation button on the upper tab of RViz screen.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 13")
            msg.setText("5)After travelling through all map, the 3D map must be ready to be saved. Notice that in figure 4, the path that is drawn by the robot is colored with blue. This means that the robot has completed a loop and the loop detector has detected this movement.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 13")
            msg.setText("6)After completing the map, CTRL-C keys can be used. For a further detailed saving procedure, RTAB-Map database must be opened. The command below is used to open the database.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg.setWindowTitle("Experiment 13")
            msg.setText("7)After opening the database, choose file, and export 3D clouds options. Choose where you want to save the map as a .ply file. After completing the saving process, you can open the saved map through RTAB-Map.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == "Experiment 14":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 14-Objectives")
            msg.setText("The find_object_2d package uses SURF,SIFT,ORB,FAST and BRİEF function detector to detect objects.The package can be used in many surfaces.User can use the package in usb cameras,robot’s camera in simulation and a camera which is impelemented on robot in reality.Using the graphical interface provided by this package,user can mark the objects which he want to detect.After marking operation,the detector node detects objects in camera images and publish to the subject.Additionally,using 3D sensor,detector node can estimate height,width and depth of object.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 14")
            msg.setText("1)Install find_object_2d package on your catkin folder.(Hint: sudo apt get or git clone)\n2)Install usb cam on your catkin folder.(Hint: sudo apt-get install))\n3)Open your usb cam driver and test it if it is not working(Hint: roslaunch usb_cam usb_cam-test.launch)")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 14")
            msg.setText("4)Launch the find_object_2d package and use the usb camera to detection.(Hint: rosrun find_object_2d find_object_2d ... )\n5)Define an object to the camera and see the recognition is successfully made or not.\n6)Spawn the TurtleBot3 and an object on Gazebo.Open Rviz model to see the robot’s sensor,camera and the other parameters. (Hint: roslaunch turtlebot3_gazebo turtlebot3_world.launch,rosrun rviz rviz )")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 14")
            msg.setText("7)Launch find_object_2d package with publishing robot’s camera.(Hint:/camera/rgb/image/raw)\n8)Make the recognition of object to the robot camera and see the recognition is successfully made or not.(Hint: When the robot sees the object it will recognize it)\n9)Print the detected object as dimensional array on terminal which contains object’s width,height and homography matrix. (Hint: roslaunch find_object_2d print_objects_detected)")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == "Experiment 15":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 15-Objectives")
            msg.setText("The main objective of this experiment is to use YOLOv3 with TurtleBot3 for object recognition. YOLOv3(You Only Look Once) is a real time object recognition algorithm. The latest published model of YOLOv3 is capable of recognizing 80 different objects. These objects can be in pictures or in videos. In this experiment, the darknet_ros package is to be used for this purpose.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 15")
            msg.setText("1.a)Clone the darknet package which is created by YOLOv3 developers on catkin workspace folder.\n1.b)In the darknet folder, enable the GPU,CUDNN,OPENCV.\n-GPU will build with CUDA to make the process faster by using GPU\n-CUDNN is used for accelerating the process by using CPU.\n-OPENCV is used to enable connection between cameras and object detection.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 15")
            msg.setText("1.c)Download the YOLOv3 weights which are previously defined and detected object to make detection on your own environment.(Hint: The weights must be downloaded to cfg folder).\n1.d)Run the YOLOv3 object detection")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 15")
            msg.setText("2.a)Clone the darknet_ros packages which is compatible with ROS environment in catkin workspace.\n$ git clone --recursive git@github.com:leggedrobotics/darknet_ros.git")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 15")
            msg.setText("2.b)Build the package in Relase mode. Build mode maximizes the performances of execution When building package is done, if nvcc fatal : Unsupported gpu architecture 'compute_30' or “make -j8 -l8” error is occurred , check the compute capability of your GPU and delete the unsupported -gencode lines from CMakeLists.txt in darknet_ros folder.\n$ catkin_make -DCMAKE_BUILD_TYPE=Release")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 15")
            msg.setText("2.c)Operate a launch file which includes a map and robot. The map must have some object to try detection operation.\n $ roslaunch new_world new_world.launch\n2.d)Operate the YOLOv3 launch file.\n $ roslaunch darknet_ros yolo_v3.launch")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
        elif self.experiment_comboBox.currentText() == "Experiment 16":
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 16-Objectives")
            msg.setText("The purpose of this experiments is to get the robot to the finish line by following the lanes on the map which we will launch.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 16")
            msg.setText("1.a)Import the necessary libraries rospy, cv2, cv_bridge, numpy ,Twist and Image.\n1.b)Create a class named Lane.\n1.c)Create a Constructor and firstly create an object named bridge from the Cv_bridge class.Then Subscribe to the camera / image topic to view the image and publish on cmd_vel. Lastly create an object named twist from the twist class.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 16")
            msg.setText("1.d)Define a new function named as func .Take self and ros_image as parameters. In this function to convert ros_image from ros format to open_cv format, use the self.bridge.imgmsg_to_cv2 method. Then use cv2_cvtColor method to also convert to hsv color space.\n1.e)To make masking, determine the limit values with rgb values. Then show the mask .")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 16")
            msg.setText("1.f)Generate the length, width and depth values to get the image values. Assign these values according to the area we want the image to be taken and show it in the name of clipped_mask.\n1.g)Go to the moment function and insert the mask value into it. Then use the moment function to find the midpoint of the line.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 16")
            msg.setText("1.h)With the Circle method, place a circle on the line that you will base your movement on. To determine where the point will be for the robot, assign the appropriate value to the variable err. For this experiment we want to keep the line to the left of the robot.(Hint: Use the x value of the center point and width.)")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 16")
            msg.setText("1.i)Enter linear and angular velocity values.\n(Hint:Use -float(err) / 100 for angular velocity)\n1.j)Publish the twist object that we created the speed values and show the red dot we created and create a wait value.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()
            msg = QMessageBox()
            msg.setWindowTitle("Experiment 16")
            msg.setText("1.k)Finally, define the node inside main and create an object from the Lane class and call the spin method.\n1.l)Launch the robot at turtlebot3_autorace_2020 map and run your python code.")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()


            






    def terminal_on_tab(self):
        self.tab1.setStyleSheet(
            "color:#ffffff; background-color:#353535; border: 2px solid #353535; border-radius: 3px;font-size: 12px;")
        self.process4 = QProcess()
        self.process4.start('rxvt', ['-fg', 'white', '-bg', 'black', '-embed', str(int(self.tab1.winId()))])
        self.tab1.setStyleSheet(
            "color:#ffffff; background-color:#353535; border: 2px solid #353535; border-radius: 3px;font-size: 12px;")
        self.process5 = QProcess()
        self.process5.start('rxvt', ['-fg', 'white', '-bg', 'black', '-embed', str(int(self.tab2.winId()))])
        self.tab1.setStyleSheet(
            "color:#ffffff; background-color:#353535; border: 2px solid #353535; border-radius: 3px;font-size: 12px;")
        self.process6 = QProcess()
        self.process6.start('rxvt', ['-fg', 'white', '-bg', 'black', '-embed', str(int(self.tab3.winId()))])
        self.tab1.setStyleSheet(
            "color:#ffffff; background-color:#353535; border: 2px solid #353535; border-radius: 3px;font-size: 12px;")
        self.process7 = QProcess()
        self.process7.start('rxvt', ['-fg', 'white', '-bg', 'black', '-embed', str(int(self.tab4.winId()))])
        self.tab1.setStyleSheet(
            "color:#ffffff; background-color:#353535; border: 2px solid #353535; border-radius: 3px;font-size: 12px;")
        self.process8 = QProcess()
        self.process8.start('rxvt', ['-fg', 'white', '-bg', 'black', '-embed', str(int(self.tab5.winId()))])


        
    def choose_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_name, _ = QFileDialog.getOpenFileName(self,'Import Script')
        path_on_cloud="/assignments"
        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()
            if file_name[0].endswith('.py'):
                head, tail = ntpath.split(file_name[0])

                if self.experiment_comboBox.currentText() == 'Experiment 1':
                    tail_str = os.path.join(path_on_cloud, "experiment1", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 2':
                    tail_str = os.path.join(path_on_cloud, "experiment2", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 3':
                    tail_str = os.path.join(path_on_cloud, "experiment3", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 4':
                    tail_str = os.path.join(path_on_cloud, "experiment4", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 5':
                    tail_str = os.path.join(path_on_cloud, "experiment5", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 6':
                    tail_str = os.path.join(path_on_cloud, "experiment6", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 7':
                    tail_str = os.path.join(path_on_cloud, "experiment7", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 8':
                    tail_str = os.path.join(path_on_cloud, "experiment8", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 9':
                    tail_str = os.path.join(path_on_cloud, "experiment9", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 10':
                    tail_str = os.path.join(path_on_cloud, "experiment10", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 11':
                    tail_str = os.path.join(path_on_cloud, "experiment11", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 12':
                    tail_str = os.path.join(path_on_cloud, "experiment12", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 13':
                    tail_str = os.path.join(path_on_cloud, "experiment13", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 14':
                    tail_str = os.path.join(path_on_cloud, "experiment14", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 15':
                    tail_str = os.path.join(path_on_cloud, "experiment15", tail)

                elif self.experiment_comboBox.currentText() == 'Experiment 16':
                    tail_str = os.path.join(path_on_cloud, "experiment16", tail)

                storage.child(tail_str).put(file_name[0])
                msg = QMessageBox()
                msg.setWindowTitle("Upload Succesful!")
                msg.setText("Your assignment has been sent succesfully!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Upload Failed!")
                msg.setText("Please select an appropriate Python script!")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                
    def warn_student(self):
        msg = QMessageBox()
        msg.setWindowTitle("Please be careful!")
        msg.setText("Please use the format 1512xxxxxxxx_experimentx.py")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()
                
    def inc_speed(self):
        twist.linear.x = twist.linear.x + 0.05
        pub.publish(twist)
        self.linear_speed.display(twist.linear.x)
        self.angular_speed.display(twist.angular.z)
    def dec_speed(self):
        twist.linear.x = twist.linear.x - 0.05
        pub.publish(twist)
        self.linear_speed.display(twist.linear.x)
        self.angular_speed.display(twist.angular.z)
    def res_speed(self):
        twist.linear.x = 0.2
        pub.publish(twist)
        self.linear_speed.display(twist.linear.x)
        self.angular_speed.display(twist.angular.z)


    def camera_msg_callback(self, msg):
        self.camera_msg = msg

    def take_picture(self):
        if not os.path.exists('documents/pictures'):
            os.makedirs('documents/pictures')
        image_name="documents/pictures/"
        image_name=image_name+str(email[0:12])+'_'+str(self.experiment_comboBox.currentText())+'.jpg'
        cv_image = self.bridge.imgmsg_to_cv2(self.camera_msg, 'bgr8')
        #cv2.imshow(image_name,self.camera_map)
        cv2.imwrite(image_name,cv_image)


    def draw_frames(self):
            cv_image = self.bridge.imgmsg_to_cv2(self.camera_msg, 'bgr8')
            h, w, _ = cv_image.shape
            self.camera_label.resize(h, w)
            self.camera_map = cv_image
            self.camera_map = cv2.cvtColor(self.camera_map, cv2.COLOR_BGR2RGB)
            height, width, channels = np.shape(self.camera_map)
            totalBytes = self.camera_map.nbytes
            bytesPerLine = int(totalBytes / height)
            qimg = PyQt5.QtGui.QImage(self.camera_map.data, self.camera_map.shape[1], self.camera_map.shape[0],
                                        bytesPerLine, PyQt5.QtGui.QImage.Format_RGB888)
            pixmap = PyQt5.QtGui.QPixmap.fromImage(qimg).scaled(450,260)

            self.camera_label.setPixmap(pixmap)
            self.camera_label.show()

    def goto_camera(self):
        widget.setCurrentIndex(6)

    def update(self):
        self.draw_frames()

    def logout(self):
        with open('logfile.csv', 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([email[0:12], 'Logged out at', datetime.now()])
        storage.child('logfile.csv').put("logfile.csv")
        widget.setCurrentIndex(0)

    def download_pdf(self):
        if self.experiment_comboBox.currentText() == 'Experiment 1':
            path_on_cloud = "experiment1.pdf"
            storage.child(path_on_cloud).download("documents/experiment1.pdf")
            webbrowser.open_new(r'documents/experiment1.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12],'opened experiment 1 on', datetime.now()])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 2':
            path_on_cloud = "experiment2.pdf"
            storage.child(path_on_cloud).download("documents/experiment2.pdf")
            webbrowser.open_new(r'documents/experiment2.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 2'])
            storage.child('logfile.csv').put("logfile.csv")
        if self.experiment_comboBox.currentText() == 'Experiment 3':
            path_on_cloud = "experiment3.pdf"
            storage.child(path_on_cloud).download("documents/experiment3.pdf")
            webbrowser.open_new(r'documents/experiment3.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 3'])
            storage.child('logfile.csv').put("logfile.csv")
        if self.experiment_comboBox.currentText() == 'Experiment 4':
            path_on_cloud = "experiment4.pdf"
            storage.child(path_on_cloud).download("documents/experiment4.pdf")
            webbrowser.open_new(r'documents/experiment4.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 4'])
            storage.child('logfile.csv').put("logfile.csv")
        if self.experiment_comboBox.currentText() == 'Experiment 5':
            path_on_cloud = "experiment5.pdf"
            storage.child(path_on_cloud).download("documents/experiment5.pdf")
            webbrowser.open_new(r'documents/experiment5.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 5'])
            storage.child('logfile.csv').put("logfile.csv")
        if self.experiment_comboBox.currentText() == 'Experiment 6':
            path_on_cloud = "experiment6.pdf"
            storage.child(path_on_cloud).download("documents/experiment6.pdf")
            webbrowser.open_new(r'documents/experiment6.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 6'])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 7':
            path_on_cloud = "experiment7.pdf"
            storage.child(path_on_cloud).download("documents/experiment7.pdf")
            webbrowser.open_new(r'documents/experiment7.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:11], datetime.now(), 'Experiment 7'])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 8':
            path_on_cloud = "experiment8.pdf"
            storage.child(path_on_cloud).download("documents/experiment8.pdf")
            webbrowser.open_new(r'documents/experiment8.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 8'])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 9':
            path_on_cloud = "experiment9.pdf"
            storage.child(path_on_cloud).download("documents/experiment9.pdf")
            webbrowser.open_new(r'documents/experiment9.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 9'])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 10':
            path_on_cloud = "experiment10.pdf"
            storage.child(path_on_cloud).download("documents/experiment10.pdf")
            webbrowser.open_new(r'documents/experiment10.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 10'])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 11':
            path_on_cloud = "experiment11.pdf"
            storage.child(path_on_cloud).download("documents/experiment11.pdf")
            webbrowser.open_new(r'documents/experiment11.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 11'])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 12':
            path_on_cloud = "experiment12.pdf"
            storage.child(path_on_cloud).download("documents/experiment12.pdf")
            webbrowser.open_new(r'documents/experiment12.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 12'])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 13':
            path_on_cloud = "experiment13.pdf"
            storage.child(path_on_cloud).download("documents/experiment13.pdf")
            webbrowser.open_new(r'documents/experiment13.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 13'])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 14':
            path_on_cloud = "experiment14.pdf"
            storage.child(path_on_cloud).download("documents/experiment14.pdf")
            webbrowser.open_new(r'documents/experiment14.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 14'])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 15':
            path_on_cloud = "experiment15.pdf"
            storage.child(path_on_cloud).download("documents/experiment15.pdf")
            webbrowser.open_new(r'documents/experiment15.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 15'])
            storage.child('logfile.csv').put("logfile.csv")

        if self.experiment_comboBox.currentText() == 'Experiment 16':
            path_on_cloud = "experiment16.pdf"
            storage.child(path_on_cloud).download("documents/experiment16.pdf")
            webbrowser.open_new(r'documents/experiment16.pdf')
            with open('logfile.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email[0:12], datetime.now(), 'Experiment 16'])
            storage.child('logfile.csv').put("logfile.csv")


    def move_forward(self):

        twist.linear.x = 0.2
        twist.angular.z = 0.0
        self.linear_speed.display(twist.linear.x)
        self.angular_speed.display(twist.angular.z)
        pub.publish(twist)

    def turn_right(self):

        twist.angular.z = -0.2
        twist.linear.x = 0.0
        self.linear_speed.display(twist.linear.x)
        self.angular_speed.display(twist.angular.z)
        pub.publish(twist)

    def turn_left(self):

        twist.angular.z = 0.2
        twist.linear.x = 0.0
        self.linear_speed.display(twist.linear.x)
        self.angular_speed.display(twist.angular.z)
        pub.publish(twist)

    def go_back(self):

        twist.linear.x = -0.2
        twist.angular.z = 0.0
        self.linear_speed.display(twist.linear.x)
        self.angular_speed.display(twist.angular.z)
        pub.publish(twist)

    def stop_robot(self):

        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.linear_speed.display(twist.linear.x)
        self.angular_speed.display(twist.angular.z)
        pub.publish(twist)

    def show_odom(self, msg):

        self.position_x.display(msg.pose.pose.position.x)
        self.position_y.display(msg.pose.pose.position.y)

    def lidar_info(self, msg):
        self.lidar_front.display(msg.ranges[0])
        self.lidar_back.display(msg.ranges[180])
        self.lidar_left.display(msg.ranges[90])
        self.lidar_right.display(msg.ranges[270])


class student_camera(QMainWindow):
    def __init__(self):
        super(student_camera, self).__init__()
        loadUi("camera_screen.ui", self)
        self.bridge = CvBridge()
        self.back_button.clicked.connect(self.goto_std_main)
        rospy.Subscriber('/Realsense_Camera/RGB/image_raw', Image, self.camera_msg_callback)
        self.qTimer = QTimer()
        self.qTimer.setInterval(5)
        self.qTimer.timeout.connect(self.update)
        self.qTimer.start()
        self.timer = time.time()




    def goto_std_main(self):
        widget.setCurrentIndex(5)

    def camera_msg_callback(self, msg):
        self.camera_msg = msg

    def update(self):
        self.draw_frames()

    def draw_frames(self):
            cv_image = self.bridge.imgmsg_to_cv2(self.camera_msg, 'bgr8')
            h, w, _ = cv_image.shape
            self.camera_label.resize(h, w)
            self.camera_map = cv_image
            self.camera_map = cv2.cvtColor(self.camera_map, cv2.COLOR_BGR2RGB)
            height, width, channels = np.shape(self.camera_map)
            totalBytes = self.camera_map.nbytes
            bytesPerLine = int(totalBytes / height)
            qimg = PyQt5.QtGui.QImage(self.camera_map.data, self.camera_map.shape[1], self.camera_map.shape[0],
                                      bytesPerLine, PyQt5.QtGui.QImage.Format_RGB888)
            pixmap = PyQt5.QtGui.QPixmap.fromImage(qimg).scaled(1000,500)

            self.camera_label.setPixmap(pixmap)
            self.camera_label.show()


class instructor_main_window(QMainWindow):
    def __init__(self):
        super(instructor_main_window, self).__init__()
        loadUi("instructor_main.ui", self)
        self.download_button.clicked.connect(self.download_file)
        self.clear_button.clicked.connect(self.clear_csv)
        self.logout_button.clicked.connect(self.logout)
        self.open_pdf_button.clicked.connect(self.download_pdf)
        self.open_solution.clicked.connect(self.download_solution)
        self.download_script.clicked.connect(self.show_item)
        self.check_progress.clicked.connect(self.check_student_progress)
        self.update_csv.clicked.connect(self.show_logfile)
        self.designer.triggered.connect(self.designer1)
        self.designer2.triggered.connect(self.goto_designer2)
        self.designer3.triggered.connect(self.goto_designer3)
        self.hamer.triggered.connect(self.goto_hamer)
        self.terminal_on_tab()
        self.show_logfile()

    def download_file(self):
        path_on_cloud = "logfile.csv"
        storage.child(path_on_cloud).download("logfile.csv")
        webbrowser.open_new(r'logfile.csv')
    def clear_csv(self):
        with open('logfile.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([''])
        storage.child('logfile.csv').put("logfile.csv")

    def logout(self):
        widget.setCurrentIndex(0)
    def goto_hamer(self):
        webbrowser.open('https://github.com/Akerdogmus/hamer')
    def designer1(self):
        webbrowser.open('https://github.com/fatihvatansever')
    def goto_designer2(self):
        webbrowser.open('https://github.com/yagizumur')
    def goto_designer3(self):
        webbrowser.open('https://github.com/byariss')

    def show_logfile(self):
        path_on_cloud = "logfile.csv"
        storage.child(path_on_cloud).download("documents/logfile.csv")
        str_log = ""
        with open('logfile.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                str_log = str_log + str(row) + "\n"
            str_log=str_log.replace('"',' ')
            str_log=str_log.replace('[',' ')
            str_log=str_log.replace(']',' ')
            str_log=str_log.replace(',',' ')
            str_log=str_log.replace("'"," ")
            self.logfile_label.setText(str_log)
            self.logfile_label.show()





    def terminal_on_tab(self):
        self.tab1.setStyleSheet(
            "color:#ffffff; background-color:#353535; border: 2px solid #353535; border-radius: 3px;font-size: 12px;")
        self.process4 = QProcess()
        self.process4.start('rxvt', ['-fg', 'white', '-bg', 'black', '-embed', str(int(self.tab1.winId()))])
        self.tab1.setStyleSheet(
            "color:#ffffff; background-color:#353535; border: 2px solid #353535; border-radius: 3px;font-size: 12px;")
        self.process5 = QProcess()
        self.process5.start('rxvt', ['-fg', 'white', '-bg', 'black', '-embed', str(int(self.tab2.winId()))])
        self.tab1.setStyleSheet(
            "color:#ffffff; background-color:#353535; border: 2px solid #353535; border-radius: 3px;font-size: 12px;")
        self.process6 = QProcess()
        self.process6.start('rxvt', ['-fg', 'white', '-bg', 'black', '-embed', str(int(self.tab3.winId()))])
        self.tab1.setStyleSheet(
            "color:#ffffff; background-color:#353535; border: 2px solid #353535; border-radius: 3px;font-size: 12px;")
        self.process7 = QProcess()
        self.process7.start('rxvt', ['-fg', 'white', '-bg', 'black', '-embed', str(int(self.tab4.winId()))])
        self.tab1.setStyleSheet(
            "color:#ffffff; background-color:#353535; border: 2px solid #353535; border-radius: 3px;font-size: 12px;")
        self.process8 = QProcess()
        self.process8.start('rxvt', ['-fg', 'white', '-bg', 'black', '-embed', str(int(self.tab5.winId()))])


    def check_student_progress(self):
        msg = QMessageBox()
        msg.setWindowTitle("Check Progress")
        msg.setText("Please select the file that you want to check the progress of, from the assignments folder.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_name, _ = QFileDialog.getOpenFileName(self, 'Check Progress')
        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()
            if file_name[0].endswith('.py'):
                head, tail = ntpath.split(file_name[0])
                if tail.endswith('experiment1.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1" in f.read():
                            progress_text += 'Problem 1' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 2" in f.read():
                            progress_text += 'Problem 2' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 3" in f.read():
                            progress_text += 'Problem 3' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 3' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 4" in f.read():
                            progress_text += 'Problem 4' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 4' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 5" in f.read():
                            progress_text += 'Problem 5' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 5' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 6" in f.read():
                            progress_text += 'Problem 6' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 6' + "✘" + "\n"
                    progress_text += "The file awaits to be graded in assignments/experiment1/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 1-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment2.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1" in f.read():
                            progress_text += 'Problem 1' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 2" in f.read():
                            progress_text += 'Problem 2' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 3" in f.read():
                            progress_text += 'Problem 3' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 3' + "✘" + "\n"
                    progress_text += "The file awaits to be graded in assignments/experiment2/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 2-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment3.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.b" in f.read():
                            progress_text += 'Problem 1.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.c" in f.read():
                            progress_text += 'Problem 1.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 1.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.e" in f.read():
                            progress_text += 'Problem 1.e' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.e' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.f" in f.read():
                            progress_text += 'Problem 1.f' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.f' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.g" in f.read():
                            progress_text += 'Problem 1.g' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.g' + "✘" + "\n"
                    progress_text += "The file awaits to be graded in assignments/experiment3/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 3-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()


                if tail.endswith('experiment4.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.b" in f.read():
                            progress_text += 'Problem 1.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.c" in f.read():
                            progress_text += 'Problem 1.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 1.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.e" in f.read():
                            progress_text += 'Problem 1.e' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.e' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.f" in f.read():
                            progress_text += 'Problem 1.f' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.f' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.g" in f.read():
                            progress_text += 'Problem 1.g' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.g' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.h" in f.read():
                            progress_text += 'Problem 1.h' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.h' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.i" in f.read():
                            progress_text += 'Problem 1.i' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.i' + "✘" + "\n"
                    progress_text += "The file awaits to be graded in assignments/experiment4/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 4-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment5.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.b" in f.read():
                            progress_text += 'Problem 1.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.c" in f.read():
                            progress_text += 'Problem 1.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 1.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.d.1" in f.read():
                            progress_text += 'Problem 1.d.1' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d.1' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.d.2" in f.read():
                            progress_text += 'Problem 1.d.2' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d.2' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d.3" in f.read():
                            progress_text += 'Problem 1.d.3' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d.3' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d.4" in f.read():
                            progress_text += 'Problem 1.d.4' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d.4' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.d.5" in f.read():
                            progress_text += 'Problem 1.d.5' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d.5' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d.6" in f.read():
                            progress_text += 'Problem 1.d.6' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d.6' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d.7" in f.read():
                            progress_text += 'Problem 1.d.7' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d.7' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.e" in f.read():
                            progress_text += 'Problem 1.e' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.e' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 2" in f.read():
                            progress_text += 'Problem 2' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2' + "✘" + "\n"

                    progress_text += "The file awaits to be graded in assignments/experiment5/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 5-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment6.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.b" in f.read():
                            progress_text += 'Problem 1.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.c" in f.read():
                            progress_text += 'Problem 1.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 1.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.e" in f.read():
                            progress_text += 'Problem 1.e' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.e' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.f" in f.read():
                            progress_text += 'Problem 1.f' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.f' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.g" in f.read():
                            progress_text += 'Problem 1.g' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.g' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.h" in f.read():
                            progress_text += 'Problem 1.h' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.h' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.i" in f.read():
                            progress_text += 'Problem 1.i' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.i' + "✘" + "\n"
                    progress_text += "The file awaits to be graded in assignments/experiment6/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 6-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment7.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.b" in f.read():
                            progress_text += 'Problem 1.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.c" in f.read():
                            progress_text += 'Problem 1.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 1.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.e" in f.read():
                            progress_text += 'Problem 1.e' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.e' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.f" in f.read():
                            progress_text += 'Problem 1.f' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.f' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.g" in f.read():
                            progress_text += 'Problem 1.g' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.g' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.h" in f.read():
                            progress_text += 'Problem 1.h' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.h' + "✘" + "\n"

                    progress_text += "The file awaits to be graded in assignments/experiment7/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 7-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment8.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.a.1" in f.read():
                            progress_text += 'Problem 1.a.1' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a.1' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.a.2" in f.read():
                            progress_text += 'Problem 1.a.2' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a.2' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.a.3" in f.read():
                            progress_text += 'Problem 1.a.3' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a.3' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.b.1" in f.read():
                            progress_text += 'Problem 1.b.1' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.1' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.b.2" in f.read():
                            progress_text += 'Problem 1.b.2' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.2' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.b.3" in f.read():
                            progress_text += 'Problem 1.b.3' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.3' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.b.4" in f.read():
                            progress_text += 'Problem 1.b.4' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.4' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.b.5" in f.read():
                            progress_text += 'Problem 1.b.5' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.5' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.b.6" in f.read():
                            progress_text += 'Problem 1.b.6' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.6' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.b.7" in f.read():
                            progress_text += 'Problem 1.b.7' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.7' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.b.8" in f.read():
                            progress_text += 'Problem 1.b.8' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.8' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.b.9" in f.read():
                            progress_text += 'Problem 1.b.9' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.9' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.b.10" in f.read():
                            progress_text += 'Problem 1.b.10' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.10' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.b.11" in f.read():
                            progress_text += 'Problem 1.b.11' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b.11' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 2.a" in f.read():
                            progress_text += 'Problem 2.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 2.b" in f.read():
                            progress_text += 'Problem 2.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 2.c" in f.read():
                            progress_text += 'Problem 2.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.c' + "✘" + "\n"



                    progress_text += "The file awaits to be graded in assignments/experiment8/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 8-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment9.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.b" in f.read():
                            progress_text += 'Problem 1.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.c" in f.read():
                            progress_text += 'Problem 1.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 1.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.e" in f.read():
                            progress_text += 'Problem 1.e' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.e' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.f" in f.read():
                            progress_text += 'Problem 1.f' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.f' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.g" in f.read():
                            progress_text += 'Problem 1.g' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.g' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.h" in f.read():
                            progress_text += 'Problem 1.h' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.h' + "✘" + "\n"


                    with open(file_name[0]) as f:
                        if "Problem 1.i" in f.read():
                            progress_text += 'Problem 1.i' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.i' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.j" in f.read():
                            progress_text += 'Problem 1.j' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.j' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.k" in f.read():
                            progress_text += 'Problem 1.k' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.k' + "✘" + "\n"


                    with open(file_name[0]) as f:
                        if "Problem 2.a" in f.read():
                            progress_text += 'Problem 2.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 2.b" in f.read():
                            progress_text += 'Problem 2.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 2.c" in f.read():
                            progress_text += 'Problem 2.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 2.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 2.e" in f.read():
                            progress_text += 'Problem 2.e' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.e' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 2.f" in f.read():
                            progress_text += 'Problem 2.f' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.f' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 2.g" in f.read():
                            progress_text += 'Problem 2.g' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.g' + "✘" + "\n"

                    progress_text += "The file awaits to be graded in assignments/experiment9/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 9-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()


                if tail.endswith('experiment10.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1" in f.read():
                            progress_text += 'Problem 1' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 2" in f.read():
                            progress_text += 'Problem 2' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 3" in f.read():
                            progress_text += 'Problem 3' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 3' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 4" in f.read():
                            progress_text += 'Problem 4' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 4' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 5" in f.read():
                            progress_text += 'Problem 5' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 5' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 6" in f.read():
                            progress_text += 'Problem 6' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 6' + "✘" + "\n"
                    progress_text += "The file awaits to be graded in assignments/experiment10/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 10-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment11.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.b" in f.read():
                            progress_text += 'Problem 1.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.c" in f.read():
                            progress_text += 'Problem 1.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 1.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.e" in f.read():
                            progress_text += 'Problem 1.e' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.e' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.f" in f.read():
                            progress_text += 'Problem 1.f' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.f' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.g" in f.read():
                            progress_text += 'Problem 1.g' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.g' + "✘" + "\n"

                    progress_text += "The file awaits to be graded in assignments/experiment11/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 11-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment12.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.b" in f.read():
                            progress_text += 'Problem 1.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.c" in f.read():
                            progress_text += 'Problem 1.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 1.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.e" in f.read():
                            progress_text += 'Problem 1.e' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.e' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.f" in f.read():
                            progress_text += 'Problem 1.f' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.f' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.g" in f.read():
                            progress_text += 'Problem 1.g' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.g' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.h" in f.read():
                            progress_text += 'Problem 1.h' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.h' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.i" in f.read():
                            progress_text += 'Problem 1.i' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.i' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.j" in f.read():
                            progress_text += 'Problem 1.j' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.j' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.k" in f.read():
                            progress_text += 'Problem 1.k' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.k' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.l" in f.read():
                            progress_text += 'Problem 1.l' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.l' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.m" in f.read():
                            progress_text += 'Problem 1.m' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.m' + "✘" + "\n"

                    progress_text += "The file awaits to be graded in assignments/experiment12/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 12-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()


                if tail.endswith('experiment13.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1" in f.read():
                            progress_text += 'Problem 1' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 2" in f.read():
                            progress_text += 'Problem 2' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 3" in f.read():
                            progress_text += 'Problem 3' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 3' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 4" in f.read():
                            progress_text += 'Problem 4' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 4' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 5" in f.read():
                            progress_text += 'Problem 5' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 5' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 6" in f.read():
                            progress_text += 'Problem 6' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 6' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 7" in f.read():
                            progress_text += 'Problem 7' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 7' + "✘" + "\n"
                    progress_text += "The file awaits to be graded in assignments/experiment13/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 13-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment14.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1" in f.read():
                            progress_text += 'Problem 1' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 2" in f.read():
                            progress_text += 'Problem 2' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 3" in f.read():
                            progress_text += 'Problem 3' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 3' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 4" in f.read():
                            progress_text += 'Problem 4' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 4' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 5" in f.read():
                            progress_text += 'Problem 5' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 5' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 6" in f.read():
                            progress_text += 'Problem 6' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 6' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 7" in f.read():
                            progress_text += 'Problem 7' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 7' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 8" in f.read():
                            progress_text += 'Problem 8' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 8' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 9" in f.read():
                            progress_text += 'Problem 9' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 9' + "✘" + "\n"
                    progress_text += "The file awaits to be graded in assignments/experiment14/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 14-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment15.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.b" in f.read():
                            progress_text += 'Problem 1.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.c" in f.read():
                            progress_text += 'Problem 1.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 1.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 2.a" in f.read():
                            progress_text += 'Problem 2.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.a' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 2.b" in f.read():
                            progress_text += 'Problem 2.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 2.c" in f.read():
                            progress_text += 'Problem 2.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 2.d" in f.read():
                            progress_text += 'Problem 2.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 2.d' + "✘" + "\n"

                    progress_text += "The file awaits to be graded in assignments/experiment15/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 15-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                if tail.endswith('experiment16.py'):
                    progress_text = ""
                    with open(file_name[0]) as f:
                        if "Problem 1.a" in f.read():
                            progress_text += 'Problem 1.a' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.a' + "✘" + "\n "
                    with open(file_name[0]) as f:
                        if "Problem 1.b" in f.read():
                            progress_text += 'Problem 1.b' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.b' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.c" in f.read():
                            progress_text += 'Problem 1.c' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.c' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.d" in f.read():
                            progress_text += 'Problem 1.d' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.d' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.e" in f.read():
                            progress_text += 'Problem 1.e' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.e' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.f" in f.read():
                            progress_text += 'Problem 1.f' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.f' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.g" in f.read():
                            progress_text += 'Problem 1.g' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.g' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.h" in f.read():
                            progress_text += 'Problem 1.h' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.h' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.i" in f.read():
                            progress_text += 'Problem 1.i' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.i' + "✘" + "\n"
                    with open(file_name[0]) as f:
                        if "Problem 1.j" in f.read():
                            progress_text += 'Problem 1.j' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.j' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.k" in f.read():
                            progress_text += 'Problem 1.k' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.k' + "✘" + "\n"

                    with open(file_name[0]) as f:
                        if "Problem 1.l" in f.read():
                            progress_text += 'Problem 1.l' + "✅" + "\n"
                        else:
                            progress_text += 'Problem 1.l' + "✘" + "\n"

                    progress_text += "The file awaits to be graded in assignments/experiment16/"+str(tail)+" file!"
                    msg = QMessageBox()
                    msg.setWindowTitle("Experiment 16-"+str(tail)[0:12])
                    msg.setText(progress_text)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

            else:
                msg = QMessageBox()
                msg.setWindowTitle("File Error!")
                msg.setText("Please select an appropriate Python script!")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()






    def download_solution(self):
        
            if self.experiment_comboBox.currentText() == 'Experiment 1':
                path_on_cloud = "experiment1.pdf"
                storage.child(path_on_cloud).download("solutions/experiment1.pdf")
                webbrowser.open_new(r'solutions/experiment1.pdf')

            if self.experiment_comboBox.currentText() == 'Experiment 2':
                path_on_cloud = "experiment2_solution.pdf"
                storage.child(path_on_cloud).download("solutions/experiment2_solution.pdf")
                webbrowser.open_new(r'solutions/experiment2_solution.pdf')

            if self.experiment_comboBox.currentText() == 'Experiment 3':
                path_on_cloud = "experiment3_solution.pdf"
                storage.child(path_on_cloud).download("solutions/experiment3_solution.pdf")
                webbrowser.open_new(r'solutions/experiment3_solution.pdf')

            if self.experiment_comboBox.currentText() == 'Experiment 4':
                path_on_cloud = "experiment4_solution.pdf"
                storage.child(path_on_cloud).download("solutions/experiment4_solution.pdf")
                webbrowser.open_new(r'solutions/experiment4_solution.pdf')

            if self.experiment_comboBox.currentText() == 'Experiment 5':
                path_on_cloud = "experiment5_solution.pdf"
                storage.child(path_on_cloud).download("solutions/experiment5_solution.pdf")
                webbrowser.open_new(r'solutions/experiment5_solution.pdf')

            if self.experiment_comboBox.currentText() == 'Experiment 6':
                path_on_cloud = "experiment6_solution.pdf"
                storage.child(path_on_cloud).download("solutions/experiment6_solution.pdf")
                webbrowser.open_new(r'solutions/experiment6_solution.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 7':
                path_on_cloud = "experiment7_solutions.pdf"
                storage.child(path_on_cloud).download("solutions/experiment7_solution.pdf")
                webbrowser.open_new(r'solutions/experiment7_solution.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 8':
                path_on_cloud = "experiment8_solution.pdf"
                storage.child(path_on_cloud).download("solutions/experiment8_solution.pdf")
                webbrowser.open_new(r'solutions/experiment8_solution.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 9':
                path_on_cloud = "experiment9_solution.pdf"
                storage.child(path_on_cloud).download("solutions/experiment9_solution.pdf")
                webbrowser.open_new(r'solutions/experiment9_solution.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 10':
                path_on_cloud = "experiment10.pdf"
                storage.child(path_on_cloud).download("solutions/experiment10_solution.pdf")
                webbrowser.open_new(r'solutions/experiment10_solution.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 11':
                path_on_cloud = "experiment11.pdf"
                storage.child(path_on_cloud).download("solutions/experiment11.pdf")
                webbrowser.open_new(r'solutions/experiment11.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 12':
                path_on_cloud = "experiment12_solution.pdf"
                storage.child(path_on_cloud).download("solutions/experiment12_solution.pdf")
                webbrowser.open_new(r'solutions/experiment12_solution.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 13':
                path_on_cloud = "experiment13.pdf"
                storage.child(path_on_cloud).download("solutions/experiment13_solution.pdf")
                webbrowser.open_new(r'solutions/experiment13_solution.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 14':
                path_on_cloud = "experiment14.pdf"
                storage.child(path_on_cloud).download("solutions/experiment14_solution.pdf")
                webbrowser.open_new(r'solutions/experiment14_solution.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 15':
                path_on_cloud = "experiment15.pdf"
                storage.child(path_on_cloud).download("solutions/experiment15_solution.pdf")
                webbrowser.open_new(r'solutions/experiment15_solution.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 16':
                path_on_cloud = "experiment16.pdf"
                storage.child(path_on_cloud).download("solutions/experiment16_solution.pdf")
                webbrowser.open_new(r'solutions/experiment16_solution.pdf')
                
    def download_pdf(self):
            if self.experiment_comboBox.currentText() == 'Experiment 1':
                path_on_cloud = "experiment1.pdf"
                storage.child(path_on_cloud).download("documents/experiment1.pdf")
                webbrowser.open_new(r'documents/experiment1.pdf')

            if self.experiment_comboBox.currentText() == 'Experiment 2':
                path_on_cloud = "experiment2.pdf"
                storage.child(path_on_cloud).download("documents/experiment2.pdf")
                webbrowser.open_new(r'documents/experiment2.pdf')

            if self.experiment_comboBox.currentText() == 'Experiment 3':
                path_on_cloud = "experiment3.pdf"
                storage.child(path_on_cloud).download("documents/experiment3.pdf")
                webbrowser.open_new(r'documents/experiment3.pdf')

            if self.experiment_comboBox.currentText() == 'Experiment 4':
                path_on_cloud = "experiment4.pdf"
                storage.child(path_on_cloud).download("documents/experiment4.pdf")
                webbrowser.open_new(r'documents/experiment4.pdf')

            if self.experiment_comboBox.currentText() == 'Experiment 5':
                path_on_cloud = "experiment5.pdf"
                storage.child(path_on_cloud).download("documents/experiment5.pdf")
                webbrowser.open_new(r'documents/experiment5.pdf')

            if self.experiment_comboBox.currentText() == 'Experiment 6':
                path_on_cloud = "experiment6.pdf"
                storage.child(path_on_cloud).download("documents/experiment6.pdf")
                webbrowser.open_new(r'documents/experiment6.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 7':
                path_on_cloud = "experiment7.pdf"
                storage.child(path_on_cloud).download("documents/experiment7.pdf")
                webbrowser.open_new(r'documents/experiment7.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 8':
                path_on_cloud = "experiment8.pdf"
                storage.child(path_on_cloud).download("documents/experiment8.pdf")
                webbrowser.open_new(r'documents/experiment8.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 9':
                path_on_cloud = "experiment9.pdf"
                storage.child(path_on_cloud).download("documents/experiment9.pdf")
                webbrowser.open_new(r'documents/experiment9.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 10':
                path_on_cloud = "experiment10.pdf"
                storage.child(path_on_cloud).download("documents/experiment10.pdf")
                webbrowser.open_new(r'documents/experiment10.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 11':
                path_on_cloud = "experiment11.pdf"
                storage.child(path_on_cloud).download("documents/experiment11.pdf")
                webbrowser.open_new(r'documents/experiment11.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 12':
                path_on_cloud = "experiment12.pdf"
                storage.child(path_on_cloud).download("documents/experiment12.pdf")
                webbrowser.open_new(r'documents/experiment12.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 13':
                path_on_cloud = "experiment13.pdf"
                storage.child(path_on_cloud).download("documents/experiment13.pdf")
                webbrowser.open_new(r'documents/experiment13.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 14':
                path_on_cloud = "experiment14.pdf"
                storage.child(path_on_cloud).download("documents/experiment14.pdf")
                webbrowser.open_new(r'documents/experiment14.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 15':
                path_on_cloud = "experiment15.pdf"
                storage.child(path_on_cloud).download("documents/experiment15.pdf")
                webbrowser.open_new(r'documents/experiment15.pdf')


            if self.experiment_comboBox.currentText() == 'Experiment 16':
                path_on_cloud = "experiment16.pdf"
                storage.child(path_on_cloud).download("documents/experiment16.pdf")
                webbrowser.open_new(r'documents/experiment16.pdf')
                
    def show_item(self):
        if self.experiment_comboBox.currentText() == 'Experiment 1':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment1.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 2':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment2.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 3':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment3.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 4':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment4.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 5':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment5.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 6':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment6.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 7':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment7.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 8':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment8.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 9':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment9.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 10':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment10.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 11':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment11.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 12':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment12.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 13':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment13.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 14':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment14.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 15':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment15.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()

        if self.experiment_comboBox.currentText() == 'Experiment 16':
            files = storage.child().list_files()
            for file in files:
                try:
                    if file.name.endswith('experiment16.py'):
                        print(file.name)
                        storage.child(file.name).download(file.name)
                        msg = QMessageBox()
                        msg.setWindowTitle("Download Succesful!")
                        msg.setText("All the files that the students sent are downloaded!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Download Failed!!")
                    msg.setText("Something went wrong with the download phase!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()


pub = rospy.Publisher('/hamer/cmd_vel', Twist, queue_size=5)
app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()
mainWindow = first_screen()
st = student_login()
inst = instructor_login()
st_cr = student_create_account()
std_create_appr = student_create_acc_approved()
std_main = student_main()
std_cam = student_camera()
inst_main = instructor_main_window()
widget.addWidget(mainWindow)  # 0
widget.addWidget(st)  # 1
widget.addWidget(inst)  # 2
widget.addWidget(st_cr)  # 3
widget.addWidget(std_create_appr)  # 4
widget.addWidget(std_main)  # 5
widget.addWidget(std_cam) # 6
widget.addWidget(inst_main) # 7
widget.setFixedHeight(900)
widget.setFixedWidth(1300)
widget.show()

if __name__ == "__main__":
    twist = Twist()
    odom = Odometry()
    sys.exit(app.exec_())