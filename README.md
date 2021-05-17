# BrainPEP
[![Build Status](https://travis-ci.com/eclipse-researchlabs/brain-iot-privacy-control-system-api.svg?branch=main)](https://travis-ci.com/eclipse-researchlabs/brain-iot-privacy-control-system-api)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.9+](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release)

![image](static/BRAIN_IoT_FullLogo_LD.png)

## Overview
BrainPEP is a back-end that offers RESTful API that follows [OpenAPI Specification](https://swagger.io/specification/).
Its scope is to manage the resources associated to Services and Devices interacting with an Identity and Access Manager i.e. [Keycloak](https://www.keycloak.org/).

For more information click the image below

[![image](static/api_logo.png)](https://ipt-services.polito.it/brainpep/docs)

## Installation

### Prerequisites
1.
   Install [Docker](https://www.docker.com/)

2.
   Install [PostgreSql](https://www.postgresql.org/)
   
### Clone the repository
````
$ git clone https://github.com/eclipse-researchlabs/brain-iot-privacy-control-system-api
````

### Configuration
The service assume that you have a Keycloak instance running in a host, so before
proceed with the configuration of the environment variables you must configure Keycloak

#### File .env

Before building the container, set the right values to the settings inside `.env` file.
The settings can be divided in:

   1. *Security variables*
   2. *Admin Keycloak Credentials*
   3. *BrainPEP*
   4. *Database*
   5. *Gunicorn*
   
### Security Variables

|   Variable	   |            Description	                     |  Default   |                  Example                        |
|------------------|---------------------------------------------|------------|-------------------------------------------------|
|   ALGORITHM 	   | Encryption algorithm used for decode JWT    |  "RS256"   |                                                 |
|   AUDIENCE	   | Audience associated to the JWT  	         |  "client"  |                                                 |
|   ISSUER	       | Url of who emitted the token  	             |            |  "https://aut-server.it/auth/realms/Brainiot"   |
| JWS_ALGORITHM    | Encryption algorithm used for decode JWS    |  "RS256"   |                                                 |
| JWS_PRIVATE_KEY  | Private cryptography key used for sign JWS  |            | "MIIEogIBAAKCAQEArVxYJPkQejSCMdgKuuW/STuk...."  |
| JWS_PUBLIC_KEY   | Public cryptography key used for decode JWS |            | "MIIEogIBAAKCAQEArVxYJPkQejSCMdgKuuW/STuk...."  |
| REALM_PUBLIC_KEY | Public cryptography key used for decode JWT |            | "MIIEogIBAAKCAQEArVxYJPkQejSCMdgKuuW/STuk...."  |


## Benchmarks
To ensure the reliability of the system it was run a benchmark simulating
100 gateways sending packets in cascade for 20 seconds in the production environment, and it was
calculated the latency of the responses and if every response was successful.

For more information and stats click the image below

[![image](static/benchmark.png)](https://ipt-services.polito.it/brainpep/static/benchmark.html)


## Release Notes
