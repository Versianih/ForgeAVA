from sys import argv
from modules.file_manager import FileManager
from modules.setup import Setup

class Tools:
    def __init__(self):
        args = ['-c', '-s']
        if argv:
            for arg in argv[1:]:
                if not arg in args:
                    break
                self.exec_tools(arg)

    def exec_tools(self, tool_name: str, *args, **kwargs):
        match tool_name:
            case "-c":
                FileManager.clean_output_directory()
            case "-s":
                Setup().run()