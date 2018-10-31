# MAS-UAV
Multi agent system to coordinate multiple UAVs

## Usage

Create docker network
```bash
$ docker network create ros_net
```

Build mas_uav:middle image:
```bash
$ docker build --tag mas_uav:middle MiddleNode/
```

Roscore:
```bash
$ docker run -it --rm --net ros_net  --name master --env ROS_HOSTNAME=master ros:melodic roscore 
```

Allow xhost:
```bash
$ xhost +local:root # for the lazy and reckless
```

Ardupilot container:
```bash
$ docker run -it --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw"  --net ros_net rezenders/ardupilot-ubuntu 
```

```bash
$ sim_vehicle.py -v ArduCopter --console --map -L UFSC --out 172.19.0.3:14551
```
Note: 172.19.0.3 is the ip of the container which will be running mavros (Still needs to be automated)

Mavros container:
```bash
$ docker run -it --rm --net ros_net  --name mavros --env ROS_HOSTNAME=mavros --env ROS_MASTER_URI=http://master:11311 -p 14555:14555 -p 14551:14551 rezenders/mavros:melodic 
```

```bash
$ roslaunch launch/apm.launch fcu_url:="udp://:14551@172.19.0.2:14555"
```
Note: 172.19.0.2 is the ip of the ardupilot container

Container publishing to mavros:
```bash
$ docker run -it --rm --net ros_net --name fly --env ROS_HOSTNAME=fly --env ROS_MASTER_URI=http://master:11311 mas_uav:middle rosrun fly fly.py
```
