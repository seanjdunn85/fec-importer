#!/bin/bash
docker run \
  -dit \
  --name fec-python-running \
  --restart unless-stopped  \
  -v /Users/seandunn/workspace/fec:/usr/src/app  \
  -v /Users/seandunn/Desktop/zips:/data \
  fec-python
