FROM rezenders/jason-ros

## Copy Jason files
COPY uav_agents /uav_agents

# Dev
#COPY jason-ros/rosjava_agents/src/java/* /uav_agents/src/java/

WORKDIR /uav_agents/
RUN ["/bin/bash", "-c","gradle build"]

CMD ["bash"]
