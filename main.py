
from src.employee import Employee, Employees_manager
from src.recognizer import Recognizer
from src.config import log                  

log.info("Begin!")
manager = Employees_manager()
employees = manager.get_employees()
recognizer = Recognizer(employees)
recognizer.run()
