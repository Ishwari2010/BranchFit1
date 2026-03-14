from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import numpy as np
import json
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import random
from pymongo import MongoClient
from dotenv import load_dotenv
import os

print("🚀 Starting BranchFit - Fixed Branch Tests...")

# Load components
try:
    # Load dataset for questions
    df = pd.read_csv('balanced_dataset_full__1_.csv')
    all_questions = list(df.columns[1:])
    
    # Load model and scaler
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('branch_labels.json', 'r') as f:
        branch_labels = json.load(f)
    
    print(f"✓ Loaded {len(all_questions)} questions")
    print(f"✓ Model: {model.__class__.__name__}")
    
except Exception as e:
    print(f"❌ Error loading components: {e}")
    exit(1)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# MongoDB setup
load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client['branchfit']
users_collection = db['users']
results_collection = db['test_results']

# Storage
users = {}
test_sessions = {}

# Branch information
BRANCHES = {
    'Computer Engineering': {
        'description': 'Design and develop computer hardware, embedded systems, and digital circuits',
        'skills': ['Hardware Design', 'Digital Circuits', 'Embedded Systems', 'VLSI Design'],
        'icon': 'fas fa-microchip',
        'color': 'primary'
    },
    'EXTC': {
        'description': 'Electronics and Telecommunication - signals, communication systems, and networks',
        'skills': ['Signal Processing', 'Communication Systems', 'RF Engineering', 'Network Protocols'],
        'icon': 'fas fa-broadcast-tower',
        'color': 'success'
    },
    'Electrical': {
        'description': 'Power systems, electrical machines, and energy distribution',
        'skills': ['Power Systems', 'Electrical Machines', 'Control Systems', 'Power Electronics'],
        'icon': 'fas fa-bolt',
        'color': 'warning'
    },
    'Information Technology/CSE': {
        'description': 'Software development, databases, algorithms, and information systems',
        'skills': ['Programming', 'Database Management', 'Web Development', 'Data Structures'],
        'icon': 'fas fa-laptop-code',
        'color': 'info'
    },
    'Mechanical': {
        'description': 'Mechanical systems, manufacturing, thermodynamics, and design',
        'skills': ['Mechanical Design', 'Thermodynamics', 'Manufacturing', 'CAD/CAM'],
        'icon': 'fas fa-cogs',
        'color': 'danger'
    }
}

# Pre-computed question categories for fast selection
QUESTION_CATEGORIES = {
    'foundation': [0, 1, 2, 3, 4],  # First 5 questions - always ask these
    'computer_eng': [],
    'extc': [],
    'electrical': [],
    'it_cse': [],
    'mechanical': []
}

# Categorize questions by keywords (pre-computed for speed)
def categorize_questions():
    """Pre-categorize questions by branch keywords for fast lookup."""
    keywords = {
        'computer_eng': ['hardware', 'circuits', 'electronic', 'digital', 'components'],
        'extc': ['signals', 'communication', 'transmission', 'frequency', 'networks'],
        'electrical': ['electrical', 'voltage', 'current', 'power', 'electricity'],
        'it_cse': ['software', 'code', 'database', 'programming', 'apps'],
        'mechanical': ['mechanical', 'machines', 'motion', 'forces', 'materials']
    }
    
    for i, question in enumerate(all_questions):
        question_lower = question.lower()
        max_matches = 0
        best_category = 'foundation'
        
        for category, category_keywords in keywords.items():
            matches = sum(1 for keyword in category_keywords if keyword in question_lower)
            if matches > max_matches:
                max_matches = matches
                best_category = category
        
        if best_category != 'foundation' and i >= 5:  # Skip first 5 for foundation
            QUESTION_CATEGORIES[best_category].append(i)
        elif i < 5:
            QUESTION_CATEGORIES['foundation'].append(i)

# Initialize question categories
categorize_questions()

def get_fast_prediction(responses):
    """Fast prediction using the trained model."""
    features = np.array([3.0] * len(all_questions))  # Neutral default
    
    for q_idx, response in responses.items():
        if q_idx < len(features):
            features[q_idx] = float(response)
    
    features_scaled = scaler.transform(features.reshape(1, -1))
    probabilities = model.predict_proba(features_scaled)[0]
    
    branch_probs = {}
    for label_str, branch_name in branch_labels.items():
        label_idx = int(label_str)
        if label_idx < len(probabilities):
            branch_probs[branch_name] = probabilities[label_idx]
    
    return branch_probs

def get_branch_specific_score(responses, target_branch):
    """Calculate a more accurate branch-specific score."""
    if not responses:
        return 0.5  # Neutral score
    
    # Get model prediction
    model_probs = get_fast_prediction(responses)
    base_score = model_probs.get(target_branch, 0)
    
    # Calculate response-based score for the target branch
    branch_to_category = {
        'Computer Engineering': 'computer_eng',
        'EXTC': 'extc',
        'Electrical': 'electrical',
        'Information Technology/CSE': 'it_cse',
        'Mechanical': 'mechanical'
    }
    
    if target_branch not in branch_to_category:
        return base_score
    
    category = branch_to_category[target_branch]
    relevant_questions = QUESTION_CATEGORIES[category]
    
    # Calculate average response for relevant questions
    relevant_responses = [responses[q] for q in relevant_questions if q in responses]
    
    if relevant_responses:
        avg_response = sum(relevant_responses) / len(relevant_responses)
        # Convert 1-5 scale to 0-1 probability
        response_score = (avg_response - 1) / 4  # 1->0, 3->0.5, 5->1
        
        # Combine model prediction with response-based score
        combined_score = 0.6 * base_score + 0.4 * response_score
        return combined_score
    
    return base_score

def select_next_question_fast(responses, asked_questions, question_count, target_branch=None):
    """Fast adaptive question selection."""
    available = [i for i in range(len(all_questions)) if i not in asked_questions]
    
    if not available:
        return None
    
    # For branch-specific tests, focus heavily on that branch
    if target_branch:
        branch_to_category = {
            'Computer Engineering': 'computer_eng',
            'EXTC': 'extc',
            'Electrical': 'electrical',
            'Information Technology/CSE': 'it_cse',
            'Mechanical': 'mechanical'
        }
        
        if target_branch in branch_to_category:
            category = branch_to_category[target_branch]
            
            # First few questions: mix of foundation and target branch
            if question_count < 3:
                foundation_available = [q for q in QUESTION_CATEGORIES['foundation'] if q not in asked_questions]
                if foundation_available:
                    return foundation_available[0]
            
            # Most questions should be from target branch
            category_questions = [q for q in QUESTION_CATEGORIES[category] if q not in asked_questions]
            if category_questions:
                return random.choice(category_questions[:5])  # Pick from top 5
    
    # General test logic
    # Phase 1: Foundation questions (first 5)
    if question_count < 5:
        foundation_available = [q for q in QUESTION_CATEGORIES['foundation'] if q not in asked_questions]
        if foundation_available:
            return foundation_available[0]
    
    # Phase 2: Adaptive selection based on current predictions
    if len(responses) >= 3:
        current_probs = get_fast_prediction(responses)
        
        # Get top 2 branches
        sorted_branches = sorted(current_probs.items(), key=lambda x: x[1], reverse=True)
        top_branch = sorted_branches[0][0]
        
        # Map branch names to categories
        branch_to_category = {
            'Computer Engineering': 'computer_eng',
            'EXTC': 'extc',
            'Electrical': 'electrical',
            'Information Technology/CSE': 'it_cse',
            'Mechanical': 'mechanical'
        }
        
        # Get questions from top branch category
        if top_branch in branch_to_category:
            category = branch_to_category[top_branch]
            category_questions = [q for q in QUESTION_CATEGORIES[category] if q not in asked_questions]
            
            if category_questions:
                # Add some randomness to avoid predictable patterns
                if len(category_questions) > 3:
                    return random.choice(category_questions[:3])  # Pick from top 3
                else:
                    return category_questions[0]
    
    # Phase 3: Random selection from remaining questions
    return random.choice(available)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            flash('Username already exists', 'error')
        else:
            users_collection.insert_one({
                'username': username,
                'email': email,
                'password': generate_password_hash(password),
                'created_at': datetime.now().isoformat()
            })
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', branches=BRANCHES)

@app.route('/general-test')
def general_test():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    session_id = f"{session['user']}_{datetime.now().timestamp()}"
    
    test_sessions[session_id] = {
        'user': session['user'],
        'type': 'general',
        'responses': {},
        'asked_questions': set(),
        'question_count': 0,
        'start_time': datetime.now().isoformat()
    }
    
    session['test_session'] = session_id
    session['test_type'] = 'general'
    
    print(f"✓ Created general test session: {session_id}")
    return render_template('test_start.html', test_type='General Branch Fit Test')

@app.route('/branch-test/<branch>')
def branch_test(branch):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if branch not in BRANCHES:
        flash('Invalid branch selected', 'error')
        return redirect(url_for('dashboard'))
    
    session_id = f"{session['user']}_{branch}_{datetime.now().timestamp()}"
    
    test_sessions[session_id] = {
        'user': session['user'],
        'type': 'branch',
        'target_branch': branch,
        'responses': {},
        'asked_questions': set(),
        'question_count': 0,
        'start_time': datetime.now().isoformat()
    }
    
    session['test_session'] = session_id
    session['test_type'] = 'branch'
    session['target_branch'] = branch
    
    print(f"✓ Created {branch} focused test session: {session_id}")
    return render_template('test_start.html', 
                         test_type=f'{branch} Suitability Test',
                         branch_info=BRANCHES[branch])

@app.route('/question')
def question():
    if 'user' not in session or 'test_session' not in session:
        return redirect(url_for('login'))
    
    session_id = session['test_session']
    if session_id not in test_sessions:
        flash('Test session expired. Please start a new test.', 'error')
        return redirect(url_for('dashboard'))
    
    test_session = test_sessions[session_id]
    
    # Set question limits: 30 for general, 20 for branch tests
    max_questions = 30 if test_session['type'] == 'general' else 20
    
    # Check if we've reached the limit
    if test_session['question_count'] >= max_questions:
        print(f"📊 Completed maximum {max_questions} questions")
        return redirect(url_for('results'))
    
    # Fast early stopping check
    if test_session['question_count'] >= 10 and len(test_session['responses']) >= 10:
        if test_session['type'] == 'general':
            current_probs = get_fast_prediction(test_session['responses'])
            max_confidence = max(current_probs.values())
            if max_confidence >= 0.80:
                print(f"🎯 Stopping early due to high confidence: {max_confidence:.1%}")
                return redirect(url_for('results'))
        else:
            # For branch tests, use branch-specific scoring
            target_branch = test_session.get('target_branch')
            if target_branch:
                branch_score = get_branch_specific_score(test_session['responses'], target_branch)
                if branch_score >= 0.80 or branch_score <= 0.20:  # Very high or very low
                    print(f"🎯 Stopping early - {target_branch} score: {branch_score:.1%}")
                    return redirect(url_for('results'))
    
    # Get next question (fast selection)
    target_branch = test_session.get('target_branch') if test_session['type'] == 'branch' else None
    question_idx = select_next_question_fast(
        test_session['responses'], 
        test_session['asked_questions'],
        test_session['question_count'],
        target_branch
    )
    
    if question_idx is None:
        print("🔚 No more questions available")
        return redirect(url_for('results'))
    
    session['current_question_idx'] = question_idx
    
    # Get question text
    question_text = all_questions[question_idx]
    
    question_data = {
        'id': question_idx,
        'question': question_text,
        'type': 'scale'
    }
    
    # Calculate progress
    progress = ((test_session['question_count'] + 1) / max_questions) * 100
    
    # Get current prediction
    current_prediction = None
    if test_session['question_count'] > 2:
        try:
            if test_session['type'] == 'branch':
                target_branch = test_session.get('target_branch')
                if target_branch:
                    branch_score = get_branch_specific_score(test_session['responses'], target_branch)
                    current_prediction = f"{target_branch} Fit: {branch_score*100:.0f}%"
            else:
                current_probs = get_fast_prediction(test_session['responses'])
                top_branch = max(current_probs.items(), key=lambda x: x[1])
                current_prediction = f"{top_branch[0]} ({top_branch[1]*100:.0f}%)"
        except:
            pass
    
    return render_template('question.html', 
                         question=question_data,
                         progress=min(progress, 100),
                         question_num=test_session['question_count'] + 1,
                         total_questions=max_questions,
                         current_prediction=current_prediction)

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    if 'user' not in session or 'test_session' not in session:
        return redirect(url_for('login'))
    
    session_id = session['test_session']
    if session_id not in test_sessions:
        flash('Test session expired. Please start a new test.', 'error')
        return redirect(url_for('dashboard'))
    
    test_session = test_sessions[session_id]
    answer = request.form.get('answer')
    
    if not answer:
        flash('Please select an answer', 'error')
        return redirect(url_for('question'))
    
    try:
        answer_value = int(answer)
        
        question_idx = session.get('current_question_idx')
        
        if question_idx is not None:
            # Record the answer
            test_session['responses'][question_idx] = answer_value
            test_session['asked_questions'].add(question_idx)
            test_session['question_count'] += 1
            
            print(f"📝 Q{test_session['question_count']}: Answer {answer_value}")
            
            # Show current prediction (only occasionally to save time)
            if test_session['question_count'] % 3 == 0:  # Every 3rd question
                if test_session['type'] == 'branch':
                    target_branch = test_session.get('target_branch')
                    if target_branch:
                        branch_score = get_branch_specific_score(test_session['responses'], target_branch)
                        print(f"🎯 {target_branch} fit: {branch_score*100:.1f}%")
                else:
                    current_probs = get_fast_prediction(test_session['responses'])
                    top_branch = max(current_probs.items(), key=lambda x: x[1])
                    print(f"🎯 Current prediction: {top_branch[0]} ({top_branch[1]*100:.1f}%)")
        
        return redirect(url_for('question'))
        
    except Exception as e:
        print(f"Error processing answer: {e}")
        flash('Error processing your answer. Please try again.', 'error')
        return redirect(url_for('question'))

@app.route('/results')
def results():
    if 'user' not in session or 'test_session' not in session:
        return redirect(url_for('login'))
    
    session_id = session['test_session']
    if session_id not in test_sessions:
        flash('Test session expired. Please start a new test.', 'error')
        return redirect(url_for('dashboard'))
    
    test_session = test_sessions[session_id]
    
    # Get results based on test type
    if test_session['type'] == 'branch':
        # Branch-specific test results
        target_branch = test_session.get('target_branch')
        if target_branch:
            branch_score = get_branch_specific_score(test_session['responses'], target_branch)
            
            # Create results focused on the target branch
            branch_results = [{
                'branch': target_branch,
                'probability': branch_score * 100,
                'info': BRANCHES.get(target_branch, {})
            }]
            
            # Add other branches for comparison (using model predictions)
            model_probs = get_fast_prediction(test_session['responses'])
            for branch_name, probability in model_probs.items():
                if branch_name != target_branch:
                    branch_results.append({
                        'branch': branch_name,
                        'probability': probability * 100,
                        'info': BRANCHES.get(branch_name, {})
                    })
        else:
            # Fallback to model predictions
            current_probs = get_fast_prediction(test_session['responses'])
            branch_results = []
            for branch_name, probability in current_probs.items():
                branch_results.append({
                    'branch': branch_name,
                    'probability': probability * 100,
                    'info': BRANCHES.get(branch_name, {})
                })
    else:
        # General test results using model predictions
        current_probs = get_fast_prediction(test_session['responses'])
        branch_results = []
        for branch_name, probability in current_probs.items():
            branch_results.append({
                'branch': branch_name,
                'probability': probability * 100,
                'info': BRANCHES.get(branch_name, {})
            })
    
    # Sort by probability
    branch_results.sort(key=lambda x: x['probability'], reverse=True)
    
    print(f"🏆 Test completed! {test_session['question_count']} questions asked")
    print(f"🎯 Final prediction: {branch_results[0]['branch']} ({branch_results[0]['probability']:.1f}%)")
    
    # Save test result to MongoDB
    results_collection.insert_one({
        'username': session['user'],
        'test_type': test_session.get('type'),
        'target_branch': test_session.get('target_branch'),
        'top_branch': branch_results[0]['branch'],
        'confidence': branch_results[0]['probability'],
        'questions_asked': test_session['question_count'],
        'timestamp': datetime.now().isoformat()
    })
    
    return render_template('results.html', 
                         results=branch_results,
                         test_type=test_session.get('type', 'general'),
                         target_branch=test_session.get('target_branch'),
                         questions_asked=test_session['question_count'],
                         confidence=branch_results[0]['probability']/100 if branch_results else 0)

@app.route('/test-history')
def test_history():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    tests = list(results_collection.find(
        {'username': session['user']},
        {'_id': 0}
    ).sort('timestamp', -1))
    
    return render_template('test_history.html', tests=tests)

if __name__ == '__main__':
    print("="*70)
    print("🌐 BranchFit Server: http://localhost:5000")
    print("⚡ Fixed Branch Tests - Accurate Individual Scoring")
    print("📊 General Test: 30 questions | Branch Test: 20 questions")
    print("🎯 Branch tests now focus on target branch questions")
    print("="*70)
    
    app.run(debug=True, port=5000, host='0.0.0.0')