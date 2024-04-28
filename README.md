# rateLimitedQueues v0.0.1a3

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

rateLimiter = Manager()

def functionToCall(a, b, c, d, *args, **kwargs):
    sleep(2)
    print(a, b, c, d, args, kwargs)


for _ in range(10):
    rateLimiter.queueAction(functionToCall, randrange(1,5), True, 1, 2, 3, 4, 5, c=10, d=12, e=60)

```


###### <br>This project is always open to suggestions and feature requests.