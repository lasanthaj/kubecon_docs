# application.bitesize

Builds docker image according to application specification. Installs custom
packages built in `build.bitesize` (also other external packages).

```
project: example
applications:
  - name: sample-app
    runtime: nginx
    dependencies:
      - name: static-content
        type: debian-package
        origin:
          build: static-content
        version: 1.1.2
      - name: different-dir
        type: debian-package
        version: 1.1.1
        origin:
          build: static-content
    command: 'nginx -g "daemon off;"'
  - name: another-app
    runtime: nginx
    dependencies:
      - name: another-artifact
        type: debian-package
        origin:
          build: another-artifact
        version: 1.1.2
    command: 'nginx -g "daemon off;"'

```

<br>
## Adding custom start command

Default path on all base images is `/app`. By default, your application will
inherit startup command specified in `runtime` image. To override it, use
`command` instruction:

```
  applications:
    - name: test
      ...
      command: "/app/startup_script.sh"
```
<br>
## Adding application dependencies

In `dependencies` configuration section, you can add custom packages to your
application. These packages will be installed on top of what is provided By
application's `runtime` image. These packages can be something that was built
using `build.bitesize` file or any other external package. Currently supported
package types are:

  * `debian-package`
  * `gem-package`
  * `pip-package`

<br>
## List of supported runtime images (base images) can be found [here](http://kubecon.dev-bite.io/base-images.html)
