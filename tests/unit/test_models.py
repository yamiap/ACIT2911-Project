import json
import pytest
from werkzeug.security import check_password_hash
from trivia.models import Question, Quiz, QuizQuestion, User


# Basic User fixture
@pytest.fixture
def user():
    user = User(username="user9", email="user9@example.com", password="P@ssw0rd!")
    return user


# Basic Quiz fixture
@pytest.fixture
def quiz(user):
    quiz = Quiz(user=user)
    return quiz


# Basic Question fixture
@pytest.fixture
def question():
    question = Question(
        category="Geography",
        difficulty="hard",
        question="Which is not a country in Africa?",
        correct_answer="Guyana",
        incorrect_answers_string=json.dumps(["Senegal", "Liberia", "Somalia"]),
    )
    return question


# Basic QuizQuestion fixture
@pytest.fixture
def quiz_question(question, quiz):
    quiz_question = QuizQuestion(question=question, quiz=quiz)
    return quiz_question


# Test User attributes
def test_new_user(user):
    assert user.username == "user9"
    assert user.email == "user9@example.com"
    assert user.password_hashed != "P@ssw0rd!"
    assert user.password_hashed is not None


# Test password hashing
def test_password_hashing(user):
    assert check_password_hash(user.password_hashed, "P@ssw0rd!")


# Test relationship between User and Quiz
def test_quiz_user_relationship(user, quiz):
    assert quiz.user == user
    assert user.quiz == quiz


# Test relationship between Quiz and QuizQuestion
def test_quiz_quiz_question_relationship(quiz, question, quiz_question):
    assert quiz_question.quiz == quiz
    assert quiz_question.question == question


# Test conversion of dictionary for api
def test_question_to_api_dict(question):
    assert question.to_api_dict() == {
        "id": question.id,
        "category": question.category,
        "difficulty": question.difficulty,
        "question": question.question,
        "correct_answer": question.correct_answer,
        "incorrect_answers": json.loads(question.incorrect_answers_string),
    }


# Test conversion of dictionary for game
def test_question_to_play_dict(question):
    play_dict = question.to_play_dict()
    assert play_dict["id"] == question.id
    assert play_dict["category"] == question.category
    assert play_dict["difficulty"] == question.difficulty
    assert play_dict["question"] == question.question
    assert play_dict["correct_answer"] == question.correct_answer
    assert set(play_dict["answers"]) == set(
        json.loads(question.incorrect_answers_string) + [question.correct_answer]
    )
