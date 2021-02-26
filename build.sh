#!/bin/bash

download_link=https://github.com/ArjunSahlot/maze_visualizer/archive/main.zip
temporary_dir=$(mktemp -d) \
&& curl -LO $download_link \
&& unzip -d $temporary_dir main.zip \
&& rm -rf main.zip \
&& mv $temporary_dir/maze_visualizer-main $1/maze_visualizer \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/maze_visualizer[0m"
