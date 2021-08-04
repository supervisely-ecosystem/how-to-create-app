
<div align="left" markdown>

## **Part 4 — SDK Preview [Lemons counter app]**  
<br/>
</div>  

In this part, we will load a project from the Ecosystem and count the number of annotated lemons.

We have a powerful SDK for this task. Let's touch it gently?


### Step 1 — About states

Have you heard about the state machine? It is the same.
State fields help the application core store lightweight data and pass it to Python as needed.


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
