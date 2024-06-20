#!/usr/bin/env bash

set -x

docker build $@ -t yaml_attacker .
