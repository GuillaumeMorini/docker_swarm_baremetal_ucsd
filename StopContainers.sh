#!/bin/bash
for i in `docker ps -a |grep alpine |awk '{print$1}'`
do
	docker stop $i && docker rm $i
done
