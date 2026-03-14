# BranchFit V2 Setup Instructions (MongoDB Version)

## Overview

BranchFit is a Flask web application that:
- 🧠 Uses an adaptive AI test to recommend engineering branches
- 📊 Supports general and branch-specific tests
- 📈 Shows a dashboard and test history
- 💾 Stores users and test results in **MongoDB Atlas**

---

## Step 1: MongoDB Atlas Setup

1. Go to `https://www.mongodb.com/atlas` and create a free account (or log in).
2. Create a new **free shared cluster**.
3. Under **Database Access**, create a database user with username and password.
4. Under **Network Access**, allow access from your IP (or `0.0.0.0/0` for testing only).
5. From **Database > Connect > Drivers**, copy your connection string, e.g.:
   `mongodb+srv://USERNAME:PASSWORD@your-cluster.mongodb.net/branchfit?retryWrites=true&w=majority&appName=your-app-name`

---

## Step 2: Environment Setup

### 2.1 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.2 Create Environment File

1. Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

2. Edit `.env` and set:

```env
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
MONGO_URI=your_mongodb_connection_string_here
```

---

## Step 3: Run the Application

### 3.1 Start the Server

```bash
python app.py
```

### 3.2 Access the Application

- Open your browser to: `http://localhost:5000`
- Register a new account
- Start taking tests!

---

## Application Structure

### Main Features

#### 1. **Landing Page** (`/`)
- Introduction to BranchFit
- Login/Register options

#### 2. **User Dashboard** (`/dashboard`)
- Branch cards and entry points to tests
- Access to test history stored in MongoDB

#### 3. **Test Types**

**Adaptive Test Logic**
- Advanced adaptive logic is implemented in `adaptive_system_v2.py`.
- A faster heuristic adaptive flow is implemented directly in `app.py`.

**General and Branch Tests**
- General test and branch-focused tests are implemented as routes in `app.py`.

#### 4. **User Management**
- Registration, login, and test history retrieval are handled in `app.py` using MongoDB.

---

## Database Data Model (MongoDB)

- **users** collection (stored via `users_collection` in `app.py`):
  - `username`, `email`, `password` (hashed), `created_at`
- **test_results** collection (stored via `results_collection` in `app.py`):
  - `username`, `test_type`, `target_branch`, `top_branch`, `confidence`, `questions_asked`, `timestamp`
  
Active test sessions are kept **in memory** in `app.py` and are not persisted.

---

## Customization Options

### Adding New Questions
1. Edit `adaptive_questions.json`
2. Add questions to appropriate sections
3. Retrain model if needed: `python retrain_model.py`

### Modifying Test Logic
1. Edit `adaptive_system_v2.py` for adaptive logic
2. Edit `app_v2.py` for individual branch test logic

### Styling and UI
1. Templates are in `templates/` folder
2. Static files (CSS, JS) go in `static/` folder
3. Uses Bootstrap for responsive design

---

## Troubleshooting

### Common Issues:

**1. MongoDB Connection Error**
- Check your `MONGO_URI` in `.env` is correct.
- Ensure your Atlas cluster is running and IP access is configured.

**2. Model Loading Error**
- Ensure `model.pkl` and `scaler.pkl` exist
- Retrain if needed: `python retrain_model.py`

**3. Import Errors**
- Install all dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ recommended)

**4. Database Errors**
- Verify your MongoDB user has correct permissions for the `branchfit` database.

### Getting Help:
1. Check the console output for detailed error messages
2. Verify all files are in the correct directory
3. Test each component individually using the provided scripts

---

## Production Deployment

### Security Checklist:
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS
- [ ] Configure proper CORS settings
- [ ] Set up MongoDB backups / snapshots

---

## Next Steps

1. **Complete the setup** following steps 1-3
2. **Test the application** with sample users
3. **Customize the questions** for your specific needs
4. **Add more features** like:
   - Email notifications
   - PDF report generation
   - Admin dashboard
   - Advanced analytics
   - Career guidance integration

Enjoy your new BranchFit application! 🚀