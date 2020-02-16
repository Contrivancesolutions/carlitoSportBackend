# calritoSportBackend
![Continous Integration](https://github.com/azimgivron/carlitoSportBackend/workflows/Continous%20Integration/badge.svg)


All the dependencies are handled using Pipenv. You need to install that first using
```
pip3 install pipenv
``` 
To enter the virutal env
```
pipenv shell
```
Where you can run the web app using
```
pipenv run server
```



### Developement
Run tests
```
pipenv run tests
```

Run linter tests
```
pipenv run flake8 ./main/*.py
```


### Translations
In order to translate the application, open a .po file under `main/locale` using an application like Poedit and translate the whole thing.
TODO: add how to merge i18n
