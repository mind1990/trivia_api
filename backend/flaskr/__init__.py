import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r'/api/*': {'origins': '*'}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  Get all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()

    # Create categories dict
    categories_dict = {}
    for category in categories:
      categories_dict[category.id] = category.type
  
    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories_dict
    })
    

  '''
  Get questions, pagination, a list of questions, 
  number of total questions, current category, categories.
  '''
  @app.route('/questions')
  def get_questions():

    # Get questions then paginate
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)

    # Create categories dict
    categories = Category.query.order_by(Category.id).all()
    categories_dict = {}
    for category in categories:
      categories_dict[category.id] = category.type

    if len(questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': categories_dict
    })


  '''
  Delete a question.
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      select_question = Question.query.filter_by(id=id).one_or_none()

      if select_question is None:
        abort(404)
      
      else:
        select_question.delete()

      return jsonify({
        'success': True,
        'deleted': id
      })

    except:
      abort(422)
  

  '''
  Get questions based on a search term.
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    if body.get('searchTerm'):
      search_Term = body.get('searchTerm')
      selection = Question.query.filter(Question.question.ilike(f'%{search_Term}%')).all()
      
      if len(selection) == 0:
        abort(404)

      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })
    
    
    # Post a new question.
    else:
      new_question = body.get('question')
      new_answer = body.get('answer')
      new_category = body.get('category')
      new_difficulty = body.get('difficulty')
      
      if ((new_question is None) or (new_answer is None) or (new_category is None) or (new_difficulty is None)):
        abort(422)
      
      try:
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'created': question.id,
          'questions': current_questions,
          'question_created': question.question,
          'total_questions': len(Question.query.all())
        })

      except:
        abort(422)
      

  '''
  Get questions based on category.
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    category = Category.query.filter_by(id=id).one_or_none()

    if category is None:
      abort(400)
    
    selection = Question.query.filter_by(category=category.id).all()
    paginated_questions = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(Question.query.all()),
      'current_category': category.type
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  Error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  
  return app

    