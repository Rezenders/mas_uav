FROM rezenders/jason-ros

## Copy Jason files
COPY uav_agents /uav_agents

WORKDIR /uav_agents/
RUN ["/bin/bash", "-c","gradle build"]

CMD ["bash"]
