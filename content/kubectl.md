##  Bitesize : How-to: use kubectl  
=============================================================


The Latest Kubectl version can be retrieved like so:
 - Note: Change 'amd64' for 'darwin' if running on Mac
```
#!/bin/bash
echo "Finding latest kubectl..."
LATEST=$(wget -qO- https://github.com/kubernetes/kubernetes/releases/latest | awk -F '[<>]' '/href="\/kubernetes\/kubernetes\/tree\/.*"/ { match($0, "tree/([^\"]+)",a); print a[1] }' | head -1)
echo "Getting $LATEST..."
sudo wget -NP /usr/bin http://storage.googleapis.com/kubernetes-release/release/$LATEST/bin/linux/amd64/kubectl
sudo chmod 755 /usr/bin/kubectl
```

Additional information can be found [here](http://kubernetes.io/docs/user-guide/kubectl/kubectl/)

Apr 28, 2016
 
```
kubectl --namespace=<namespace_name> will be your friend

kubectl --namespace=<namespace_name> get {po,rc,svc,ingress}
```

are all commands you will want to use.

po = pod (the container),

rc = replication controller (the mechanism that asserts the state of
pods),

service = the 'loadbalancer' that makes connection from inside pod
available inside all of namespace, and ingress, to connection to service for which the public ingress routes to, from outside world

 
another useful command for you will be
```
kubectl --namespace=reg get logs --previous &lt;pod\_name&gt;
```

the --previous flag is useful when the pod has died due to an error, and
you want the logs from when it was running

to enter a container (use this sparingly.. only when you need) you can
use
```
kubectl --namespace=reg exec it &lt;pod\_name&gt; /bin/bash
```
 

Editing replication controllers

Sometimes, rarely, you may need to manually bump an image.

use a command like such:

EDITOR="vim" kubectl --namespace=&lt;yournamespace&gt; edit rc
&lt;rc-name&gt;

/image

replace the version of the image with you intended image.

You may also want to dump the config of an svc,rc,po,ns or ingress out
to a yaml file. You can accomplish that like this:

```
kubectl --namespace=&lt;namespace&gt; get -o yaml &lt;model&gt; &gt;
file.yaml
```

You can then hand edit and create
```
kubectl create -f &lt;file&gt;\
```
somewhere else, or in the same namespace, git to vcs - whatever you
want.

This is also handy when debugging thorny syntax errors.


"Why isn't my pod starting?"

Get the pod name:
```
kubectl --namespace=my-namespace get pods
```

Then with the pod name, get the description:

```
kubectl --namespace=my-namespace describe podname-aaaaa
```

The last few lines will describe the error.
