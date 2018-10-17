from console_interface.main_menu import Menu
from db.db import Database

db = Database()
db.connect('lab1')
m = Menu(db)
m.main_loop()