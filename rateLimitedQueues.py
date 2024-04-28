__version__ = "0.0.1a4"
__packagename__ = "rateLimitedQueues"


def updatePackage():
    from time import sleep
    from json import loads
    import http.client
    print(f"Checking updates for Package {__packagename__}")
    try:
        host = "pypi.org"
        conn = http.client.HTTPSConnection(host, 443)
        conn.request("GET", f"/pypi/{__packagename__}/json")
        data = loads(conn.getresponse().read())
        latest = data['info']['version']
        if latest != __version__:
            try:
                import pip
                pip.main(["install", __packagename__, "--upgrade"])
                print(f"\nUpdated package {__packagename__} v{__version__} to v{latest}\nPlease restart the program for changes to take effect")
                sleep(3)
            except:
                print(f"\nFailed to update package {__packagename__} v{__version__} (Latest: v{latest})\nPlease consider using pip install {__packagename__} --upgrade")
                sleep(3)
        else:
            print(f"Package {__packagename__} already the latest version")
    except:
        print(f"Ignoring version check for {__packagename__} (Failed)")


class Imports:
    from typing import Any, Callable
    from time import sleep
    from threading import Thread


class Manager:
    def __init__(self, timeBetweenExecution:float=1):
        self.__workerIdle = True
        self.__tasks:dict[int, list[list[Imports.Callable | tuple[Imports.Any] | dict[str, Imports.Any]]]] = {}
        self.defaultRateLimitWaitDuration = timeBetweenExecution
        self.maxRateLimitWaitDuration = self.defaultRateLimitWaitDuration
        self.minRateLimitWaitDuration = 0.001


    def __startExecution(self) -> None:
        """
        Private method to start executing all pending actions for current visitor. Has to be called everytime there is a new action queued
        :return:
        """
        if self.__workerIdle: self.__workerIdle = False
        else: return
        while self.__tasks:
            topPriorityTasks = self.__tasks.pop(max(self.__tasks))
            for task in topPriorityTasks:
                mainFunction, args, kwargs, executeThreaded, postFunction, postArgs, postKwArgs = task
                if postKwArgs is None: postKwArgs = {}
                if postArgs is None: postArgs = ()
                if self.maxRateLimitWaitDuration >= self.minRateLimitWaitDuration: Imports.sleep(self.maxRateLimitWaitDuration)
                if executeThreaded: Imports.Thread(target=mainFunction, args=args, kwargs=kwargs).start()
                else: postKwArgs.update({"functionResponse": mainFunction(*args, **kwargs)})
                if postFunction is not None: Imports.Thread(target=postFunction, args=postArgs, kwargs=postKwArgs).start()
        self.__workerIdle = True


    def queueAction(self, mainFunction, executePriority:int=0, executeThreaded: bool = False, postFunction = None, postArgs:tuple = None, postKwArgs:dict = None, *args, **kwargs):
        """
        Queue a new function to be executed
        :param postKwArgs:
        :param postArgs:
        :param postFunction:
        :param mainFunction:
        :param executePriority:
        :param executeThreaded:
        :return:
        """
        if not callable(mainFunction): return print("Please pass a callable object as the `mainFunction` parameter...")
        if postFunction is not None and not callable(postFunction): return print("Please pass a callable object as the `postFunction` parameter...")
        if postArgs is not None and type(postArgs)!=tuple: return print("Please pass a tuple as postArgs...")
        if postKwArgs is not None and type(postKwArgs)!=dict: return print("Please pass a dictionary as postKwArgs...")
        execList = [mainFunction, args, kwargs, executeThreaded, postFunction, postArgs, postKwArgs]
        if executePriority in self.__tasks: self.__tasks[executePriority].append(execList)
        else: self.__tasks[executePriority] = [execList]
        Imports.Thread(target=self.__startExecution).start()
