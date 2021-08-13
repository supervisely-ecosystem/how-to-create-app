
<div align="left" markdown>

## **Part 12 — Remote Developing with Docker [Docker Image]**  

</div>  


In this part, you will learn how to start developing remotely via docker image. We'll use **Ubuntu 20.04** as an example.

1. <a href="#step-1--create-ssh-key">Create SSH key</a>
2. <a href="#step-2--docker-image">Docker Image</a>
3. <a href="#step-3--install-ssh-server-inside-docker-container">Install SSH server inside Docker container</a>
4. <a href="#step-4--edit-ssh-config">Edit SSH Config</a>
5. <a href="#step-5--connect-to-ssh-server-from-pycharm">Connect to SSH server from PyCharm</a>

---
### Step 1 — Create SSH key
On your client system – the one you’re using to connect to the server – you need to create a pair of key codes.

To generate a pair of SSH key codes, enter the commands:
```commandline
ssh-keygen
```
If you’ve already generated a key pair, this will prompt to overwrite them, and those old keys will not work anymore.

**Note:** This process creates two keys. 
One is a public key, which you can hand out to anyone – in this case, you’ll save it to the server. 
The other one is a private key, which you will need to keep secure. 
The secure private key ensures that you are the only person who can encrypt the data that is decrypted by the public key.

result img

---
### Step 2 — Docker Image

You can use pre-configured **Dockerfile** and **docker-compose.yml** from docker directory or create them from scratch. 

#### Step 2.1 — Create Dockerfile
The first thing you need to do is to create a directory in which you can store **Dockerfile** and **docker-compose.yml**.

1. As an example, we will create a directory named docker inside our project with the command:
   ```commandline
   mkdir docker
   ```

2. Move into that directory and create a new empty file (Dockerfile) in it by typing:
   ```commandline
   cd docker
   ```
   
   ```commandline
   touch Dockerfile
   ```

3. Open the file with a text editor of your choice. In this example, we opened the file using Nano:
   ```commandline
   nano Dockerfile
   ```

4. Then, add the following content:
   ```dockerfile
   ARG IMAGE
   FROM $IMAGE
   
   RUN apt-get update && apt-get install -y openssh-server
   EXPOSE 22
   
   RUN apt-get install -y sudo
   RUN mkdir -p /run/sshd
   
   ARG home=/root
   RUN mkdir $home/.ssh
   COPY authorized_keys $home/.ssh/authorized_keys
   RUN chown root:root $home/.ssh/authorized_keys && \
       chmod 600 $home/.ssh/authorized_keys
   
   COPY sshd_deamon.sh /sshd_deamon.sh
   RUN chmod 755 /sshd_deamon.sh
   CMD ["/sshd_deamon.sh"]
   ENTRYPOINT ["sh", "-c", "/sshd_deamon.sh"]
   ```

5. Save and exit the file.

6. You can check the content of the file by using the cat command:
   ```commandline
   cat Dockerfile
   ```
   
#### Step 2.2 — Create docker-compose

1. **Create docker-compose.yml** file
   ```commandline
   touch docker-compose.yml
   ```

2. Open the file with a text editor of your choice. In this example, we opened the file using Nano:
   ```commandline
   nano docker-compose.yml
   ```

3. Then, add the following content:
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

4. Save and exit the file.

5. You can check the content of the file by using the cat command:
   ```commandline
   cat docker-compose.yml
   ```
   
---
### Step 3 — Build Dockerfile

The basic syntax used to build an image using a docker-compose is:
```commandline
docker-compose up --build -d
```

Once the image is successfully built, you can verify whether it is on the list of images with the command:
```commandline
docker container list
```

result img

---
### Step 4 — Edit local SSH Config

---
### Step 5 — Connect to SSH server from PyCharm


#### RUN ALL COMMANDS FROM docker dir