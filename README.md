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

Build mas_uav:jason image:
```bash
$ docker build --tag mas_uav:jason AgentsNode/
```

Roscore:
```bash
$ docker run -it --rm --net ros_net  --name master --env ROS_HOSTNAME=master --env ROS_MASTER_URI=http://master:11311 rezenders/jason-ros:melodic roslaunch rosbridge_server rosbridge_websocket.launch address:=master
```

Allow xhost:
```bash
$ xhost +local:root # for the lazy and reckless
```

Ardupilot container:
```bash
$ docker run -it --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --name ardupilot --net ros_net rezenders/ardupilot-ubuntu 
```

```bash
$ sim_vehicle.py -v ArduCopter --console --map -L UFSC --out 172.18.0.4:14551
```
Note: 172.18.0.4 is the ip of the container which will be running mavros (Still needs to be automated)

Mavros container:
```bash
$ docker run -it --rm --net ros_net  --name mavros --env ROS_HOSTNAME=mavros --env ROS_MASTER_URI=http://master:11311  rezenders/mavros:melodic 
```

```bash
$ roslaunch launch/apm.launch fcu_url:="udp://:14551@172.18.0.3:14555"
```
Note: 172.18.0.3 is the ip of the ardupilot container

Container publishing to mavros:
```bash
$ docker run -it --rm --net ros_net --name fly --env ROS_HOSTNAME=fly --env ROS_MASTER_URI=http://master:11311 mas_uav:middle rosrun fly jason_flight.py
```

Jason container:

```bash
$ docker run -it --rm --net ros_net --name jason --env ROS_HOSTNAME=jason --env ROS_MASTER_URI=http://master:11311 mas_uav:jason
```

```bash
$ jason uav_agents.mas2j
```
