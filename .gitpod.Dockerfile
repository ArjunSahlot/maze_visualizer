FROM gitpod/workspace-full-vnc

RUN sudo install_packages -y \
        tk-dev \
        python3-tk \
        python-tk \
    && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*
RUN pip install -r https://raw.githubusercontent.com/ArjunSahlot/maze_visualizer/main/requirements.txt
