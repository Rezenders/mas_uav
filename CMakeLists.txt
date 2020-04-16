cmake_minimum_required(VERSION 2.8.3)
project(mas_uav)

find_package(catkin REQUIRED COMPONENTS
  jason_hw_bridge
  jason_msgs
  mavros
  rospy
  std_msgs
)

catkin_package(
)
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
