#!/usr/bin/env python
# -*- coding: utf-8 -*-

# prompts
ubuntu_pass = raw_input("Enter password for 'ubuntu' user: ")

# scripts
PRIMARY_OS = 'Ubuntu-14.04'
PRIMARY = '''#!/bin/sh
#
FQDN="{{fqdn}}"

export DEBIAN_FRONTEND=noninteractive

# locale
sudo locale-gen en_US.UTF-8

# /etc/hostname - /etc/hosts
echo $FQDN > /etc/hostname
service hostname restart
sleep 5

# uncomment either docker os release or docker specific release section

# docker os release
#curl -sSL https://get.docker.com/ | sh

# install 1.12
apt-get update
apt-get -y install apt-transport-https ca-certificates
apt-get -y install curl
curl -fsSL https://yum.dockerproject.org/gpg | sudo apt-key add -
apt-get -y install software-properties-common
add-apt-repository "deb https://apt.dockerproject.org/repo ubuntu-trusty main"
apt-get update
apt-get -y install docker-engine=1.12.6-0~ubuntu-trusty
# we need to add a hold here so that upgrade does not upgrade docker too
apt-mark hold docker-engine


usermod -aG docker ubuntu

# updates
apt-get update
apt-get -y upgrade
apt-get install -y git tree jq linux-image-extra-4.2.0-30-generic linux-image-4.2.0-30-generic

# compose
curl -L https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# password authentication
echo ubuntu:{0} | chpasswd
sed -i 's|[#]*PasswordAuthentication no|PasswordAuthentication yes|g' /etc/ssh/sshd_config
service ssh restart

# cleanup.sh
# ==========
cat >/home/ubuntu/cleanup.sh <<EOL
#!/bin/bash

sudo service docker stop

# /etc/default/docker
sudo rm /etc/default/docker
sudo cp /etc/default/docker.bak /etc/default/docker

unset -v DOCKER_HOST
unset -v DOCKER_OPTS
unset -v DOCKER_CONTENT_TRUST

sudo rm -r /var/lib/docker
sudo service docker start
EOL

chmod +x /home/ubuntu/cleanup.sh
chown ubuntu:ubuntu /home/ubuntu/cleanup.sh

service docker stop
rm -r /var/lib/docker
rm /etc/docker/key.json
cp /etc/default/docker /etc/default/docker.bak

{{dinfo}}
reboot
'''.format(ubuntu_pass)


# Script to use if launching from a custom lab AMI image
AMIBUILD = '''#!/bin/sh
#
FQDN="{{fqdn}}"

# /etc/hostname - /etc/hosts
sed -i "1 c\\127.0.0.1 $FQDN localhost" /etc/hosts
echo $FQDN > /etc/hostname
service hostname restart
sleep 5

# password authentication
echo ubuntu:{0} | chpasswd
sed -i 's|[#]*PasswordAuthentication no|PasswordAuthentication yes|g' /etc/ssh/sshd_config
service ssh restart

service docker stop
rm -r /var/lib/docker
rm /etc/docker/key.json

{{dinfo}}
reboot
'''.format(ubuntu_pass)


def pre_process():
    """Executed before launching instances in AWS"""
    pass

def post_process():
    """Executed after launching instances in AWS"""
    pass
