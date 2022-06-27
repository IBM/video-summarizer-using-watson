# Summarize a video or audio file using Watson

In this code pattern, we will [create something] using [technologies] and [components]. [Explain briefly how things work]. [Give acknowledgements to others if necessary]

When you have completed this code pattern, you will understand how to:

* [goal 1]
* [goal 2]
* [goal 3]
* [goal 4]

<!--add an image in this path-->
![architecture](doc/source/images/architecture.png)

<!--Optionally, add flow steps based on the architecture diagram-->
## Flow

1. Step 1.
2. Step 2.
3. Step 3.
4. Step 4.
5. Step 5.

<!--Optionally, update this section when the video is created-->
# Watch the Video

[![video](http://img.youtube.com/vi/Jxi7U7VOMYg/0.jpg)](https://www.youtube.com/watch?v=Jxi7U7VOMYg)

# Steps

1. [Clone the repo](#1-clone-the-repo)
1. [Create Watson Services](#2-create-watson-services)
    - 2.1. [Create Watson Speech to Text service on IBM Cloud](#21-create-watson-speech-to-text-service-on-ibm-cloud)
    - 2.2. [Add Watson Speech to Text credentials to the application](#22-add-watson-speech-to-text-credentials-to-the-application)
1. [Run the Application](#3-run-the-application)
1. [Analyze the Application](#4-analyze-the-application)

## 1. Clone the repo

Clone the `video-summarizer-using-watson` repo locally. In a terminal, run:

```bash
git clone https://github.com/IBM/video-summarizer-using-watson.git
```

### Application Directory structure

The Application is built on Python Flask Framework.

* The directory structure is as follows:

    <pre>
    .
    ├── Dockerfile
    ├── LICENSE
    ├── Notebooks
    │   ├── IBM Watson Speech to Text custom model training.ipynb
    │   └── Summarize.ipynb
    ├── Procfile
    ├── README.md
    ├── apis
    │   ├── __init__.py
    │   ├── summarizer.py
    │   ├── videoUtils.py
    │   └── watsonSpeechToText.py
    ├── app.py
    ├── deploy.yaml
    ├── manifest.yml
    ├── requirements.txt
    ├── static
    │   ├── audios
    │   ├── chunks
    │   ├── credentials
    │   │   └── speechtotext.json
    │   ├── css
    │   │   └── style.css
    │   ├── images
    │   ├── js
    │   │   └── script.js
    │   ├── transcripts
    │   └── videos
    │       └── wc.png
    └── templates
        └── index.html
    </pre>

* `apis/` contains the API endpoints.
  * `/api/v1.0/uploadVideo`: This API is used to upload the video file, extract audio from the video file, detect long pauses in the audio file and split the audio file into chunks.
  * `/api/v1.0/transcribe/<string:model>`: This API is used to transcribe the audio files using Watson Speech to Text.
  * `/api/v1.0/summarize`: This API is used to summarize the text using GTP-2, Gensim and XLNET summarizers.
* `static/` contains the following static files.
  * `credentials/` contains the credentials for Watson Speech to Text.
  * `videos/` contains the uploaded video files.
  * `audios/` contains the extracted audio files.
  * `transcripts/` contains the transcribed text files.
  * `chunks/` contains the audio chunks.
  * `css/` contains the CSS files.
  * `js/` contains the JavaScript files.
* `templates/` contains the HTML templates.
* `app.py` is the main application file to run the flask server.
* `Dockerfile` is the Dockerfile to build the Docker image.
* `requirements.txt` is the list of requirements for the application.
* `deploy.yaml` is the deployment configuration file.

## 2. Create Watson Services

### 2.1. Create Watson Speech to Text service on IBM Cloud

* Login to IBM Cloud, create a [Watson Speech To Text Service](https://cloud.ibm.com/catalog/services/speech-to-text), and click on `create` as shown.
![Speech-to-text-service](doc/source/images/stt-service.png)

* In Speech To Text Dashboard, Click on `Services Credentials`.
![](doc/source/images/service-credentials.png)

- Click on `New credential` and add a service credential as shown.
![](doc/source/images/create-stt-credentials.gif)

- Copy the credentials.

### 2.2. Add Watson Speech to Text credentials to the application

* Add the Watson Speech to Text credentials in the `static/credentials/speechtotext.json` file.

    ```json
    {
        "apikey": "xxxx",
        "iam_apikey_description": "xxxx",
        "iam_apikey_name": "xxxx",
        "iam_role_crn": "xxxx",
        "iam_serviceid_crn": "xxxx",
        "url": "xxxx"
    }
    ```

## 3. Run the Application

You can choose to run the application Locally or deploy on Red Hat OpenShift or deploy on IBM Public Cloud Foundry.

<details><summary><b>Locally</b></summary>

* Navigate to the root of the cloned repo. In terminal, run the following command:

    ```docker
    docker build -t video-summarizer-using-watson:v1.0 .
    ```

* Run the application locally. In terminal, run the following command:

    ```docker
    docker run -p 8080:8080 video-summarizer-using-watson:v1.0
    ```

* Visit <http://localhost:8080> to see the application.

</details>

<details><summary><b>Red Hat OpenShift</b></summary>

### Steps to Build and Deploy on OpenShift

#### Build

> Note: Make sure you have docker cli installed and logged in to DockerHub

* In cloned repo, build the docker image. In terminal run:

    ```bash
    docker build -t <your-docker-username>/video-summarizer-using-watson:v1.0 .
    ```

    > Replace `<your-docker-username>` with your docker hub username

* Once the docker image is built, deploy the docker image to Dockerhub. In terminal run:

    ```bash
    docker push <your-docker-username>/video-summarizer-using-watson:v1.0
    ```

* At this point you have built the container image and successfully pushed to to a container repository dockerhub.

* Copy the image tag `<your-docker-username>/video-summarizer-using-watson:v1.0` and replace it on line no `18` in [deploy.yaml](deploy.yaml)

    <pre><code>spec:
        containers:
        - name: video-summarizer-using-watson
            image:<b> < your-docker-username >/video-summarizer-using-watson:v1.0 </b>
            ports:
            - containerPort: 8080
    </code></pre>

#### Deploy

* Login to your OpenShift cluster, In terminal run:

    ```bash
    oc login -u <username> -p <password>
    ```

* Alternatively you can also login with an auth token. Follow the [Step here](https://developer.ibm.com/tutorials/configure-a-red-hat-openshift-cluster-with-red-hat-marketplace/#4-connect-to-the-openshift-cluster-in-your-cli) to login through an auth token.

* Once you have logged into OpenShift from your terminal, you can run the `oc apply` command to deploy the Application on OpenShift. In cloned repo, navigate to `` directory and in terminal run:

    ```bash
    oc apply -f deploy.yaml
    ```

    ```
    deployment.apps/video-summarizer-using-watson-deployment created
    service/video-summarizer-using-watson-service created
    ```
* Run the `oc get services` to get the service External URL.
   
   ```bash
   oc get services | grep video-summarizer-using-watson-service
   ```

   ```bash
   NAME                        TYPE           CLUSTER-IP       EXTERNAL-IP                            PORT(S)        AGE
   video-summarizer-using-watson-service             LoadBalancer   172.21.170.157   169.60.236.228                         80:32020/TCP   2m
   ```

* At this point, you will have successfully deployed the Application on OpenShift.

* Visit **EXTERNAL-IP** for example: <http://169.60.236.228> to see the application.

</details>

<details><summary><b>IBM Public Cloud Foundry</b></summary>

### Steps to Build and Deploy on IBM Public Cloud Foundry

#### Build and Deploy

* Before you proceed, make sure you have installed [IBM Cloud CLI](https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started&locale=en-US) in your deployment machine.

> Note: You need to set the `disk-quote` to be more than 2GB since pytorch library is huge and requires more than 2GB of disk space to get installed.

* From the cloned repo, in terminal, run the following commands to deploy the Application to IBM Cloud Foundry.

    * Log in to your IBM Cloud account, and select an API endpoint.

        ```bash
        ibmcloud login
        ```

        >NOTE: If you have a federated user ID, instead use the following command to log in with your single sign-on ID.

        ```bash
        ibmcloud login --sso
        ```

    * Target a Cloud Foundry org and space:

        ```bash
        ibmcloud target --cf
        ```

    * From within the root of the cloned repo, push your app to IBM Cloud.

        ```bash
        ibmcloud cf push video-summarizer-using-watson
        ```

* The [manifest.yml](manifest.yml) file will be used here to deploy the application to IBM Cloud Foundry.

* On Successful deployment of the application you will see something similar on your terminal as shown.

    <pre><code>
    Invoking 'cf push'...
    Shown below is a sample output

    Pushing from manifest to org abc@in.ibm.com / space dev as abc@in.ibm.com...

    ...

    Waiting for app to start...

    name:              video-summarizer-using-watson
    requested state:   started
    routes:            <b>video-summarizer-using-watson.xx-xx.mybluemix.net </b>
    last uploaded:     Sat 16 May 18:05:16 IST 2020
    stack:             cflinuxfs3
    buildpacks:        python

    type:            web
    instances:       1/1
    memory usage:    4G
    start command:   python app.py
        state     since                  cpu     memory           disk           details
    #0   <b>running</b>   2020-05-16T12:36:15Z   12.6%   116.5M of 4G   
    </code></pre>

* Once the app is deployed, from the output of the above command, you can visit the `routes` to launch the application.

* At this point, you will have successfully deployed the Application on IBM Cloud.

* Visit <http://video-summarizer-using-watson.xx-xx.mybluemix.net> to see the application.

</details>

## 4. Analyze the Application

* Upload any video/audio file. (.mp4/.mov or .mp3/.wav). You can use the dataset provided in the repo [data/earnings-call-2019.mp4](data/earnings-call-2019.mp4) or [data/earnings-call-Q-and-A.mp4](data/earnings-call-Q-and-A.mp4)
![screenshot1](doc/source/images/screenshot1.png)

<details><summary><b>About the Dataset</b></summary>

For the code pattern demonstration, we have considered `IBM Earnings Call Q1 2019` Webex recording. The data has 20+ min of IBM Revenue discussion, and 2+ min of Q & A at the end of the recording. We have split the data into 2 parts:

- `earnings-call-2019.mp4` - (Duration - 24:40)
This is IBM revenue discussion meeting recording.

- `earnings-call-Q-and-A.mp4` - (Duration - 2:40)
This is a part of Q & A's asked at the end of the meeting.

</details>

* Select the Watson Speech to Text Language and Acoustic Model.
![screenshot2](doc/source/images/screenshot2.png)

    >Custom language model is built to recognize the **out of vocabulary**  words from the audio. [Learn more](https://cloud.ibm.com/docs/speech-to-text?topic=speech-to-text-languageCreate)

    >Custom accoustic model is built to recognize the **accent** of the speaker from the audio. [Learn more](https://cloud.ibm.com/docs/speech-to-text?topic=speech-to-text-acoustic)

    >NOTE: A **Standard account** is required to train a custom Speech To Text Model. There are three types of plans, Lite (FREE), Standard and Premium (PAID) for more info visit <https://cloud.ibm.com/catalog/services/speech-to-text>

    >You can refer to the [IBM Watson Speech to Text custom model training.ipynb](Notebooks/IBM%20Watson%20Speech%20to%20Text%20custom%20model%20training.ipynb) notebook to learn in detail how to build and train custom Watson Speech to Text models.

* Click on submit.
![screenshot3](doc/source/images/screenshot3.png)

* It will take approximately the same amount of time as the duration of the video to process the Speaker Diarized Output, Summary and Transcript.

* You can view the Speaker Diarized Output.
![screenshot4](doc/source/images/screenshot4.png)

>Speaker Diarization is a process of extracting multiple speakers information from an audio. [Learn more](https://en.wikipedia.org/wiki/Speaker_diarisation)

* You can view the Summary from Gensim, GPT2, XLNet and Key Bert.
![screenshot5-1](doc/source/images/screenshot5-1.png)
![screenshot5-2](doc/source/images/screenshot5-2.png)

* You can also view the transcript.
![screenshot6](doc/source/images/screenshot6.png)

# Summary

<!-- keep this -->
## License

This code pattern is licensed under the Apache License, Version 2. Separate third-party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/) and the [Apache License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

[Apache License FAQ](https://www.apache.org/foundation/license-faq.html#WhatDoesItMEAN)
