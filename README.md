# LSC Portal - Complete Educational Management System

A comprehensive educational portal system built with Django REST Framework (backend) and React/TypeScript (frontend) featuring dual authentication and admission management.

## 🚀 Features

### Authentication System
- **Dual Login System**: Separate authentication for LSC users and administrators
- **JWT Authentication**: Secure token-based authentication with custom claims
- **Role-based Access**: Different permissions for users and admins

### Admission Management
- **Admission Sessions**: Create and manage admission periods
- **Application Settings**: Configure admission parameters, dates, and limits
- **Status Management**: Open/close admissions with automated status tracking
- **Validation**: Comprehensive form validation with detailed error messages

### Database Architecture
- **Triple Database Setup**: Separate databases for different data types
  - `lsc_portal_db`: LSC user data and Django internals
  - `online_edu`: Admin user data
  - `lsc_admindb`: Portal application data (admissions, settings)
- **Custom Database Router**: Automatic routing based on model types

### Frontend Features
- **Modern UI**: Built with React, TypeScript, and Tailwind CSS
- **Component Library**: Shadcn/ui components with Radix UI primitives
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Dynamic data loading and updates

## 🛠️ Tech Stack

### Backend
- **Django 5.2.7**: Web framework
- **Django REST Framework**: API development
- **MySQL**: Database
- **Simple JWT**: Authentication
- **Custom Database Router**: Multi-database management

### Frontend
- **React 18+**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Radix UI**: Component primitives
- **Axios**: HTTP client

## 📁 Project Structure

```
cdoe-lsc-portal/
├── backend/                 # Django backend
│   ├── backend/            # Django settings and configuration
│   ├── lsc_auth/           # Authentication app
│   ├── portal/             # Portal app (admissions, settings)
│   ├── admissions/         # Admission management app
│   └── manage.py           # Django management script
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── lib/           # Utilities and API functions
│   │   └── pages/         # Page components
│   └── public/            # Static assets
└── docs/                  # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup databases:**
   ```bash
   python migrate_to_lsc_admindb.py
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start development server:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

## 🔧 Configuration

### Database Configuration
The system uses three MySQL databases. Update `backend/backend/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lsc_portal_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'online_edu': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'online_edu',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'lsc_admindb': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lsc_admindb',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/login/` - User login
- `POST /api/auth/admin-login/` - Admin login
- `POST /api/auth/refresh/` - Refresh JWT token

### Admission Management
- `GET /api/application-settings/` - List admission sessions
- `POST /api/application-settings/` - Create admission session
- `PUT /api/application-settings/{id}/` - Update admission session
- `DELETE /api/application-settings/{id}/` - Delete admission session
- `POST /api/application-settings/{id}/toggle_status/` - Toggle admission status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions, please open an issue on GitHub.

## 🔄 Recent Updates

- ✅ Complete admission management system
- ✅ Triple database architecture with custom routing
- ✅ Enhanced authentication with dual login
- ✅ Modern React frontend with TypeScript
- ✅ Comprehensive error handling and validation
- ✅ Automated database migration scripts