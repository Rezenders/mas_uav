FROM rezenders/jason-ros:HwBridge

RUN apt-get update && apt-get install -y \
    ros-melodic-mavros \
    && rm -rf /var/lib/apt/lists/

COPY actions_manifest /HwBridge/
COPY perceptions_manifest /HwBridge/
