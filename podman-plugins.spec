%global with_devel 0
%global with_bundled 1
%global with_check 0
%global with_unit_test 0

%if 0%{?fedora} || 0%{?centos} >= 8
#### DO NOT REMOVE - NEEDED FOR CENTOS
%bcond_without varlink
%else
%bcond_with varlink
%endif

%if 0%{?fedora}
%global with_debug 1
%else
%global with_debug 0
%endif

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) GO111MODULE=off go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld '" -a -v -x %{?**};
%endif
%define gogenerate go generate

%define provider github
%define provider_tld com
%define project containers

%define repo_plugins dnsname
# https://github.com/containers/libpod
%define import_path_plugins %{provider}.%{provider_tld}/%{project}/%{repo_plugins}
%define git_plugins https://github.com/containers/dnsname
%define commit_plugins f5af33dedcfc5e707e5560baa4a72f8d96a968fe
## this kind of macros if currenlty not supported in download_sources plugin
#%define shortcommit_plugins %(c=%{commit_plugins}; echo ${c:0:7})
%define shortcommit_plugins f5af33d

Name: podman-plugins
%if 0%{?fedora}
Epoch: 2
%else
Epoch: 0
%endif
Version: 1.8.2
Release: 1%{?dist}
Summary: Plugins for podman
License: ASL 2.0
URL: https://%{name}.io/
Source: https://github.com/containers/dnsname/archive/%{commit_plugins}/dnsname-%{shortcommit_plugins}.tar.gz
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: golang
BuildRequires: glibc-devel
BuildRequires: glibc-static
BuildRequires: git
BuildRequires: make
Requires: podman
Requires: dnsmasq

%description
This plugin sets up the use of dnsmasq on a given CNI network so
that Pods can resolve each other by name.  When configured,
the pod and its IP address are added to a network specific hosts file
that dnsmasq will read in.  Similarly, when a pod
is removed from the network, it will remove the entry from the hosts
file.  Each CNI network will have its own dnsmasq instance.

%prep
%setup -n dnsname-%{commit_plugins}

%build
export GO111MODULE=off

mkdir _build
pushd _build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../../ src/%{import_path_plugins}
popd
ln -s vendor src
export GOPATH=$(pwd)/_build:$(pwd)
%gobuild -o bin/dnsname %{import_path_plugins}/plugins/meta/dnsname

%install
%{__make} PREFIX=%{_prefix} DESTDIR=%{buildroot} install

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc {README.md,README_PODMAN.md}
%{_libexecdir}/cni/dnsname
