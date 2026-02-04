# SmartCity Insight - Urban Issue Management System

## 📋 Overview

**SmartCity Insight** is a full-stack web application for urban issue management aligned with **SDG 11** (Sustainable Cities and Communities). This platform bridges the gap between citizens and municipal administration, enabling transparent, accountable, and efficient resolution of urban infrastructure issues.

### 🎯 Key Highlights
- **Role-Based System**: Separate interfaces for Citizens and Administrators
- **SLA-Driven**: Automated Service Level Agreement tracking (24-72 hours based on issue type)
- **Geo-Located Complaints**: Interactive map integration for precise location marking
- **Real-Time Analytics**: Dashboard with statistics, resolution rates, and performance metrics
- **Image Proof**: Before/after image upload capability
- **Responsive Design**: Mobile-first approach with civic/government aesthetic

## 🚀 Quick Start Guide (For Beginners)

This guide will help you set up the SmartCity Insight application on your computer, even if you have no programming experience. Just follow these steps carefully!

### 📋 What You'll Need

Before we begin, let's make sure you have everything installed:

#### 1. **Python** (The programming language this app uses)
   - **What is it?** Python is a programming language that makes this application work
   - **How to check if you have it:**
     - Open **Command Prompt** (Windows) or **Terminal** (Mac/Linux)
       - *Windows*: Press `Windows key + R`, type `cmd`, press Enter
       - *Mac*: Press `Command + Space`, type "Terminal", press Enter
     - Type: `python --version` and press Enter
     - You should see something like: `Python 3.10.0` or higher
   
   - **Don't have Python?** Download it here: https://www.python.org/downloads/
     - ✅ **IMPORTANT**: During installation, check the box that says "Add Python to PATH"
     - Choose version 3.10 or newer

#### 2. **A Text Editor** (To view/edit files)
   - We recommend **VS Code** (free): https://code.visualstudio.com/
   - Or use **Notepad** (already on Windows) or **TextEdit** (Mac)

#### 3. **A Web Browser** (To view the application)
   - Chrome, Firefox, Safari, or Edge will work perfectly

#### 4. **Internet Connection** (To download required files)

---

### 📥 Step-by-Step Installation

#### **Step 1: Download the Project Files**

**Option A - If you have the ZIP file:**
1. Right-click the ZIP file and select "Extract All"
2. Choose a location (like your Desktop or Documents folder)
3. Remember where you saved it!

**Option B - If using Git (advanced):**
```bash
git clone <repository-url>
```

#### **Step 2: Open Command Prompt/Terminal in the Project Folder**

**Windows:**
1. Open File Explorer and go to where you extracted the files
2. Navigate to the `SmartCities` folder inside the project
3. Click on the address bar at the top (where the folder path is shown)
4. Type `cmd` and press Enter
5. A black window (Command Prompt) will open in that folder

**Mac/Linux:**
1. Open Terminal
2. Type `cd ` (with a space after cd)
3. Drag the `SmartCities` folder onto the Terminal window
4. Press Enter

You should now see something like: `C:\Projects\SmartCities_Insights_Trash\SmartCities>`

#### **Step 3: Create a Virtual Environment**

*Don't worry! A "virtual environment" is like a separate workspace for this project.*

**Copy and paste this command, then press Enter:**

**For Windows:**
```bash
python -m venv .venv
```

**For Mac/Linux:**
```bash
python3 -m venv .venv
```

*Wait a few seconds. A new folder called `.venv` will be created.*

#### **Step 4: Activate the Virtual Environment**

*This tells your computer to use the project's workspace.*

**For Windows PowerShell:**
```bash
.\.venv\Scripts\Activate.ps1
```

**If you get an error about execution policy, try this instead:**
```bash
.\.venv\Scripts\activate.bat
```

**For Mac/Linux:**
```bash
source .venv/bin/activate
```

**✅ Success!** You should see `(.venv)` appear at the beginning of your command line.

#### **Step 5: Install Required Software Packages**

*These are the tools the application needs to work.*

**Copy and paste this command:**
```bash
pip install django python-dotenv
```

*Wait 1-2 minutes while it downloads and installs everything. You'll see lots of text scrolling.*

**✅ Done!** When you see the command prompt again, it's finished.

#### **Step 6: Set Up the Database**

*The database stores all the complaint information.*

**Run these commands one by one:**

```bash
python manage.py makemigrations
```
*Press Enter, wait for it to finish*

```bash
python manage.py migrate
```
*Press Enter, wait for it to finish*

**✅ Success!** You should see messages about creating database tables.

#### **Step 7: Create Demo User Accounts (Optional but Recommended)**

*This creates sample accounts so you can test the app immediately.*

```bash
python manage.py create_demo_account
```

**🔑 IMPORTANT:** The command will show usernames and passwords on the screen. **Write them down** or take a screenshot! You'll need these to login.

#### **Step 8: Start the Application**

*This command runs the website on your computer.*

```bash
python manage.py runserver
```

**✅ It's working!** When you see:
```
Starting development server at http://127.0.0.1:8000/
```

#### **Step 9: Open the Application in Your Browser**

1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Type this in the address bar: `http://127.0.0.1:8000/`
3. Press Enter

**🎉 Congratulations!** You should now see the SmartCity Insight home page!

---

### 🔐 Login Credentials

After running `create_demo_account`, you'll see:
- **Citizen Account**: Email and password will be shown in the terminal
- **Admin Account**: Email and password will be shown in the terminal

**Copy these down before logging in!**

---

### 🛑 How to Stop the Application

When you're done testing:
1. Go back to the Command Prompt/Terminal window
2. Press `Ctrl + C` (hold Ctrl and press C)
3. The server will stop

To close the virtual environment, type: `deactivate`

---

### 🔄 How to Start It Again Later

When you come back to work on the project:

1. Open Command Prompt/Terminal in the `SmartCities` folder (see Step 2)
2. Activate the virtual environment (see Step 4)
3. Run the server: `python manage.py runserver`
4. Open browser to: `http://127.0.0.1:8000/`

---

### ⚠️ Common Problems & Solutions

#### **Problem 1: "python is not recognized as a command"**
**Solution:**
- Python is not installed, or not added to PATH
- Reinstall Python and **check "Add Python to PATH"** during installation
- Restart your computer after installing

#### **Problem 2: "Cannot activate virtual environment"**
**Solution for Windows:**
- Try using `activate.bat` instead of `Activate.ps1`
- Or open PowerShell as Administrator and run:
  ```bash
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

#### **Problem 3: "Port 8000 is already in use"**
**Solution:**
- Another program is using port 8000
- Use a different port: `python manage.py runserver 8080`
- Then visit: `http://127.0.0.1:8080/`

#### **Problem 4: "No module named django"**
**Solution:**
- Make sure your virtual environment is activated (you should see `(.venv)`)
- Run: `pip install django python-dotenv` again

#### **Problem 5: Can't see the website in browser**
**Solution:**
- Make sure the server is running (look for "Starting development server" message)
- Check you're using the exact address: `http://127.0.0.1:8000/`
- Try a different browser
- Check if your firewall is blocking the connection

#### **Problem 6: Forgot demo account credentials**
**Solution:**
- Run this command again: `python manage.py create_demo_account`
- Or create a new admin account: `python manage.py createsuperuser`

---

### 📞 Need More Help?

If you're stuck:
1. Read the error message carefully - it often tells you what's wrong
2. Copy the error message and search for it online
3. Check that you followed each step exactly as written
4. Make sure you're in the correct folder (`SmartCities` folder)
5. Try restarting your computer and starting from Step 2

---

### ✅ Quick Checklist

Before asking for help, verify:
- [ ] Python 3.10+ is installed
- [ ] You're in the `SmartCities` folder
- [ ] Virtual environment is activated (you see `(.venv)`)
- [ ] You ran all commands in order
- [ ] No error messages appeared (or you tried the solutions above)
- [ ] The server is running (you see "Starting development server")
- [ ] You're using the correct URL: `http://127.0.0.1:8000/`

## 💻 Tech Stack

### Backend
- **Framework**: Django 5.2
- **Language**: Python 3.10
- **Database**: SQLite3 (development)
- **ORM**: Django ORM with custom properties
- **Authentication**: Django built-in auth system
- **Security**: python-dotenv for environment variables

### Frontend
- **Template Engine**: Django Templates (Jinja2 syntax)
- **CSS**: Custom responsive CSS with CSS variables
- **JavaScript**: Vanilla JS
- **Libraries**:
  - Leaflet.js (Interactive maps)
  - Chart.js (Data visualization)
  - Google Fonts (Typography)

### Architecture
- **Pattern**: MVT (Model-View-Template)
- **Design**: Mobile-first, responsive
- **Theme**: Civic/government aesthetic

## 🎨 Design Philosophy

The interface features a **civic/government aesthetic** with:
- Professional, trustworthy appearance
- Clear hierarchy and accountability indicators
- Accessible, readable typography (Bitter serif + Work Sans sans-serif)
- Civic color palette (forest green primary, amber secondary)
- Transparent data visualization
- Mobile-first responsive design

## 📁 Project Structure

```
SmartCities_Insights_Trash/
├── SmartCities/                    # Django project root
│   ├── .env                        # Environment variables (not in git)
│   ├── .env.example                # Environment template
│   ├── db.sqlite3                  # SQLite database
│   ├── manage.py                   # Django management script
│   ├── check_db.py                 # Database verification utility
│   │
│   ├── core/                       # Main application
│   │   ├── models.py               # Complaint & UserProfile models
│   │   ├── views.py                # View controllers (15+ views)
│   │   ├── forms.py                # Django forms
│   │   ├── urls.py                 # URL routing
│   │   ├── admin.py                # Admin configuration
│   │   │
│   │   ├── templates/              # HTML templates
│   │   │   ├── index.html          # Public home page
│   │   │   ├── register.html       # User registration
│   │   │   ├── login.html          # Login page
│   │   │   ├── dashboard.html      # Citizen dashboard
│   │   │   ├── admin-dashboard.html # Admin dashboard
│   │   │   ├── register-complaint.html # Complaint form
│   │   │   ├── complaints.html     # Complaint listing
│   │   │   ├── complaint-detail.html # Single complaint view
│   │   │   ├── profile.html        # User profile
│   │   │   ├── settings.html       # User settings
│   │   │   ├── navbar.html         # Navigation component
│   │   │   └── styles.css          # Main stylesheet
│   │   │
│   │   ├── management/             # Custom commands
│   │   │   └── commands/
│   │   │       └── create_demo_account.py
│   │   │
│   │   └── migrations/             # Database migrations
│   │
│   ├── media/                      # Uploaded files
│   │   └── complaints/
│   │       ├── before/             # Before images
│   │       └── after/              # After images
│   │
│   └── SmartCities/                # Project settings
│       ├── settings.py             # Configuration
│       ├── urls.py                 # Root URL config
│       ├── wsgi.py                 # WSGI config
│       └── asgi.py                 # ASGI config
│
├── .gitignore                      # Git ignore file
├── LICENSE                         # License file
└── README.md                       # This file
```

## 🔧 Core Features

### For Citizens

1. **User Registration & Authentication**
   - Application introduction
   - SDG 11 alignment messaging
   - Login/Register call-to-action
   - NO complaint data or registration button visible

2. **register.html** - User Registration Page
   - Complete signup form with all required fields
   - Locality/ward selection
   - Form validation ready

3. **login.html** - User Login Page
   - Email and password authentication
   - Role auto-detection note
   - Password recovery option

4. **dashboard.html** - Authenticated Home Page (Locality Dashboard)
   - Locality-level statistics (total, resolved, pending)
   - Pie chart visualization (Chart.js)
   - Conditional rendering with Django templates
   - "Register Complaint" button (only when logged in)
   - Recent activity feed

5. **register-complaint.html** - Complaint Registration Form
   - Issue type dropdown (Garbage/Pothole/Streetlight)
   - Interactive map (Leaflet.js) for location selection
   - Image upload with preview
   - Character counter for description
   - Auto-timestamp and status notes

6. **complaints.html** - Complaint Listing Page
   - Locality-wise complaint display
   - Advanced filtering (status, type, SLA)
   - Card-based layout with before/after images
   - SLA status indicators
   - Pagination support

7. **profile.html** - User Profile Page
   - User-specific complaint history
   - Personal statistics
   - Toggle between card and table view
   - Account details display

8. **admin-dashboard.html** - Ward Admin Dashboard
   - Restricted to Admin users only
   - SLA breach alerts
   - Interactive complaint map
   - Bulk complaint management
   - Resolution modal with image upload
   - Priority complaint sections

### Components

9. **navbar.html** - Reusable Navigation Component
   - Conditional rendering for auth state
   - User dropdown menu
   - Admin panel link (for admins only)
   - Mobile responsive hamburger menu

10. **styles.css** - Complete Stylesheet
    - CSS custom properties for theming
    - Responsive grid layouts
    - Component-based styling
    - Print-friendly styles
    - Animations and transitions

## 🔧 Technical Features

### Django Template Integration

All pages use Django-style template tags:

```django
{% if user.is_authenticated %}
  <!-- Authenticated content -->
{% else %}
  <!-- Public content -->
{% endif %}

{% for complaint in complaints %}
  <!-- Loop content -->
{% endfor %}

{% csrf_token %}
```

### Conditional Rendering Examples

**Dashboard Page:**
```django
{% if user.is_authenticated %}
  <div class="dashboard-main">
    <!-- Stats, charts, actions -->
  </div>
{% else %}
  <div class="auth-required">
    <!-- Login prompt -->
  </div>
{% endif %}
```

**Admin Dashboard:**
```django
{% if user.is_authenticated and user.role == 'Admin' %}
  <!-- Admin tools -->
{% else %}
  <div class="access-denied">
    <!-- Access restriction message -->
  </div>
{% endif %}
```

### External Libraries Used

1. **Google Fonts**
   - Bitter (serif, display)
   - Work Sans (sans-serif, body)

2. **Chart.js** (Dashboard)
   - Pie/doughnut chart for status distribution
   - CDN: `https://cdn.jsdelivr.net/npm/chart.js`

3. **Leaflet.js** (Maps)
   - Interactive location selection
   - Complaint mapping
   - CDN: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js`

### Key CSS Custom Properties

```css
:root {
  --primary-color: #1e5a3f;     /* Forest green */
  --secondary-color: #d97706;    /* Amber */
  --success-color: #2a9d4e;      /* Green */
  --warning-color: #f59e0b;      /* Orange */
  --danger-color: #dc2626;       /* Red */
  --font-display: 'Bitter', serif;
  --font-body: 'Work Sans', sans-serif;
}
```

## 🔗 Django Backend Integration

### Required URL Patterns

```python
# urls.py
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register-complaint/', views.register_complaint, name='register_complaint'),
    path('complaints/', views.complaints_list, name='complaints'),
    path('profile/', views.profile, name='profile'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('resolve-complaint/', views.resolve_complaint, name='resolve_complaint'),
]
```

### Required Context Variables

**Dashboard:**
```python
context = {
    'user': request.user,
    'total_complaints': int,
    'resolved_complaints': int,
    'pending_complaints': int,
    'sla_breached': int,
    'avg_resolution_time': str,
    'active_reporters': int,
    'recent_activities': QuerySet,
}
```

**Complaints List:**
```python
context = {
    'complaints': QuerySet,  # Paginated
    # Each complaint object should have:
    # - id, issue_type, description, status
    # - created_at, resolved_at, landmark
    # - before_image, after_image
    # - sla_status, days_pending
    # - user.name
}
```

**Admin Dashboard:**
```python
context = {
    'total_complaints': int,
    'pending_complaints': int,
    'resolved_complaints': int,
    'sla_breached_count': int,
    'resolution_rate': float,
    'sla_breached_complaints': QuerySet,
    'pending_complaints_list': QuerySet,
    'complaints_json': str,  # JSON for map markers
    'ward_center_lat': float,
    'ward_center_lng': float,
}
```

### Form Handling

**Registration:**
```python
# Expected POST data
{
    'name': str,
    'email': str,
    'password': str,
    'age': int,
    'mobile': str (10 digits),
    'locality': str,
}
```

**Complaint Registration:**
```python
# Expected POST data
{
    'issue_type': str,  # 'garbage', 'pothole', 'streetlight'
    'description': str,
    'latitude': float,
    'longitude': float,
    'landmark': str (optional),
    'before_image': File,
}
```

**Complaint Resolution (Admin):**
```python
# Expected POST data
{
    'complaint_id': int,
    'after_image': File,
    'resolution_notes': str (optional),
}
```

## 📱 Responsive Breakpoints

- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px
- **Mobile**: < 768px

All layouts adapt gracefully across devices with:
- Flexible grid systems
- Collapsible navigation
- Touch-friendly controls
- Readable text at all sizes

## 🎯 SLA (Service Level Agreement) Implementation

The design includes SLA status indicators:

**Issue Types & Timelines:**
- Garbage: 24 hours
- Pothole: 72 hours
- Streetlight: 48 hours

**Status Colors:**
- Normal (green): Within SLA
- Breached (red): Exceeded SLA

Backend should calculate `days_pending` and set `sla_status` accordingly.

## 🔐 Access Control Logic

**Public Pages:**
- index.html (always accessible)
- login.html (always accessible)
- register.html (always accessible)

**Authenticated Pages:**
- dashboard.html (requires login)
- register-complaint.html (requires login)
- complaints.html (requires login)
- profile.html (requires login)

**Admin-Only Pages:**
- admin-dashboard.html (requires login + Admin role)

## 🎨 Customization Guide

### Changing Colors

Edit CSS custom properties in `styles.css`:

```css
:root {
  --primary-color: #YOUR_COLOR;
  --secondary-color: #YOUR_COLOR;
}
```

### Changing Fonts

Replace Google Fonts link in HTML `<head>`:

```html
<link href="https://fonts.googleapis.com/css2?family=Your+Font&display=swap" rel="stylesheet">
```

Update CSS:

```css
:root {
  --font-display: 'Your Font', serif;
  --font-body: 'Your Font', sans-serif;
}
```

### Adding New Status Types

Update badge styles in CSS:

```css
.status-badge.your-status {
    background-color: #color;
    color: #text-color;
}
```

## 📊 JavaScript Features

### Chart Initialization (Dashboard)

```javascript
// Automatic Chart.js pie chart
// Reads complaint data from Django context
// Customizable colors and animations
```

### Interactive Map (Complaint Registration)

```javascript
// Leaflet.js map
// Click to select location
// Updates hidden lat/lng inputs
// Marker placement
```

### File Upload Preview

```javascript
// Real-time image preview
// Before uploading to server
// Works for before_image and after_image
```

### Filtering System

```javascript
// Client-side filtering
// Instant results
// Multiple filter combinations
```

## ✅ Verification Checklist

After following the installation steps above, verify everything is working:

### After Initial Setup
- ✅ Python is installed (version 3.10 or higher)
- ✅ Virtual environment folder (`.venv`) exists in `SmartCities` folder
- ✅ Virtual environment is activated (you see `(.venv)` in command line)
- ✅ Django and python-dotenv are installed (no errors when installing)
- ✅ Database file (`db.sqlite3`) created in `SmartCities` folder
- ✅ Demo accounts created (credentials shown in terminal)

### When Server is Running
- ✅ No error messages in the terminal
- ✅ You see "Starting development server at http://127.0.0.1:8000/"
- ✅ Website opens in browser at `http://127.0.0.1:8000/`
- ✅ Home page loads with "SmartCity Insight" branding
- ✅ You can click "Login / Register" button
- ✅ You can login with the demo credentials

### Testing the Application
**For Citizens:**
- ✅ Can register a new account
- ✅ Can login and see dashboard
- ✅ Can view complaint statistics
- ✅ Can click on map to select location
- ✅ Can upload images for complaints
- ✅ Can view list of all complaints

**For Admins:**
- ✅ Can login with admin credentials
- ✅ Can access Admin Dashboard
- ✅ Can see all complaints on map
- ✅ Can view SLA breach alerts
- ✅ Can mark complaints as resolved
- ✅ Can upload after-images

---

## 🚀 What to Do Next

Once your application is running successfully:

### 1. **Explore the Features**
   - Register as a new citizen
   - Submit a test complaint with images
   - Login as admin and resolve the complaint
   - Check the analytics dashboard

### 2. **Customize for Your City**
   - Update city name and branding
   - Add your city's localities/wards
   - Change color scheme (see Customization Guide below)
   - Add your contact information

### 3. **Add Real Data**
   - Create actual citizen accounts
   - Update issue types for your city
   - Configure actual ward boundaries on map
   - Set appropriate SLA timings

---

## 🎨 Simple Customization Guide

### Change the Application Name
1. Open `SmartCities/core/templates/navbar.html`
2. Find: `<span class="brand-name">SmartCity Insight</span>`
3. Change "SmartCity Insight" to your city name

### Change the Colors
1. Open `SmartCities/core/templates/styles.css`
2. Find the `:root {` section at the top
3. Change the color codes:
   ```css
   --primary-color: #1e5a3f;     /* Change this to your color */
   --secondary-color: #d97706;    /* Change this to your color */
   ```
   You can use a color picker tool like: https://htmlcolorcodes.com/

### Add Your Contact Email
1. Open `README.md`
2. Find: `**Email**: [Your contact email]`
3. Replace with your actual email

---

## 🛠️ Useful Commands Reference

Keep these commands handy for managing the application:

### Starting the Application
```bash
# Navigate to project folder
cd SmartCities

# Activate virtual environment (Windows)
.\.venv\Scripts\Activate.ps1

# Activate virtual environment (Mac/Linux)
source .venv/bin/activate

# Start the server
python manage.py runserver
```

### Stopping the Application
```bash
# Press Ctrl+C in the terminal where server is running
# Then deactivate virtual environment
deactivate
```

### Creating New Accounts
```bash
# Create demo accounts (citizen + admin)
python manage.py create_demo_account

# Create a superuser (most powerful admin)
python manage.py createsuperuser
```

### Database Management
```bash
# Check database contents
python check_db.py

# Create new database tables (after model changes)
python manage.py makemigrations
python manage.py migrate
```

### Getting Help
```bash
# See all available commands
python manage.py help

# Get help for a specific command
python manage.py help <command_name>
```

## 🌍 Advanced Configuration (Optional)

### Environment Variables

*Note: For basic usage, you don't need to change these. The application works with default settings.*

If you want to customize advanced settings, create a `.env` file in the `SmartCities/` folder:

**What is this?** Environment variables are like secret settings that tell the application how to behave.

**How to create:**
1. Open Notepad (Windows) or TextEdit (Mac)
2. Copy the text below:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-make-it-long-and-random
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

3. Save the file as `.env` (with the dot at the start) in the `SmartCities` folder
4. Make sure it's saved as `.env` and not `.env.txt`

**⚠️ Important Security Note:** 
- The SECRET_KEY should be a long random string (at least 50 characters)
- Never share your `.env` file with others
- Never upload it to GitHub or public websites

**What each setting means:**
- `SECRET_KEY`: A random password that keeps your application secure
- `DEBUG`: When True, shows detailed error messages (useful for learning)
- `ALLOWED_HOSTS`: Which web addresses can access your application
- `DATABASE_ENGINE`: What type of database to use (SQLite is simplest)
- `DATABASE_NAME`: Name of your database file

## 📊 Analytics & Metrics

The system tracks:
- **Complaint Volume**: Total, resolved, pending counts
- **Resolution Performance**: Average resolution time, resolution rate
- **SLA Compliance**: Breach counts, on-time resolution percentage
- **User Engagement**: Active reporters, localities covered
- **Issue Distribution**: By type (garbage/pothole/streetlight)
- **Geographic Patterns**: Complaint clustering by location

## 🔄 Workflows

### Citizen Workflow
```
Registration → Login → View Dashboard → 
Register Complaint (with map & image) → 
Track Status → Receive Resolution → View After Image
```

### Admin Workflow
```
Login → Admin Dashboard → View SLA Breaches → 
Select Complaint → Upload After Image → 
Mark as Resolved → Monitor Analytics
```

## 🎯 Key Features Implemented

✅ Public home page with SDG 11 alignment  
✅ Complete user registration and authentication  
✅ Role-based access control (Citizen/Admin)  
✅ Interactive map (Leaflet.js) for location selection  
✅ Image upload with preview (before/after)  
✅ Automated SLA tracking (24-72 hours)  
✅ Real-time dashboard with Chart.js visualizations  
✅ Admin complaint management interface  
✅ Pagination (6 complaints per page)  
✅ Responsive design (mobile-first)  
✅ Professional civic aesthetic  
✅ Environment variable security  
✅ Virtual environment isolation  

## 🚧 Future Enhancements

### Phase 1 (Short-term)
- [ ] Email notifications on status change
- [ ] SMS alerts for SLA breaches
- [ ] Password reset functionality
- [ ] Advanced search and filters
- [ ] Export complaints to CSV/PDF
- [ ] Complaint upvoting system

### Phase 2 (Medium-term)
- [ ] Mobile app (Android/iOS)
- [ ] Multi-language support (Hindi, Marathi)
- [ ] AI-powered issue type detection from images
- [ ] Predictive analytics for maintenance
- [ ] Public API for third-party integration
- [ ] Real-time notifications (WebSockets)

### Phase 3 (Long-term)
- [ ] Citizen feedback/rating system
- [ ] Integration with municipal ERP systems
- [ ] Chatbot for complaint registration
- [ ] Blockchain for transparency
- [ ] IoT sensor integration
- [ ] Mobile app for field workers

## 📈 SDG 11 Alignment

This project contributes to **Sustainable Development Goal 11**:

**Target 11.3**: Enhance inclusive and sustainable urbanization  
**Target 11.6**: Reduce environmental impact of cities  
**Target 11.7**: Provide universal access to safe public spaces  

### Impact Metrics
- **Transparency**: Citizens track complaint progress in real-time
- **Accountability**: SLA-based timelines ensure timely resolution
- **Participation**: Digital platform encourages civic engagement
- **Efficiency**: Data-driven resource allocation by administrators
- **Sustainability**: Proactive maintenance prevents major issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use meaningful variable/function names
- Add docstrings to all functions
- Write unit tests for new features
- Update README for significant changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Support & Contact

For questions, issues, or feature requests:
- **Issues**: Create a GitHub issue
- **Documentation**: Refer to inline code comments
- **Email**: [Your contact email]

## 🙏 Acknowledgments

- Django Framework for robust backend
- Leaflet.js for mapping capabilities
- Chart.js for data visualization
- Google Fonts for typography
- Open-source community for inspiration

---

**Built for SDG 11: Sustainable Cities and Communities**  
*Making cities inclusive, safe, resilient and sustainable*

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: Active Development
