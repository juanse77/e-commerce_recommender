import yaml
from yaml.loader import SafeLoader

#from pydantic import BaseModel

class Configuration():
    instance:list = []
    
    def __init__(self, data:dict):
        self.DATA = data["DATA"]
        self.MODEL = data["MODEL"]
        self.FILTERED_TRAIN_DATA = data["FILTERED_TRAIN_DATA"]
        self.FREQUENT_MATRIX = data["FREQUENT_MATRIX"]
        self.MODEL_FILE_NAME = data["MODEL_FILE_NAME"]
        self.RECOMMENDATION_FILE_NAME = data["RECOMMENDATION_FILE_NAME"]
        self.N_ITEMS = data["N_ITEMS"]
        self.CAT_FIELDS = data["CAT_FIELDS"]
        self.SUBSET_FIELDS = data["SUBSET_FIELDS"]
    
    @classmethod
    def get_instance(cls):

        if len(cls.instance) == 0:
            with open('configuration.yaml') as f:
                data = yaml.load(f, Loader=SafeLoader)
        
            cls.instance.append(cls(data))
        
        return cls.instance[0]

def get_conf() -> Configuration:
    return Configuration.get_instance()