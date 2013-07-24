import queryt
import time
import os
path = os.path.dirname(os.path.abspath(__file__))
queryt.queryt(path, 'template.sql')
time.sleep(10)