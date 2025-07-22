import requests
import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry( 700,300,500,500)
        self.Cityname_Box = QLineEdit(self)
        self.Button = QPushButton("Submit", self)
        self.Icon = QLabel(self)
        self.Temperature = QLabel("test2",self)
        self.initUI()
    
    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.Cityname_Box)
        vbox.addWidget(self.Button)
        vbox.addWidget(self.Icon)                ##initializing the alignment
        vbox.addWidget(self.Temperature)
        self.setLayout(vbox)
        self.Icon.setAlignment(Qt.AlignCenter)
        self.Temperature.setAlignment(Qt.AlignCenter)
        
        self.Cityname_Box.setStyleSheet(
            "background: white;"
            "color: black;"
        )
        self.Cityname_Box.setPlaceholderText("Enter the name of a city")
        self.Button.clicked.connect(self.get_weather_info)

    def get_weather_info(self):
        API_key = "fbee0422f577761266cbc616bf3e2858"
        city_name = self.Cityname_Box.text()
        url =  f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            self.set_weather_info(weather_data)
        else:
            print(f"Failed to retrive data {response.status_code}")


    
    def set_weather_info(self, weather_data):
        temperature = str(weather_data["main"]["temp"])
        weather_type = weather_data["weather"][0]["main"]
        weather_icon_id= weather_data["weather"][0]["icon"]
        self.Temperature.setText(temperature)
        
        weather_icon = requests.get(f"https://openweathermap.org/img/wn/{weather_icon_id}@2x.png")
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(weather_icon.content)
        self.Icon.setPixmap(self.pixmap)
    
        print(weather_type)
        print(temperature)
        print(weather_icon_id)






def main():
    app = QApplication(sys.argv)
    WeatherApp = MainWindow()
    WeatherApp.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()