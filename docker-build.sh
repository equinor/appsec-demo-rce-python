#!/usr/bin/env bash

set -x

docker build $@ -t python34 .
