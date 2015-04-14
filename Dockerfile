FROM centos:centos6

RUN yum install -y tar git hg rpmdevtools gcc glibc-static device-mapper-devel sqlite-devel
RUN rpm -ivh http://ftp.iij.ad.jp/pub/linux/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN yum install -y pandoc golang go-md2man 
RUN mkdir -p /go