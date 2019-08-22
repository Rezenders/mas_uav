Build image:
```
sudo docker build -t ns3 .
```

Create network:
```
sudo docker network create ns3_net
```

Run containers:
```
sudo docker run -it --rm --cap-add=NET_ADMIN --device=/dev/net/tun --net ns3_net --name ns3 ns3
```

```
sudo docker run -it --rm --cap-add=NET_ADMIN --device=/dev/net/tun --net ns3_net --name tap-left ns3
```

```
sudo docker run -it --rm --cap-add=NET_ADMIN --device=/dev/net/tun --net ns3_net --name tap-right ns3
```
