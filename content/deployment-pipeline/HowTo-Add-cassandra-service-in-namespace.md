##  Bitesize : How-to: Add cassandra service inside a namespace  
==========================================================================================

Apr 20, 2016

**NOTE - This should be used for dev environments only as cassandra is
being provided from within a container with no persisted storage**

This is not the most elegant solution, but If you need changes to the
way cassandra is provisioned, please talk with Eric Malloy, or submit a
pull request to  which hosts the
code responsible for provisioning and launching cassandra in the
container.

 

For cassandra == 2.0.9, use cassandra2x runtime as spelled out below.
Standby for cassandra-3 support
<br>

**application.bitesize**

``` {.syntaxhighlighter-pre data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence"}
project:
applications:
  - name: cassandra2x-provision
    runtime: ubuntu-cassandra2x:1.1
    version: 1.0.1
    dependencies:
      - name: cassandra2x-provision
        type: debian-package
        origin:
          build: cassandra2x-provision
        version: 1.0.1
    command: cassandra2x_prov
```

<br>

**build.bitesize**

``` {.syntaxhighlighter-pre data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence"}
project:
components:
  - name: cassandra2x-provision
    version: 1.0.1
    os: linux
    dependencies:
      - type: gem-package
        package: fpm
      - type: debian-package
        package: rlwrap
      - type: debian-package
        package: build-essential
    repository:
      git: https://github.com/lv0/cassandra_prov.git
      branch: master
    build:
      - shell: fpm -s dir -t deb -n cassandra2x-provision -x "**/.git/**" -v 1.0.1 --prefix /usr/local/bin .
    artifacts:
      - location: '*.deb'
```
<br>

**environments.bitesize**

``` {.syntaxhighlighter-pre data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence"}
project:
environments:
  - name: Development
    namespace:
    next_environment: QA
    deployment:
      method: rolling-upgrade
    services:
      - name: cassandra2x-provision
        external_url: cassandra2x..io
        port: 9160
        env:
          - name: C_ADMIN_USER
            value: cassandraUser
          - name: C_ADMIN_PASS
            value: cassandraPassword
```
