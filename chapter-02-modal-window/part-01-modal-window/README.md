
<div align="left" markdown>

## **Part 1 — Modal window [What is it?]**  
<br/>
</div>  

The modal window in Supervisely appears after clicking on the launch button of the application.
It can be used for at least two things:

1. **to inform the user**
2. **to enter arguments**

In this part, we will create a basic application with modal window.  
We will use the modal window as an **information board**.


1. <a href="#step-1--html-file">HTML file</a>
2. <a href="#step-2--results">Results</a>


---
### Step 1 — HTML file

We use HTML to create the UI.

📝 **you can preview your HTML in [our Application Designer](https://app.supervise.ly/apps/designer)**

Here's our modal window:


**src/modal.html**  
```HTML
<div>
    <h3>This is my first modal window app.</h3>
</div>
```

Simple. Isn't?  
Now let's add it to our config file:


**config.json**  
```json
{
  "name": "Modal Window",
  "type": "app",
  "categories": [
    "quickstart"
  ],
  "description": "There will be some description",
  "docker_image": "supervisely/base-py-sdk:6.1.93",
  "main_script": "chapter-02-headless/part-01-modal-window/src/main.py",
  "modal_template": "chapter-02-headless/part-01-modal-window/src/modal.html",
  "task_location": "workspace_tasks",
  "icon": "https://img.icons8.com/color/100/000000/1.png",
  "icon_background": "#FFFFFF"
}

```

---
### Step 2 — Results



<a data-key="sly-embeded-video-link" href="https://youtu.be/yHV4pUhO1DQ" data-video-code="yHV4pUhO1DQ">
    <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-02-modal-window/part-05-modal-window/media/video-preview.png" alt="SLY_EMBEDED_VIDEO_LINK"  style="max-width:100%;">
</a>


