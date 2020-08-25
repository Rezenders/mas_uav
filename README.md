# MAS-UAV
Multi agent system to coordinate multiple UAVs

This repository was tested with ubuntu 18.04, ROS melodic and gazebo 9.
## Build
This repository is a ROS package, therefore it is necessary to set up a ROS workspace with the necessary packages and build it.

First, source ROS and create a new workspace:

```
$ source /opt/ros/melodic/setup.bash
$ mkdir -p ~/jason_ros_ws/src
$ cd ~/jason_ros_ws/
$ catkin_make
```

Then, download the necessary packages:
```
$ cd ~/jason_ros_ws/src/
$ git clone https://github.com/Rezenders/mas_uav.git
$ git clone https://github.com/jason-lang/jason_ros.git
```

Download deps and build the workspace:
```
$ cd ~/jason_ros_ws/
$ apt update
$ rosdep install --from-paths src --ignore-src -r -y
$ catkin_make
```

Install some more deps:
```
$ rosrun mavros install_geographiclib_datasets.sh
$ apt install gradle
```

Also, this experiments use ardupilot SITL to simulate the UAVs so it is necessary to set it up. The instructions for installing it can be found in: https://ardupilot.org/dev/docs/building-setup-linux.html#building-setup-linux

After installing ardupilot add UFSC location into locations.txt

```
$ echo 'UFSC=-27.604033,-48.518363,21,0' >> /ardupilot/Tools/autotest/locations.txt
```

It is also possible to use gazebo with ardupilot SITL, in case you do not want to use it you can skip the following instructions.

First, it is necessary to install a plugin to enable ardupilot to communicate with gazebo.

```
$ sudo apt-get install libgazebo9-dev
```

```
$ cd ~/jason_ros_ws/src
$ git clone https://github.com/Rezenders/ardupilot_gazebo
$ cd ardupilot_gazebo
$ mkdir build
$ cd build
$ cmake ..
$ make -j4
$ sudo make install
```

````
echo 'source /usr/share/gazebo/setup.sh' >> ~/.bashrc
````

Set Path of Gazebo Models (Adapt the path to where to clone the repo)
````
echo 'export GAZEBO_MODEL_PATH=~/jason_ros_ws/src/ardupilot_gazebo/models' >> ~/.bashrc
````

Set Path of Gazebo Worlds (Adapt the path to where to clone the repo)
````
echo 'export GAZEBO_RESOURCE_PATH=~/jason_ros_ws/src/ardupilot_gazebo/worlds:${GAZEBO_RESOURCE_PATH}' >> ~/.bashrc
````

````
source ~/.bashrc
````

DONE !

## Experiments
### Single UAV

For this experiment a simple mission was performed: the UAV had to (1) takeoff; (2) fly to a predefined waypoint; (3) return to home; and finally (4) land.

#### Start ardupilot:

If you will not use gazebo:
```
$ sim_vehicle.py -v ArduCopter --map --console -L UFSC -I 0
```

If you will use gazebo (optional):
```
$ sim_vehicle.py -v ArduCopter -f gazebo-iris --map --console -L UFSC -I 0
```

If you want to use gazebo run it in another terminal (optional):

```
$ gazebo --verbose iris_arducopter_runway.world
```

#### Run the experiment:
Remeber to source the workspace:

```
$ source ~/jason_ros_ws/devel/setup.bash
```

Jason version:
```
$ roslaunch mas_uav single_uav_jason.launch
```

Python version:
```
$ roslaunch mas_uav single_uav_python.launch
```
You should see this as result:

[![singleUAV video](https://img.youtube.com/vi/5kYMEPmcZ6g/0.jpg)](https://www.youtube.com/watch?v=5kYMEPmcZ6g)

### Multiple UAVs Negotiating

In the context of S&R missions, it is really useful to have more than one UAV collaborating since when vehicles are equipped with buoys their flight autonomy time is reduced due to the increased payload. Hence, a good strategy to adopt is to have two types of UAVs working together: (i) the Scouts which are equipped with cameras and (ii) the Rescuers that are in possession of buoys, using the former to find victims and inform the latter about their location, which then deliver the buoys.

Thus, an application was designed to mimic a S&R mission that uses one Scout and two Rescuers agents working in cooperation. Firstly, the Scout takes off and flies over an area looking for victims. When a victim is located the agent informs the rescuers about the victim's position. When the rescuers receive information about a victim's location they negotiate to decide which one will deliver the buoy. The one that ends up in charge of the rescue takes off, flies to the designated position, drops a buoy, and then returns to the landing area to recharge and replace the buoy. For the sake of simplicity, scouts are only in charge to locate victims and the rescuers to drop buoys.

#### Start ardupilot:

In this experiments it will be necessary to start 3 instances of ardupilot

If you will not use gazebo:
```
$ sim_vehicle.py -v ArduCopter --map --console -L UFSC -I 0
$ sim_vehicle.py -v ArduCopter --map --console -L UFSC -I 1
$ sim_vehicle.py -v ArduCopter --map --console -L UFSC -I 2
```

If you will use gazebo (optional):
```
$ sim_vehicle.py -v ArduCopter -f gazebo-iris --map --console -L UFSC -I 0
$ sim_vehicle.py -v ArduCopter -f gazebo-iris --map --console -L UFSC -I 1
$ sim_vehicle.py -v ArduCopter -f gazebo-iris --map --console -L UFSC -I 2
```

If you want to use gazebo run it in another terminal (optional):

```
$ gazebo --verbose iris_arducopter_3uav.world
```
Note: In this experiment there may be some bugs while using gazebo
#### Run the experiment:
Remeber to source the workspace:

```
$ source ~/jason_ros_ws/devel/setup.bash
```

Jason version:
```
$ roslaunch mas_uav multiple_uav_jason_internal.launch
```

Python version:
```
$ roslaunch mas_uav multiple_uav_python_internal.launch
```
You should see this as result:

[![singleUAV video](https://img.youtube.com/vi/XkmROBkXzao/0.jpg)](https://www.youtube.com/watch?v=XkmROBkXzao&feature=youtu.be)


## Future Works
 - Dockerfile shall be created/updated for this project
 - Dockerfile-compose shall be created/update for this project
 - It should be possible to run the docker-compose with balena
 - Gazebo world and models shall be improved
 - ardupilot_gazebo should be turned into a ROS package
