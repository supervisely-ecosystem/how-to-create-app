
<div align="left" markdown>

## **Part 12 — Remote Developing with Docker [Docker Image]**  

</div>  


In this part, you will learn how to start developing remotely via docker image. We'll use **Ubuntu 18.04** as an example.

1. <a href="#step-1--create-a-separate-folder">Create a separate folder</a>
2. <a href="#step-2--create-ssh-key">Create SSH key</a>
3. <a href="#step-3--docker-image">Docker Image</a>
4. <a href="#step-4--connect-to-ssh-server">Connect to SSH server</a>
5. <a href="#step-5--connect-to-ssh-server-from-pycharm">Connect to SSH server from PyCharm</a>


### Step 1 - Create a separate folder
The first thing you need to do is to create a directory in which you can store docker and ssh related files.

As an example, we will create a directory named **docker** inside our project and move into that directory with the command:
```commandline
mkdir docker && cd docker
```

---
### Step 2 — Create SSH key
On your client system – the one you’re using to connect to the server – you need to create a pair of key codes.

To generate a pair of SSH key codes, enter the command:
```commandline
ssh-keygen -t rsa -b 4096 -f my_key
```

Files `my_key` and `my_key.pub` will be created in the docker directory.

If you’ve already generated a key pair, this will prompt to overwrite them, and those old keys will not work anymore.

---
### Step 3 — Docker Image

You can use pre-configured `GPU` ready **Dockerfile** and **docker-compose.yml** from docker directory or create your own from scratch. 

#### Step 3.1 — Create Dockerfile

A **Dockerfile** is a script with instructions on how to build a Docker image. 
These instructions are, in fact, a group of commands executed automatically in the Docker environment to build a specific Docker image.
This **Dockerfile** inherits **Ubuntu 18.04** image and launch SSH server via **sshd_daemon.sh**

**docker/sshd_daemon.sh**
```shell
#!/bin/bash -l

echo $PATH
/usr/sbin/sshd -D
```

**docker/Dockerfile**
```dockerfile
ARG IMAGE
FROM $IMAGE

RUN apt-get update && apt-get install -y openssh-server
EXPOSE 22

RUN apt-get install -y sudo
RUN mkdir -p /run/sshd

ARG home=/root
RUN mkdir $home/.ssh
COPY my_key.pub $home/.ssh/authorized_keys
RUN chown root:root $home/.ssh/authorized_keys && \
    chmod 600 $home/.ssh/authorized_keys

COPY sshd_daemon.sh /sshd_daemon.sh
RUN chmod 755 /sshd_daemon.sh
CMD ["/sshd_daemon.sh"]
ENTRYPOINT ["sh", "-c", "/sshd_daemon.sh"]
```


#### Step 3.2 — Create docker-compose

We prefer to use **Docker Compose**, but it's not a requirement. **Docker Compose** is yet another useful Docker tool. 
It allows users to launch, execute, communicate, and close containers with a single coordinated command.

**docker/docker-compose.yml**
```dockerfile
version: "2.2"
services:
  remote_dev_service:
    shm_size: '8gb'
    runtime: nvidia
    build:
      context: .
      args:
        IMAGE: nvidia/cuda:11.1.1-devel-ubuntu18.04
    ports:
      - "1234:22"
    volumes:
      - "./data:/data"
```
   
#### Step 3.3 — Build Dockerfile

Prerequisities:
* [Install docker and nvidia-docker2](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)
   ```commandline
   curl https://get.docker.com | sh \
     && sudo systemctl --now enable docker
   ```
  
   ```commandline
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt update
   sudo apt install -y nvidia-docker2
   sudo systemctl restart docker
   ```

The basic syntax used to build an image using a docker-compose is:
```commandline
docker-compose up --build -d
```

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/build-docker-compose.png" width="80%" style='padding-top: 10px'>

Once the image is successfully built, you can verify whether it is on the list of images with the command:
```commandline
docker container list
```

---
### Step 4 — Connect to SSH server

Optional. Add server with the ports specified in **docker-compose.yml**

**~/.ssh/config**
```commandline
Host gpu1
    HostName 192.168.1.10
    User root
    Port 1234
    IdentityFile ~/.ssh/id_rsa
```

To connect to SSH server, use this command:
```commandline
ssh -i ./my_key root@<server endpoint> -p <port specified in docker-compose.yml>
```

Example:
```commandline
ssh -i ./my_key root@localhost -p 1234
```

---
### Step 5 — Connect to SSH server from PyCharm

1. Configure connection
   
   Go to **Tools** -> **Deployment** and select **Configuration**.
   Add new **SFTP** connection by pressing **+** icon in the top left corner of the window and name it.
   Press on the **3 dots** next to SSH configuration and configure it.
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/deployment-1.png" width="80%" style='padding-top: 10px'>
   
   Add new **SFTP** configuration by pressing **+** icon in the top left corner of the window and name it. Fill out the form and press **OK**.
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-configuration.png" width="80%" style='padding-top: 10px'>
   
   New configuration will be automatically selected in the deployment window. Press **OK** again.
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/deployment-2.png" width="80%" style='padding-top: 10px'>


2. Configure interpreter
   
   Go to **File** -> **Settings** -> **Project** and select **Python interpreter**.
   
   Click on the **Gear** icon and select **Add**, **Add python interpreter window** will pop up. Select **SSH interpreter** -> **Existing server configuration**
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-interpreter-1.png" width="80%" style='padding-top: 10px'>

   Specify the path to the interpreter.
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-interpreter-2.png" width="80%" style='padding-top: 10px'>

   And configure mapping between local paths and remote paths if needed.
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-interpreter-3.png" width="80%" style='padding-top: 10px'>
   
   Apply selected interpreter and run the script
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/run-script.png" width="80%" style='padding-top: 10px'>
   