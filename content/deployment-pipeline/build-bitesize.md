## build.bitesize

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
