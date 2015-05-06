# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_rpmconfigdir}/brp-compress

# docker builds in a checksum of dockerinit into docker,
# so stripping the binaries breaks docker
%global debug_package %{nil}

%global import_path github.com/docker/docker
%global commit      39fa2faad2f3d6fa5133de4eb740677202f53ef4
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           docker-io
Version:        1.7.0
Release:        1%{?dist}
Summary:        Automates deployment of containerized applications
License:        ASL 2.0
URL:            http://www.docker.com
# only x86_64 for now: https://github.com/docker/docker/issues/136
ExclusiveArch:  x86_64
Source0:        https://github.com/docker/docker/archive/v%{version}.tar.gz
# though final name for sysconf file is simply 'docker',
# having .sysconfig makes things clear
Source1:        docker.sysconfig
Source2:        docker-storage.sysconfig
# have init script wait up to 5 mins before forcibly terminating docker daemon
# https://github.com/docker/docker/commit/640d2ef6f54d96ac4fc3f0f745cb1e6a35148607
Source3:        docker.sysvinit
#Patch0:         ignore-selinux-if-disabled.patch
BuildRequires:  glibc-static
BuildRequires:  pandoc
# ensure build uses golang 1.2-7 and above
# http://code.google.com/p/go/source/detail?r=a15f344a9efa35ef168c8feaa92a15a1cdc93db5
BuildRequires:  golang >= 1.3.3
# for gorilla/mux and kr/pty https://github.com/dotcloud/docker/pull/5950
#BuildRequires:  golang(github.com/gorilla/mux) >= 0-0.13
#BuildRequires:  golang(github.com/kr/pty) >= 0-0.19
#BuildRequires:  golang(github.com/godbus/dbus)
# for coreos/go-systemd https://github.com/dotcloud/docker/pull/5981
#BuildRequires:  golang(github.com/coreos/go-systemd) >= 2-1
#BuildRequires:  golang(code.google.com/p/go.net/websocket)
#BuildRequires:  golang(code.google.com/p/gosqlite/sqlite3)
# RHBZ#1109039 use syndtr/gocapability >= 0-0.7
#BuildRequires:  golang(github.com/syndtr/gocapability/capability) >= 0-0.7
#BuildRequires:  golang(github.com/docker/libcontainer) >= 1.1.0-10
#BuildRequires:  golang(github.com/tchap/go-patricia/patricia)
BuildRequires:   device-mapper-devel
Requires:        device-mapper-libs >= 1.02.90-1
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(postun):   initscripts
# need xz to work with ubuntu images
# https://bugzilla.redhat.com/show_bug.cgi?id=1045220
Requires:       xz
# https://bugzilla.redhat.com/show_bug.cgi?id=1035436
# this won't be needed for rhel7+
Requires:       bridge-utils
Requires:       lxc

# https://bugzilla.redhat.com/show_bug.cgi?id=1034919
# No longer needed in Fedora because of libcontainer
Requires:       libcgroup

Provides:       lxc-docker = %{version}

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%package devel
BuildRequires:  golang >= 1.2.1-3
Requires:       golang >= 1.2.1-3
Requires:       docker-io-pkg-devel
Summary:        A golang registry for global request variables (source libraries)
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/api) = %{version}-%{release}
Provides:       golang(%{import_path}/api/client) = %{version}-%{release}
Provides:       golang(%{import_path}/api/server) = %{version}-%{release}
#Provides:       golang(%{import_path}/archive) = %{version}-%{release}
#Provides:       golang(%{import_path}/builtins) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib/docker-device-tool) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib/host-integration) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/execdrivers) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/lxc) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native) = %{version}-%{release}
#Provides:       golang(%{import_path}/daemon/execdriver/native/configuration) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native/template) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/aufs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/btrfs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/devmapper) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/graphtest) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/vfs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/bridge) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/ipallocator) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/portallocator) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/portmapper) = %{version}-%{release}
#Provides:       golang(%{import_path}/dockerversion) = %{version}-%{release}
#Provides:       golang(%{import_path}/engine) = %{version}-%{release}
Provides:       golang(%{import_path}/graph) = %{version}-%{release}
Provides:       golang(%{import_path}/image) = %{version}-%{release}
Provides:       golang(%{import_path}/integration) = %{version}-%{release}
Provides:       golang(%{import_path}/integration-cli) = %{version}-%{release}
Provides:       golang(%{import_path}/links) = %{version}-%{release}
Provides:       golang(%{import_path}/nat) = %{version}-%{release}
Provides:       golang(%{import_path}/opts) = %{version}-%{release}
Provides:       golang(%{import_path}/registry) = %{version}-%{release}
Provides:       golang(%{import_path}/runconfig) = %{version}-%{release}
Provides:       golang(%{import_path}/utils) = %{version}-%{release}
Provides:       golang(%{import_path}/utils/broadcastwriter) = %{version}-%{release}
%description devel
This is the source libraries for docker.

%package pkg-devel
BuildRequires:  golang >= 1.2.1-3
Requires:       golang >= 1.2.1-3
Summary:        A golang registry for global request variables (source libraries)
Provides:       golang(%{import_path}/pkg/graphdb) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/iptables) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/listenbuffer) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mflag) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mflag/example) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mount) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/namesgenerator) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/networkfs/etchosts) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/networkfs/resolvconf) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/proxy) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/signal) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/symlink) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/sysinfo) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/system) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/systemd) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/tailfile) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/term) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/testutils) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/truncindex) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/units) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/user) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/version) = %{version}-%{release}

%description pkg-devel
These source librariees are provided by docker, but are independent of docker specific logic.
The import paths of %{import_path}/pkg/...

%prep
%setup -q -n docker-%{version}
mv vendor/src /go
rm -rf vendor
find . -name "*.go" \
        -print |\
        xargs sed -i 's/github.com\/docker\/docker\/vendor\/src\/code.google.com\/p\/go\/src\/pkg\///g'
sed -i 's/go-md2man -in "$FILE" -out/pandoc -s -t man "$FILE" -o/g' docs/man/md2man-all.sh
sed -i 's/\!bash//g' contrib/completion/bash/docker
#%patch0 -p1
#rm daemon/daemon.go.orig

%build
# set up temporary build gopath, and put our directory there
mkdir -p ./_build/src/github.com/docker
ln -s $(pwd) ./_build/src/github.com/docker/docker
ln -s $(pwd)/../libcontainer ./_build/src/github.com/docker/libcontainer
ln -s $(pwd)/../libtrust ./_build/src/github.com/docker/libtrust

export DOCKER_GITCOMMIT="%{shortcommit}/%{version}"
#export DOCKER_BUILDTAGS='selinux'
export GOPATH=$(pwd)/_build:%{gopath}:/go
export DOCKER_BUILDTAGS='exclude_graphdriver_btrfs'

hack/make.sh dynbinary
docs/man/md2man-all.sh
cp contrib/syntax/vim/LICENSE LICENSE-vim-syntax
cp contrib/syntax/vim/README.md README-vim-syntax.md

%install
# install binary
install -d %{buildroot}%{_bindir}
install -p -m 755 bundles/%{version}/dynbinary/docker-%{version} %{buildroot}%{_bindir}/docker

# install dockerinit
install -d %{buildroot}%{_libexecdir}/docker
install -p -m 755 bundles/%{version}/dynbinary/dockerinit-%{version} %{buildroot}%{_libexecdir}/docker/dockerinit

# install manpage
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 docs/man/man1/docker*.1 %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -p -m 644 docs/man/man5/Dockerfile.5 %{buildroot}%{_mandir}/man5

# install bash completion
install -dp %{buildroot}%{_datadir}/bash-completion/completions
install -p -m 644 contrib/completion/bash/docker %{buildroot}%{_datadir}/bash-completion/completions

# install zsh completion
# zsh completion has been upstreamed into docker and
# this will be removed once it enters the zsh rpm
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 contrib/completion/zsh/_docker %{buildroot}%{_datadir}/zsh/site-functions

# install vim syntax highlighting
# (in the process of being upstreamed into vim)
install -d %{buildroot}%{_datadir}/vim/vimfiles/{doc,ftdetect,syntax}
install -p -m 644 contrib/syntax/vim/doc/dockerfile.txt %{buildroot}%{_datadir}/vim/vimfiles/doc
install -p -m 644 contrib/syntax/vim/ftdetect/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -p -m 644 contrib/syntax/vim/syntax/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax

# install udev rules
install -d %{buildroot}%{_sysconfdir}/udev/rules.d
install -p -m 755 contrib/udev/80-docker.rules %{buildroot}%{_sysconfdir}/udev/rules.d

# install storage dir
install -d -m 700 %{buildroot}%{_sharedstatedir}/docker

# install init scripts
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/docker
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/docker-storage
install -d %{buildroot}%{_initddir}
install -p -m 755 %{SOURCE3} %{buildroot}%{_initddir}/docker

# sources
install -d -p %{buildroot}/%{gopath}/src/%{import_path}

for dir in api daemon  graph \
           image links nat opts pkg registry runconfig utils
do
    cp -pav $dir %{buildroot}/%{gopath}/src/%{import_path}/
done

%pre
getent group docker > /dev/null || %{_sbindir}/groupadd -r docker
exit 0

%post
# Only do this on install, don't need to re-add each update
if [ $1 -eq 1 ] ; then
  # install but don't activate
  /sbin/chkconfig --add docker
fi

%preun
# Only perform these tasks when erasing, not during updates
if [ $1 -eq 0 ] ; then
  /sbin/service docker stop >/dev/null 2>&1
  /sbin/chkconfig --del docker
fi

%postun
# Needed only during upgrades
if [ $1 -ge 1 ] ; then
  /sbin/service docker condrestart >/dev/null 2>&1 || :
fi

%posttrans
# This is a dirty hack to clean up old-%preun
# Needed only during upgrades

# Previous releases caused an issue with upgrades and chkconfig. 
# Need to clean it up.
if ! /sbin/chkconfig --list docker >/dev/null 2>&1 ; then
  /sbin/chkconfig --add docker 
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md 
%doc LICENSE-vim-syntax README-vim-syntax.md
%config(noreplace) %{_sysconfdir}/sysconfig/docker
%config(noreplace) %{_sysconfdir}/sysconfig/docker-storage
%{_mandir}/man1/docker*.1.gz
%{_mandir}/man5/Dockerfile.5.gz
%{_bindir}/docker
%dir %{_libexecdir}/docker
%{_libexecdir}/docker/dockerinit
%{_initddir}/docker
%{_datadir}/bash-completion/completions/docker
%{_datadir}/zsh/site-functions/_docker
%dir %{_sharedstatedir}/docker
%{_sysconfdir}/udev/rules.d/80-docker.rules
%{_datadir}/vim/vimfiles/doc/dockerfile.txt
%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
%{_datadir}/vim/vimfiles/syntax/dockerfile.vim

%files devel
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md 
%dir %{gopath}/src/github.com/docker
%dir %{gopath}/src/%{import_path}
%dir %{gopath}/src/%{import_path}/*
%dir %{gopath}/src/%{import_path}/*/*
%dir %{gopath}/src/%{import_path}/*/*/*
%dir %{gopath}/src/%{import_path}/*/*/*/*
#%{gopath}/src/%{import_path}/*/MAINTAINERS
%{gopath}/src/%{import_path}/*/README.md
%{gopath}/src/%{import_path}/*/*.go
%{gopath}/src/%{import_path}/*/*/*.go
#%{gopath}/src/%{import_path}/*/*/MAINTAINERS
%{gopath}/src/%{import_path}/*/*/*/*.go
#%{gopath}/src/%{import_path}/*/*/*/MAINTAINERS
%{gopath}/src/%{import_path}/*/*/*/README.md
%{gopath}/src/%{import_path}/*/*/*/*/*.go

%files pkg-devel
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md 
%dir %{gopath}/src/github.com/docker
%dir %{gopath}/src/%{import_path}
%dir %{gopath}/src/%{import_path}/pkg
%dir %{gopath}/src/%{import_path}/pkg/*
%dir %{gopath}/src/%{import_path}/pkg/*/*
%dir %{gopath}/src/%{import_path}/pkg/*/*/*
%dir %{gopath}/src/%{import_path}/pkg/*/*/*/*
%{gopath}/src/%{import_path}/pkg/README.md
#%{gopath}/src/%{import_path}/pkg/*/MAINTAINER*
%{gopath}/src/%{import_path}/pkg/*/LICENSE
%{gopath}/src/%{import_path}/pkg/*/README.md
%{gopath}/src/%{import_path}/pkg/*/*.go
%{gopath}/src/%{import_path}/pkg/*/*/*.tar
%{gopath}/src/%{import_path}/pkg/*/*/*.go
%{gopath}/src/%{import_path}/pkg/*/*/*/json
%{gopath}/src/%{import_path}/pkg/*/*/*/*.tar
%{gopath}/src/%{import_path}/pkg/symlink/*.go

%changelog
* Thu Oct 09 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.2.0-3
- Resolves: rhbz#1139415 - correct path for bash completion
    /usr/share/bash-completion/completions
- sysvinit script update as per upstream commit 
    640d2ef6f54d96ac4fc3f0f745cb1e6a35148607 
- don't own dirs for vim highlighting, bash completion and udev

