
A Docker `image` is a lightweight, stand-alone, executable software package that includes everything needed to run a piece of software, including the code, a runtime, libraries, environment variables, and config files.

Images are **just data** identfiable with hashes. Think of them like bootable disks:

<div style="text-align:center"><img src="ubuntu.png" width="200" alt="ubuntu"> <br> f3d495355b4e </div>

Images contain

* Code - The actual code that runs your application.
* Runtime - The runtime environment where your code executes, for instance, Node.js, Python, or Java runtime.
* Libraries - Any libraries or frameworks your code depends on.
* Environment Variables - Configurable parameters your code uses to interact with its environment.
* Config Files - Configuration files which might contain settings or setup information for your application.
* Dependencies - Other resources or files your application needs to run.


## Image Registries

Images may stored locally or hosted on various registries

* [Docker Hub](https://hub.docker.com/) - this is the default registry for pulling/pushing
* [Google Container Registry (GCR)](https://cloud.google.com/artifact-registry)
* [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/)
* [Azure Container Registry (ACR)](https://azure.microsoft.com/en-us/free/container-registry)
