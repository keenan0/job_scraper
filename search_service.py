import importlib

class Context:
    def __init__(self, module):
        self.module = module
    def set_strategy(self, module):
        self.module = module
    def execute(self):
        importlib.import_module(self.module)

if __name__ == "__main__":
    Context("hipo_service").execute()



