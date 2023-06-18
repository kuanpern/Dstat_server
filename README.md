## DSTAT Server
Cloud provider agnostic Linux VM resource monitoring and alert system

Note 2023-06-18: This repository is not maintained anymore. It is encouraged to use container solution e.g. OpenTelemetry, Prometheus etc for this use case.

### Introduction
This package provides a simple server/receiver system to query the current and historical usage of system resource (CPU, RAM, DISK) for Linux virtual machines. The  package is a simple wrapper for psutil and dstat program.

### Packages
#### Receiver
A dashboard interface shared with all backend dstat resource server. It currently support 3 server modes:

 * Generic
     * interface to generic backend server
 * AWS EC2
     * interface to AWS cloudwatcher API
 * Azure VM
     * interface to Azure VM usage statistic API
#### Server
 * Generic servers
     * "generic" is applicable for linux server, as long as Docker is supported.
     * note that individual cloud service provider could provide API end-points for the same functionality. In such case the receivers provide interfaces to these end-points and server needs not to be installed.

### Installation
See server/README.md for backend server installation guide.
