##  Working with Kafka
=====================================================================================

Background
----------

<br>

The bitesize PaaS uses Kafka to store container logs. It is the best location to pull log events into your central logging platform.

<b> Key things to remember: </b>

  0.  **MUST** be on the Pearson network
  1.  Logs for each namespaces are stored in separate Kafka topics, which
      name after the logs "namespace" value
  2.  Kafka generate new topics once it receive logs with new
      "namespace"
  3.  Logs stay in Kafka cluster for 3 days/72 hours
  4.  Topics have a maximum retention bytes limit = 107374182400 to prevent
      out of storage by periodically meaningless logs
  5.  Rest API endpoint is used to create Kafka Consumers so as to read
      logs from Kafka cluster
  6.  API base url: http://logs.prsn.io
  7.  For additional information on the API: [Kafka Rest API](http://docs.confluent.io/2.0.1/kafka-rest/docs/api.html)
  8.  Sysdig-agent and td-agent(Fluentd) logs are filtered out from the
      cluster since they are providing constantly useless logs


This section introduces the Rest API endpoints to interact with Kafka
cluster.

***NOTE:*** the process described below is workable at the time of
writing but it is expected to change and improve over time.

<br>

Key Terms
----
Topic = a Kafka topic. In our case, analogous to the logs for a given namespace in Kubernetes.

Offset = The numeric position where an event is located in a topic.

<br>


API Commands
------------
### Get /topics

List of Kafka topics (i.e.namespaces).
```
curl "http://logs.prsn.io/topics"
```


Example:
```
$ curl "http://logs.prsn.io/topics"
["_schemas","ciso","contentsandbox","default","demo","escrow","gradebook","hed-console-dev","hed-console-stage","http","hworldmc","image-factory","justiceleague","kube-system","kubernetes","nickpoore","passport","pulse","pulse-dev","pulse-stage","pulse-test","pulseauth","pulseauth-dev","pulseauth-stage","pulseauth-test","readerplus","reg","reg-stage","sample-app","sample-app-dev","strategicreader","sysdigtest","techblog","testprivaterepo"]
```
<br>
### Create a new Consumer
must be done before retrieving logs from Kafka
<br>

### POST /consumers/(string: name)

Create a new consumer instance where **&lt;SOME_NAME&gt;** = the consumer name (arbitrary).
**DON'T CHANGE THE URL! ONLY THE "NAME"**


```
curl -X POST -H "Content-Type: application/vnd.kafka.v1+json" \
--data '{"name": "<SOME_NAME>", "format": "json", "auto.offset.reset": "largest"}' \
http://logs.prsn.io/consumers/my_json_consumer
```

*Important:* Check out "auto.offset.reset" param. 'largest' means it will set your consumer offset to the most recent event in the queue. 'smallest' will set it at the beginning (i.e. 72hours worth of logs).

Example:
```
curl -X POST -H "Content-Type: application/vnd.kafka.v1+json" \
--data '{"name": "michael", "format": "json", "auto.offset.reset": "largest"}' \
http://logs.prsn.io/consumers/my_json_consumer
```
 
### Now lets get some messages
### GET /consumers/my_json_consumer/instances/&lt;SOME_NAME&gt;/topics/&lt;TOPIC_NAME&gt;

Consume messages from a topic.

Example:

```
$ curl -X GET -H "Accept: application/vnd.kafka.json.v1+json" \
http://logs.prsn.io/consumers/my_json_consumer/instances/michael/topics/reg
```
```
{
  "key": null,
  "value": {
    "log": "Thu Jul 28 04:52:42.111 [conn2462488] command denied: { serverStatus: 1, tcmalloc: false }\n",
    "stream": "stdout",
    "docker": {
      "container_id": "a20cb48850d3cf7bfdf362c8d0452639303b421716a0e815e331876610602778"
    },
    "kubernetes": {
      "namespace_name": "reg",
      "pod_name": "mongo21x-provision-1328673652-gzp1c",
      "container_name": "mongo21x-provision"
    },
    "topic": "reg"
  },
  "partition": 0,
  "offset": 19688171
}
```
<br>
The above is ONE single event from a given topic. If you ran a similar command you will likely get thousands if not tens of thousands of events.
<br>


### Get 1KB of data returned


```
curl -X GET -H "Accept: application/vnd.kafka.json.v1+json" \
http://logs.prsn.io/consumers/my_json_consumer/instances/michael/topics/reg?max_bytes=1000
```
Notice `?max_bytes=1000` tells Kafka to return around 1KB of data. This will not cut off events. It will fulfill the request closest to the request param given.
```
[
  {
    "key": null,
    "value": {
      "log": "Thu Jul 28 09:59:21.516 [conn1793503] end connection 127.0.0.1:45276 (7 connections now open)\n",
      "stream": "stdout",
      "docker": {
        "container_id": "d26ade0b81ff202855a75e0ca77a6919e05aa53faf005c29a98f717f49c2ee56"
      },
      "kubernetes": {
        "namespace_name": "reg",
        "pod_name": "mongo2x-provision-826675415-xo6ls",
        "container_name": "mongo2x-provision"
      },
      "topic": "reg"
    },
    "partition": 0,
    "offset": 19810838
  },
  {
    "key": null,
    "value": {
      "log": "Thu Jul 28 09:59:22.130 [initandlisten] connection accepted from 127.0.0.1:58556 #2480888 (3 connections now open)\n",
      "stream": "stdout",
      "docker": {
        "container_id": "a20cb48850d3cf7bfdf362c8d0452639303b421716a0e815e331876610602778"
      },
      "kubernetes": {
        "namespace_name": "reg",
        "pod_name": "mongo21x-provision-1328673652-gzp1c",
        "container_name": "mongo21x-provision"
      },
      "topic": "reg"
    },
    "partition": 0,
    "offset": 19810839
  }
]
```

Performing this request again will give you the next 1KB of data in the topic.

<br>
### Query data from offset
Now lets imagine we have an offset to work from. Such as `"offset": 19810839` above.
We can use this for our next query and event provide a count of events we want to receive.

```
curl -H "Accept: application/vnd.kafka.json.v1+json" "http://logs.prsn.io/topics/reg/partitions/0/messages?offset=19810839&count=10"
```
Now you have the ability to move forward and backward through the Kafka queue based on the offset value. As many or as few message as you want to pull can be set.
```
[
  {
    "key": null,
    "value": {
      "log": "Code: 500. Errors:\n",
      "stream": "stderr",
      "docker": {
        "container_id": "94a55d5c1a7eb462fd000e28e4cb3f5be4d7a16abd7def54ea86125f89559153"
      },
      "kubernetes": {
        "namespace_name": "pulse",
        "pod_name": "web-3806673570-sp8td",
        "container_name": "web"
      },
      "topic": "pulse"
    },
    "partition": 0,
    "offset": 209395502
  },
  {
    "key": null,
    "value": {
      "log": "\n",
      "stream": "stderr",
      "docker": {
        "container_id": "94a55d5c1a7eb462fd000e28e4cb3f5be4d7a16abd7def54ea86125f89559153"
      },
      "kubernetes": {
        "namespace_name": "pulse",
        "pod_name": "web-3806673570-sp8td",
        "container_name": "web"
      },
      "topic": "pulse"
    },
    "partition": 0,
    "offset": 209395503
  },
  {
    "key": null,
    "value": {
      "log": "* lease not found or lease is not renewable\n",
      "stream": "stderr",
      "docker": {
        "container_id": "94a55d5c1a7eb462fd000e28e4cb3f5be4d7a16abd7def54ea86125f89559153"
      },
      "kubernetes": {
        "namespace_name": "pulse",
        "pod_name": "web-3806673570-sp8td",
        "container_name": "web"
      },
      "topic": "pulse"
    },
    "partition": 0,
    "offset": 209395504
  },...

```


### GET /consumers/(string: group\_name)/instances/(string: instance)/topics/(string: topic\_name)

    Delete the consumer.

curl -X DELETE http://logs.prsn.io/consumers/my\_json\_consumer/instances/<YOUR\_CONSUMER\_NAME>
