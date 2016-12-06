## environments.bitesize


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
    tests:
    ## Environment level tests
      - name: Account Create Windows 7 Firefox
        repository: ssh://git@somerepo.com/occ/console-testautomation.git
        branch: dev
        commands:
          - shell: mvn --settings ./settings.xml verify -e -Dmaven.javadoc.skip=true -Dsuite=account-create-tests -Ddriverurl=http://some_url/new_endpoint -Dbrowser=firefox -Dversion=68.0 -Dplatform="Windows 7" -Dconfigfiles="test-users/auto-browser-test1.xml,dev-con.xml,jenkins-sample-settings.xml" -X
```
