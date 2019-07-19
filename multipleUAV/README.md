balena run -it --rm --net ros_net  --name master --env ROS_HOSTNAME=master --env ROS_MASTER_URI=http://master:11311 local_image_master roscore

balena run -it --rm -p 14551:14551/udp --net ros_net  --name mavros --env ROS_HOSTNAME=mavros --env ROS_MASTER_URI=http://master:11311  local_image_mavros

$ roslaunch launch/apm.launch fcu_url:="udp://:14551@150.162.53.104:14555"


comm:
balena run -it --rm -p 1024:1024/udp --net ros_net --name comm --env ROS_HOSTNAME=comm --env ROS_MASTER_URI=http://master:11311 local_image_comm

hwbridge:
balena run -it --rm --net ros_net --name hwbridge --env ROS_HOSTNAME=hwbridge --env ROS_MASTER_URI=http://master:11311 local_image_hwbridge ./hw_bridge.py

jason:
balena run -it --rm --net ros_net --name jason --env ROS_HOSTNAME=jason --env ROS_MASTER_URI=http://master:11311 local_image_jason
