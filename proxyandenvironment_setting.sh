############ Run this file as root user ###################
export http_proxy="http://edcguest:edcguest@172.31.100.14:3128"
export http_proxy="https://edcguest:edcguest@172.31.100.14:3128"
echo "http_proxy=\"http://edcguest:edcguest@172.31.100.14:3128/\"">> /etc/environment
echo "https_proxy=\"https://edcguest:edcguest@172.31.100.14:3128/\"">> /etc/environment
echo "http_proxy=\"http://edcguest:edcguest@172.31.100.14:3128/\"">> /etc/apt/apt.conf
echo "https_proxy=\"https://edcguest:edcguest@172.31.100.14:3128/\"">> /etc/apt/apt.conf

################ install pip ########################
sudo apt-get -y install python3-pip

################ install PyQt5 ######################
sudo -E pip3 install pyqt5

############## install docker module in python #################
sudo -E pip3 install docker

