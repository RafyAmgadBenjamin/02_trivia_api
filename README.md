# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

### Prerequisites and Installation
To be able to work on this project you must have

* python3 
```bash
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get install python3.6

```
* pip3 
``` bash
sudo apt install python3-pip
```
* Node.js
```bash
sudo apt install nodejs
```
* npm 
```bash
sudo apt install npm
```

#### Frontend dependencies:
This project depends on NPM, npm (originally short for Node Package Manager) is a package manager for the JavaScript programming language. It is the default package manager for the JavaScript runtime environment Node.js. It consists of a command line client, also called npm.
npm uses package.json files which is located in the ```frontend``` directory to install the packages needed for this project, after cloning the project go to the frontend directory, open the terminal and run:
``` bash
npm install
```

#### Backend dependencies:
once your environment is ready either you are using a virtual environment or developing on the local machine without a virtual environment, you have to install the backend dependencies, navigate to the ```backend``` directory, open the terminal and run:
```bash
pip3 install -r requirements.txt
```

#### Running the frontend in development mode
* The frontend application was built using React which is JavaScript library for building user interfaces.
* The frontend run on port 3000 the url on local machine will be ```http://loccalhost:3000```
* We will use the development mode as we are still working on the application and it facilitates the developing by adding some features likes debugging and refreshing the page automatically upon any change.
* To start the application, navigate to the ```frontend``` directory and run:
```bash
npm start
```
#### Running the backend in development mode.
* The backend application was built using Flask which is  micro web framework written in Python.
* We will use the development mode as we are still working on the application and it facilitates the developing by adding some features likes debugging and refreshing the page automatically upon any change.
* To run the server,navigate to the ```backend``` directory and run:

```bash 
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

#### Testing
* the application in testing dependes on ```unittest``` which is framework was originally inspired by JUnit and has a similar flavor as major unit testing frameworks in other languages.
* To run the tests, navigate 
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

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
  * List of questions
  * Results are paginated into groups each group is of 10 quesions
  * Total number of questions
  * Current category
  * List of all categories

* Sample:

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
  "current_category": "Science", 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total_questions": 24
}

```

#### DELETE /questions/\<int:question_id\>

* General:
  * It deletes a question of specific Id.
  * It returns deleted question Id.
  * It returns list of remaining questions.
  * It returns the total number of questions.
* Sample: ```curl http://127.0.0.1:5000/questions/9 -X DELETE```

``` json
{
  "deleted": 6, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 23
}


```

#### POST /questions

This endpoint can add new question or search for questions

1. If there is no a **search term** included in the request body so the endpoint will add a new question.

* General:
  * Creates new question using the submitted question, answer, category and difficulty.
  * Returns Id of the created question.
  * Returns a list of all paginated questions after adding the new one.
  * Returns the length of all questions.
* Sample:```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "who is the best football player?", "answer": "missi", "difficulty": 3, "category": "6" }'```

``` json
{
  "created": 33, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 25
}

```
2- If there is a **search term** included in the request body so the endpoint will search for questions with this term included.

* General:

  * It returns list of all questions contain the **search term** which was submitted and the questions will be paginated.
  * Total number of questions that have the **search term**
* Sample:```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "player"}'```

``` json
{
  "questions": [
    {
      "answer": "missi", 
      "category": 6, 
      "difficulty": 3, 
      "id": 33, 
      "question": "who is the best football player?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}

```

#### GET /categories/\<int:category_id\>/questions

* General:
  * Returns list of questions in specific category paginated.
  * Returns the total number of questions in this category.
  * Returns the current category. 
* Sample:```curl http://127.0.0.1:5000/categories/2/questions```

``` json
{
  "current_category": "Art", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "26", 
      "category": 2, 
      "difficulty": 1, 
      "id": 24, 
      "question": "how old are you ?"
    }, 
    {
      "answer": "cairo", 
      "category": 2, 
      "difficulty": 1, 
      "id": 25, 
      "question": "what is the capital of egypt?"
    }
  ], 
  "success": true, 
  "total_questions": 6
}

```


#### POST /quizzes

* General:
  * It allows the user to play the **quiz game**
  * You have to submit the quiz category and previous questions in request body
  * It returns a new question to answer which is not in the previous questions
* Sample: ```curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [22], "quiz_category": {"type": "Art", "id": "2"}}'```

``` json
{
  "question": {
    "answer": "Mona Lisa", 
    "category": 2, 
    "difficulty": 3, 
    "id": 17, 
    "question": "La Giaconda is better known as what?"
  }, 
  "success": true
}

```

## Authors

Rafy amgad benjamin is the author of APIs in  ```__init__.py``` file, APIs testing in ```test_flaskr.py``` and the API documentation part in this ```Readme.md``` file, the rest of the files and even the models are authored by **Udacity** in full stack development track in Nanodegree.
 