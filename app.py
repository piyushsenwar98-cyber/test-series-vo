import json
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Define the file path for saving results
RESULTS_FILE = 'results.json'
# Define a secret password for the admin dashboard
ADMIN_PASSWORD = 'Piyush11@'  # <--- CHANGE THIS TO A SECURE PASSWORD

# --- Existing quiz data structure ---
test_series = {
    'gk': {
        'title': 'General Knowledge Test Series',
        'quizzes': [
            {
                'id': 'gk-test-1',
                'title': 'GK Test 1',
                'status': 'available',
                'duration': 15,
                'questions': [
                    {'id': 1, 'question': 'What is the capital of France?', 'options': ['Berlin', 'Madrid', 'Paris', 'Rome'], 'answer': 'Paris'},
                    {'id': 2, 'question': 'Which planet is known as the Red Planet?', 'options': ['Mars', 'Venus', 'Jupiter', 'Saturn'], 'answer': 'Mars'},
                    {'id': 3, 'question': 'What is the largest ocean on Earth?', 'options': ['Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Pacific Ocean'], 'answer': 'Pacific Ocean'},
                    {'id': 4, 'question': 'Who wrote "Romeo and Juliet"?', 'options': ['Charles Dickens', 'William Shakespeare', 'Mark Twain', 'Jane Austen'], 'answer': 'William Shakespeare'},
                    {'id': 5, 'question': 'What is the currency of Japan?', 'options': ['Yuan', 'Euro', 'Yen', 'Dollar'], 'answer': 'Yen'},
                    {'id': 6, 'question': 'Which element has the chemical symbol "O"?', 'options': ['Gold', 'Oxygen', 'Silver', 'Hydrogen'], 'answer': 'Oxygen'},
                    {'id': 7, 'question': 'What is the smallest country in the world?', 'options': ['Monaco', 'Vatican City', 'San Marino', 'Liechtenstein'], 'answer': 'Vatican City'},
                    {'id': 8, 'question': 'How many continents are there?', 'options': ['5', '6', '7', '8'], 'answer': '7'},
                    {'id': 9, 'question': 'What is the boiling point of water in Celsius?', 'options': ['0°C', '50°C', '100°C', '200°C'], 'answer': '100°C'},
                    {'id': 10, 'question': 'Which animal is the largest on Earth?', 'options': ['African Elephant', 'Blue Whale', 'Great White Shark', 'Giraffe'], 'answer': 'Blue Whale'},
                    {'id': 11, 'question': 'What is the powerhouse of the cell?', 'options': ['Nucleus', 'Mitochondria', 'Cytoplasm', 'Ribosome'], 'answer': 'Mitochondria'},
                    {'id': 12, 'question': 'Who painted the Mona Lisa?', 'options': ['Vincent van Gogh', 'Pablo Picasso', 'Leonardo da Vinci', 'Claude Monet'], 'answer': 'Leonardo da Vinci'},
                    {'id': 13, 'question': 'Which country is the Great Wall in?', 'options': ['Japan', 'India', 'China', 'Russia'], 'answer': 'China'},
                    {'id': 14, 'question': 'What is the hardest natural substance?', 'options': ['Gold', 'Iron', 'Diamond', 'Quartz'], 'answer': 'Diamond'},
                    {'id': 15, 'question': 'In which year did the Titanic sink?', 'options': ['1910', '1912', '1915', '1920'], 'answer': '1912'},
                    {'id': 16, 'question': 'What is the largest desert in the world?', 'options': ['Gobi Desert', 'Sahara Desert', 'Kalahari Desert', 'Arabian Desert'], 'answer': 'Sahara Desert'},
                    {'id': 17, 'question': 'How many bones are in the human body?', 'options': ['206', '210', '198', '200'], 'answer': '206'},
                    {'id': 18, 'question': 'What is the main component of Earth\'s atmosphere?', 'options': ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Argon'], 'answer': 'Nitrogen'},
                    {'id': 19, 'question': 'Which is the fastest land animal?', 'options': ['Cheetah', 'Lion', 'Gazelle', 'Leopard'], 'answer': 'Cheetah'},
                    {'id': 20, 'question': 'What is the square root of 64?', 'options': ['6', '7', '8', '9'], 'answer': '8'}
                ]
            },
            {
                'id': 'gk-test-2',
                'title': 'GK Test 2',
                'status': 'coming_soon',
                'available_date': 'October 25, 2025'
            },
            {
                'id': 'gk-test-3',
                'title': 'GK Test 3',
                'status': 'coming_soon',
                'available_date': 'November 10, 2025'
            }
        ]
    },
    'veterinary': {
        'title': 'Veterinary Science Test Series',
        'quizzes': [
            {
                'id': 'vet-test-1',
                'title': 'Vet Test 1',
                'status': 'coming_soon',
                'available_date': 'October 30, 2025'
            },
            {
                'id': 'vet-test-2',
                'title': 'Vet Test 2',
                'status': 'coming_soon',
                'available_date': 'November 15, 2025'
            }
        ]
    }
}
# --- End of existing quiz data structure ---

def get_quiz_by_id(series_id, quiz_id):
    series = test_series.get(series_id)
    if not series:
        return None, None
    for quiz in series['quizzes']:
        if quiz['id'] == quiz_id:
            return series, quiz
    return series, None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/series')
def series_list():
    return render_template('series.html', series_list=test_series)

@app.route('/series/<string:series_id>')
def quiz_list(series_id):
    series = test_series.get(series_id)
    if not series:
        return "Test series not found", 404
    return render_template('quizzes.html', series=series, series_id=series_id)

@app.route('/quiz/<string:series_id>/<string:quiz_id>')
def quiz(series_id, quiz_id):
    series, selected_quiz = get_quiz_by_id(series_id, quiz_id)
    if not selected_quiz:
        return "Quiz not found", 404
    if selected_quiz['status'] == 'available':
        return render_template('quiz.html', quiz=selected_quiz, series_id=series_id)
    else:
        return render_template('coming_soon.html', quiz=selected_quiz, series_id=series_id)

@app.route('/submit/<string:series_id>/<string:quiz_id>', methods=['POST'])
def submit(series_id, quiz_id):
    user_answers = request.get_json()
    series, quiz_info = get_quiz_by_id(series_id, quiz_id)
    
    if not quiz_info or quiz_info['status'] != 'available':
        return jsonify({'error': 'Quiz not available'}), 404

    correct_answers = {str(q['id']): q['answer'] for q in quiz_info['questions']}
    
    score = 0
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    
    for q_id, correct_ans in correct_answers.items():
        user_ans = user_answers.get(q_id)
        if user_ans and user_ans == correct_ans:
            score += 4
            correct_count += 1
        elif user_ans:
            score -= 1
            wrong_count += 1
        else:
            unanswered_count += 1
            
    result_data = {
        'total_score': score,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'unanswered_count': unanswered_count,
        'total_questions': len(quiz_info['questions']),
        'user_answers': user_answers,
        'correct_answers': correct_answers,
        'time_taken_seconds': user_answers.get('time_taken_seconds')
    }

    # Save results to file for admin view
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            all_results = json.load(f)
    else:
        all_results = []
    all_results.append({
        'quiz_id': quiz_id,
        'series_id': series_id,
        'total_score': score,
        'time_taken_seconds': user_answers.get('time_taken_seconds'),
        'user_answers': user_answers,
        'correct_answers': correct_answers
    })
    with open(RESULTS_FILE, 'w') as f:
        json.dump(all_results, f, indent=4)
        
    # Store the result and original questions in the user's session
    session['results'] = result_data
    session['quiz_questions'] = quiz_info['questions']
    
    return jsonify({'success': True, 'redirect_url': url_for('submission_received')})

@app.route('/submission_received')
def submission_received():
    return render_template('submission_received.html')

@app.route('/user_results')
def show_user_results():
    if 'results' not in session or 'quiz_questions' not in session:
        return redirect(url_for('home'))
    
    results = session.pop('results')
    questions = session.pop('quiz_questions')
    
    return render_template('results.html', results=results, questions=questions)

# New route to handle password submission
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_results_list'))
        return render_template('admin_login.html', error='Invalid Password')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))
    
# This is the protected admin results list page
@app.route('/admin/results')
def admin_results_list():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    if not os.path.exists(RESULTS_FILE):
        return render_template('admin_results_list.html', all_results=[])
    with open(RESULTS_FILE, 'r') as f:
        all_results = json.load(f)
    return render_template('admin_results_list.html', all_results=all_results)

# This is the protected individual result page
@app.route('/admin/results/<int:result_id>')
def admin_results_detail(result_id):
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))

    if not os.path.exists(RESULTS_FILE):
        return "No results found.", 404
    with open(RESULTS_FILE, 'r') as f:
        all_results = json.load(f)
    if 0 <= result_id - 1 < len(all_results):
        result = all_results[result_id - 1]
        series, quiz_data = get_quiz_by_id(result['series_id'], result['quiz_id'])
        if not quiz_data:
            return "Quiz data for this result not found.", 404
        results_data = {
            'total_score': result['total_score'],
            'correct_count': sum(1 for q_id, ans in result['correct_answers'].items() if result['user_answers'].get(q_id) == ans),
            'wrong_count': sum(1 for q_id, ans in result['correct_answers'].items() if result['user_answers'].get(q_id) and result['user_answers'].get(q_id) != ans),
            'unanswered_count': sum(1 for q_id in result['correct_answers'] if q_id not in result['user_answers']),
            'total_questions': len(quiz_data['questions']),
            'user_answers': result['user_answers'],
            'correct_answers': result['correct_answers'],
            'time_taken_seconds': result['time_taken_seconds']
        }
        return render_template('results.html', results=results_data, questions=quiz_data['questions'])
    else:
        return "Result not found.", 404

if __name__ == '__main__':
    app.run(debug=True)