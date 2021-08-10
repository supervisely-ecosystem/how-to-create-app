
<div align="left" markdown>

## **Part 9 — APP Handlers [Handle Events and Errors]**  
<br/>
</div>  

In this part, we will introduce you to app handlers and tell you what they are for.


1. <a href="#step-1--handle-html-events">Handle HTML events</a>
2. <a href="#step-2--dialog-window-instead-of-an-error">Dialog window instead of an error</a>
3. <a href="#step-3--results">Results</a>


---
### Step 1 — Handle HTML events

How do I make the IU buttons work?  
It's very simple.  
In the HTML file, I will create a button that invokes the command on **click**:

**src/gui.html** (partially)
```HTML
<div>
	<el-button
		type="success"
	    	@click="command('normal_handler')">
        		Call normal handler
	 </el-button>
</div>

```

In Python code I will handle this command using callback handler

**src/main.py** (partially)
```python
@app.callback('normal_handler')
def normal_handler(api: sly.Api, task_id, context, state, app_logger):
```

This callback is triggered if the command name matches the name of the callback parameter.  
**Arguments that come to the input:**
* api — api the object of the user who called the callback
* task_id — app task_id
* context — information about the environment in which the application is running
* state — state of all widgets in Python dict format
* app_logger — sly_logger with task_id

---
### Step 2 — Dialog window instead of an error

Sometimes we want the application not to crash  after an error occurs.  
Therefore, we can use `app.ignore_errors_and_show_dialog_window()`
handler:

**src/main.py** (partially)
```python
@app.callback('error_handler')
@app.ignore_errors_and_show_dialog_window()
def error_handler(api: sly.Api, task_id, context, state, app_logger):
    logger.info('normal handler called')
    raise SystemError('there could be an error message here')


```

---
### Step 3 — Results

Let's run the application and see what we get.

<a data-key="sly-embeded-video-link" href="https://youtu.be/U2XtONhiZaw" data-video-code="U2XtONhiZaw">
    <img src="https://github.com/supervisely-ecosystem/how-to-create-app/blob/master/chapter-03-ui/part-09-app-handlers/media/video-preview.png" alt="SLY_EMBEDED_VIDEO_LINK"  style="max-width:100%;">
</a>
