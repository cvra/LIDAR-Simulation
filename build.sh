#!/usr/bin/env bash

mkdir -p nodes/build
pushd nodes/build
cmake ..
make
popd
