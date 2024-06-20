#!/usr/bin/env bash

docker run -v ./sharedvolume:/mystuff -p 10000:10000 -it --rm yaml_attacker $1
