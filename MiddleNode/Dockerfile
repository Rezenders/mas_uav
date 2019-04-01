FROM rezenders/jason-ros:HwBridge

RUN apt-get update && apt-get install -y \
    ros-melodic-mavros \
    && rm -rf /var/lib/apt/lists/

COPY actions_manifest /jason_ws/src/hw_bridge/src/
COPY perceptions_manifest /jason_ws/src/hw_bridge/src/
WORKDIR /jason_ws/src/hw_bridge/src/
