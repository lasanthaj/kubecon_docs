[albert]: http://plainicon.com/dboard/userprod/2802_db2aa/prod_thumb/plainicon.com-46949-256px-353.png

#  Demonstration : Using Bitesize for Automated Deployments

Welcome to the demonstration in a few easy steps we're going to show how simple it is to push updates into Bitesize with automated testing and deployment.

![This is a picture of Albert][albert]

## Step One - Make the Change

Go to [Github](https://github.com/pearsontechnology/kubecon_docs/edit/master/content/albert-demo.md) - the page will open in "edit" mode

Change line number 1 from: 

```
[albert]: http://plainicon.com/dboard/userprod/2802_db2aa/prod_thumb/plainicon.com-46949-256px-353.png
```
to
```
[albert]: http://www.v3.co.uk/IMG/598/353598/albert-hitchcock-pearson-2-2-580x358.jpe
```

Scroll to the bottom of the Github page and click the "Commit changes" green button

## Step Two - Follow the Deployment

Go to the Jenkins instance for this site [here](https://docs.dev-bite.io/)

(TODO) - Explain how to watch the most recent build and see the log - notice the build failed because it could not find the image?

## Step Three - Fix the Code

Go back to [Github](https://github.com/pearsontechnology/kubecon_docs/edit/master/content/albert-demo.md) - the page will open in "edit" mode

Change line number 1 from: 

```
[albert]: http://www.v3.co.uk/IMG/598/353598/albert-hitchcock-pearson-2-2-580x358.jpe
```
to
```
[albert]: http://www.v3.co.uk/IMG/598/353598/albert-hitchcock-pearson-2-2-580x358.jpeg
```

Scroll to the bottom of the Github page and click the "Commit changes" green button

## Step Four - Follow the Deployment

Go to the Jenkins instance for this site [here](https://docs.dev-bite.io/)

(TODO) - Explain how to watch the most recent build and see the log - notice the build now passes

## Step Five - Reload this Page

Demo complete!
