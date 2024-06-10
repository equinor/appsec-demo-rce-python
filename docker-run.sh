#!/usr/bin/env bash

docker run -v ./sharedvolume:/myapp -p 9999:9999 -it --rm python34 $1
