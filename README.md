# Periwinkle

## CEN4914 Senior Project



### What is it?

This is Fernando Rivera's and Caleb Wong's semester-long project for CEN4914 at the University of Florida. With Periwinkl, we aim to create a hub for students in computer science to find and work on projects with likeminded peers. We have launched a web application using Python with Django for the backend, and HTML, CSS, and JS with MaterializeCSS for a responsive, modern graphical user interface based off Google’s Material Design principles. 



### Main Features

Here is the most important functionality that Periwinkl provides.

- Custom Firebase Authentication
- Explore tab for users to filter for and find new projects.
  - Users may request to join an existing project
- Groups tab for users to manage the groups they are a part of
- Group specific pages for users to take advantage of built-in project management
  - GitHub issues integration
  - Task creation and status assigning
  - Member request acceptance or rejection



### Credentials

This project uses Firebase, and therefore will require an API key to run. This can be replaced inside of the `views.py` file. It is also deployed on Heroku which will require an account for their service. Finally, for full group functionality and integration with GitHub, users must provide an authorization token upon creating a group.



### Requirements

For local versions of this app, you must install those services that are listed in the `requirements.txt` file. It will automatically connect to the appropriate Firebase project from the API key in the code. The following are the modules necessary. Once cloned, the repo can be run using the `python manage.py runserver` command.

```
django
gunicorn
django-heroku
pyrebase4
PyGithub
```

