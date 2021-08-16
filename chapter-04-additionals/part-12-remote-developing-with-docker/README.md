
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

To generate a pair of SSH key codes, enter the command:
```commandline
ssh-keygen -t rsa -b 4096 -f my_key
```
Files `my_key` and `my_key.pub` will be created in the docker directory

If you’ve already generated a key pair, this will prompt to overwrite them, and those old keys will not work anymore.

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/generate-keys.png" width="80%" style='padding-top: 10px'>  


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

Once the image is successfully built, you can verify whether it is on the list of images with the command:
```commandline
docker container list
```

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/build-docker-compose.png" width="80%" style='padding-top: 10px'>

---
### Step 4 — Connect to SSH server

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
   
   Add new **SFTP** configuration by pressing **+** icon in the top left corner of the window and name it.
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-configuration.png" width="80%" style='padding-top: 10px'>
   
   Fill out the form and press **OK**, new configuration will be automatically selected in the deployment window. Press **OK** again.
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/deployment-2.png" width="80%" style='padding-top: 10px'>


2. Configure interpreter
   Go to **File** -> **Settings** -> **Project** and select **Python interpreter**
   
   Click on the **Gear** icon and select **Add**, **Add python interpreter window** will pop up. Select **SSH interpreter** -> **Existing server configuration**
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-interpreter-1.png" width="80%" style='padding-top: 10px'>

   Specify the path to the interpreter.
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-interpreter-2.png" width="80%" style='padding-top: 10px'>

   And configure mapping between local paths and remote paths
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-interpreter-3.png" width="80%" style='padding-top: 10px'>
   
   Apply selected interpreter and run the script
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/run-script.png" width="80%" style='padding-top: 10px'>
   