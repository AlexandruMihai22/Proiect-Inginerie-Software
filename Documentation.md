
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
      
``
        Username is required.
``
        
``
        Password is required.
``
        
``
        User is already registered.
``
        


 
