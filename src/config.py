import os.path as osp
import os
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
    ARCHIVE_DIR = osp.join(BASE_DIR, 'archive')

    @staticmethod
    def employee_img_path(name): return osp.join(Config.EMPLOYEES_DIR, name, "{}.jpg".format(name))
    
    @staticmethod
    def employee_encoded_img_path(name): return osp.join(Config.EMPLOYEES_DIR, name, "{}.npy".format(name))
    
    @staticmethod
    def employee_data_path(name): return osp.join(Config.EMPLOYEES_DIR, name, "{}.json".format(name))
        
    @staticmethod
    def employee_archive_in_path(name): 
        archive_emp_dir = osp.join(Config.ARCHIVE_DIR, name)
        os.makedirs(archive_emp_dir, exist_ok=True)
        return osp.join(archive_emp_dir, "%d-%m-%Y_%H-%M-%S_IN.jpg")
    
    @staticmethod
    def employee_archive_out_path(name): 
        return osp.join(Config.ARCHIVE_DIR, name, "%d-%m-%Y_%H-%M-%S_OUT.jpg")
    