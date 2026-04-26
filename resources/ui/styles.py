class Styles():
    def blue_push_button(self):
        return """QPushButton {
                background-color: #0099cc;
                color: white;
                border-radius: 10px;
                padding: 10px; /* Adjust padding */
                }
                
                QPushButton:hover {
                    background-color: #0077aa; /* Darken button on hover */
                }"""
    def green_push_button(self):
        return """QPushButton {
                background-color: #00cc00;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                }
                QPushButton:hover {
                background-color: #009900; /* Darken button on hover */
                }"""
    def red_push_button(self):
        return """QPushButton {
                background-color: #FF9999;
                color: black;
                border-radius: 10px;
                padding: 10px 20px;
                }
                QPushButton:hover {
                background-color: #CC0000; /* Darken button on hover */
                }"""
    def dark_red_push_button(self): # logout
        return """QPushButton {
                background-color: #cc3333; 
                color: white; 
                border-radius: 10px; 
                padding: 10px; }
                QPushButton:hover {
                background-color: #CC0000; /* Darken button on hover */
                }"""

    def dark_red_non_hover_button(self): # logout
        return """QPushButton {
                background-color: #cc3333; 
                color: white; 
                border-radius: 10px; 
                padding: 10px; }
                """
    def rectangle_lightgreen_button(self):
        return """QPushButton { 
                background-color: lightgreen; 
                font-size: 16px; 
                padding: 10px; }
                QPushButton:hover {
                background-color: #009900; /* Darken button on hover */
                }"""