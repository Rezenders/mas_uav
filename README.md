# MAS-UAV
Multi agent system to coordinate multiple UAVs

## Usage

### Build images and create network
Create docker network
```bash
$ docker network create ros_net
```

Build mas_uav:middle image:
```bash
$ docker build --tag middle_node MiddleNode/
```

Build mas_uav:jason image:
```bash
$ docker build --tag agents_node AgentsNode/
```

### Run containers

Allow xhost:
```bash
$ xhost +local:root # for the lazy and reckless
```

Ardupilot container:
```bash
$ docker run -it --rm --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --name ardupilot --net ros_net rezenders/ardupilot-ubuntu 
```

```bash
$ sim_vehicle.py -v ArduCopter --console --map -L UFSC --out 172.18.0.4:14551
```
Note: 172.18.0.4 is the ip of the container which will be running mavros (Still needs to be automated)

Roscore:
```bash
$ docker run -it --rm --net ros_net  --name master --env ROS_HOSTNAME=master --env ROS_MASTER_URI=http://master:11311 rezenders/jason-ros roslaunch rosbridge_server rosbridge_websocket.launch address:=master
```

Mavros container:
```bash
$ docker run -it --rm --net ros_net  --name mavros --env ROS_HOSTNAME=mavros --env ROS_MASTER_URI=http://master:11311  rezenders/mavros 
```

```bash
$ roslaunch launch/apm.launch fcu_url:="udp://:14551@172.18.0.3:14555"
```
Note: 172.18.0.3 is the ip of the ardupilot container

Container publishing to mavros:
```bash
$ docker run --rm --net ros_net --name fly --env ROS_HOSTNAME=fly --env ROS_MASTER_URI=http://master:11311 middle_node rosrun fly jason_flight.py
```

Jason container:
```bash
$ docker run -it --rm --net ros_net --name jason --env ROS_HOSTNAME=jason --env ROS_MASTER_URI=http://master:11311 agents_node jason uav_agents.mas2j
```
## Hardware in the loop

The hardware in the loop was tested using a beaglebone black but it should work with other armv7 boards.

[balenaOS](https://www.balena.io/os/#download) is used as Operating System, you must download it and install before running this project.

Also, you have to download and install [balena-cli](https://www.balena.io/docs/reference/cli/) on your host machine.

Another difference is that balenaOS uses balena as container engine not docker engine. However, they are compatible.

### Create Netwrok, build and push images
First you will need to ssh into the board, for that you can the following command to find the board ip:

```bash
$ balena local scan
```
After that you can ssh using:

```bash
$ ssh root@<ip> -p22222
```

Then you must create the network:

```bash
$ balena network create ros_net
```
In order to build and push the middle_node and agent_node images you need to run:

```bash
$ balena local push -s MiddleNode/ --app-name middle_node
```
```bash
$ balena local push -s AgentsNode/ --app-name agent_node
```

### Running containers
The main difference here is that ardupilot container will be executed in the host machine and that you need to ssh into the board to run each container (this will be improved in the future). 

#### In your host machine.

Allow xhost:
```bash
$ xhost +local:root # for the lazy and reckless
```

Ardupilot container:
```bash
$ docker run -it --rm -p 14555:14555/udp --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --name ardupilot --net ros_net rezenders/ardupilot-ubuntu 
```

Note: Now we have to use ```-p 14555:14555/udp``` to bind the container 14555 port with the host 14555 port

Then:
```bash
$ sim_vehicle.py -v ArduCopter --console --map -L UFSC --out 150.162.53.23:14551
```

Note: 150.162.53.23 is the ip of the board which will be running the mavros container, not the container\`s ip. 

#### In the board
Roscore:
```bash
$ balena run -it --rm --net ros_net  --name master --env ROS_HOSTNAME=master --env ROS_MASTER_URI=http://master:11311 rezenders/jason-ros roslaunch rosbridge_server rosbridge_websocket.launch address:=master
```

Mavros container:
```bash
$ balena run -it --rm -p 14551:14551/udp --net ros_net  --name mavros --env ROS_HOSTNAME=mavros --env ROS_MASTER_URI=http://master:11311  rezenders/mavros 
```
Note: Now we have to use ```-p 14551:14551/udp``` to bind the container 14551 port with the board 14551 port

```bash
$ roslaunch launch/apm.launch fcu_url:="udp://:14551@150.162.53.104:14555"
```
Note: 150.162.53.104 is the ip of the host computer

Container publishing to mavros:
```bash
$ balena run --rm --net ros_net --name fly --env ROS_HOSTNAME=fly --env ROS_MASTER_URI=http://master:11311 middle_node rosrun fly jason_flight.py
```

Jason container:
```bash
$ balena run -it --rm --net ros_net --name jason --env ROS_HOSTNAME=jason --env ROS_MASTER_URI=http://master:11311 agents_node jason uav_agents.mas2j
```

### Docker-compose
Not working yet
