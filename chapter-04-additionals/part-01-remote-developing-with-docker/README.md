
<div align="left" markdown>

## **Part 1 — Remote Developing with Docker [PyCharm SSH Interpreter]**  

</div>  


In this part, you will learn how to start developing using Docker.  

1. <a href="#step-1--create-a-working-directory">Create a working directory</a>
2. <a href="#step-2--create-ssh-key">Create SSH key</a>
3. <a href="#step-3--docker-image">Docker Image</a>
4. <a href="#step-4--connect-to-ssh-server">Connect to container over SSH</a>
5. <a href="#step-5--Connect-to container in PyCharm">Connect to container in PyCharm</a>


### Step 1 — Create a working directory
The first thing you need to do is to create a directory in which you can store docker and ssh related files.

As an example, we will create a directory named **remote_dev** inside our project and move into that directory with the command:
```commandline
mkdir remote_dev && cd remote_dev
```

---
### Step 2 — Create SSH key
On your client system – the one you’re using to connect to the server – you need to create a pair of key codes.

To generate a pair of SSH key codes, enter the command:
```commandline
ssh-keygen -t rsa -b 4096 -f my_key
```

Files `my_key` and `my_key.pub` will be created in the docker directory.

<img src="2-1.png" width="100%" style='padding-top: 10px'>  

---
### Step 3 — Docker Image

Let's create all the files necessary for building the container.

#### Step 3.1 — Create Dockerfile

Let's create a simple image in which we will deploy the **SSH server**:

**remote_dev/Dockerfile**
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

Add a script to start the server:

**remote_dev/sshd_daemon.sh**
```shell
#!/bin/bash -l

echo $PATH
/usr/sbin/sshd -D
```


#### Step 3.2 — Create docker-compose

Since we need a **GPU inside the container**, we will take **Image with** pre-installed **CUDA** as a basis and set runtime to **nvidia**.  
For convenience, let's create a **docker-compose** file:

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
        IMAGE: nvidia/cuda:11.1.1-devel-ubuntu18.04
    ports:
      - "1234:22"
    volumes:
      - "./data:/data"
```

#### Step 3.3 — Build container


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

<img src="3-1.png" width="80%" style='padding-top: 10px'>

Once the image is successfully built, you can verify whether it is on the list of containers with the command:
```commandline
docker ps | grep grep remote_dev_service
```

---
### Step 4 — Connect to SSH server

Add server with the ports specified in **docker-compose.yml**

**~/.ssh/config**
```commandline
Host docker_remote_container
    HostName 192.168.1.10
    User root
    Port 1234
    IdentityFile /root/qanelph/how-to-create-app/chapter-04-additionals/part-01-remote-developing-with-docker/docker/my_key
```

To connect to container by SSH, use command:
```commandline
ssh docker_remote_container
```

---
### Step 5 — Connect to container in PyCharm

1. Create new project

<img src="5-1.png" width="100%" style='padding-top: 10px'>  

---

<img src="5-2.png" width="100%" style='padding-top: 10px'>  


2. Add new interpreter

- **Open Preferences -> Python Interpreter**  
- **Show all**  
- **Plus button**

<img src="5-3.png" width="100%" style='padding-top: 10px'>  

---
<img src="5-4.png" width="100%" style='padding-top: 10px'>  

3. Configure interpreter

<img src="5-5.png" width="100%" style='padding-top: 10px'>  

 ---   

<img src="5-6.png" width="100%" style='padding-top: 10px'>  

4. Run simple code

<img src="5-7.png" width="100%" style='padding-top: 10px'>  
