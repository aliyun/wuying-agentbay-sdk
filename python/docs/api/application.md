# Application Class

The Application class provides methods for managing applications in the AgentBay cloud environment, including listing installed applications, starting applications, and stopping running processes.

## Class Properties

###

```python
class Application:
    def __init__(self, session):
        self.session = session
```

## Data Types


Represents an installed application.


```python
class InstalledApp:
    name: str          # The name of the application
    start_cmd: str     # The command used to start the application
    stop_cmd: str      # The command used to stop the application (optional)
    work_directory: str # The working directory for the application (optional)
```


```python
class Process:
    pname: str    # The name of the process
    pid: int      # The process ID
    cmdline: str  # The command line used to start the process (optional)
```


```python
def get_installed_apps(self, include_system_apps: bool = True, include_store_apps: bool = False, include_desktop_apps: bool = True) -> List[InstalledApp]:
```

**Parameters:**
- `include_system_apps` (bool, optional): Whether to include system applications. Default is True.
- `include_store_apps` (bool, optional): Whether to include store applications. Default is False.
- `include_desktop_apps` (bool, optional): Whether to include desktop applications. Default is True.

**Returns:**
- `List[InstalledApp]`: A list of installed applications.

**Raises:**
- `ApplicationError`: If there's an error retrieving the installed applications.


```python
def start_app(self, start_cmd: str, work_directory: str = "") -> List[Process]:
```

**Parameters:**
- `start_cmd` (str): The command used to start the application.
- `work_directory` (str, optional): The working directory for the application. Default is an empty string.

**Returns:**
- `List[Process]`: A list of processes started.

**Raises:**
- `ApplicationError`: If there's an error starting the application.


```python
def stop_app_by_pname(self, pname: str) -> bool:
```

**Parameters:**
- `pname` (str): The name of the process to stop.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `ApplicationError`: If there's an error stopping the application.


```python
def stop_app_by_pid(self, pid: int) -> bool:
```

**Parameters:**
- `pid` (int): The process ID to stop.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `ApplicationError`: If there's an error stopping the application.


```python
def stop_app_by_cmd(self, stop_cmd: str) -> bool:
```

**Parameters:**
- `stop_cmd` (str): The command used to stop the application.

**Returns:**
- `bool`: True if the operation was successful, False otherwise.

**Raises:**
- `ApplicationError`: If there's an error stopping the application.


```python
def list_visible_apps(self) -> List[Process]:
```

**Returns:**
- `List[Process]`: A list of visible processes.

**Raises:**
- `ApplicationError`: If there's an error listing the visible applications.
