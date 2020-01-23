import os.path as osp
import logging


logging.basicConfig(level=logging.INFO,
                    handlers=[
                    logging.FileHandler(osp.join("log", "log.txt")),
                    logging.StreamHandler()
                    ])
log = logging.getLogger()



class Config:
    BASE_DIR = osp.realpath('.')
    STATIC_DIR = osp.join(BASE_DIR, 'static')
    EMPLOYEES_DIR = osp.join(BASE_DIR, 'employees')

    @staticmethod
    def employee_img_path(name): return osp.join(Config.EMPLOYEES_DIR, name, f"{name}.jpg")
    
    @staticmethod
    def employee_encoded_img_path(name): return osp.join(Config.EMPLOYEES_DIR, name, f"{name}.npy")
    
    @staticmethod
    def employee_data_path(name): return osp.join(Config.EMPLOYEES_DIR, name, f"{name}.json")
        
    