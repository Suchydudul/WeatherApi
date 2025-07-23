import requests
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.Cityname_Box = QLineEdit(self)
        self.Button = QPushButton("Submit", self)
        self.Icon = QLabel(self)
        self.Cityname_text = QLabel(self)
        self.Description_text = QLabel(self)
        self.Temperature_text = QLabel(self)
        self.initUI()
    
    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.Cityname_Box)
        vbox.addWidget(self.Button)
        vbox.addWidget(self.Cityname_text) 
        vbox.addWidget(self.Icon)
        vbox.addWidget(self.Description_text)          ##initializing the alignment
        vbox.addWidget(self.Temperature_text)

        self.setLayout(vbox)
        self.Cityname_text.setAlignment(Qt.AlignCenter)
        self.Description_text.setAlignment(Qt.AlignCenter)
        self.Icon.setAlignment(Qt.AlignCenter)
        self.Temperature_text.setAlignment(Qt.AlignCenter)
        
        self.Cityname_Box.setStyleSheet(
            "background: white;"
            "color: black;"
            "font-size: 25px;"
        )

        self.Cityname_text.setStyleSheet(
            "font-size: 25px;"
        )

        self.Description_text.setStyleSheet(
            "font-size: 12px;"
        )

        self.Temperature_text.setStyleSheet(
            "font-size: 25px;"
        )

        self.Cityname_Box.setPlaceholderText("Enter the name of a city")
        self.Button.clicked.connect(self.get_weather_info)

    def get_weather_info(self):
        API_KEY = "7f6bb00fcf85dc962dd56b45b59c3d5d"
        city_name = self.Cityname_Box.text()
        self.Cityname_text.setText(city_name.capitalize())
        url =  f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            self.set_weather_info(weather_data)
        else:

            self.Temperature_text.setText(f"Error code: {response.status_code}")
            self.error_handling(response.status_code)

    def set_weather_info(self, weather_data):
        temperature = str(weather_data["main"]["temp"])
        weather_icon_id = weather_data["weather"][0]["icon"]
        description = weather_data["weather"][0]["description"]

        self.Temperature_text.setText(f"{temperature}°C")
        self.Description_text.setText(f"{description.capitalize()}")

        weather_icon = requests.get(f"https://openweathermap.org/img/wn/{weather_icon_id}@2x.png")
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(weather_icon.content)
        self.Icon.setPixmap(self.pixmap)

    def error_handling(self, status_code):
        print(status_code)
        pass

def main():
    app = QApplication(sys.argv)
    WeatherApp = MainWindow()
    WeatherApp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()