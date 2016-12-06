### Working with envconsul
===============================================

Envconsul exports k/v data from Consul and Vault into environment variables,
typically for consumption by applications at runtime.

<br>
[envconsul](https://github.com/hashicorp/envconsul) full documentation.

ACLs
----

You must always suffix your requests with a token as follows:

    ?token=blabla-bla-bla

Example:

    curl -k -X DELETE https://consul.prod-117.prsn.io/v1/kv/console-test/key1?token=blabla-bla-bla

<br>
To find the tokens, look for secrets in the kubernetes config, e.g:

    kubectl get secret pulse-read-write --namespace=pulse -o json

The data must be decoded from base64:

        "data": {

            "pulse-read-write": "Mjk5OWUyYzYtMWQHRS1hMmVhLTg5MkygRfZDk1MzFhN2NhCg=="

    echo "Mjk5OWUyYzYtMWQHRS1hMmVhLTg5MkygRfZDk1MzFhN2NhCg==" | base64 -d

When consumed as a secret through kubernetes this is not necessary.
<br><br>

envconsul
---------

```
envconsul -consul=consul.prod-117.prsn.io -ssl -ssl-verify=false -prefix=console-test
```

This will expose the k/v data
under [https://consul.prod-117.prsn.io/v1/kv/](https://consul.mdev.prsn.io/v1/kv/key1) [console-test/](https://consul.mdev.prsn.io/v1/kv/key1)
as environment variables for the process &lt;some\_daemon\_cmd&gt;,
which can refer to the value in **key1**, for example, as **\$key1**


For processes running inside Kubernetes, the envconsul command would
look like this:

    envconsul -consul=consul.kube-system.svc.cluster.local:8543 -ssl -ssl-verify=false -prefix=console-test

### WebUI

Lastly, the k/v store is accessible through the WebUI here:

Note, however, this should not be available in production.

### Simple python example (originally intended for use in StackStorm)

The following is an example of using python requests to interact with
the consul REST API. It is both robust and performant. Note that
self.setup\['consul\_api\_url'\] here would be
[https://consul.prod-117.prsn.io/v1](https://consul.prod-117.prsn.io/ui/#/prod-117/kv/) in our examples.

    import httplib

    import requests

     

    from st2actions.runners.pythonrunner import Action

     

    class ConsulAction(Action):

     

        def __init__(self, config):

            super(ConsulAction, self).__init__(config)

            self.setup = config['setup']

     

        def consul_get_kv(self, key, recurse=False):

            url = self.setup['consul_api_url']

            url = url + '/kv/' + key

            if recurse:

              recurse = 'recurse'

            else

              recurse = None

            response = requests.get(url=url, data=recurse)

     

            return self._validate_result(response=response)    

     

        def consul_put_kv(self, key, value):

            url = self.setup['consul_api_url']

            url = url + '/kv/' + key

            response = requests.put(url=url, data=value)

     

            return self._validate_result(response=response)    

     

        def consul_del_kv(self, key, recurse=False):

            url = self.setup['consul_api_url']

            url = url + '/kv/' + key

            if recurse:

              recurse = 'recurse'

            else

              recurse = None

            response = requests.delete(url=url, data=recurse)

     

            return self._validate_result(response=response)    

     

        def _validate_result(self, response):

            if response.status_code in [httplib.OK, httplib.CREATED]:

                status = 'ok'

                error = None

            else:

                status = 'failure'

                error = response.text

     

            result = {

                'status_code': response.status_code,

                'status': status,

                'error': error

            }

     

            if error:

                result['error'] = error

     

            return result
