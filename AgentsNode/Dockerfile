FROM rezenders/jason-ros:HwBridge

## Copy Jason files
COPY uav_agents /uav_agents

# Dev
#COPY jason-ros/rosjava_agents/src/java/* /uav_agents/src/java/

# Production
RUN ["/bin/bash", "-c","mkdir -p /uav_agents/lib && cp /rosjava_agents/lib/* /uav_agents/lib/"]

WORKDIR /uav_agents/
RUN ["/bin/bash", "-c","gradle build"]

CMD ["bash"]
