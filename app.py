from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# The quiz data
questions = [
    {
        'id': 1,
        'question': 'What is the capital of France?',
        'options': ['Berlin', 'Madrid', 'Paris', 'Rome'],
        'answer': 'Paris'
    },
    {
        'id': 2,
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Mars', 'Venus', 'Jupiter', 'Saturn'],
        'answer': 'Mars'
    },
    {
        'id': 3,
        'question': 'What is the largest ocean on Earth?',
        'options': ['Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Pacific Ocean'],
        'answer': 'Pacific Ocean'
    },
    {
        'id': 4,
        'question': 'Who wrote "Romeo and Juliet"?',
        'options': ['Charles Dickens', 'William Shakespeare', 'Mark Twain', 'Jane Austen'],
        'answer': 'William Shakespeare'
    },
    {
        'id': 5,
        'question': 'What is the currency of Japan?',
        'options': ['Yuan', 'Euro', 'Yen', 'Dollar'],
        'answer': 'Yen'
    },
    {
        'id': 6,
        'question': 'Which element has the chemical symbol "O"?',
        'options': ['Gold', 'Oxygen', 'Silver', 'Hydrogen'],
        'answer': 'Oxygen'
    },
    {
        'id': 7,
        'question': 'What is the smallest country in the world?',
        'options': ['Monaco', 'Vatican City', 'San Marino', 'Liechtenstein'],
        'answer': 'Vatican City'
    },
    {
        'id': 8,
        'question': 'How many continents are there?',
        'options': ['5', '6', '7', '8'],
        'answer': '7'
    },
    {
        'id': 9,
        'question': 'What is the boiling point of water in Celsius?',
        'options': ['0°C', '50°C', '100°C', '200°C'],
        'answer': '100°C'
    },
    {
        'id': 10,
        'question': 'Which animal is the largest on Earth?',
        'options': ['African Elephant', 'Blue Whale', 'Great White Shark', 'Giraffe'],
        'answer': 'Blue Whale'
    },
    {
        'id': 11,
        'question': 'What is the powerhouse of the cell?',
        'options': ['Nucleus', 'Mitochondria', 'Cytoplasm', 'Ribosome'],
        'answer': 'Mitochondria'
    },
    {
        'id': 12,
        'question': 'Who painted the Mona Lisa?',
        'options': ['Vincent van Gogh', 'Pablo Picasso', 'Leonardo da Vinci', 'Claude Monet'],
        'answer': 'Leonardo da Vinci'
    },
    {
        'id': 13,
        'question': 'Which country is the Great Wall in?',
        'options': ['Japan', 'India', 'China', 'Russia'],
        'answer': 'China'
    },
    {
        'id': 14,
        'question': 'What is the hardest natural substance?',
        'options': ['Gold', 'Iron', 'Diamond', 'Quartz'],
        'answer': 'Diamond'
    },
    {
        'id': 15,
        'question': 'In which year did the Titanic sink?',
        'options': ['1910', '1912', '1915', '1920'],
        'answer': '1912'
    },
    {
        'id': 16,
        'question': 'What is the largest desert in the world?',
        'options': ['Gobi Desert', 'Sahara Desert', 'Kalahari Desert', 'Arabian Desert'],
        'answer': 'Sahara Desert'
    },
    {
        'id': 17,
        'question': 'How many bones are in the human body?',
        'options': ['206', '210', '198', '200'],
        'answer': '206'
    },
    {
        'id': 18,
        'question': 'What is the main component of Earth\'s atmosphere?',
        'options': ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Argon'],
        'answer': 'Nitrogen'
    },
    {
        'id': 19,
        'question': 'Which is the fastest land animal?',
        'options': ['Cheetah', 'Lion', 'Gazelle', 'Leopard'],
        'answer': 'Cheetah'
    },
    {
        'id': 20,
        'question': 'What is the square root of 64?',
        'options': ['6', '7', '8', '9'],
        'answer': '8'
    }
]


@app.route('/')
def quiz():
    return render_template('quiz.html', questions=questions)


@app.route('/submit', methods=['POST'])
def submit():
    answers = request.get_json()
    score = 0
    correct_answers = {}

    for q in questions:
        question_id = str(q['id'])
        correct_answer = q['answer']
        user_answer = answers.get(question_id)
        correct_answers[question_id] = correct_answer

        if user_answer == correct_answer:
            score += 1

    return jsonify({'score': score, 'total': len(questions), 'correct_answers': correct_answers})

if __name__ == '__main__':
    app.run(debug=True)
