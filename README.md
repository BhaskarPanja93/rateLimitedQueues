# rateLimitedQueues v0.0.2

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
from rateLimitedQueues import Manager

rateLimiter = Manager(timeBetweenExecution=1, smallestWaitTime=0)

def mainFunction(url, headers, json, *args, **kwargs):
    sleep(1)
    print(args, kwargs)


for _ in range(10):
    rateLimiter.queueAction(mainFunction, postFunction=functionToCallAfterMainFunction, postKwArgs={"kwarg1":True, "kwarg2": 20},
                            executePriority=3, executeThreaded=False,
                            'https://www.google.com',
                            headers={'Authorization': "Bearer 1234"},
                            json={})
```


###### <br>This project is always open to suggestions and feature requests.