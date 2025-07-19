import requests
import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import QTimer, Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry( 700,300,500,500)
        self.Cityname_Box = QLineEdit(self)
        self.Button = QPushButton("Submit", self)
        self.WeatherEmojii = QLabel("test1",self)
        self.Temperature = QLabel("test2",self)
        self.initUI()
    
    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.Cityname_Box)
        vbox.addWidget(self.Button)
        vbox.addWidget(self.WeatherEmojii)                ##initializing the alignment
        vbox.addWidget(self.Temperature)
        self.setLayout(vbox)


        self.WeatherEmojii.setAlignment(Qt.AlignCenter)
        self.Temperature.setAlignment(Qt.AlignCenter)
        
        self.Cityname_Box.setStyleSheet(
            "background: white;"
            "color: black;"
        )
        self.Cityname_Box.setPlaceholderText("Enter the name of a city")
        self.Button.clicked.connect(self.get_weather_info)

    def get_weather_info(self):
        API_key = ""
        city_name = self.Cityname_Box.text()
        url =  f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
        else:
            print(f"Failed to retrive data {response.status_code}")
        print(weather_data["weather"])
    






def main():
    app = QApplication(sys.argv)
    WeatherApp = MainWindow()
    WeatherApp.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()