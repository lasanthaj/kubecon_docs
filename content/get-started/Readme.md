# Getting Started

### Requirements:
----
You will need to reach out to the Cloud Ops Team by submitting a Jira @ https://one-jira.pearson.com/projects/COPS.<br>

Please provide the following information in your request:<br>
  - Production or Proof of Concept (POC)<br>
  - Preferred location - USE or AP<br>
  - Project Name: ex. pulse<br>
  - Repo name: In order to enable CD pipelines, we need a location to specify where your bitesize config files will be stored.  Generally this is not the same repository as your code base.<br>
  - Repo location: URL to repo<br>
  - List the environments you require: <dev, stg, prd, qa>
  - Provide an email address for Grafana admin access

In return the Cloud Ops Team will:<br>
 - Setup environments for you<br>
 - Create a Grafana Organization for you view log events<br>
 - Deploy Jenkins which will connect back to the repo provided above<br>
 - Provide Consul and Vault ACL access<br>





last modified 14 Oct, 2016
