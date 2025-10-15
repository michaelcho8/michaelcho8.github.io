# michaelcho8.github.io

Welcome to my personal website and tutoring platform hosted on GitHub Pages!

## About
This site serves as my online portfolio showcasing my robotics & software projects, and provides a platform for my tutoring services. I'm a Systems Project Engineer with expertise in mathematics, programming, and engineering fundamentals.

## 🚀 Features

### Portfolio Section
- **Robotics & Software Projects**: Showcasing hands-on technical work
- **Project Highlights**: OCR Pipeline, Smartsheet Automations, Property Data Crawler
- **Professional Background**: Systems engineering and technical problem-solving

### Tutoring Services
- **Subject Areas**: Mathematics (Pre-Calc to Calc III), Programming (Python, C++), Engineering Fundamentals
- **Flexible Packages**: Individual sessions ($50/hr), Weekly ($180/month), Intensive ($380/month)
- **Interactive Scheduling**: Multiple booking options with smart form generation
- **Payment Tracking System**: Built-in SQLite database for managing student payments and sessions

## 🗂️ File Structure

```
├── index.html                    # Main website with integrated tutoring section
├── tutoring.html                 # Standalone tutoring page (Calendly integration)
├── tutoring_simple.html          # Self-contained tutoring page (no external dependencies)
├── app.py                       # Flask web interface for payment management
├── payment_manager.py           # Python CLI for managing tutoring business
├── tutoring_payments.sql        # Database schema for payment tracking
├── requirements.txt             # Python dependencies
├── templates/                   # Web interface templates for admin panel
│   ├── base.html
│   ├── dashboard.html
│   ├── students.html
│   ├── add_student.html
│   ├── sessions.html
│   ├── add_session.html
│   ├── payments.html
│   ├── add_payment.html
│   └── reports.html
├── TUTORING_SETUP.md           # Comprehensive setup guide
├── SCHEDULING_ALTERNATIVES.md   # Alternative scheduling solutions
└── README.md                   # This file
```

## 🧪 Testing Your Website

### Method 1: Direct Browser Testing (Simplest)
1. **Navigate to your project folder** in file explorer
2. **Double-click `index.html`** to open in your default browser
3. **Test navigation**: Click "Tutoring" in the menu to jump to the tutoring section
4. **Test scheduling**: Try both "Send Scheduling Email" and "Fill Out Form" buttons
5. **Check mobile view**: Resize browser window to test responsive design

### Method 2: Local Web Server (Recommended)
```bash
# Navigate to your website directory
cd /path/to/michaelcho8.github.io

# Start a local server (Python 3)
python3 -m http.server 8000

# Or using Python 2
python -m SimpleHTTPServer 8000

# Or using Node.js (if installed)
npx http-server -p 8000
```

Then visit: `http://localhost:8000`

### Method 3: Live Server (VS Code Extension)
1. Install "Live Server" extension in VS Code
2. Right-click `index.html` → "Open with Live Server"
3. Auto-refreshes when you make changes

### Method 4: GitHub Pages (Production)
Your site is automatically deployed at: [https://michaelcho8.github.io](https://michaelcho8.github.io)
Changes to the `main` branch are automatically deployed.

## 🎯 Testing Checklist

### Main Website Features
- [ ] **Navigation**: All menu links work (Work, Tutoring, About, Contact)
- [ ] **Responsive Design**: Looks good on desktop, tablet, and mobile
- [ ] **Project Links**: GitHub links open correctly
- [ ] **Email Links**: Contact email opens mail client

### Tutoring Section Features
- [ ] **Pricing Display**: All three packages show correctly
- [ ] **Subject Areas**: Mathematics, Programming, Engineering sections display
- [ ] **Email Template**: "Send Scheduling Email" opens pre-filled email
- [ ] **Detailed Form**: "Fill Out Form" shows/hides form correctly
- [ ] **Form Validation**: Required fields prevent submission when empty
- [ ] **Form Submission**: Generates properly formatted email
- [ ] **Date Picker**: Minimum date is set to today
- [ ] **Mobile Friendly**: Form works on mobile devices

### Payment Management System (Optional)
```bash
# Test the Python payment system
python payment_manager.py

# Or start the web interface
python app.py
# Then visit http://localhost:5000
```

## 🔄 How to Update & Deploy

### Local Development
1. **Clone the repository**:
   ```bash
   git clone https://github.com/michaelcho8/michaelcho8.github.io.git
   cd michaelcho8.github.io
   ```

2. **Make your changes** to `index.html` or other files

3. **Test locally** using one of the methods above

4. **Commit and deploy**:
   ```bash
   git add .
   git commit -m "Update website content"
   git push origin main
   ```

### Customization Options

#### Update Tutoring Prices
Edit the pricing in `index.html`:
```html
<div class="price">$XX/hr</div>     <!-- Individual -->
<div class="price">$XXX/month</div> <!-- Weekly -->
<div class="price">$XXX/month</div> <!-- Intensive -->
```

#### Add/Remove Subjects
Update the subject dropdown in the tutoring form:
```html
<option value="New Subject">New Subject</option>
```

#### Customize Available Times
Edit the time options in the scheduling form:
```html
<option value="8:00 AM">8:00 AM</option>
```

#### Change Contact Information
Update email addresses throughout the file:
- Navigation contact link
- Form action mailto addresses
- Footer information

## 📚 Additional Resources

- **`TUTORING_SETUP.md`**: Complete guide for setting up the tutoring business management system
- **`SCHEDULING_ALTERNATIVES.md`**: Different scheduling options (Calendly, WhatsApp, etc.)
- **Payment Management**: Full SQLite database system for tracking students and payments
- **Admin Interface**: Web-based dashboard for managing tutoring business

## 🛠️ Technical Stack

- **Frontend**: HTML5, CSS3 (Pico CSS Framework), Vanilla JavaScript
- **Backend**: Python Flask (for payment management)
- **Database**: SQLite (for payment tracking)
- **Hosting**: GitHub Pages (automatic deployment)
- **Styling**: Responsive design with mobile-first approach

## 📝 Recent Changes

### Version 2.0 (October 2025)
- ✅ **Integrated Tutoring Services**: Added comprehensive tutoring section to main website
- ✅ **Payment Management System**: Built complete SQLite-based system for tracking students and payments
- ✅ **Multiple Scheduling Options**: Email templates, detailed forms, and external service integration
- ✅ **Web Admin Interface**: Flask-based dashboard for managing tutoring business
- ✅ **Mobile Optimization**: Fully responsive design for all devices
- ✅ **Professional Pricing Display**: Clean pricing cards with package details

## 🤝 Contact & Support

- **Email**: michael.sm.cho@email.com
- **LinkedIn**: [michael-sm-cho](https://www.linkedin.com/in/michael-sm-cho/)
- **GitHub**: [michaelcho8](https://github.com/michaelcho8)

## 📄 License
This website is open source and available under the MIT License.

---
**Ready to tutor!** 🎓 The website now showcases both technical projects and tutoring services in one professional platform.
