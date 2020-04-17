cmake_minimum_required(VERSION 2.8.3)
project(mas_uav)

find_package(catkin REQUIRED COMPONENTS
  jason_ros
  jason_ros_msgs
  jason_ros_comm
  mavros
  rospy
  std_msgs
)
catkin_python_setup()

catkin_package()

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
