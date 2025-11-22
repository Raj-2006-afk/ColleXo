# ColleXo - College Societies Management System

A production-grade web application for managing college societies, streamlining recruitment processes, and connecting students with opportunities.

## 👥 Team Members

- **Prachetas Shukla** (2024UCM2345)
- **Ranbir Singh** (2024UCM2308)
- **Supreet Singh** (2024UCM2333)

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Demo Credentials](#demo-credentials)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## ✨ Features

### For Students

- Browse and explore various college societies
- Submit applications through easy-to-use forms
- Track application status in real-time

### For Society Heads

- Manage society profile and information
- Create and publish recruitment forms
- Review and filter incoming applications
- Shortlist and accept/reject candidates
- Create new societies

### For Administrators

- Oversee all societies and activities
- Monitor platform usage and statistics
- Manage user accounts

## 🛠 Technology Stack

- **Backend**: Flask 3.0.0 + JWT Authentication + MySQL
- **Frontend**: React 18.2.0 + Vite 5.0.8 + Tailwind CSS 3.3.6
- **Database**: MySQL 8.0+ (via XAMPP)
- **Authentication**: JWT tokens with bcrypt password hashing

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** and npm - [Download Node.js](https://nodejs.org/)
- **XAMPP** (for MySQL) - [Download XAMPP](https://www.apachefriends.org/)
- **Git** - [Download Git](https://git-scm.com/)

## 🚀 Installation & Setup

### Step 0: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Raj-2006-afk/ColleXo.git
cd ColleXo
```

Or download the ZIP file from GitHub and extract it.

### Step 1: Start MySQL Database

1. Open **XAMPP Control Panel**
2. Click **Start** next to **MySQL**
3. Ensure MySQL is running on port 3306 (default)

> **Note**: The application will automatically create the database and tables on first run!

### Step 2: Backend Setup

Open a terminal and navigate to the backend directory:

```powershell
cd backend
```

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

### Step 3: Frontend Setup

Open a **new** terminal window and navigate to the frontend directory:

```powershell
cd frontend
```

Install Node.js dependencies:

```powershell
npm install
```

## ▶️ Running the Application

### Start the Backend

In the backend terminal:

```powershell
python app.py
```

**Expected Output:**

```
============================================================
🚀 ColleXo Backend Starting...
============================================================
📍 Server: http://localhost:5000
📊 Database: MySQL (localhost:3306)
============================================================
🔧 Initializing Database...
✅ Database 'collexo' ready
✅ Table 'users' ready
✅ Table 'societies' ready
✅ Table 'forms' ready
✅ Table 'applications' ready
✅ Seed data inserted successfully!
```

Backend is now running at **http://localhost:5000**

### Start the Frontend

In the frontend terminal:

```powershell
npm run dev
```

**Expected Output:**

```
  VITE v5.0.8  ready in 324 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Frontend is now running at **http://localhost:5173**

### Access the Application

Open your browser and navigate to:

```
http://localhost:5173
```

## 🔑 Demo Credentials

| Role             | Email               | Password   |
| ---------------- | ------------------- | ---------- |
| **Student**      | student@collexo.com | student123 |
| **Society Head** | john@collexo.com    | head123    |
| **Admin**        | admin@collexo.com   | admin123   |

## 📁 Project Structure

```
ColleXo/
├── backend/                   # Flask API
│   ├── app.py                # Main application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── config/
│   │   └── db.py            # Database configuration
│   ├── controllers/
│   │   └── auth_controller.py
│   ├── middleware/
│   │   └── auth.py          # JWT authentication
│   ├── models/              # Database models
│   │   ├── user.py
│   │   ├── society.py
│   │   ├── form.py
│   │   └── application.py
│   ├── routes/              # API endpoints
│   │   ├── auth_routes.py
│   │   ├── society_routes.py
│   │   ├── form_routes.py
│   │   ├── application_routes.py
│   │   └── admin_routes.py
│   └── utils/
│       └── validators.py
│
├── frontend/                 # React application
│   ├── src/
│   │   ├── main.jsx         # Entry point
│   │   ├── App.jsx          # Root component
│   │   ├── api/             # API client
│   │   ├── context/         # Auth context
│   │   ├── router/          # Routing configuration
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   │   ├── student/
│   │   │   ├── societyHead/
│   │   │   └── admin/
│   │   └── styles/          # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── docs/
│   ├── postman.json         # API collection
│   ├── schema.md            # Database schema
│   └── PROJECT_SUMMARY.md   # Feature documentation
│
├── .gitignore
├── run.bat                  # Windows run script
└── README.md
```

## 🔌 API Documentation

### Authentication Endpoints (3)

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Society Endpoints (6)

- `GET /api/societies/browse` - Browse all societies (public)
- `GET /api/societies/<id>` - Get society details
- `POST /api/societies` - Create new society (Society Head/Admin)
- `GET /api/societies/my-society` - Get current user's society
- `PUT /api/societies/<id>` - Update society
- `DELETE /api/societies/<id>` - Delete society (Admin)

### Form Endpoints (6)

- `GET /api/forms/published` - Get published forms
- `GET /api/forms/<id>` - Get form details
- `POST /api/forms` - Create form (Society Head)
- `GET /api/forms/society/<id>` - Get society forms
- `PUT /api/forms/<id>` - Update form
- `DELETE /api/forms/<id>` - Delete form

### Application Endpoints (6)

- `POST /api/applications` - Submit application
- `GET /api/applications/my-applications` - Get user's applications
- `GET /api/applications/society/<id>` - Get society applications
- `GET /api/applications/form/<id>` - Get form applications
- `GET /api/applications/<id>` - Get application details
- `PUT /api/applications/<id>/status` - Update application status

### Admin Endpoints (4)

- `GET /api/admin/users` - Get all users
- `GET /api/admin/societies` - Get all societies
- `PUT /api/admin/societies/<id>/approve` - Approve society
- `GET /api/admin/dashboard/stats` - Get dashboard statistics

For complete API testing, import `docs/postman.json` into Postman.

## 🗄️ Database Schema

The application automatically creates 4 tables:

### USERS

- `user_id` (PK, AUTO_INCREMENT)
- `user_name` (VARCHAR)
- `user_email` (UNIQUE)
- `user_password` (Bcrypt hashed)
- `user_role` (ENUM: student/societyHead/admin)
- `created_at` (DATETIME)

### SOCIETIES

- `society_id` (PK, AUTO_INCREMENT)
- `society_name` (UNIQUE)
- `tagline` (VARCHAR)
- `description` (TEXT)
- `category` (VARCHAR)
- `logo_url` (VARCHAR)
- `member_count` (INT)
- `admission_open` (BOOLEAN)
- `admission_deadline` (DATE)
- `society_head_id` (FK → users)
- `created_at` (DATETIME)

### FORMS

- `form_id` (PK, AUTO_INCREMENT)
- `society_id` (FK → societies)
- `title` (VARCHAR)
- `status` (ENUM: draft/published)
- `created_at` (DATETIME)
- `published_at` (DATETIME)

### APPLICATIONS

- `application_id` (PK, AUTO_INCREMENT)
- `user_id` (FK → users)
- `society_id` (FK → societies)
- `form_id` (FK → forms)
- `application_date` (DATE)
- `status` (ENUM: pending/shortlisted/accepted/rejected)
- `submitted_at` (DATETIME)

## 🔧 Troubleshooting

### Backend Issues

#### Error: "Can't connect to MySQL server"

**Solution**:

- Ensure XAMPP MySQL is running
- Check that MySQL is on port 3306
- Verify MySQL credentials in `backend/config/db.py`

#### Error: "ModuleNotFoundError"

**Solution**:

```powershell
cd backend
pip install -r requirements.txt
```

#### Error: "Port 5000 already in use"

**Solution**: Kill the process or change the port in `backend/app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Frontend Issues

#### Error: "Cannot find module 'react'"

**Solution**:

```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

#### Error: "Failed to fetch" or CORS errors

**Solution**:

- Ensure backend is running on http://localhost:5000
- Check browser console for specific error messages
- Verify CORS is properly configured in `backend/app.py`

#### Blank page after login

**Solution**:

- Clear browser cache and local storage
- Hard refresh (Ctrl+Shift+R)
- Check browser console for errors

### Database Issues

#### Tables not created

**Solution**:

- Restart the backend application
- Check terminal output for database creation logs
- Verify MySQL is running and accessible

## 🧪 Testing the Application

### Manual Testing Flow

1. **As Student**:

   - Register new account or login with `student@collexo.com`
   - Browse societies
   - View society details
   - Submit applications

2. **As Society Head**:

   - Login with `john@collexo.com`
   - Create a new society (if not assigned)
   - Manage society profile
   - Create recruitment forms
   - Review applications
   - Update application statuses

3. **As Admin**:
   - Login with `admin@collexo.com`
   - View all users and societies
   - Approve societies
   - View platform statistics

### API Testing

1. Import `docs/postman.json` into Postman
2. Use the login endpoint to get a JWT token
3. Set the token in the authorization header
4. Test all endpoints

## 📝 Development Commands

### Backend Development

```powershell
# Run development server
python app.py

# Install new package
pip install package_name
pip freeze > requirements.txt
```

### Frontend Development

```powershell
# Run development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🔒 Security Features

- **Password Hashing**: Bcrypt with salt
- **JWT Authentication**: Token-based auth with 7-day expiration
- **Role-Based Access Control**: Three distinct user roles
- **SQL Injection Prevention**: Parameterized queries
- **Input Validation**: Server-side validation on all endpoints
- **CORS Protection**: Configured for localhost development

## 🌟 Features Roadmap

- [x] User authentication and authorization
- [x] Society management
- [x] Application workflow
- [x] Admin dashboard
- [x] Society head dashboard
- [x] Student dashboard
- [x] Society creation by heads
- [ ] Email notifications
- [ ] File uploads for applications
- [ ] Advanced search and filters
- [ ] Analytics and reporting
- [ ] Mobile responsive design improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes.

## 📞 Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Check existing documentation in `/docs`
- Review troubleshooting section above

---

**Built with ❤️ using Flask, React, and MySQL**

_Last Updated: November 2025_
