#!/bin/bash
docker image rm fec-python
docker build ./ -t fec-python

