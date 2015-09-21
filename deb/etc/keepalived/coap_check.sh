#!/bin/bash

(echo -ne '\x40\x01\x00\xc1' & sleep 1) | timeout 1 nc -uw 1 $1 $2 | grep -a CoAP > /dev/null || exit 1