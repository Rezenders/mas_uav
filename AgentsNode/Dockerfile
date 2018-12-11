FROM rezenders/jason-ros

RUN ["/bin/bash","-c","mkdir -p /uav_agents/lib && cp /java_rosbridge/target/java_rosbridge-2.0.2-jar-with-dependencies.jar /uav_agents/lib/"]
WORKDIR /uav_agents

## Copy Jason files
COPY uav_agents /uav_agents

COPY jason-ros/rosbridge_agents/rosbridgeArch.java /uav_agents/

CMD ["bash"]
