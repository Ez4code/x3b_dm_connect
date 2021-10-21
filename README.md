# x3b_dm_connect
To test x3b module communication, Ez4code build a ros package.

use xbee to connect windows with ROS or ROS with ROS
- RF module: XBEE 900HP module × 3 (or 2)
- protocol: digimesh
- ROS version: Melodic

if something is wrong, PLEASE email me: iexliu@163.com, THANK YOU!!! 

<a name="I1FoN"></a>
# 1 环境搭建
- ros版本--melodic
- Python3.6
   - **The XBee Python library is currently only compatible with Python 3.**
- PySerial 3
   - **This module is automatically downloaded when you install the XBee Python library.**​
- SRP
   - **This module is automatically downloaded when you install the XBee Python library.**​
- XBee Python library software

`$ pip install digi-xbee`

- (XCTU)
<a name="PwxNZ"></a>
# 2 Configure your XBee modules
<a name="JOUYY"></a>
### DigiMesh devices

1. Click **Load default firmware settings** in the **Radio Configuration** toolbar to load the default values for the device firmware.
1. Ensure the API mode (API1 or API2) is enabled. To do so, the **AP** parameter value must be **1** (API mode without escapes) or **2** (API mode with escapes).
1. Configure **ID** (PAN ID) setting to **CAFE**.
1. Configure **CH** (Operating Channel) to **C**.
1. Click **Write radio settings** in the **Radio Configuration** toolbar to apply the new values to the module.
1. Once you have configured both modules, check to make sure they can see each other. Click **Discover radio modules in the same network**, the second button of the device panel in the **Radio Modules** view. The other device must be listed in the **Discovering remote devices** dialog.

​<br />
<a name="tuboU"></a>
# 3 Test your Xbee radio module
```cpp
import codecs
import numpy as np
from digi.xbee.devices import XBeeDevice
from digi.xbee.models.message import XBeeMessage
#msg = XBeeMessage(rx_data ="None",rx_remote_node= None,rx_timestamp=None)
msg = None
device = XBeeDevice("/dev/ttyUSB0",9600)
device.open()
device.send_data_broadcast("hello life")
while 1:
    msg = device.read_data()
    if msg:
        rx_bytearray = msg.data
        rx_message = codecs.decode(rx_bytearray)
        print (rx_message)
        print(type(rx_message))

#device.close()
```
I'm just a beginner of Python, so...this code is ugly. You can totally rewrite it in your own habits. Remember, You should use Python3.
<a name="XVBFU"></a>
# 4 Creating the ROS package
<a name="YFw4b"></a>
## 4.1 Creating a catkin Package
First change to the source space directory of the catkin workspace you created.
```cpp
$ cd ~/catkin_ws/src
```
Use catkin_create_pkg script to create a new package called 'x3b_dm_connect' which depends on geometry_msgs( turtlesim use it! ), roscpp, rospy, std_msg, message_generation:
```cpp
$ catkin_create_pkg geometry_msgs roscpp rospy std_msg message_generation
```
Because use python to create the ROS package, the following codes must be included:
```cpp
catkin_python_setup()
```
By adding the .msg files manually, we make sure that CMake knows when it has to reconfigure the project after you add other .msg files.
```cpp
add_message_files(
   FILES
   Pose.msg
 )
```
Now we must ensure the generate_messages() function is called.
```cpp
generate_messages(
  DEPENDENCIES
  geometry_msgs
  std_msgs
)
```
The following code is actually not quite understood, but is written according to the ROS package specification
```cpp
catkin_package(
  CATKIN_DEPENDS message_runtime
)


catkin_install_python(
  PROGRAMS nodes/turtle_s3b_ctl.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
```
<a name="cY1ma"></a>
## 4.2 Building a catkin workspace 
Now you need to build the packages in the catkin workspace:
```cpp
$ cd ~/catkin_ws
$ catkin_make
```
After the workspace has been built it has created a similar structure in the devel subfolder as you usually find under /opt/ros/$ROSDISTRO_NAME.
<a name="xxjqw"></a>
## 4.3 Customizing the package.xml
The following code is easy to understand
```cpp
<?xml version="1.0"?>
<package format="2">
  <name>x3b_dm_connect</name>
  <version>0.0.0</version>
  <description>The x3b_dm_connect package</description>
  <maintainer email="ubuntu@todo.todo">ubuntu</maintainer>
  <license>TODO</license>

  <buildtool_depend>catkin</buildtool_depend>
  <build_depend>geometry_msgs</build_depend>
  <build_depend>roscpp</build_depend>
  <build_depend>rospy</build_depend>
  <build_depend>std_msgs</build_depend>
  <build_export_depend>geometry_msgs</build_export_depend>
  <build_export_depend>roscpp</build_export_depend>
  <build_export_depend>rospy</build_export_depend>
  <build_export_depend>std_msgs</build_export_depend>
  <exec_depend>geometry_msgs</exec_depend>
  <exec_depend>roscpp</exec_depend>
  <exec_depend>rospy</exec_depend>
  <exec_depend>std_msgs</exec_depend>
  <build_depend>message_generation</build_depend>
  <exec_depend>message_runtime</exec_depend>
  <export>
  </export>
</package>
```
<a name="ReV0o"></a>
## 4.4 Complete the ROS package
Supplement the missing contents of the ROS package according to the python usage specification in the package:

- ROS Package中的Python使用规范_（通过实际工程举例基于Python的ros包结构）_
> [https://blog.csdn.net/Cyril__Li/article/details/78979253](https://blog.csdn.net/Cyril__Li/article/details/78979253)

<a name="hJyd2"></a>
## 4.5 node
Remember, you should also install catkin-tools and rospkg in Python3 environment.
```cpp
$ pip3 install catkin-tools
$ pip3 install rospkg
```
It is important that:`#!/usr/bin/env python3`, this is not code annotation. Symbol #! is called "shebang". Its function is to specify which interpreter will execute the script
```python
#!/usr/bin/env python3
import rospy
import codecs
import numpy
from geometry_msgs.msg import Twist
from digi.xbee.devices import XBeeDevice
from digi.xbee.models.message import XBeeMessage

if __name__== '__main__':

# Receiver the data from x3b

    msg = None
    device = XBeeDevice("/dev/ttyUSB0",9600)
    device.open()
    device.send_data_broadcast("hello life")
        

    rospy.init_node('turtle_s3b_ctl')
    topicName =  "/turtle1/cmd_vel"

    #def talker():
    pub = rospy.Publisher(topicName, Twist, queue_size=1000)

    while 1:

        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        # endless loop if not receive data
        msg = device.read_data()
        if msg:
            rx_bytearray = msg.data
            rx_message = codecs.decode(rx_bytearray)
            print (rx_message)
            print(type(rx_message))

# Convert keyboard input to speed  //not done
    

            if rx_message == '1':
                twist.linear.x = 1.0
            if rx_message == '2':
                twist.linear.x = -1.0
            if rx_message == '3':
                twist.angular.z = 1.0
            if rx_message == '4':
                twist.angular.z = -1.0

            pub.publish(twist)
        
```
<a name="nix4W"></a>
## 4.6 最终编写的ROS包结构如下：
![image.png](https://cdn.nlark.com/yuque/0/2021/png/22224922/1634644541248-2ebbba9f-c047-4224-8572-24e6bde247de.png#clientId=ud3425ab5-1b5d-4&from=paste&height=252&id=ue0624ddf&margin=%5Bobject%20Object%5D&name=image.png&originHeight=252&originWidth=256&originalType=binary&ratio=1&size=24751&status=done&style=none&taskId=uf4783190-b5e0-4b7d-8c62-0ee680b029d&width=256)
<a name="mSp1p"></a>
## 4.7 catkin_make
```cpp
$ cd catkin_ws
$ catkin_make
```
<a name="sUavE"></a>
## 4.8 Just try it!
Before running, you should give the user permission to read and write /dev/ttyUSB0.
```cpp
$ sudo chmod 666 /dev/ttyUSB0
```
And then:
```cpp
$ roscore
$ rosrun x3b_dm_connect turtle_s3b_ctl.py 
$ rosrun turtlesim turtlesim_node 
```
If you send message to xbee, the turtle will run!!!
<a name="xYyNM"></a>
# 5 references

- Digi Xbee Python Library:
> [https://xbplib.readthedocs.io/en/latest/getting_started_with_xbee_python_library.html#gsgconfigdmdevices](https://xbplib.readthedocs.io/en/latest/getting_started_with_xbee_python_library.html#gsgconfigdmdevices)

- ros_packages Ros python包新手教程
> [https://github.com/jlyw1017/ros_packages](https://github.com/jlyw1017/ros_packages)

- ROS Package中的Python使用规范_（通过实际工程举例基于Python的ros包结构）_
> [https://blog.csdn.net/Cyril__Li/article/details/78979253](https://blog.csdn.net/Cyril__Li/article/details/78979253)

- ROS.org上的PyStyleGuide介绍
> [http://wiki.ros.org/PyStyleGuide](http://wiki.ros.org/PyStyleGuide)

- turtlesim源代码
> [https://github.com/ros/ros_tutorials](https://github.com/ros/ros_tutorials)

- python：bytes和bytearray、编码和解码_（xbee收发格式解析）_
> [https://www.cnblogs.com/f-ck-need-u/archive/2018/12/27/10185965.html](https://www.cnblogs.com/f-ck-need-u/archive/2018/12/27/10185965.html)

- 如何在Ros环境下使用Python3的包-三行代码解决
> [https://blog.csdn.net/weixin_43572595/article/details/109029259?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-16.no_search_link&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-16.no_search_link](https://blog.csdn.net/weixin_43572595/article/details/109029259?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-16.no_search_link&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-16.no_search_link)

