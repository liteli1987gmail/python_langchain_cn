# File System Tools

LangChain provides tools for interacting with a local file system out of the box. This notebook walks through some of them.

Note: these tools are not recommended for use outside a sandboxed environment! 

First, we'll import the tools.


```python
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
from langchain.agents.agent_toolkits import FileManagementToolkit
from tempfile import TemporaryDirectory

# We'll make a temporary directory to avoid clutter
working_directory = TemporaryDirectory()
```

## The FileManagementToolkit

If you want to provide all the file tooling to your agent, it's easy to do so with the toolkit. We'll pass the temporary directory in as a root directory as a workspace for the LLM.

It's recommended to always pass in a root directory, since without one, it's easy for the LLM to pollute the working directory, and without one, there isn't any validation against
straightforward prompt injection.


```python
toolkit = FileManagementToolkit(
    root_dir=str(working_directory.name)
)  # If you don't provide a root_dir, operations will default to the current working directory
toolkit.get_tools()
```




    [CopyFileTool(name='copy_file', description='Create a copy of a file in a specified location', args_schema=<class 'langchain.tools.file_management.copy.FileCopyInput'>, return_direct=False, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root_dir='/var/folders/gf/6rnp_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),
     DeleteFileTool(name='file_delete', description='Delete a file', args_schema=<class 'langchain.tools.file_management.delete.FileDeleteInput'>, return_direct=False, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root_dir='/var/folders/gf/6rnp_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),
     FileSearchTool(name='file_search', description='Recursively search for files in a subdirectory that match the regex pattern', args_schema=<class 'langchain.tools.file_management.file_search.FileSearchInput'>, return_direct=False, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root_dir='/var/folders/gf/6rnp_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),
     MoveFileTool(name='move_file', description='Move or rename a file from one location to another', args_schema=<class 'langchain.tools.file_management.move.FileMoveInput'>, return_direct=False, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root_dir='/var/folders/gf/6rnp_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),
     ReadFileTool(name='read_file', description='Read file from disk', args_schema=<class 'langchain.tools.file_management.read.ReadFileInput'>, return_direct=False, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root_dir='/var/folders/gf/6rnp_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),
     WriteFileTool(name='write_file', description='Write file to disk', args_schema=<class 'langchain.tools.file_management.write.WriteFileInput'>, return_direct=False, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root_dir='/var/folders/gf/6rnp_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),
     ListDirectoryTool(name='list_directory', description='List files and directories in a specified folder', args_schema=<class 'langchain.tools.file_management.list_dir.DirectoryListingInput'>, return_direct=False, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root_dir='/var/folders/gf/6rnp_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug')]



### Selecting File System Tools

If you only want to select certain tools, you can pass them in as arguments when initializing the toolkit, or you can individually initialize the desired tools.


```python
tools = FileManagementToolkit(
    root_dir=str(working_directory.name),
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()
tools
```




    [ReadFileTool(name='read_file', description='Read file from disk', args_schema=<class 'langchain.tools.file_management.read.ReadFileInput'>, return_direct=False, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root_dir='/var/folders/gf/6rnp_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),
     WriteFileTool(name='write_file', description='Write file to disk', args_schema=<class 'langchain.tools.file_management.write.WriteFileInput'>, return_direct=False, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root_dir='/var/folders/gf/6rnp_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),
     ListDirectoryTool(name='list_directory', description='List files and directories in a specified folder', args_schema=<class 'langchain.tools.file_management.list_dir.DirectoryListingInput'>, return_direct=False, verbose=False, callback_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root_dir='/var/folders/gf/6rnp_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug')]




```python
read_tool, write_tool, list_tool = tools
write_tool.run({"file_path": "example.txt", "text": "Hello World!"})
```




    'File written successfully to example.txt.'




```python
# List files in the working directory
list_tool.run({})
```




    'example.txt'




```python

```
