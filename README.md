# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)

### API Reference
___

#### Getting started

* Base URL: At present this app can only run locally and is not hosted at a base URL. The backend app is hosted at the default, ```http://127.0.0.1:5000/``` Which is set as a proxy in the frontend configuration.

* Authentication: This version of the application does not require authentication or API keys.

#### Error Handling

Errors are returned as JSON objects in the following format:

``` json
{
    "success": False,
    "error": 400,
    "message":"bad request"
}
```

The api will return five error types when requests fail:

* 400: Bad Request
* 404: Resource not found
* 422: Not processable
* 405: Not allowed
* 500: Internal server error

## Endpoints

#### GET /categories

* General: It returns a list of all available categories
* Sample: ```curl http://127.0.0.1:5000/categories```


``` json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### GET /questions

* General: It returns 
    * list of questions 
    * Total number of questions
    * current category 
    * 

* Sample:

``` json
```


#### DELETE /questions/\<int:question_id\>

* General:
* Sample:

``` json
```

#### POST /questions

* General:
* Sample:

``` json
```

#### GET /categories/\<int:category_id\>/questions

* General:
* Sample:

``` json
```


#### POST /quizzes

* General:
* Sample:

``` json
```
