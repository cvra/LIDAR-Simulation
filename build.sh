#!/usr/bin/env bash

mkdir -p listener/build
pushd listener/build
cmake ..
make
popd
