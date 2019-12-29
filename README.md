# Full Stack API Final Project

## Full Stack Trivia

This project is part of Udacity's Full-stack Web Development nano degree program. This project's goal is for students to develop the API and test cases.

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Runninng this project

To run this project you will need:

1. Python3
2. pip3
3. psycopg2 or psycopg2-binary
4. node
5. npm

### Backend

#### Installing dependencies

After cloning this project, in your terminal, cd into `/backend` directory then run: 

`pip3 install -r requirements.txt`

#### Running the server

After installing the dependencies, in `/bakend` directory run:

`export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
`


### Frontend

#### Installing dependencies

Go to`/frontend` directory then run:

`npm install`

#### Running Frontend

In `/frontend` directory run:

`npm start`

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:





Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
