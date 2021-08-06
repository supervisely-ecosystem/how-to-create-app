
<div align="left" markdown>

## **Part 9 — APP Handlers [Handle Events and Errors]**  
<br/>
</div>  

In this part, we will introduce you to app handlers and tell you what they are for.

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

In Python code I will handle this command using callback handler:

**src/main.py** (partially)
```python
@app.callback('normal_handler')
def normal_handler(api: sly.Api, task_id, context, state, app_logger):
    logger.info('normal handler called')

```

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

### Step 3 — Results

Let's run the application and see what we get.

`gif run app and show buttons results`