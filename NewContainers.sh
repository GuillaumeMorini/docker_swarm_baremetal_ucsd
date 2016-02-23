#!/bin/bash
for i in `seq 15`
do
	docker -H=tcp://10.60.7.20:5000 run  -e "HTTP_PROXY=http://173.38.209.13:80/" -e "HTTPS_PROXY=http://173.38.209.13:80/" -e "NO_PROXY=192.168.7.193" -d --net=swarm-network alpine init
done
