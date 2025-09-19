from sys import argv
from modules.file_manager import FileManager

class Tools:
    def __init__(self):
        args = ['-c']
        if argv:
            for arg in argv[1:]:
                if not arg in args:
                    break
                self.exec_tools(arg)

    def exec_tools(self, tool_name: str, *args, **kwargs):
        if tool_name == "-c":
            FileManager.clean_output_directory()