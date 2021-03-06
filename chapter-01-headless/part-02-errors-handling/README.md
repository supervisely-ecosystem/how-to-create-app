
## **Part 2 — Errors handling [Catching all bugs]**
<br/>
</div>


In this part, we will work with bugs. We will catch them.

1. <a href="#step-1--supervisely-logger">Supervisely logger</a>
2. <a href="#step-2--use-try-except-with-traceback">Use [try: except] with traceback</a>
3. <a href="#step-3--results">Results</a>



---
### Step 1 — Supervisely logger

Supervisely has a logger. It is a wrapper over Python's built-in [logging](https://docs.python.org/3/howto/logging.html) package.

First thing we need to do is install Supervisely Python SDK to your environment:
<br/>

`pip install supervisely`
<br/>

Let's take the code from Part 1 as a basis and add a logger:  



``` python
import supervisely_lib as sly

worlds = ['Westeros', 'Azeroth', 'Middle Earth', 'Narnia']

sly_logger = sly.logger

for world in worlds:
    sly_logger.info(f'Hello {world}!')
```

---
### Step 2 — Use [try: except] with traceback

To handle errors, you can use the `[try: except]` construction



**src/main.py**
``` python
import supervisely_lib as sly

worlds = ['Westeros', 'Azeroth', 'Middle Earth', 'Narnia']

sly_logger = sly.logger

try:
    for world in worlds:
        sly_logger.info(f'Hello {world}!')

    if 'Our World' not in worlds:
        raise ValueError(f"Can't find Our World")

except Exception as ex:
    sly_logger.warning(ex)
```


---
### Step 3 — Results



<a data-key="sly-embeded-video-link" href="https://youtu.be/MMcNsW3wI_I" data-video-code="MMcNsW3wI_I">
    <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-01-headless/part-02-errors-handling/media/video-preview.png" alt="SLY_EMBEDED_VIDEO_LINK"  style="max-width:100%;">
</a>
