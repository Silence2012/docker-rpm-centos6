## About

This is Dockerfile/spec/patches to create Docker RPM for CentOS6.

Some parts are forked from https://github.com/maebashi/docker-rpm-el6. Many thanks.

## Building

1. Get the docker source code(https://github.com/docker/docker).
2. Put docker-rpm-centos6 into docker/hack(project).
3. cd hack/docker-rpm-centos6
4. make
5. The RPM will be created in hack/docker-rpm-centos6/rpmbuild/RPMS.


