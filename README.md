# rpm-podman-plugins

This repository provides a spec file for building the dnsname plugin ([containers/dnsname](https://github.com/containers/dnsname)) for the podman container engine.

It is based on the spec files provided by the [Kubic project](https://build.opensuse.org/project/show/devel:kubic:libcontainers:stable) which provides updated packages for CentOS 7, 8 and Stream as well, but also updates the podman package.

Using this spec file just the **podman-plugins** is build to be used with the podman package provided in the CentOS 8 AppStream repository.

Builds for this package can be downloaded from my [home project](https://build.opensuse.org/package/show/home:cfelder:CentOS-8/podman-plugins).