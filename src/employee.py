import numpy as np
from PIL import Image
import os.path as osp
import os
import json
from src.config import Config, log



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
        self.out_timestamp = None
        
        self.load_encoding()
        self.load_data()
        log.info("Employee named {} was loaded".format(self.name))

    def save_data(self):
        log.info("Saving {}'s data".format(self.name))
        with open(self.data_path, 'w') as file:
            json.dump(self.data, file)


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
            return
        self.encoded_face = np.load(self.encoded_img_path)

    def save_encoded_face(self):
        log.info("Saving {}'s face encoding".format(self.name))
        if self.encoded_face:
            np.save(self.encoded_img_path, self.encoded_face)


    def add_timestamp(self):
        if not self.in_timestamp:
            log.info("Welcome to work {}!".format(self.name))




class Employees_manager:
    def __init__(self):
        self.conf = Config()
        self.employees_dir = self.conf.EMPLOYEES_DIR 
        self.employees = []
        self.load_employees()


    def load_employees(self):
        log.info(f"Getting all existed employees")
        
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







