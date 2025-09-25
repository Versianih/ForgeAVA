class Setup:
    @staticmethod
    def run():
        from modules.file_manager import FileManager
        from modules.env_manager import EnvManager
        FileManager.create_output_or_pass()
        EnvManager.create_env_or_pass()