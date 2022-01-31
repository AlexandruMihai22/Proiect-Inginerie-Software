

## About The Project

Our application is a prototype for an IoT device, which implements a smart plant care system.The system aims to adjust the water, light, or temperature of the plants, depending on certain parameters set by the user or
parameters that are updated based on weather-related information.


![Plant logo](https://github.com/AlexandruMihai22/Proiect-Inginerie-Software/blob/master/plant.jpg)

### Implemented endpoints:




### Built With


* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Mosquitto](https://mosquitto.org/documentation/)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started



You should have [python3](https://www.python.org/download/releases/3.0/) installed and [pip3](https://www.activestate.com/resources/quick-reads/how-to-install-and-use-pip3/). 
In order to run the project locally you should go through the following steps:
 
### Installation

1. cd into this project  

2. Install venv if not already installed:  
```sh
pip install virtualenv
```

  
3. Create an environment:  
```sh
python3 -m venv ./
```

  
Windows: 
```sh
python -m venv venv
```


4. Activate environment  

macOS/Linux:  
```sh
source venv/bin/activate
```


Windows:  
```sh
venv\Scripts\activate.bat
```


5. Install libraries
```sh
pip install -r requirements.txt
```


6. Set environment value for development:
```sh
export FLASK_ENV=development
```


CMD:
```sh
set FLASK_ENV=development
```


PowerShell:
```sh
$env:FLASK_ENV = "development
```


7. Initialize (or reinitialize) database:  
```sh
flask init-db
```
8. Run  

```sh
flask run
```
### Mosquitto 

Install and run [mosquitto](https://mosquitto.org/download/).

Mac

1. 
```sh
brew install mosquitto
```
3. If restarting the service is needed: 
```sh
brew services restart mosquitto
```

### Storm Glass API 

In order to collect data about weather, we used The Storm Glass API, which allows you to fetch weather data for any coordinate on the globe in a simple, programmatic way using conventional HTTP requests. When a request is successful, a response will be sent back in the form of a JSON object.
The weather request is used to fetch weather data for a point. The Storm Glass API provides marine weather as well as global weather for land and lakes.

Point Requests are used to retrieve data for a single coordinate.

```sh
https://api.stormglass.io/v2/weather/point
```
You can read more about the required parameters and the response format [here](https://docs.stormglass.io/?_gl=1*1hkz7yn*_ga*MTcyNzk0ODA3OS4xNjM2OTE4ODk2*_ga_79XDW52F27*MTYzNjkxODg5Ni4xLjAuMTYzNjkxODkwOC4w&_ga=2.44520877.823273569.1636918896-1727948079.1636918896#/weather)


