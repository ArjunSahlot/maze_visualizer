FROM gitpod/workspace-full-vnc

USER gitpod

RUN sudo apt update && sudo apt install -y tk-dev