__version__ = "0.0.1a1"
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
                if not task[3]:
                    task[0](*task[1], **task[2])
                else:
                    Imports.Thread(target=task[0], args=task[1], kwargs=task[2]).start()
                if self.maxRateLimitWaitDuration >= self.minRateLimitWaitDuration: Imports.sleep(self.maxRateLimitWaitDuration)
        self.__workerIdle = True


    def queueAction(self, function, priority:int=0, threaded: bool = False, *args, **kwargs):
        """
        Queue a new function to be executed
        :param function:
        :param priority:
        :param threaded:
        :return:
        """
        if not callable(function): return print("Please pass a callable object as the `function` parameter...")
        if priority in self.__tasks: self.__tasks[priority].append([function, args, kwargs, threaded])
        else: self.__tasks[priority] = [[function, args, kwargs, threaded]]
        Imports.Thread(target=self.__startExecution).start()
