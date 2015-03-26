.PHONY: rpm-build rpm clean

DOCKER_RPM_IMAGE := docker-rpm-centos6
DOCKER_RPM_MOUNT := -v "$(CURDIR)/rpmbuild:/rpmbuild"
DOCKER_RUN_RPM_DOCKER := docker run --rm -it $(DOCKER_RPM_MOUNT) "$(DOCKER_RPM_IMAGE)"

default: rpm	

clean:
	rm -rf $(CURDIR)/rpmbuild/BUILD
	rm -rf $(CURDIR)/rpmbuild/BUILDROOT
	rm -rf $(CURDIR)/rpmbuild/RPMS
	
tar:
	python pack_docker.py
	
rpm-build:
	docker build -t "$(DOCKER_RPM_IMAGE)" .
		
rpm: clean rpm-build tar
	$(DOCKER_RUN_RPM_DOCKER) rpmbuild -bb /rpmbuild/SPECS/docker-io.spec -D "_topdir /rpmbuild"
