#  Working with Jenkins  

Bitesize PaaS uses a custom workflow to build and deploy
applications. The whole CI/CD pipeline is built using just three
manifest files, which have very distinctive roles in the build
process. First, let’s define some terms to understand what exactly they
mean in our context:


| Term | Definition |
| --- | :--- |
| *Component* | Individual code repository necessary to create an Application. Your application will have one or more internal components. |
| *Application*      | Artifacts as a single Artifact necessary to create a running instance (a collection of components). Application includes the full stack required to run an instance. |
| *Build* | Process that outputs artifacts (Debian Package, Docker Image, etc…) |
| *Job* | An instance (success or fail) of a Build |
| *Build Definition* | What actions need to be executed to generate the output artifact. |
| *Job Definition* | Specifics related to the Job, generally Version Number, Tags, .... |
| *Build Dependency* | An tool or utility necessary to create a Component Artifact. |
| *Service* | Instance (or multiple grouped instances in HA mode) of  running application. |
| *Environment* | Collection of services, grouped together to represent a fully working application stack. |


<br><br>
Given this, the three files mentioned above are the following:<br>

-   **build.bitesize** - defines how to build one or more components
-   **application.bitesize** - defines how to build one or more
    applications using required components (mentioned above) and
    external dependencies
-   **environments.bitesize** - defines how to layout environments,
    which applications (services) to run in them, what tests to run
    against your applications and the method to deploy applications.
    Builds out the whole CI/CD pipeline

Your project will store these files in a git repository. It can be
either your source repository, or (more commonly) a repository dedicated
just to managing these three files. This git repository will be used as
an input to the pipeline generation process.
 
If you don't already have a namespace/project in bitesize, this will
need to be created first. Reach out to a Bitesize Core Team member to
get started or @[bitesize-operations@pearson.com](bitesize-operations@pearson.com)
<br>

### Deploying your applications continuously

Build process tracks your application's dependencies by using versioned
packages. Normally, in `application.bitesize` you will have local versioned
dependencies listed. This guards you from promoting unstable versions
through the pipeline, but it also introduces challenges in continuous
deployment process, because it essentially means that you have to maintain
these package dependencies manually. That prevents you from promoting
commited code automatically -- you also need to bump your package version.

In newer versions of our deployment pipeline, there is a solution that
allows you to both version your packages and promote your changes without
bumping package version. For this, we're using iteration suffix in versioning
scheme. All you need to do is to make sure that artifacts built with
`build.bitesize` are unique with each build. Usually, if your project uses
`fpm` to package component, it means applying unique `--iteration` option.
So your build command would change from this:

```
shell: fpm -s dir -t deb -n appname -v 1.0 --prefix /app -C build .
```

to this:

```
shell: fpm -s dir -t deb -n appname -v 1.0 --iteration $(date "+%Y%m%d%H%M%S") -C build/ --prefix /app .
```

`--iteration` option in the example above will append date with time to your
package version (e.g. package vesion will become `1.0-201608181248`). Your
application's docker image will be versioned accordingly and will be tagged
with `1.0`, `1.0-201608181250`, `latest` tags (date and time will not be
aligned with the .deb package version).

In the future deployment pipeline versions we are planning to apply
application image tags relating to your environments as well (so you could
have references to latest and one previous build by tags `1.0-dev-current`
and `1.0-prd-previous`).


### Common Gotchas
1. *Jenks&Crash* - When providing the wrong apt-get package, your Jenkins container will crash and restart.
`apt-get update` - You must explicitly perform an update when installing apt packages.

```
dependencies:
  - type: debian-package
    package: update
```
<br>

### Getting Started with .bitesize files

The first file you will want to configure is build.bitesize. It defines
how to build your components and produce artifacts, that will be
consumed further in the process. Currently we only support Debian
packages as build output, but in the future we plan to add support for a
number of different artifacts. Below is a sample build.bitesize:


**build.bitesize**

```
 
project: example               # Mandatory, unique within PaaS
components:
  - name: static-content       # Component name
    version: 1.1.1             # Component version
    build_runtime: ubuntu14.04 # Currently not used, planned support (base runtime, e.g. ubuntu14.04-oracle-java-7)
    os: linux                  # Currently not used
    dependencies:              # Dependencies required to build your project
      - type: gem-package      # Supported types: gem-package, debian-package
        package: fpm           # Package name
        version: 0.0.1         # (Optional) version. Default: latest

    repository:                # Git repository and branch. Only ssh protocol is supported
      git: git@bitbucket.org:pearson-techops/sample-app.git
      branch: master
    build:                     # List of build commands to output artifact
      - shell: "rm -f *.deb"
      - shell: fpm -s dir -t deb -n static-content -v 1.1.1 -C src --prefix /usr/share/nginx/html .
    artifacts:
      - location: "*.deb”      # Location of artifacts to publish/archive
        type: debian-package # Currently not used, planned support
```

 

application.bitesize is the next step in the CI/CD process. It
assembles your components (built with build.bitesize) and your
application dependencies (e.g. specific php modules) into a single
application that can be run as a service.

**application.bitesize**

```
project: hed-console
applications:
  - name: console
    runtime: 'ubuntu-nodejs:0.2.1'
    version: 3.0.36
    dependencies:
      - name: console-ui      # package name
        type: debian-package  # type
        origin:
          build: console-ui   # specifies job which produced this package
        version: 3.0.37
      - name: random-package
        type: debian-package
        version: 3.0.32
    command: node /app/console-server/server --LOG.MODE=json --WEB.WEB_ROOT=../console-ui/dist
  - name: mongo3x-provision
    runtime: 'ubuntu-mongo3x:1.0'
    version: 1.0.1
    dependencies:
      - name: mongo3x-provision
        type: debian-package
        origin:
          build: mongo3x-provision
        version: 1.0.1
    command: 'mongo_prov &'
```
 
Although most of the options in application.bitesize are
self-explanatory, one thing to note is dependencies block. This block
lists your application dependencies, which could be either external or
internal. Internal dependencies are the components you have built with
build.bitesize. In the example above, console application has a
dependency on component 'console-ui' and it's artifact can be found in
the job 'console-ui'.

A single job can produce multiple artifacts that have different names. If
your application produces 'random-package-static' debian package as a
part of 'random-package' job, you will set name property to
'random-package-static' and origin build property to 'random-package' in
application.bitesize definition.

External dependencies can be installed either by direct url (will not
fetch package dependencies) to the package, or by specifying it's name
that can be retrieved from repository:

```
dependencies:
  - name: sample-dep
    location: http://some.external.ul/sample-dep_1.1.1.x86.deb
  - name: another-dep
    repository: https://repository_url.com/ubuntu # Full repository URL
    repository_key: SIn29Xkq82                    # repository's GPG-key
```

Your application progresses through environments, specified in
environments.bitesize file sequentially, top to bottom. Currently it
automatically triggers deployment to the downstream environment once
tests for an environment pass (e.g. development deploy → development
tests → staging deploy).

**environments.bitesize**

```
project: hed-console
environments:
  - name: Development
    namespace: console-test
    next_environment: Staging
    deployment:
      method: rolling-upgrade
    services:
      - name: mongo3x-provision           # Service name
        external_url: mongod3x.console.io # External HTTP(s) endpoint
        ssl: true # Serve HTTP/HTTPS on a load balancer
        port: 27017
        env:   # List of environment variables your service needs to consume
          - name: MONGO_DBNAME
            value: SOME_DB_NAME
          - name: MONGO_DB_ADMIN_USER
            value: SOME_ADMIN_USER
          - name: MONGO_DB_ADMIN_PASS
            value: SOME_DB_ADMIN_PASSWORD
          - name: MONGO_DBUSER
            value: console-user
          - name: MONGO_DBPASS
            value: SOME_DB_PASSWORD
        tests: null                      # Tests
      - name: console
        external_url: console-origin.dev-prsn.com
        ssl: true
        port: 8080
        env:
          - name: ENV_CONFIG
            value: paas
          - name: NODE_ENV
            value: dev
        tests: null
    tests: null
```
<br>
### Add DataBases to environments.bitesize (Mongo, MySQL)

These are defined the same way as normal services are, with the
exception of having "type" field. Type field indicates that this is an
external resource and manages it accordingly. Currently only "create"
action is supported (i.e. you will not be able to change the service
params once it is created). Below is a service snippet (goes to
environments.bitesize services definition):

**Note: These are persistent production scale databases. The Bitesize
team requests you use non-persistent databases for Dev environments and POCs
that will not be long lived.**

```
   services:
      - type: mysql  # mysql or mongo currently
        name: db     # unique name (within environment namespace) of your service
        version: 5.6 # resource version -- e.g. 5.6 for MySQL 5.6
```
```
   services:
      - type: mongo
        name: mongodb
```
<br>
Databases for Dev environments and POCs:
* [Add Mongo service to namespace](/deployment-pipeline/howto-add-mongo-service-in-namespace.html)
* [Add Cassandra service to namespace](/deployment-pipeline/howto-add-cassandra-service-in-namespace.html)


<br>
### Adding persistent volumes

Since Jenkins 3.4.28 release you can attach persistent volumes to your pods using
`environments.bitesize` file. First, ask Bitesize admin team to create required
volumes for the cluster (this is still administrative task). Specify size, volume
type required (e.g. NFS shared volume, EBS volume for a single pod). Once storage
is present in the cluster and available for your pods, you can attach volumes by
having this definition in `environments.bitesize` service block:

```
  services:
    - name: myservice-with-volume
      ...
      volumes:
        - name: myservice-data
          path: /data
          modes: ReadWriteMany
          size: 20G
```

Volume options:
  * **name** - unique name for the persistent volume. Must match volume name
  created by administrator.
  * **path** - mount path in the pod.
  * **modes** - mount options. Available options - ReadWriteMany,
  ReadOnlyMany, ReadWriteOnce
  * **size** - mounted disk size. Must not exceed volume size that was created
  by administrator

NB: EBS volumes are not available at the present.

### Blue/Green deployments

We have a beta support for Blue/Green deployments.


#### How it works

Every environment has a two sets of services - "blue" and "green" ones. All
endpoints, service names and external URLs have colour suffix to the base name.
E.g. external URL `test.prsn.io` will have `test-blue.prsn.io` and
`test-green.prsn.io` entries.

Every environment has an "active" set of services, controlled by the option in
`environments.bitesize` file. This is the environment to which points external
load balancers. If using the example above, and having "blue" service set as an
active one, `test.prsn.io` will point to the same backend service as
`test-blue.prsn.io`.

When deployment pipeline for the specific environment kicks in, it deploys to
the inactive service set. That is, "green" services will be deployed when active
is set to "blue". After testing is complete, to switch over to "green" environment,
you will need to update `environments.bitesize`.

#### environments.bitesize options

```
  environments:
    - name: dev
      deployment:
        mode: bluegreen # Marks environment as blue/green
        active: blue
```


#### Things to consider

Your application needs to be aware of environment variable differences. E.g.,
if your service pod refers to another internal service by environment variable
`${SVC_ANOTHER_SERVICE}`, now you will have to differentiate between "blue" and
"green" services by using `${SVC_ANOTHER_SERVICE_BLUE}` and
`${SVC_ANOTHER_SERVICE_GREEN}`.

Automatic tests will also need to be aware of these changes. Running tests
against main URL (e.g. `test.prsn.io`) will run them against "active" service set,
which is most probably not the thing you will want to do.

 
