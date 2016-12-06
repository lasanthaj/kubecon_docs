## Working with Consul
========================================================================================

### Introduction
----

[Consul](https://www.consul.io/intro/) includes a robust
[k/v
store](https://www.consul.io/intro/getting-started/kv.html)
that can be queried/updated via a number of methods.

<br>
Quick Commands:

##### ADD/PUT new value to Consul:
    $ curl -k -X PUT -d 'value1' https://consul.use-prod.prsn.io/v1/kv/console-test/key1

    $ curl -k -X PUT -d 'subvalue1' https://consul.use-prod.prsn.io/v1/kv/console-test/key1/subkey1


##### DELETE values from Consul:
    $ curl -k -X DELETE https://consul.use-prod.prsn.io/v1/kv/console-test/key1

    $ curl -k -X DELETE https://consul.use-prod.prsn.io/v1/kv/console-test/key1?recurse


You should get a simple response 'true' to all the above.



##### GET values from Consul:
    $ curl -k https://consul.use-prod.prsn.io/v1/kv/console-test/key1
    [{"CreateIndex":6100,"ModifyIndex":6100,"LockIndex":0,"Key":"console-test/key1","Flags":0,"Value":"dmFsdWUx"}]

Notice the response is a base64 encoded string. To decode it, run something like:

    $ echo "dmFsdWUx" | base64 -d

    value1


##### You can also use [envconsul](https://github.com/hashicorp/envconsul). A much easier method of consuming key/values which is used in your containers to retrieve data.


<br>

### ACLs
----

ACLs are an important security consideration which is used heavily especially in production.

When ACLs are enabled, suffix the token as follows:

    curl -k -X DELETE https://consul.use-prod.prsn.io/v1/kv/console-test/key1?token=blabla-bla-bla


To find the tokens, look for secrets in the kubernetes config, e.g:

    kubectl get secret pulse-read-write --namespace=pulse -o json


The data must be decoded from base64:

        "data": {

            "pulse-read-write": "Mjk5OWUyYzYtMWQHRS1hMmVhLTg5MkygRfZDk1MzFhN2NhCg=="

    echo "Mjk5OWUyYzYtMWQHRS1hMmVhLTg5MkygRfZDk1MzFhN2NhCg==" | base64 -d


When consumed as a secret through kubernetes this is not necessary.


### envconsul
---------

Envconsul exports k/v data from consul into environment variables,
typically for consumption by applications at runtime.

```
envconsul -consul=consul.use-prod.prsn.io -ssl -ssl-verify=false -prefix=console-test
```

This will expose the k/v data
under [https://consul.use-prod.prsn.io/v1/kv/](https://consul.mdev.prsn.io/v1/kv/key1)[console-test/](https://consul.mdev.prsn.io/v1/kv/key1)
as environment variables for the process &lt;some\_daemon\_cmd&gt;,
which can refer to the value in **key1**, for example, as **$key1**


For processes running inside Kubernetes, the envconsul command would
look like this:

    envconsul -consul=consul.kube-system.svc.cluster.local:8543 -ssl -ssl-verify=false -prefix=console-test


### Simple python example (originally intended for use in StackStorm)

The following is an example of using python requests to interact with
the consul REST API. It is both robust and performant. Note that
self.setup\['consul\_api\_url'\] here would be
[https://consul.use-prod.prsn.io/v1](https://consul.use-prod.prsn.io/ui/#/use-prod/kv/)
in our examples.

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



 

Last Modified Michael Ward on Aug 1, 2016
 
