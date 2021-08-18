
<div align="left" markdown>

## **Part 5 — Integrate to Videos Annotator [OpenCV Tracker]**  

</div>  

In this part, we will learn how to integrate **any tracker** into **Videos Annotator**.


1. <a href="#step-1--videos-annotator">Videos Annotator?</a>
2. <a href="#step-2--trackers">Trackers</a>
3. <a href="#step-3--creating-the-app">Creating the APP</a>
4. <a href="#step-4--"></a>


---
### Step 1 — Videos Annotator?

Ok. This is the video annotation software available in Supervisely.  
To launch the Annotator, click on the videos dataset. Done!

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-01-headless/part-05-integrate-to-videos-annotator/media/1-1.png" width="80%" style='padding-top: 10px'>   

---   
<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-01-headless/part-05-integrate-to-videos-annotator/media/1-2.png" width="80%" style='padding-top: 10px'>

---
### Step 2 — Trackers

Supervisely has **two types** of tracking algorithms:
1. **Predefined**
2. **Apps**

They become available when you select the marked object.  
In this part, we will integrate our own tracker (**Apps**).

<img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-01-headless/part-05-integrate-to-videos-annotator/media/2-1.png" width="80%" style='padding-top: 10px'>  


---
### Step 3 — Creating the APP

#### 1. Add session tag to config

In order for the video annotator to see our application, we link it through the **sessions tags** space.  
⚠️ Only through the `sly_video_tracking` tag will Videos Annotator see our application. So:

**config.json (partially)**

```json
"session_tags": [
  "sly_video_tracking"
]

```

#### 2. Handle track command

How to handle commands — [see here](https://github.com/supervisely-ecosystem/how-to-create-app/tree/master/chapter-03-ui/part-03-app-handlers#step-1--handle-html-events).  
The most important thing is to write a handler for the **track command**.

**src/main.py (partially)**

```python
@g.my_app.callback("track")
@sly.timeit
@send_error_data
def track(api: sly.Api, task_id, context, state, app_logger):
    tracker = TrackerContainer(context)
    tracker.track()

```

The OpenCV tracker logic is described [here](https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-01-headless/part-05-integrate-to-videos-annotator/src/tracker.py#L42-L100).  
**You can replace it with your own code (your own tracker)**.

---
### Step 4 — Results

`in develop 🧑🏼‍💻`
