__version__ = "0.0.3rev1"
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
                import subprocess
                from pip._internal.utils.entrypoints import (
                    get_best_invocation_for_this_pip,
                    get_best_invocation_for_this_python,
                )
                from pip._internal.utils.compat import WINDOWS
                if WINDOWS:
                    pip_cmd = f"{get_best_invocation_for_this_python()} -m pip"
                else:
                    pip_cmd = get_best_invocation_for_this_pip()
                subprocess.run(f"{pip_cmd} install {__packagename__} --upgrade")
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
    from time import sleep, time
    from threading import Thread
    from typing import Callable
    class Executable:
        def __init__(self, manager, mainFunction, mainThreaded:bool, args=None, kwargs=None, postFunction=None, postThreaded:bool=None, postArgs=None, postKwArgs=None):
            self.manager = manager
            self.mainThreaded = mainThreaded
            self.main = mainFunction
            self.post = postFunction
            self.postThreaded = postThreaded
            self.mainArgs = args
            self.mainKwArgs = kwargs
            self.postArgs = postArgs
            self.postKwArgs = postKwArgs
            self.response = None
            self.start = 0
            self.end = 0
        def execute(self):
            self.start = Imports.time()
            self.response = self.main(*self.mainArgs, **self.mainKwArgs)
            if self.post is not None:
                self.postKwArgs["FunctionResponse"] = self.response
                if self.postThreaded: Imports.Thread(target=self.post, args=self.postArgs, kwargs=self.postKwArgs).start()
                else: self.post(*self.postArgs, **self.postKwArgs)
            self.end = Imports.time()


class RateLimitedQueues:
    def __init__(self, timeBetweenExecution:float=0):
        """
        Initialises a rate limiter cum queued event executor
        :param timeBetweenExecution: Time to wait between concurrent executions (in seconds). By default, executed immediately without any time wait.
        """
        self.__idle = True
        self.__queue:dict[int, list[Imports.Executable]] = {}
        self.__delay = timeBetweenExecution
        self.lastExecutionAt = 0

    def __executionCompleted(self):
        """
        Private function to automatically start the next function executor
        :return:
        """
        self.lastExecutionAt = Imports.time()
        self.__idle = True
        self.__executeNext()

    def __executeNext(self) -> None:
        """
        Private function to execute the next in queue, and ignore if some other function is already executing
        Handles rate limits and priorities
        :return:
        """
        if not self.__idle: return
        if self.__queue:
            while self.__queue:
                topPriority = max(self.__queue)
                if not self.__queue[topPriority]: self.__queue.pop(topPriority)
                else:
                    executable = self.__queue[topPriority].pop(0)
                    break
            else: return
            self.__idle = False
            if self.__delay > 0:
                while True:
                    toSleep = self.__delay - (Imports.time() - self.lastExecutionAt)
                    if toSleep > 0:
                        if toSleep > self.__delay: Imports.sleep(toSleep)
                        else: Imports.sleep(self.__delay)
                    else:
                        break
            if executable.mainThreaded: Imports.Thread(target=executable.execute).start()
            else: executable.execute()
            self.__executionCompleted()


    def queueAction(self, mainFunction:Imports.Callable, executeMainInThread:bool = False, executePriority:int=0, postFunction:Imports.Callable=None, executePostInThread:bool=None, postArgs:tuple=None, postKwArgs:dict=None, *args, **kwargs):
        """
        Queue here.
        :param mainFunction: The function to be run when it reaches its turn.
        :param executeMainInThread: mainFunction is executed in a new thread. If True Rate limit is calculated from the start of execution of mainFunction. If False Rate limit is calculated from ending of execution of the mainFunction
        :param executePriority: Priority for execution. High priority tasks are executed before low priority ones. There's no limit for highest or lowest value.
        :param postFunction: A second function(optional) to execute when the main function completes its execution (even if threaded). postFunction if present gets "FunctionResponse" in its kwargs which contains the value returned my mainFunction
        :param executePostInThread: postFunction is executed in a new thread. If True Rate limit is calculated from the start of execution of postFunction. If False Rate limit is calculated from ending of execution of the postFunction
        :param postArgs: Arguments to pass only to the postFunction. Must be a tuple.
        :param postKwArgs: Keyword-Arguments to pass only to the postFunction. Must be a dictionary.
        :param args: All additional arguments to be passed to mainFunction
        :param kwargs: All additional keyword-arguments to be passed to mainFunction
        :return:
        """
        if not callable(mainFunction): return print("Please pass a callable object as the `mainFunction` parameter...")
        if postFunction is not None and not callable(postFunction): return print("Please pass a callable object as the `postFunction` parameter...")
        if postArgs is not None and type(postArgs)!=tuple: return print("Please pass a tuple as postArgs...")
        if postKwArgs is not None and type(postKwArgs)!=dict: return print("Please pass a dictionary as postKwArgs...")
        executable = Imports.Executable(self, mainFunction, executeMainInThread, args, kwargs, postFunction, executePostInThread, postArgs, postKwArgs)
        if executePriority not in self.__queue: self.__queue[executePriority] = []
        self.__queue[executePriority].append(executable)
        Imports.Thread(target=self.__executeNext).start()
