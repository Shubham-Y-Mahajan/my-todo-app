import sys
from PyQt6.QtWidgets import QApplication
from Windows.A_Homepage import HomePage

app = QApplication(sys.argv)
home_window = HomePage()
home_window.show()

sys.exit(app.exec())

"""DEVELOPMENT VERSION"""


"""
todo - room availability toggle karna ( json mod hi karlo ?, naya table banana padega ) [ nahi banaunga ] 

"""





