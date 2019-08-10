[![rescueCoord video](https://img.youtube.com/vi/iV1gVJdShcI/0.jpg)](https://www.youtube.com/watch?v=https://img.youtube.com/vi/iV1gVJdShcI/0.jpg)

## Hardware in the loop

The hardware in the loop was tested using a raspbery pi 3 model B but it should work with other armv7 boards.

[balenaOS](https://www.balena.io/os/#download) is used as Operating System, you must download it and install before running this project.

Also, you have to download and install [balena-cli](https://www.balena.io/docs/reference/cli/) on your host machine.

Another difference is that balenaOS uses balena as container engine not docker engine. However, they are compatible.

#### In your host machine.

Allow xhost:
```bash
$ xhost +local:root # for the lazy and reckless
```

Ardupilot container1:
```bash
$ docker run -it --rm -p 14555:14555/udp --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --name ardupilot --net ros_net rezenders/ardupilot-ubuntu
```

Note: Now we have to use ```-p 14555:14555/udp``` to bind the container 14555 port with the host 14555 port

Then:
```bash
$ sim_vehicle.py -v ArduCopter --console --map -L UFSC --out 150.162.53.67:14551
```

Note: 150.162.53.67 is the ip of the board which will be running the mavros container, not the container\`s ip.

Ardupilot container2:
```bash
$ docker run -it --rm -p 14556:14556/udp --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --name ardupilot2 --net ros_net rezenders/ardupilot-ubuntu
```

Note: Now we have to use ```-p 14556:14556/udp``` to bind the container 14556 port with the host 14556 port

Then:
```bash
$ sim_vehicle.py -v ArduCopter --console --map -L UFSC --out 150.162.53.68:14551
```

Note: 150.162.53.68 is the ip of the board which will be running the mavros container, not the container\`s ip.

Ardupilot container3:
```bash
$ docker run -it --rm -p 14557:14557/udp --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --name ardupilot3 --net ros_net rezenders/ardupilot-ubuntu
```

Note: Now we have to use ```-p 14555:14555/udp``` to bind the container 14555 port with the host 14555 port

Then:
```bash
$ sim_vehicle.py -v ArduCopter --console --map -L UFSC --out 150.162.53.78:14551
```


#### In the board

DroneA:
```
$ cd droneA/
$ balena push 150.162.53.67
```

Note: 150.162.53.67 is the droneA board ip

DroneB:
```
$ cd droneB/
$ balena push 150.162.53.68
```

Note: 150.162.53.68 is the droneB board ip
