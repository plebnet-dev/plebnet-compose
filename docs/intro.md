# Motivation

Containers are like very thin virtual machines. We summarize the benefits of this approach below

## isolation

* all requirements are self-contained within an os tailored for the app
* no dependency conflicts on the host
* inheritance

## reproducibility

* running the same container years later should produce the same results
* production version should operate similar to development

The same container can be developed on a laptop and deployed to cloud AWS/Google/Azure or decentralzed environments (Start9/Umbrel)

## modularity

apps can consist of multiple containers deployed in concert

* docker compose ([plebnet-playground](https://github.com/PLEBNET-PLAYGROUND/plebnet-playground-docker), [Start-9](https://docs.start9.com/latest/developer-docs/packaging#package-the-service), [Umbrel](https://github.com/getumbrel/umbrel-apps#1-containerizing-the-app-using-docker))
* kubernetes (targets AWS, Google, etc)


## security

Containers provide a low risk way to runing other people's apps

* host explicitly controls what the container has access to (data paths, network, etc)

Note: other containerizing solutions may be more secure than docker

* [Podman](https://podman.io/) A daemon-less architecture allowing you to create containers without root access, potentially enhancing security

* [Buildah](https://buildah.io/blogs/2017/11/02/getting-started-with-buildah.html) allows building Open Container Initiative (OCI) container images without a standalone container runtime or daemon, focusing on creating OCI images without Dockerfiles and without needing root privileges.

