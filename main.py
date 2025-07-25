import requests
import sys
import configparser
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry( 700,300,350,300)
        self.Cityname_Box = QLineEdit(self)
        self.Button = QPushButton("Submit", self)
        self.Icon = QLabel(self)
        self.Cityname_text = QLabel(self)
        self.Description_text = QLabel(self)
        self.Temperature_text = QLabel(self)
        self.pixmap = QPixmap()
        self.initUI()
        self.get_config_info()
    
    def initUI(self): #sets up the UI 
        vbox = QVBoxLayout()
        vbox.addWidget(self.Cityname_Box)
        vbox.addWidget(self.Button)
        vbox.addWidget(self.Cityname_text) 
        vbox.addWidget(self.Icon)
        vbox.addWidget(self.Description_text)          
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

    def get_config_info (self): #Gets the API KEY and chosen units of measurments from the config.ini file
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.API_KEY = config.get("General", "API_KEY")
        self.units = config.get("General", "Units")
        
    def get_weather_info(self): #uses the API key to access the API and gets the response in a json file
        city_name = self.Cityname_Box.text()
        url =  f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.API_KEY}&units={self.units.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            self.set_weather_info(weather_data)
        else:
            error_data = response.json()
            self.error_handling(error_data)

    def set_weather_info(self, weather_data): #takes data from the json file and shows the output to the UI
        temperature = str(weather_data["main"]["temp"])
        weather_icon_id = weather_data["weather"][0]["icon"]
        description = weather_data["weather"][0]["description"]
        city_name = weather_data["name"]

        match self.units.lower():
            case "metric":
                unit_symbol = "°C"
            case "imperial":
                unit_symbol = "°F"
            case _:
                unit_symbol = " K"
        
        self.Cityname_text.setText(city_name.capitalize())
        self.Temperature_text.setText(f"{temperature}{unit_symbol}")
        self.Description_text.setText(f"{description.capitalize()}")

        weather_icon = requests.get(f"https://openweathermap.org/img/wn/{weather_icon_id}@2x.png")
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(weather_icon.content)
        self.Icon.setPixmap(self.pixmap)

    def error_handling(self, error_data):
        status_code =  error_data["cod"] 
        error_message =  error_data["message"]

        self.Temperature_text.setText(f"{error_message}")
        self.Cityname_text.setText(f"Error code: {status_code}")
        self.pixmap = QPixmap("error.png")
        self.Icon.setPixmap(self.pixmap.scaled(40,40))
        self.Description_text.setText("")

def main():
    app = QApplication(sys.argv)
    WeatherApp = MainWindow()
    WeatherApp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()