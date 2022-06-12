#!/bin/bash
docker build -t venera .
docker run -d -p 443:443 venera