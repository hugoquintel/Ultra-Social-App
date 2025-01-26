# Ultra Social App project

This is a university project inspired by Instagram built in django web framework using Python. Most of the code in this project is from Lara Code. You can check out his youtube channel [here](https://www.youtube.com/@laracode7372), the original github [repository](https://github.com/byronlara5/django_instagram_clone_youtube)


## Getting Started

- Install the prerequisites

- Run the server:
```
cd to folder of this project
python <this_project>.py runserver
```
e.g: 
```
python main.py runserver:
```

- Create superuser(admin):

```
python main.py createsuperuser
```


### Prerequisites

You can install the Prerequisites by running the command: 

```
pip install -r requirements.txt
```

```
django==4.1
django-celery-beat==2.2.1
django-cleanup==7.0.0
eventlet==0.33.3
celery==5.2.7
pillow==9.3.0
```

## Functional story

- To enable story with proper function (deleted when expired), [celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) must be added with a broker, [RabbitMQ](https://www.rabbitmq.com/) is used for this project.

- Watch the tutorial how to add celery task to story [here](https://www.youtube.com/watch?v=UU6PfdyWADc&list=PL9tgJISrBWc5619CclyqYrnnMkVOPzVYM&index=36&ab_channel=LaraCode)

*Additional note*: celery doesn't work properly for windows after version 4.0. You can download a lower version or after installing eventlet, you can start a celery worker with this command:
```
celery -A [app_name] worker --pool=eventlet
```
To start a celery worker with this project:
```
celery -A main worker --pool=eventlet
```

## Screenshots

![Screen](screenshots/screen1.png?raw=true)


![Screen](screenshots/screen2.png?raw=true)


![Screen](screenshots/screen3.png?raw=true)


![Screen](screenshots/screen4.png?raw=true)


![Screen](screenshots/screen5.png?raw=true)


![Screen](screenshots/screen6.png?raw=true)


![Screen](screenshots/screen7.png?raw=true)


![Screen](screenshots/screen8.png?raw=true)


![Screen](screenshots/screen9.png?raw=true)


![Screen](screenshots/screen10.png?raw=true)





## Built With
* [Bulma](https://bulma.io/) - Bulma is a free, open source CSS framework based on Flexbox
* [Django](https://www.djangoproject.com/) - Web framework
* [jQuery](https://jquery.com/) - JavaScript library
* [Fontawesome](https://fontawesome.com/) - Internet's icon library and toolkit
