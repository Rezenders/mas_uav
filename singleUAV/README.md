## Usage

### Build images and create network
Create docker network
```bash
$ docker network create ros_net
```

Build hwbridge_node image:
```bash
$ docker build --tag hwbridge singleUAV/HwBridge/
```

Build agent_node image:

```bash
$ docker build --tag jason_agent singleUAV/JasonAgent/
```

or

```bash
$ docker build --tag python_agent singleUAV/PythonAgent/
```

### Run containers

Allow xhost:
```bash
$ xhost +local:root # for the lazy and reckless
```

Ardupilot container:
```bash
$ docker run -it --rm --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --name ardupilot --net ros_net rezenders/ardupilot-ubuntu sim_vehicle.py -v ArduCopter --console --map -L UFSC --out mavros:14551
```
Note: mavros is the address of the mavros container

Roscore:
```bash
$ docker run -it --rm --net ros_net  --name master --env ROS_HOSTNAME=master --env ROS_MASTER_URI=http://master:11311 ros:melodic-ros-core roscore
```

Mavros container:
```bash
$ docker run -it --rm --net ros_net  --name mavros --env ROS_HOSTNAME=mavros --env ROS_MASTER_URI=http://master:11311  rezenders/mavros roslaunch launch/apm.launch fcu_url:="udp://:14551@ardupilot:14555"
```
Note: ardupilot is the ip of the ardupilot container

Container publishing to mavros:
```bash
$ docker run -it --rm --net ros_net --name hwbridge --env ROS_HOSTNAME=hwbridge --env ROS_MASTER_URI=http://master:11311 hwbridge ./hw_bridge.py
```

Jason container:

```bash
$ docker run -it --rm --net ros_net --name jason --env ROS_HOSTNAME=jason --env ROS_MASTER_URI=http://master:11311 jason_agent gradle
```

or for the python container:

```bash
$ docker run -it --rm --net ros_net --name python --env ROS_HOSTNAME=python --env ROS_MASTER_URI=http://master:11311 python_agent gradle
```

## Hardware in the loop

The hardware in the loop was tested using a raspbery pi 3 model B but it should work with other armv7 boards.

[balenaOS](https://www.balena.io/os/#download) is used as Operating System, you must download it and install before running this project.

Also, you have to download and install [balena-cli](https://www.balena.io/docs/reference/cli/) on your host machine.

Another difference is that balenaOS uses balena as container engine not docker engine. However, they are compatible.

### Running the experiment

The main difference here is that ardupilot container will be executed in the host machine and all other applications directly in the board.

Boot the board with balenaOS and connect it to the same network as the host PC.

Then, you will need to find the board ip, for that run:

```bash
$ balena scan
```

#### Running ardupilot
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

Note: 150.162.53.23 is the ip of the board which will be running the mavros container, not the container\`s ip. The one you found using ```$ balena scan```

### Running mission application

In the singleUAV directory run:

```bash
$ balena push <ip>
```
