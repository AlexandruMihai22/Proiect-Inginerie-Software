
## Features



### Authentication

```sh
auth.login()
```


``      
      required:
``

* username
* password

``
responses:
``

``
200:
``

        description: user logged in succesfully.
``
403:
``

        description: there is no user with that username and password.
        

```sh
auth.register()
```


``      
      required:
``

* username
* password

``
responses:
``

``
200:
``

       user registered succesfully
``
403:
``

        Username is required.

        Password is required.

        User is already registered.

### System temperature


```sh
/system_temperature/set
```


``      
      required:
``

* temp


``
responses:
``

``
200:
``

      Temperature successfully retrieved
``
422:
``

        temperature must be numeric.

``
403:
``

       Temp is required.

```sh
/system_temperature
```


``       required:
``

* temp


``
responses:
``

``
200:
``

       Temperature successfully retrieved
       
``
403:
``

        Please set temperature

### Soil Moisture

```sh
      soil_moisture/set
```


``      
      required:
``

* soil_moisture


``
responses:
``

``
200:
``

      soil moisture successfully retrieved
``
422:
``
      soil moisture must be numeric.


``
403:
``
      Please set soil moisture
      soil_moisture is required.
```sh
/system_temperature
```


``       required:
``

* temp


``
responses:
``

``
200:
``

       Temperature successfully retrieved
       
``
403:
``

        Please set temperature
        
### Water

```sh
      /watering/
```


``      
      required:
``

* water_quantity


``
responses:
``

``
200:
``

      The plant was successfully watered


``
422:
``
      water quantity must be numeric.


``
403:
``
 
      Water quantity is required.


```sh
      /watering/
```


``
responses:
``

``
      200:
``
```
      The plant was successfully watered
```
       






 
