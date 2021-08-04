
## **Part 1 — Hello world! [From your Python script to Supervisely APP]**  
<br/>
</div>


In this part, we will show you how you can turn any Python code into a Supervisely application.


### Step 1 — Python code


Let's start with a simple python code.  

<br/>  

**src/main.py**
```python
worlds = ['Westeros', 'Azeroth', 'Middle Earth', 'Narnia']

for world in worlds:
    print(f'Hello {world}!')

```
<br/>

### Step 2 — Configuration file


Config file. **We**. **Need**. **It**.  
To add a Python application to Supervisely, let's create a configuration file for it. An example of a config file:

<br/>  

**config.json**
```json
{
  "name": "Hello world!",
  "type": "app",
  "categories": [
    "quickstart"
  ],
  "description": "There will be some description",
  "docker_image": "supervisely/base-py-sdk:6.1.93",
  "main_script": "chapter-01-headless/part-01-hello-world/src/main.py",
  "task_location": "workspace_tasks",
  "isolate": true,
  "icon": "https://img.icons8.com/color/100/000000/1.png",
  "icon_background": "#FFFFFF"
}
```

<br/>

**Pay attention to important fields:**
* docker_image — SDK version you were using, it doesn't matter in this app
* main_script — path from repository `root` to `main.py` (entry point)



### Step 3 — Create repository


We've almost reached the finish line!
In this step, we create a repository and add our code to it.

There are simple [instructions here](https://docs.supervise.ly/enterprise-edition/advanced-tuning/private-apps).

If the application is not displayed in Private apps, then you should check Refresh Ecosystem Log (in Tasks).


### Step 4 — Run our app and check output!

Let's take a look at the results of our efforts. Done!

-demo .gif / video [part 1] [created]-
