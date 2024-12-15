# rateLimitedQueues v0.0.3rev1

```pip install rateLimitedQueues --upgrade```


###### <br>A well maintained program to execute functions in queue as if only 1 worker is executing them one by one (High priority first). Works wonders when a series of time consuming tasks has to be performed but they need to be in sequence.

<br>To install: 
```
pip install rateLimitedQueues --upgrade
pip3 install rateLimitedQueues --upgrade
python -m pip install rateLimitedQueues --upgrade
python3 -m pip install rateLimitedQueues --upgrade
```


#### <br><br>Using this program is as simple as:
```
from rateLimitedQueues import RateLimitedQueues

rateLimiter = RateLimitedQueues()

def mainFunction(n, *args, **kwargs):
    sleep(1)
    print(args, kwargs)

def postFunction(*args, **kwargs):
    sleep(1)
    print(args, kwargs)

for i in range(10):
    rateLimiter.queueAction(mainFunction=mainFunction, executeMainInThread=True, executePostInThread=True, 
    postFunction=postFunction, postArgs=(i,), postKwArgs={i: i**2}, n=i)

```


###### <br>This project is always open to suggestions and feature requests.