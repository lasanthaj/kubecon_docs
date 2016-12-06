# Adding a health check

Bitesize deployment files support healthchecks for your service. This is an
important feature that could ensure your service's operational stability. Based
on them, we configure our monitoring to check if your application is healthy and
also these checks are used for your service's scaling and deployment tasks. It
is recommended that your health checks are executed against the same resource
they are running on - for example, if you have a service SVC_EXAMPLE, that runs
4 instances of itself, don't write a check against global load balanced service,
but rather execute them against local instance (localhost, or local filesystem
access). 

Health checks can be defined `environments.bitesize`. Each service can have an
optional `health_check` block, in which you define command and it's options:

```
...
    services:
    - name: SVC_EXAMPLE
    ...
    health_check:          
        command:
        - /bin/health_script.sh # Path to your script. Exit code 0 means success
        - arg1
        - arg2
        initial_delay: 15 # Time in seconds to wait for a fresh instance to
                          # warmup.
        timeout: 30       # Time in seconds to wait before health check script
                          # times out.
```  