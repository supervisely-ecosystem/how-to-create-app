
<div align="left" markdown>

## **Part 1 — Remote Developing with PyCharm [Docker SSH Server]**  

</div>  


In this part, you will learn how to start developing using PyCharm and Docker.  

1. <a href="#step-1--create-a-working-directory">Create a working directory</a>
2. <a href="#step-2--create-ssh-key">Create SSH key</a>
3. <a href="#step-3--docker-image">Docker Image</a>
4. <a href="#step-4--Connect-to-container-over-SSH">Connect to container over SSH</a>
5. <a href="#step-5--connect-to-container-in-PyCharm">Connect to container in PyCharm</a>


### Step 1 — Create a working directory
Connect to the remote host on which you will deploy the docker container.
The first thing you need to do is to create a directory in which you can store docker and ssh related files.
As an example, we will create a directory named **remote_dev** inside our project and move into that directory with the command:
```commandline
mkdir remote_dev && cd remote_dev
```

---
### Step 2 — Create SSH key
You need to create a pair of key codes on your remote host with docker container.

To generate a pair of SSH key codes, enter the command:
```commandline
ssh-keygen -t rsa -b 4096 -f my_key
```

Files `my_key` and `my_key.pub` will be created in the working directory.
Keys must be stored in 3 locations:
1. `my_key.pub` on remote host with docker container.
2. `my_key.pub` in created docker container.
3. `my_key` on your local host (you need to copy it there). 

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-01-remote-developing-with-pycharm/media/2-1.png" width="100%" style='padding-top: 10px'>  

---
### Step 3 — Docker Image

Let's create all the files necessary for building the container.

#### 1. Create Dockerfile

Let's create a simple image in which we will deploy the **SSH server**:

**remote_dev/Dockerfile**
```dockerfile
ARG IMAGE
FROM $IMAGE
#Add your libs here...
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

Add a script to start the server:

**remote_dev/sshd_daemon.sh**
```shell
#!/bin/bash -l

echo $PATH
/usr/sbin/sshd -D
```


#### 2. Create docker-compose

For convenience, let's create a **docker-compose** file.

Since we need a **GPU inside the container**, we will take **Image with** pre-installed **CUDA** as a basis and set runtime to **nvidia**.  

**remote_dev/docker-compose.yml**
```dockerfile
version: "2.2"
services:
  remote_dev_service:
    shm_size: '8gb'
    runtime: nvidia
    build:
      context: .
      args:
        IMAGE: `insert your IMAGE name here`
    ports:
      - "1234:22"
    volumes:
      - "./data:/data"
```

#### 3. Build container


Don't forget to [install docker and nvidia-docker2](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)
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

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-01-remote-developing-with-pycharm/media/3-1.png" width="80%" style='padding-top: 10px'>

Once the image is successfully built, you can verify whether it is on the list of containers with the command:
```commandline
docker ps | grep remote_dev_service
```

---
### Step 4 — Connect to container over SSH

Add server with the ports specified in **docker-compose.yml**

**~/.ssh/config** (example)[local host]
```commandline
Host docker_remote_container
    HostName ip_of_your_docker_container
    User root
    Port 1234
    IdentityFile path_to_ssh_secret_key
```

```commandline
Where:
    docker_remote_container - any name of your choice,
    ip_of_your_docker_container - you can get it by use `hostname -i` on your remote host,
    root - unchange,
    1234 - unchange,
    path_to_ssh_secret_key - path to `my_key` on your local host(step 2).
```

To connect to container by SSH, use command:
```commandline
ssh docker_remote_container
```

---
### Step 5 — Connect to container in PyCharm

#### 1. Create new project

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-01-remote-developing-with-pycharm/media/5-1.png" width="100%" style='padding-top: 10px'>  

---

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-01-remote-developing-with-pycharm/media/5-2.png" width="100%" style='padding-top: 10px'>  


#### 2. Add new interpreter

- **Open Preferences -> Python Interpreter**  
- **Show all**  
- **Plus button**

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-01-remote-developing-with-pycharm/media/5-3.png" width="100%" style='padding-top: 10px'>  

---
<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-01-remote-developing-with-pycharm/media/5-4.png" width="100%" style='padding-top: 10px'>  

#### 3. Configure interpreter

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-01-remote-developing-with-pycharm/media/5-5.png" width="100%" style='padding-top: 10px'>  

 ---   

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-01-remote-developing-with-pycharm/media/5-6.png" width="100%" style='padding-top: 10px'>  

#### 4. Run simple code

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-01-remote-developing-with-pycharm/media/5-7.png" width="100%" style='padding-top: 10px'>  
