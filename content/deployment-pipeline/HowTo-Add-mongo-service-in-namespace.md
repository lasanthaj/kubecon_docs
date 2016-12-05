##  Bitesize : How-to: Add mongo container to a namespace  

**NOTE - This should be used for dev environments only as mongo is being
provided from within a container with no persisted storage**

<span style="color: red">This is only for Development/POC purposes.</span>

Please excuse the brevity of this documentation. I wanted to get it in
your hands as quickly as possible. As the pressure is on for this to be
delivered, it's not the most elegant solution.
This process is responsible for provisioning and launching mongo in the
container.

For mongo2x == 2.4.10, use mongo2x runtime as spelled out below. For
mongo3x, == 3.2.4 , replace all instances below of mongo2x for mongo3x

NOTE - mongo3x and mongo2x are expecting different sets of environment
variables. See below for respective example versions of
environments.bitesize.

**application.bitesize**

```
project:
applications:
  - name: mongo2x-provision
    runtime: ubuntu-mongo2x:1.0 #Runtime and version
    version: 1. #Application version
    dependencies:
      - name: mongo2x-provision
        type: debian-package
        origin:
          build: mongo2x-provision
        version: 1.
    command: mongo_prov &
```


**build.bitesize**

```
  - name: mongo2x-provision
    version: 1.
    os: linux
    dependencies:
      - type: gem-package
        package: fpm
      - type: debian-package
        package: rlwrap
      - type: debian-package
        package: build-essential
    repository:
      git: https://github.com/lv0/mongod_prov.git
      branch: master
    build:
      - shell: fpm -s dir -t deb -n mongo2x-provision -x "**/.git/**" -v  --prefix /usr/local/bin .
    artifacts:
      - location: '*.deb'
```

**environments.bitesize (mongo2x)**

```
environments:
  - name: Development
    namespace:
    next_environment: Staging
    deployment:
      method: rolling-upgrade
    services:
      - name: mongo2x-provision
        #application: console #Optional, if name === application no need
        external_url: mongod2x..io
        port: 27017
        env:
          - name: MONGO_DB_1
            value:
          - name: MONGO_DB_2
            value:
          - name: MONGO_DB_3
            value:
          - name: MONGO_ADMIN_USER
            value:
          - name: MONGO_ADMIN_PASS
            value:
          - name: MONGO_DB_ADMIN_USER
            value:
          - name: MONGO_DB_ADMIN_PASS
            value:
          - name: MONGO_RW_USER
            value:
          - name: MONGO_RW_PASS
            value:
          - name: MONGO_RO_USER
            value:
          - name: MONGO_RO_PASS
            value:
```

**environments.bitesize (mongo3x)**

```
environments:
  - name: Development
    namespace:
    next_environment: QA
    deployment:
      method: rolling-upgrade
    services:
      - name: mongo3x-provision
        external_url: mongod3x..io
        port: 27017
        env:
          - name: MONGO_DBNAME
            value:
          - name: MONGO_DB_ADMIN_USER
            value:
          - name: MONGO_DB_ADMIN_PASS
            value:
          - name: MONGO_DBUSER
            value:
          - name: MONGO_DBPASS
            value:
```
