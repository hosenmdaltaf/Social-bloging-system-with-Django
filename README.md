# Social-bloging-system-with-Django

<h1 align="center">Fourth Year Applied Project And Minor Dissertation </h1>
<p align="center">
  <img src = "projectimages/projectlogo.png">
</p>
![projectlogo](https://user-images.githubusercontent.com/64326036/116879967-f48bd580-ac53-11eb-959c-0a4a62c22707.png)

# Overview
Social media today plays an expanding significant role in society, the information technology industry and the field of computer science. The use of social media is a hot-topic for many organizations, with the aim to identify approaches in which companies can use applications to increase profits and grow product awareness. On a day-to-day basis, users from across the globe are becoming increasingly frustrated, wasting valuable time, scrolling through irrelevant content while companies are wasting money advertising to users outside their market.  In order to achieve the optimal benefits from social media, for both users and businesses, the development of these technologies require approaches that focus on specific human interests and values.


This project aims to deliver a solution by developing a platform with the goal of delivering a social experience that targets a specific user base. As the authors are in the field of computer science the focus of the content will be to appeal to the tech savvy user. The proposed solution will be a web application that will offer a unique online community to users and businesses interested in technology.

# Introduction
The project has been developed as a MEAN stack Angular 6 CRUD Web Application. The initial  project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 6.0.1. The system utilises a 3 tier architecture using MongoDB, ExpressJs, Angular and NodeJs.


**Techbook** is a social bloging platform that offers a unique experience offering a community for users interested in technology to communicate.

# Features
## Application features
- An easy to use  web application with fully responsive design. 
- Full CRUD capabilities .
- Fully functional Postgress and redis database with restrictions and validation.
- Sensitive data such as passwords is encrypted before adding to database.
- Fully responsive GUI to adapt to all screen sizes.
- Created for readers and writers best experence in mind. 
- Server logging system.
- Fully aunthenticated and authorizatied Secure for users

## User features
- Can register an account.
- Can log in.
- Can stay logged in using local storage.
- Can log out.
- Can update profile info and upload profile image.
- Can follow / unfollow other users.
- Can subscribe / unsubscribe to blogs.
- Can view saved blogs.
- Can add a blog.
- Can update and delete own blog
- Can comment on blog.
- Can chat with each other
- Can ask question in disscussion forum
- Can update and delete own asked question
- Can comment on another questions
- Can search any question,blog,user 
- Can find blog by category
- Can find latest blogs for read on feed

# Technologies

<p align="center">
  <img src = "https://imgur.com/IzjUXp5.png">
</p>

Below is a brief list of some of the technologies used. For a comprehensive list of dependencies see [here](https://github.com/hosenmdaltaf/Social-bloging-system-with-Django/blob/master/requirement.txt)

- **Languages**: 
    - JavaScript
    - HTML 
    - CSS
    - Python
- **Libraries**: 
    - Bootstrap
    - Bulma
- **Frameworks**: 
    - Django
    -Django REST framework
    -Django Channels
- **Databases**:
    - postgresql
    - Redis
- **Environments**: 
    - windows
- **Development Software**
    - Docker
    - Visual Studio Code   
    - Git
    - Github

# Prerequisites
* python installed.
* Git or git bash to clone the project.
* Access to an internet browser.
* I highly recommend stay with django version 3.0 and python version 3.9.4(for avoiding any complicity)
<<<<<<< HEAD

=======
>>>>>>> 12db2bbc1ce13fe82b458ddbd288c3ea3f896218


# Deploy Project locally

## Download the Project
Clone this repository to your machine.
- Navigate to an empty directory
- In command prompt 
```bash
	> git clone https://github.com/hosenmdaltaf/Social-bloging-system-with-Django.git
```

## Run The Development Server
To deploy locally navigate to the project directory in cmd. 

Run the following command to build the project and launch the server:

```bash
    > cd Social-bloging-system-with-Django
    > pip install -r requirements.txt
    > python manage.py runserver
   
```

The server will now be running . Navigate to ```localhost:127.0.0.1:8000`` to view the application.

# Deployment
This application is currently deployed on an AWS instance. Click [Here to TechBook live](http://34.243.30.50:3000/index)

# Preview
Below is a preview of some of the applications pages rendered on both a mobile device and PC.
_Please note these are the inital screenshots of the pages and may have changed by the time the project is submitted_. To view all pages click 
[Here for TechBook live](http://34.243.30.50:3000/index). An indepth explanation of each page is available in *System Design* section of the
[Dissertation](https://github.com/Final-Year-Project-Cian-Kevin/Dissertation/blob/master/project.pdf). 

## Homepage

Web view          |  Mobile view
:-------------------------|:-------------------------:
<img src = "https://imgur.com/iu7wpzq.png" height=300>|<img height = 300 src = "https://imgur.com/EcjDWP2.png">

## Userfeed Page
Web view          |  Mobile view
:-------------------------:|:-------------------------:
<img src = "https://imgur.com/P0jQXTr.png" height=300>|<img height = 300 src = "https://imgur.com/NAcxvo1.png">

## Blogdetail Page
Web view          |  Mobile view
:-------------------------:|:-------------------------:
<img src = "https://imgur.com/P0jQXTr.png" height=300>|<img height = 300 src = "https://imgur.com/NAcxvo1.png">


## Forum home Page
Web view          |  Mobile view
:-------------------------:|:-------------------------:
<img src = "https://imgur.com/P0jQXTr.png" height=300>|<img height = 300 src = "https://imgur.com/NAcxvo1.png">


## Chat home Page
Web view          |  Mobile view
:-------------------------:|:-------------------------:
<img src = "https://imgur.com/P0jQXTr.png" height=300>|<img height = 300 src = "https://imgur.com/NAcxvo1.png">

## Profile Page
Web view          |  Mobile view
:-------------------------:|:-------------------------:
<img src = "https://imgur.com/P0jQXTr.png" height=300>|<img height = 300 src = "https://imgur.com/NAcxvo1.png">

## Log in Page
Web view          |  Mobile view
:-------------------------:|:-------------------------:
<img src = "https://imgur.com/5971dv6.png" height=300>|<img height = 300 src = "https://imgur.com/GmdtAyY.png">

## Register Page
Web view          |  Mobile view
:-------------------------:|:-------------------------:
<img src = "https://imgur.com/zL0xXo8.png" height=300>|<img height = 300 src = "https://imgur.com/DRw9UDk.png">

## Settings Page
Web view          |  Mobile view
:-------------------------:|:-------------------------:
<img src = "https://imgur.com/YWCvPvT.png" height=300>|<img height = 300 src = "https://imgur.com/PeI6lTm.png">

## Friends Page
Web view          |  Mobile view
:-------------------------:|:-------------------------:
<img src = "https://imgur.com/qPBaLZb.png" height=300>|<img height = 300 src = "https://imgur.com/YjpegMl.png">


