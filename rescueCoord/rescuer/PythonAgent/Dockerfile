FROM rezenders/jason-ros

RUN apt-get update && apt-get install -y \
    python-pip \
    && rm -rf /var/lib/apt/lists/

RUN pip install simple-settings


## Copy Agent files
COPY rescuer.py /uav_agents/
COPY r1.py /uav_agents/
COPY r2.py /uav_agents/

WORKDIR /uav_agents/
