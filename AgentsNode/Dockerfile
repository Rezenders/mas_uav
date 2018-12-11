FROM rezenders/jason-ros

## Copy Jason files
COPY uav_agents /uav_agents

#use in development only
COPY jason-ros/rosbridge_agents/rosbridgeArch.java /uav_agents/
WORKDIR /uav_agents

RUN ["/bin/bash","-c","mkdir -p lib && cp /java_rosbridge/target/java_rosbridge-2.0.2-jar-with-dependencies.jar lib/"]

CMD ["bash"]
