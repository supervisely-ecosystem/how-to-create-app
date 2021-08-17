
<div align="left" markdown>

## **Part 12 — Remote Developing with Docker [Docker Image]**  

</div>  


In this part, you will learn how to start developing remotely via docker image. We'll use **Ubuntu 18.04** as an example.

1. <a href="#step-1--create-ssh-key">Create SSH key</a>
2. <a href="#step-2--docker-image">Docker Image</a>
3. <a href="#step-3--install-ssh-server-inside-docker-container">Install SSH server inside Docker container</a>
4. <a href="#step-4--edit-ssh-config">Edit SSH Config</a>
5. <a href="#step-5--connect-to-ssh-server-from-pycharm">Connect to SSH server from PyCharm</a>


### Step 0 - Create a separate folder
The first thing you need to do is to create a directory in which you can store docker and ssh related files.

1. As an example, we will create a directory named **docker** inside our project with the command:
   ```commandline
   mkdir docker
   ```

2. Move into that directory and proceed to the next steps:
   ```commandline
   cd docker
   ```

---
### Step 1 — Create SSH key
On your client system – the one you’re using to connect to the server – you need to create a pair of key codes.

To generate a pair of SSH key codes, enter the command:
```commandline
ssh-keygen -t rsa -b 4096 -f my_key
```

Files `my_key` and `my_key.pub` will be created in the docker directory.

If you’ve already generated a key pair, this will prompt to overwrite them, and those old keys will not work anymore.

---
### Step 2 — Docker Image

You can use pre-configured `GPU` ready **Dockerfile** and **docker-compose.yml** from docker directory or create your own from scratch. 

#### Step 2.1 — Create Dockerfile
1. Create a new empty file (Dockerfile) in it by typing:
   ```commandline
   touch Dockerfile
   ```

2. Open the file with a text editor of your choice. In this example, we opened the file using Nano:
   ```commandline
   nano Dockerfile
   ```

3. Write a Dockerfile that builds a Docker image. The image contains all the dependencies the Python application requires, including Python itself.

4. Save and exit the file.

5. You can check the content of the file by using the cat command:
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

3. Define the services that make up your app in docker-compose.yml so they can be run together in an isolated environment.

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

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/build-docker-compose.png" width="80%" style='padding-top: 10px'>

Once the image is successfully built, you can verify whether it is on the list of images with the command:
```commandline
docker container list
```

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
   
   1.1 Go to **Tools** -> **Deployment** and select **Configuration**.
       Add new **SFTP** connection by pressing **+** icon in the top left corner of the window and name it.
       Press on the **3 dots** next to SSH configuration and configure it.
   
       <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/deployment-1.png" width="80%" style='padding-top: 10px'>
   
   1.2 Add new **SFTP** configuration by pressing **+** icon in the top left corner of the window and name it. Fill out the form and press **OK**.
   
       <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-configuration.png" width="80%" style='padding-top: 10px'>
   
   1.3 New configuration will be automatically selected in the deployment window. Press **OK** again.
   
       <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/deployment-2.png" width="80%" style='padding-top: 10px'>


2. Configure interpreter
   
   2.1 Go to **File** -> **Settings** -> **Project** and select **Python interpreter**.
   
   2.2 Click on the **Gear** icon and select **Add**, **Add python interpreter window** will pop up. Select **SSH interpreter** -> **Existing server configuration**
   
       <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-interpreter-1.png" width="80%" style='padding-top: 10px'>

   2.3 Specify the path to the interpreter.
       
       <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-interpreter-2.png" width="80%" style='padding-top: 10px'>

       And configure mapping between local paths and remote paths if needed.

       <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-interpreter-3.png" width="80%" style='padding-top: 10px'>

   2.4 Apply selected interpreter and run the script
       
       <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/run-script.png" width="80%" style='padding-top: 10px'>
   