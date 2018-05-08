############ Run this file as root user ###################
export http_proxy="http://edcguest:edcguest@172.31.100.14:3128"
export http_proxy="https://edcguest:edcguest@172.31.100.14:3128"
echo "http_proxy=\"http://edcguest:edcguest@172.31.100.14:3128/\"">> /etc/environment
echo "https_proxy=\"https://edcguest:edcguest@172.31.100.14:3128/\"">> /etc/environment
################ install pip ########################
sudo apt-get -y install python3-pip

################ install PyQt5 ######################
sudo -E pip3 install pyqt5

############## install docker module in python #################
sudo -E pip3 install docker

################ Download Kad file and install ##################
wget https://pypi.python.org/packages/e3/09/fada80a946dfb41c470877a0bb5c15e4e43061dfc77d0b622212c13647f6/kad.py-0.5.6-py3-none-any.whl#md5=a378a9feb12d4d51689e24649ab8d10b
sudo -E pip3 install kad.py-0.5.6-py3-none-any.whl

######################## Install Docker ##################
sudo apt-get -y update
sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get -y update
sudo apt-get -y install docker-ce

############# Proxy setting in Docker  ###################
mkdir -p /etc/systemd/system/docker.service.d
touch /etc/systemd/system/docker.service.d/http-proxy.conf
echo "[Service]
Environment=HTTP_PROXY=http://edcguest:edcguest@172.31.100.14:3128" >> /etc/systemd/system/docker.service.d/http-proxy.conf
echo "[Service]
Environment=HTTPS_PROXY=https://edcguest:edcguest@172.31.100.14:3128" >> /etc/systemd/system/docker.service.d/http-proxy.conf
systemctl daemon-reload
systemctl restart docker


