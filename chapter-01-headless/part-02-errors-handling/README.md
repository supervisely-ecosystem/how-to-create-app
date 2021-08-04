
## **Part 2 — Errors handling [Catching all bugs]**
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
