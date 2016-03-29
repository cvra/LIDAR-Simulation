#!/usr/bin/env bash

gazebo worlds/eurobot2016.world && ./nodes/build/laserscan && ./nodes/build/robotpose
