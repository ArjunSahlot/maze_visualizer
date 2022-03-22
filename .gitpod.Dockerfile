FROM axonasif/gitpod-workspace-full-vnc:latest

USER root
RUN apt update && install_packages -y \
        tk-dev \
        python3-tk \
        python-tk \
    && apt clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*
RUN pip install -r https://raw.githubusercontent.com/ArjunSahlot/maze_visualizer/main/requirements.txt
