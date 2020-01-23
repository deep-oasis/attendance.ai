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
        log.info(f"Employee named {self.name} was loaded")

    def save_data(self):
        log.info(f"Saving {self.name}'s data")
        with open(self.data_path, 'w') as file:
            json.dump(self.data, file)


    def load_data(self):
        log.info(f"Loading {self.name}'s data")
        if not osp.exists(self.data_path):
            log.info("No employee data was found")
            return
        with open(self.data_path, 'r') as file:
            self.data = json.load(file)


    def load_encoding(self):
        log.info(f"Loading {self.name}'s face encoding")
        if not osp.exists(self.encoded_img_path):
            log.info("No face encoding was found")
            return
        self.encoded_face = np.load(self.encoded_img_path)

    def save_encoded_face(self):
        log.info(f"Saving {self.name}'s face encoding")
        if self.encoded_face:
            np.save(self.encoded_img_path, self.encoded_face)


    def add_timestamp(self):
        if not self.in_timestamp:
            log.info(f"Welcome to work {self.name}!")


class Employees_manager:
    def __init__(self):
        self.conf = Config()
        self.employees_dir = self.conf.EMPLOYEES_DIR 
        self.employees = []
        self.load_employees()


    def load_employees(self):
        log.info(f"Getting all existed employees")
        saved_employees = os.listdir(self.employees_dir)
        for emp in saved_employees:
            img_path = osp.join(self.employees_dir, emp, f"{emp}.jpg")
            if osp.exists(img_path):
                self.employees.append(Employee(emp))


    def get_employees(self):
        return self.employees







