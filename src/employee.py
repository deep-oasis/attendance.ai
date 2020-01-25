import numpy as np
from PIL import Image
import os.path as osp
import os
import json
from src.config import Config, log
from time import strftime, time, sleep
from datetime import datetime
from threading import Timer



class Employee:
    def __init__(self, name):
        self.name = name
        self.conf = Config()
        self.img_path = self.conf.employee_img_path(name)  
        self.encoded_img_path = self.conf.employee_encoded_img_path(name)  
        self.data_path = self.conf.employee_data_path(name)
        self.encoded_face = None
        self.data = None
        self.in_timestamp = None
        self.last_timestamp = None

        self.load_encoding()
        log.info("Employee named {} was loaded".format(self.name))


    def save_data(self):
        log.info("Saving {}'s data".format(self.name))
        with open(self.data_path, 'w') as file:
            json.dump(self.data, file)
        del self.data


    def load_data(self):
        log.info("Loading {}'s data".format(self.name))
        if not osp.exists(self.data_path):
            log.info("No employee data was found")
            return
        with open(self.data_path, 'r') as file:
            self.data = json.load(file)


    def load_encoding(self):
        log.info("Loading {}'s face encoding".format(self.name))
        if not osp.exists(self.encoded_img_path):
            log.info("No face encoding was found")
        else: self.encoded_face = np.load(self.encoded_img_path)


    def save_encoded_face(self, encoded_face):
        log.info("Saving {}'s face encoding".format(self.name))
        self.encoded_face = encoded_face
        np.save(self.encoded_img_path, self.encoded_face)


    def save_img_to_archive(self, img_path, img):
        log.info("Saving image: {}".format(img_path))
        Image.fromarray(img).save(img_path)


    def cache_checkin(self, timestamp): 
        self.load_data()
        self.data[Config.get_daily_key(timestamp)][Config.IN_KEY] = timestamp
        self.save_data()
    
    
    def cache_checkout(self, timestamp): 
        self.load_data()
        self.data[Config.get_daily_key(timestamp)][Config.OUT_KEY] = timestamp
        self.save_data()


    def add_timestamp(self, frame, timestamp):
        self.last_frame = frame
        self.last_timestamp = timestamp
        if not self.in_timestamp or not Config.is_timestamp_today(self.in_timestamp):
            self.set_arrival()


    def set_arrival(self):
        self.in_timestamp = self.last_timestamp
        path = Config.employee_archive_checkin_path(self.name, self.in_timestamp)
        self.save_img_to_archive(path, self.last_frame)
        self.cache_checkin(self.in_timestamp)


    def set_leaving(self):
        if self.in_timestamp == self.last_timestamp:
            log.warning("Only checkin was found for {}".format(self.name))
        else: 
            path = Config.employee_archive_checkout_path(self.name, self.last_timestamp)
            self.save_img_to_archive(path, self.last_frame)
        
        self.cache_checkout(self.last_timestamp)
        self.in_timestamp = self.last_timestamp = None


class Employees_manager:
    def __init__(self):
        self.conf = Config()
        self.employees_dir = self.conf.EMPLOYEES_DIR 
        self.employees = []
        self.load_employees()
        self.cleanup_time_obj = Config.get_cleanup_time()
        self.set_timer()


    def set_timer(self):
        delta = self.cleanup_time_obj - datetime.now() 
        self.timer = Timer(delta.seconds, self.set_leavings)
        self.timer.start()


    def set_leavings(self):
        for emp in self.employees:
            emp.set_leaving()
        sleep(1)
        self.set_timer()


    def load_employees(self):
        log.info("Getting all existed employees")
        
        # Check if there is an employees dir
        if not osp.exists(self.employees_dir):
            log.info("Creating employees directory")
            os.makedirs(self.employees_dir)
        
        # Get all saved emplyees directories
        saved_employees = os.listdir(self.employees_dir)
        if not len(saved_employees): return None

        # Check if employees directories are valid. If so, add them
        for emp in saved_employees:
            img_path = osp.join(self.employees_dir, emp, "{}.jpg".format(emp))
            if osp.exists(img_path):
                self.employees.append(Employee(emp))


    def get_employees(self):
        return self.employees







