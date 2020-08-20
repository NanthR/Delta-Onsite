#!/bin/bash
sudo tcpdump -i any -nn -A src 127.0.0.1 and port 5000 | grep "username"
