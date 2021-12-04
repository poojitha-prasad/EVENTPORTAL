# EVENTPORTAL
Python Flask Project


#Fiesta Event Portal

This event portal is a user friendly one. Using this event portal we can create a unique account and register all events in our college. We can also add events with criteria like max participants, location and date and time. A confirmation email will be send to the delegate after then event is registered. Clicking on a event  shows all registered attendees for that event. A list of upcoming events are listed in the portal. Inspite of all these advantages it also has its own demerits.





##How it Works?

1. In the Welcome page, upcoming events are listed according to date and time. select " continue " we will be directed to login page.
2. In the login page if you already have an account, login by providing neccessary details.Otherwise create new account using " sign up " link provided there. User cannot use username which already existed.
3. After login, a home page will appear with details of student and  registered events.
4. In the home page, three links are provided for adding new events, register for the events and attended events of the user.
5. In the event attendance page, list of past events which are attended by the user are listed which is confirmed by user using the email received by them.
6. In the add events page, new events can be added by providing neccessary details. No new events can be added with same event title and location. 
7. Event registration page contain a link which provides the details of upcoming events. On selecting it, we will be directed to an another page which contains details of all events added. This page is also provided with a table containing list all the participants of a selected event.
8. Going back to the event register page, according to desire user can select and register for the events. If tha particular tevent has reached its max participants no new members can register that event.
9. On registering events, an email is send to provided email address of  the user which redirect to a page where user can confirm their attendance. This confirmation link will be expired the day before the  event.
 




##Libraries used

Python - 3.8.2                   
Flask  - 2.0.0   
Flask-Mail -0.9.1   
Flask-MySQLdb - 0.2.0   
Jinja2 - 3.0.0   
mysqlclient - 1.4.6  
pip - 19.2.3    
env (GNU coreutils) - 8.32

##Instructions for setting up project

* Installation process :-  
     python -m venv env     
     env\Scripts\activate      
     pip install flask    
     pip install flask-mysqldb   
     pip install FLASK-mail

* Folder Creation :- 
    A folder named Templates should be created to add HTML files and a folder named static should be created to add CSS files.
  
* Connection Setup :-
    1. To connect database to the system, provide respective host name, password, and username of the system's mysql database. Also create a database with commands given in the file bfh.sql.
    2. Connect mail server from where the email is sent by providing the mail server information in config.cfg file.

##How to run   

 activate the environment   
 env\Scripts\activate   
 set FLASK_APP=bfh1.py   
 flask run   
