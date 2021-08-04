<div align="center" markdown>

# **Content**

</div>


1. Headless apps (without UI)  

	1.1. Hello world! — From your Python script to Supervisely APP [part 1]  
	* Run you Python script in Supervisely
	* Describe app config.json
	* How to integrate into Supervisely (later)
	* How to run? (later)  
	
	1.2. Error handling — Catching all bugs [part 2]  
	* Supervisely Logger
	* Use [try:catch] with traceback
	* Error in task output  
	
	
	1.3. Site Packages — Customize your app [part 3]  
	* requirements.txt — add some package and print text at the end 

	1.4. SDK Preview — Objects counter app [part 4]  
	* Environment files
	* Print objects count for every class in project
	* Link notebooks (more examples)
	* Link to full SDK docs


<div align="center" markdown>
<br/>  

# **Let's rock**

</div>

## 1. Introduction  
Applications in Supervisely are key to solving highly specialized computer vision problems. In the application catalog (Ecosystem) you can find applications for many different tasks. We have provided the ability to create new applications by third-party developers and modify existing ones.

This guide is designed to help a Python programmer develop, debug, and integrate applications in Supervisely.



## 2. Quickstart guide  

---

<div align="center" markdown>

# Chapter 1 — Apps without UI [Headless]


</div>

---

## [Part 1 — Hello world! [From your Python script to Supervisely APP]](/%5Bchapter%201%5D%20headless/%5Bpart%201%5D%20Hello%20world!/README.md)

---

<div align="center" markdown>

## **Part 2 — Error handling [Catching all bugs]**
<br/>
</div>


In this part, we will work with bugs. We will catch them.


### Step 1 — Supervisely logger

Supervisely has a logger. It is a wrapper over Python's built-in [logging](https://docs.python.org/3/howto/logging.html) package.

First thing we need to do is install Supervisely Python SDK to your environment:

`pip install supervisely`

Let's take the code from Part 1 as a basis and add a logger:

-main.py code [part 2]-


### Step 2 — Use [try:catch] with traceback

To handle errors, you can use the [try: catch] construction

-main.py code [part 3]-


### Step 3 — Viewing the log in task output


Let's add our application to Supervisely and check the results.


-demo .gif / video [part 2] [not created]-


---


<div align="center" markdown>

## **Part 3 — Site Packages [Customize your app]**  
<br/>
</div>

In Supervisely applications, we have provided the ability to add site-packages.  
To add third-party site-packages to your application, all you need to do next steps:


### Step 1 — Create requirements.txt file in application root


-screenshot-


### Step 2 — Add a list of all required libraries with versions


-screenshot-


### Step 3 — Results

-main.py [part 3]-

-demo .gif / video [part 3] [not created]-



---


<div align="center" markdown>

## **Part 4 — SDK Preview [Lemons counter app]**  
<br/>
</div>  

In this part, we will load a project from the Ecosystem and count the number of annotated lemons.

We have a powerful SDK for this task. Let's touch it gently?


### Step 1 — Clone Lemons (Annotated) project from Ecosystem

-gif or video-

### Step 2 — Environments files

For our convenience, let's make two files in application directory: \
debug.env and secret_debug.env

We will add constants to these files to access the Supervisely SDK

-debug.env file preview-


-secret_debug.env file preview-



### Step 3 — Python script

Let's write a simple script that:



1. loads the project
2. retrieves annotations
3. counts the number of lemons

Here is the completed code: \
-main.py [part 4]-


### Step 4 — Complete SDK documentation

[Learn SDK Basics with IPython Notebooks](https://sdk.docs.supervise.ly/rst_templates/notebooks/notebooks.html)  
[Complete Python SDK](https://sdk.docs.supervise.ly/sdk_packages.html)
