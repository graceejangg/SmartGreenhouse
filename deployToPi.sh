#!/bin/bash

scp -r garden/ pi:~/

echo "Starting mainPi.py on Raspberry Pi"
ssh -t pi "python3 ~/garden/mainPi.py"