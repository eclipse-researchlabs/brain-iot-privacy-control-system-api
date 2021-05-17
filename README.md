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

   1. *Security*
   2. *Admin Keycloak Credentials*
   3. *BrainPEP*
   4. *Database*
   5. *Gunicorn*
   
#### Security

|   Variable	   |            Description	                     |  Default   |                  Example                        |
|------------------|---------------------------------------------|------------|-------------------------------------------------|
|   ALGORITHM 	   | Encryption algorithm used for decode JWT    |  "RS256"   |                                                 |
|   AUDIENCE	   | Audience associated to the JWT  	         |  "client"  |                                                 |
|   ISSUER	       | Url of who emitted the token  	             |            |  "https://aut-server.it/auth/realms/Brainiot"   |
| JWS_ALGORITHM    | Encryption algorithm used for decode JWS    |  "RS256"   |                                                 |
| JWS_PRIVATE_KEY  | Private cryptography key used for sign JWS  |            | "MIIEogIBAAKCAQEArVxYJPkQejSCMdgKuuW/STuk...."  |
| JWS_PUBLIC_KEY   | Public cryptography key used for decode JWS |            | "MIIEogIBAAKCAQEArVxYJPkQejSCMdgKuuW/STuk...."  |
| REALM_PUBLIC_KEY | Public cryptography key used for decode JWT |            | "MIIEogIBAAKCAQEArVxYJPkQejSCMdgKuuW/STuk...."  |

#### Admin Keycloak Credentials

|   Variable	          |            Description	                                                   |     Example                                                              |
|-------------------------|----------------------------------------------------------------------------|--------------------------------------------------------------------------|
| ADMIN_CLIENT_ID         | Identifier of keycloak administrator                                       |                                                                          |
| ADMIN_CLIENT_SECRET     | Secret associated to the administrator  	                               | "my super secret"                                                        |
| ADMIN_GRANT_TYPE	      | Typology of grant associated to the administrator                          | "password"                                                               |
| ADMIN_PASSWORD          | Password associated to the administrator                                   | "super_secret"                                                           |
| ADMIN_TOKEN_REQUEST_URL | Url to request a token for the administrator (must be in the master realm) | "http://auth-server.it/auth/realms/master/protocol/openid-connect/token" |
| ADMIN_USERNAME          | Administrator username                                                     | "brainadmin"                                                             |

#### BrainPEP

|   Variable	             |            Description	                                                  |     Example                                                                        |
|----------------------------|----------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| CLIENT_ID                  | Identifier of brainpep client on keycloak                                  |                                                                                    |
| CLIENT_GRANT_TYPE          | Typology of grant associated to the brainpep                               | "password"                                                                         |
| CLIENT_SECRET	             | Secret associated to brainpep  (it's an uudv4 given by keycloak)           | "6209377f-589e-439b-8278-ccd2965fb304"                                             |
| CLIENT_PASSWORD            | Password associated to brainpep                                            | "super_secret"                                                                     |
| CLIENT_TOKEN_REQUEST_URL   | Url to request a token for brainpep (must be in brainiot realm)            | "http://auth-server.it/auth/realms/Brainiot/protocol/openid-connect/token"         |
| RESOURCE_REQUEST_URL       | Url to interact with the resources associated to brainpep                  | "http://auth-server.it/auth/realms/Brainiot/authz/protection/resource_set"         |
| POLICY_REQUEST_URL         | Url to interact with keycloak to store the device policies in uud4 format  | "http://auth-server.it/auth/admin/realms/Brainiot/clients/{CLIENT_SECRET}/roles"   |
| USER_ATTRIBUTE_REQUEST_URL | Url to set user attributes on keycloak                                     | "http://auth-server.it/auth/admin/realms/Brainiot/users"                           |

## Benchmarks
To ensure the reliability of the system it was run a benchmark simulating
100 gateways sending packets in cascade for 20 seconds in the production environment, and it was
calculated the latency of the responses and if every response was successful.

For more information and stats click the image below

[![image](static/benchmark.png)](https://ipt-services.polito.it/brainpep/static/benchmark.html)


## Release Notes
