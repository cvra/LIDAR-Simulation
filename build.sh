#!/usr/bin/env bash

mkdir -p listener/build
pushd listener/build
PKG_CONFIG_PATH=`rospack find gazebo_ros`/gazebo/lib/pkgconfig cmake .. && make
popd
