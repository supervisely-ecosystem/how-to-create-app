
<div align="left" markdown>

## **Part 12 — Remote Developing with Docker [Docker Image]**  

</div>  


In this part, you will learn how to start developing remotely via docker image.

1. <a href="#step-1--create-ssh-key">Create SSH key</a>
2. <a href="#step-2--docker-image">Docker Image</a>
3. <a href="#step-3--install-ssh-server-inside-docker-container">Install SSH server inside Docker container</a>
4. <a href="#step-4--edit-ssh-config">Edit SSH Config</a>
5. <a href="#step-5--connect-to-ssh-server-from-pycharm">Connect to SSH server from PyCharm</a>

---
### Step 1 — Create SSH key
#### Prerequisites
* A server running Ubuntu 18.04, SSH enabled on Ubuntu
* A user account with sudo privileges
* Access to a terminal window/command line (Ctrl-Alt-T)

#### Step 1.1 - Enable SSH
The SSH server is not installed by default on Ubuntu systems.

1. Open the terminal either by using the CTRL+ALT+T keyboard shortcut or by running a search in Ubuntu Dash and selecting the Terminal Icon.

2. Before starting the installation process, check if an SSH server has already been installed on your computer. Use the following command:
    ```commandline
    ssh localhost
    ```
    If you see the SSH “Connection Refused” message, you will have to go through the SSH installation process.
    ```commandline
    ssh: connect to host localhost port 22: Connection refused
    ```
   
    <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-connection-refused.png" width="80%" style='padding-top: 10px'>

3. To install SSH, first update the package repository cache with:
    ```commandline
    sudo apt-get update
    ```

4. Now install the OpenSSH software package by entering:
    ```commandline
    sudo apt-get install openssh-server
    ```

    <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/install-ssh.png" width="80%" style='padding-top: 10px'>

    If prompted, type in your password and press y (yes) to permit the installation.

5. To verify that installation was successful and SSH is running use the command:
    ```commandline
    sudo service ssh status
    ```

    The confirmation message that you are looking for is: `Active: active (running)`
    
    This means you have installed and enabled SSH on your remote machine, which can now accept commands from your SSH client.
   
    <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-active-running.png" width="80%" style='padding-top: 10px'>
   
6. To return to the command line prompt enter **q**.

#### Step 1.2 - Create SSH key
On your client system – the one you’re using to connect to the server – you need to create a pair of key codes.

To generate a pair of SSH key codes, enter the commands:
```commandline
mkdir –p $HOME/.ssh
chmod 0700 $HOME/.ssh
ssh-keygen
```
This will create a hidden directory to store your SSH keys, and modify the permissions for that directory. The ssh-keygen command creates a 2048-bit RSA key pair.

For extra security, use RSA4096:
```commandline
ssh –keygen –t rsa 4096
```

If you’ve already generated a key pair, this will prompt to overwrite them, and those old keys will not work anymore.

The system will ask you to create a passphrase as an added layer of security. Input a memorable passphrase, and press Enter.

**Note:** This process creates two keys. 
One is a public key, which you can hand out to anyone – in this case, you’ll save it to the server. 
The other one is a private key, which you will need to keep secure. 
The secure private key ensures that you are the only person who can encrypt the data that is decrypted by the public key.

---
### Step 2 - Docker Image
#### Step 2.1 - Install Docker
#### Option 1 - Install Docker on Ubuntu Using Default Repositories
##### Step 1 - Update Software Repositories
Update the local database of software to make sure you’ve got access to the latest revisions.

Open a terminal window and type:
```commandline
sudo apt-get update
```

##### Step 2 - Uninstall Old Versions of Docker
Next, it’s recommended to uninstall any old Docker software before proceeding.

Use the command:
```commandline
sudo apt-get remove docker docker-engine docker.io
```

##### Step 3 - Install Docker on Ubuntu 18.04
To install Docker on Ubuntu, in the terminal window enter the command:
```commandline
sudo apt install docker.io
```

##### Step 4 - Start and Automate Docker
The Docker service needs to be setup to run at startup. To do so, type in each command followed by enter:
```commandline
sudo systemctl start docker
```

```commandline
sudo systemctl enable docker
```

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/how-to-install-docker-on-ubuntu-start-and-enable-docker.png" width="80%" style='padding-top: 10px'>

##### Step 5 (Optional) - Check Docker Version
To verify the installed Docker version number, enter:
```commandline
docker --version
```

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/how-to-install-docker-on-ubuntu-check-docker-version.png" width="80%" style='padding-top: 10px'>

**Note:** The official Docker website does not offer support for Ubuntu 18.04. It’s possible that the Ubuntu default repositories have not updated to the latest revision. There’s nothing wrong with running this installation. However, if you are up for a slightly more intensive operation, you can install a more recent (or specific) Docker from the official Docker repositories.

#### Option 2 - Install Docker from Official Repository
##### Step 1 - Update Local Database
Update the local database with the command:
```commandline
sudo apt-get update
```

##### Step 2 - Download Dependencies
You’ll need to run these commands to allow your operating system to access the Docker repositories over HTTPS.

In the terminal window, type:
```commandline
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```

To clarify, here’s a brief breakdown of each command:
* **apt-transport-https**: Allows the package manager to transfer files and data over https
* **ca-certificates**: Allows the system (and web browser) to check security certificates
* **curl**: This is a tool for transferring data
* **software-properties-common**: Adds scripts for managing software

##### Step 3 - Add Docker’s GPG Key
The GPG key is a security feature.

To ensure that the software you’re installing is authentic, enter:
```commandline
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add –
```

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/how-to-install-docker-on-ubuntu-add-docker-gpg-key.png" width="80%" style='padding-top: 10px'>

##### Step 4 - Install the Docker Repository
To install the Docker repository, enter the command:
```commandline
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs)  stable" 
```
The command **“$(lsb_release –cs)”** scans and returns the codename of your Ubuntu installation – in this case, Bionic. Also, the final word of the command **– stable–** is the type of Docker release.

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/how-to-install-docker-on-ubuntu-install-docker-repository.png" width="80%" style='padding-top: 10px'>

A stable release is tested and confirmed to work, but updates are released less frequently. You may substitute edge if you’d like more frequent updates, at the cost of potential instability. There are other repositories, but they are riskier – more info can be found on the [Docker web page](https://docs.docker.com/engine/install/ubuntu/).

##### Step 5 - Update Repositories  

Update the repositories you just added:
```commandline
sudo apt-get update

```

##### Step 6 - Install Latest Version of Docker
To install the latest version of docker:
```commandline
sudo apt-get install docker-ce
```

##### Step 7 (Optional) - Install Specific Version of Docker 
List the available versions of Docker by entering the following in a terminal window:
```commandline
apt-cache madison docker-ce
```

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/how-to-install-docker-on-ubuntu-list-available-docker-version.png" width="80%" style='padding-top: 10px'>

The system should return a list of available versions as in the image above.

At this point, type the command:
```commandline
sudo apt-get install docker-ce=[version]
```
However, substitute **[version]** for the version you want to install (pulled from the list you just generated).

For example:

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/how-to-install-docker-on-ubuntu-install-specific-version-of-docker.png" width="80%" style='padding-top: 10px'>

#### Step 2.2 - Create Docker Image

The first thing you need to do is to create a directory in which you can store all the Docker images you build.

1. As an example, we will create a directory named MyDockerImages with the command:
   ```commandline
   mkdir MyDockerImages
   ```

2. Move into that directory and create a new empty file (Dockerfile) in it by typing:
   ```commandline
   cd MyDockerImages
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
   FROM ubuntu
   
   MAINTAINER sofija
   
   RUN apt-get update
   
   CMD ["echo", "Hello World"]
   ```

* **FROM** – Defines the base of the image you are creating. You can start from a parent image (as in the example above) or a base image. When using a parent image, you are using an existing image on which you base a new one. Using a base image means you are starting from scratch (which is exactly how you would define it: FROM scratch).
* **MAINTAINER** – Specifies the author of the image. Here you can type in your first and/or last name (or even add an email address). You could also use the LABEL instruction to add metadata to an image.
* **RUN** – Instructions to execute a command while building an image in a layer on top of it. In this example, the system searches for repository updates once it starts building the Docker image. You can have more than one RUN instruction in a Dockerfile.
* **CMD** – There can be only one CMD instruction inside a Dockerfile. Its purpose is to provide defaults for an executing container. With it, you set a default command. The system will execute it if you run a container without specifying a command.

5. Save and exit the file.

6. You can check the content of the file by using the cat command:
   ```commandline
   cat Dockerfile
   ```
   
#### Step 2.3 - Build Docker Image

The basic syntax used to build an image using a Dockerfile is:
```commandline
docker build [OPTIONS] PATH | URL | -
```

To build a docker image, you would therefore use:
```commandline
docker build [location of your dockerfile]
```

If you are already in the directory where the Dockerfile is located, put a . instead of the location:
```commandline
docker build .
```

By adding the **-t** flag, you can tag the new image with a name which will help you when dealing with multiple images:
```commandline
docker build -t my_first_image .
```

**Note:** You may receive an error saying **Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker…**
This means the user does not have permission to access the Docker engine. Solve this problem by adding sudo before the command or run it as root.

Once the image is successfully built, you can verify whether it is on the list of local images with the command:
```commandline
docker images
```

The output should show **my_first_image** available in the repository.

#### Step 2.4 - Create a New Container

Launch a new Docker container based on the image you created in the previous steps. We will name the container “test” and create it with the command:
```commandline
docker run --name test my_first_image
```

The Hello World message should appear in the command line

Using **Dockerfile is a simpler and faster way of building Docker image**. It automates the process by going through the script with all the commands for assembling an image.

---
### Step 3 - Install SSH server inside Docker container
#### Step 3.1 - Copy Public Key to the Ubuntu Server
First, get the IP address of the Ubuntu server you want to connect to.

In a terminal window, enter:
```commandline
ip a
```

The system’s IP address is listed in the second entry:

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/replace-server-ip-ssh-ubuntu.png" width="80%" style='padding-top: 10px'>

On the **client** system, use the **ssh-copy-id** command to copy the identity information to the **Ubuntu server:**
```commandline
ssh-copy-id username@<server_IP>
```

Replace **server_IP** with the actual IP address of your server.

If this is the first time you’re connecting to the server, you may see a message that the authenticity of the host cannot be established:
```commandline
The authenticity of host '192.168.0.15 (192.168.0.15)' can't be established.

ECDSA key fingerprint is fd:fd:d4:f9:77:fe:73:84:e1:55:00:ad:d6:6d:22:fe.

Are you sure you want to continue connecting (yes/no)?
```

Type **yes** and press **Enter**.

The system will check your **client** system for the **id_rsa.pub** key that was previously generated. Then it will prompt you to enter the password for the **server** user account. Type it in (the system won’t display the password), and press Enter.

The system will copy the contents of the **~/.ssh/id_rsa.pub** from the client system into the **~/.ssh/authorized_keys** directory of the **server** system.

The system should display:
```commandline
Number of key(s) added: 1
```

**Alternate Method to Manually Copy the SSH Key**
If your system does not have the ssh-copy-id command, you can copy the key manually over the SSH.

Use the following command:
```commandline
cat ~/.ssh/id_rsa.pub | ssh username@remote_host "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod -R go= ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

#### Step 3.2 - Log in to the Remote Server
To log in to a remote server, input the command:
```commandline
ssh username@server_IP
```

The system should not ask for a password as it is negotiating a secure connection using the SSH keys. If you used a security passphrase, you would be prompted to enter it. After you do so, you are logged in.

**Note:** if this is the first time you’ve logged into the server, you may see a message similar to the one in **Step 3.1**. It will ask if you are sure you want to connect – type yes and press Enter.

#### Step 3.3 - Disable Password Authentication
This step creates an added layer of security. If you’re the only person logging into the server, you can disable the password. The server will only accept a login with your private key to match the stored public key.

Edit the sshd_config file:
```commandline
sudo nano /etc/ssh/sshd_config
```

Search the file and find the PasswordAuthentication option.

Edit the file and change the value to no:
```commandline
...
PasswordAuthentication no
...

```

Save the file and exit, then restart the SSH service:
```commandline
sudo systemctl restart ssh
```

Verify that SSH is still working before ending the session:
```commandline
ssh username@server_IP
```

If everything works, we can continue to the next step.

---
### Step 4 - Edit SSH Config
Edit Configuration File
After successfully installing OpenSSH on Ubuntu, you can edit its configuration file.

You can **change the default port** (generally a good idea, as a precautionary security measure), disable the “root ” user or make other configuration adjustments.

1. Open your SSH configuration file with the command:
   ```commandline
   sudo gedit /etc/ssh/sshd_config
   ```
   
   <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/open-ssh-configuration-file.png" width="80%" style='padding-top: 10px'>
   
   **Gedit** is a text editor which comes by default in Ubuntu, but you can also use other text editors such as **nano**. If you prefer using nano, you can easily install it by running the following command:
   ```commandline
   sudo apt-get install nano
   ```

2. When prompted, type in your password and press y (yes) to permit the installation.)

3. Then replace “gedit ” with “nano” type in the command:
   ```commandline
   sudo nano /etc/ssh/sshd_config
   
   ```

4. Now that you have opened the file (using any of the text editors recommended above) find and make any necessary changes.

For example, if you wish to change the port number to listen on TCP port 2222 instead of the default TCP port 22, find the line in which Port 22 is specified by default, and change it to Port 2222.

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-configuration-file.png.png" width="80%" style='padding-top: 10px'>

If you have decided to change the default port number, you must configure your firewall to allow traffic via the specified port.

The default firewall configurations tool in Ubuntu is **UFW**, configure it with the command:
```commandline
sudo ufw allow from any to any port 2222 proto tcp
```

Some firewalls may require allowing traffic to the public IP address of the machine running SSH.

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-04-additionals/part-12-remote-developing-with-docker/media/ssh-configure-firewall.png" width="80%" style='padding-top: 10px'>

**Note:** The **“p2222”** is the port number we have defined in the Configure SSH section. If you used the **default port 22**, then it is not necessary to put the port number.

---
### Step 5 - Connect to SSH server from PyCharm