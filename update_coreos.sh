#!/bin/bash

export http_proxy=http://proxy-wsa.esl.cisco.com:80/
export https_proxy=http://proxy-wsa.esl.cisco.com:80/
curl -o /opt/cnsaroot/images/CoreOS/coreos/vmlinuz http://alpha.release.core-os.net/amd64-usr/current/coreos_production_pxe.vmlinuz
curl -o /opt/cnsaroot/images/CoreOS/coreos/cpio.gz http://alpha.release.core-os.net/amd64-usr/current/coreos_production_pxe_image.cpio.gz

