# 🚀 Quick Start Guide - Dual Authentication System

## 📌 Test Credentials

### Admin Login
```
LSC Code: LC2101-CDOE
Password: admin123
Database: online_edu.lsc_admins
```

### LSC User Login
```
LSC Number: LC3001
Password: user123
Database: lsc_portal_db.lsc_auth_lscuser
```

---

## 🔥 Quick Commands

### Start Backend Server
```bash
cd backend
python manage.py runserver
```

### Test Both Logins
```bash
python test_both_logins.py
```

### Create New LSC User
```bash
python create_test_lsc_user.py
```

### Create auth_user Table (if needed)
```bash
python create_auth_user_table.py
```

---

## 🎯 API Endpoints

### Login
```http
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
  "lscNumber": "LC2101-CDOE",
  "password": "admin123"
}
```

### Response
```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci...",
  "user": {
    "lsc_code": "LC2101-CDOE",
    "lsc_name": "Centre for Distance and Online Education",
    "user_type": "admin",
    "database": "online_edu"
  }
}
```

---

## 🔍 Check User Type in Frontend

```javascript
// Get user info from localStorage
const userInfo = JSON.parse(localStorage.getItem('user_info'));

// Check user type
if (userInfo.user_type === 'admin') {
  console.log('Admin user from online_edu');
} else if (userInfo.user_type === 'user') {
  console.log('LSC user from lsc_portal_db');
}

// Access LSC code/number
const lscIdentifier = userInfo.lsc_code || userInfo.lsc_number;
```

---

## 🛠️ Key Files

### Backend
- `backend/settings.py` - Database configuration
- `backend/db_router.py` - Query routing
- `lsc_auth/models.py` - User models
- `lsc_auth/auth_backend.py` - Authentication logic
- `lsc_auth/views.py` - Login endpoint

### Frontend
- `src/lib/api.ts` - API client
- `src/components/LoginPage.tsx` - Login UI

---

## ⚡ PowerShell Test

```powershell
# Test Admin Login
$body = @{lscNumber='LC2101-CDOE'; password='admin123'} | ConvertTo-Json
Invoke-RestMethod -Uri 'http://localhost:8000/api/auth/login/' -Method POST -Body $body -ContentType 'application/json'

# Test LSC User Login
$body = @{lscNumber='LC3001'; password='user123'} | ConvertTo-Json
Invoke-RestMethod -Uri 'http://localhost:8000/api/auth/login/' -Method POST -Body $body -ContentType 'application/json'
```

---

## 📊 Database Structure

### online_edu.lsc_admins
```
- id (Primary Key)
- lsc_code (Unique)
- center_name
- admin_name
- email
- mobile
- password (hashed)
- is_active
```

### lsc_portal_db.lsc_auth_lscuser
```
- id (Primary Key)
- lsc_number (Unique)
- lsc_name
- email
- password (hashed)
- is_active
- is_staff
- date_joined
```

---

## ✅ Success Indicators

When everything is working:
- ✓ Both login types return 200 status
- ✓ JWT access & refresh tokens are generated
- ✓ `user_type` field correctly shows "admin" or "user"
- ✓ `database` field shows correct source
- ✓ No "Table doesn't exist" errors
- ✓ Frontend stores user info in localStorage

---

## 🐛 Common Issues

### "Table 'lsc_portal_db.auth_user' doesn't exist"
```bash
python create_auth_user_table.py
```

### "No module named 'rest_framework_simplejwt'"
```bash
pip install djangorestframework-simplejwt
```

### Login returns 401 Unauthorized
- Check username/password
- Verify user exists in correct database
- Check `is_active` field is True

---

## 📝 Notes

- Admin users have full access
- LSC users have limited access based on their center
- JWT tokens expire after 5 minutes (access) / 24 hours (refresh)
- User type is embedded in JWT token claims
- No need to query database to check user type after login

---

**Ready to use!** 🎉
