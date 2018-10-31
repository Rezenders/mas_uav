FROM ros_ws
# FROM rezenders/mavros:melodic

RUN apt-get update && apt-get install -y \
    ros-melodic-mavros \
    && rm -rf /var/lib/apt/lists/

RUN catkin_create_pkg fly
COPY fly /catkin_ws/src/fly
