import os.path as osp
import os
import logging
from time import strftime
from datetime import datetime


logging.basicConfig(level=logging.INFO,
                    handlers=[
                    logging.FileHandler(osp.join("log", "log.txt")),
                    logging.StreamHandler()
                    ])
log = logging.getLogger()



class Config:
    # Directories
    BASE_DIR = osp.realpath('.')
    STATIC_DIR = osp.join(BASE_DIR, 'static')
    EMPLOYEES_DIR = osp.join(BASE_DIR, 'employees')
    ARCHIVE_DIR = osp.join(BASE_DIR, 'archive')
    
    # Time formattings
    DDYYMM_FRMT = "%d-%m-%Y"
    DDYYMMHHMMSS_FRMT = "%d-%m-%Y_%H-%M-%S"
    HHMMSS_FRMT = '%H:%M:%S'
    CLEANUP_TIME = "23:59:59"

    # dictionaries keys
    IN_KEY = "CHECKIN"
    OUT_KEY = "CHECKOUT"

    @staticmethod
    def employee_img_path(name): 
        return osp.join(Config.EMPLOYEES_DIR, name, "{}.jpg".format(name))
    

    @staticmethod
    def employee_encoded_img_path(name): 
        return osp.join(Config.EMPLOYEES_DIR, name, "{}.npy".format(name))
    

    @staticmethod
    def employee_data_path(name): 
        return osp.join(Config.EMPLOYEES_DIR, name, "{}.json".format(name))
        

    @staticmethod
    def employee_archive_checkin_path(name, timestamp): 
        path_frmt = osp.join(Config.ARCHIVE_DIR, name, Config.DDYYMMHHMMSS_FRMT + "_IN.jpg")
        os.makedirs(osp.dirname(path_frmt), exist_ok=True)
        return timestamp.strftime(path_frmt)
    

    @staticmethod
    def employee_archive_checkout_path(name, timestamp):
        path_frmt = osp.join(Config.ARCHIVE_DIR, name, Config.DDYYMMHHMMSS_FRMT + "_OUT.jpg")
        return timestamp.strftime(path_frmt)


    @staticmethod
    def is_timestamp_today(timestamp): 
        return datetime.now().strftime(Config.DDYYMM_FRMT) ==  timestamp.strftime(Config.DDYYMM_FRMT)
    
    
    @staticmethod
    def get_daily_key(timestamp): 
        return timestamp.strftime(Config.DDYYMM_FRMT)


    @staticmethod
    def get_cleanup_time(): 
        return datetime.strptime(Config.CLEANUP_TIME, Config.HHMMSS_FRMT)

