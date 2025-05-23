# Baze Internship Database System

A centralized web-based platform for managing and monitoring student industrial training (SIWES) and internship activities at Baze University.

## Features

### Student Portal

- Submit internship placement details
- Mark daily/weekly attendance
- Submit weekly activity logs
- Upload workflow charts and workspace photos
- Download internship summary as PDF

### HOD/Department Supervisor Portal

- View assigned students by department and level
- Monitor student attendance and weekly logs
- Assign internal staff to monitor students
- Provide departmental evaluations
- Export student activity logs

### Organization Supervisor Portal

- View assigned interns
- Review weekly logs
- Provide feedback and comments
- Complete evaluation forms
- Upload completion letters

### System-Wide Features

- Role-based access control
- Email notifications
- Mobile-friendly interface
- PDF export functionality
- Activity history and audit trail

## Tech Stack

- **Backend**: Python 3.8+, Flask
- **Database**: SQLite3
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Authentication**: Flask-Login
- **File Handling**: Pillow (images), ReportLab (PDF)
- **Email**: Flask-Mail

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/baze-internship-system.git
   cd baze-internship-system
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**

   ```bash
   python database/init_db.py
   ```

6. **Run the application**

   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Default Login Credentials

After initialization, you can use these credentials:

**Admin:**

- Email: admin@baze.edu.ng
- Password: admin123

**HOD:**

- Email: hod.cs@baze.edu.ng
- Password: hod123

**Student:**

- Email: john.smith@baze.edu.ng
- Password: student123

**Organization Supervisor:**

- Email: supervisor@techcorp.com
- Password: supervisor123

## Project Structure

```
baze-internship-system/
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── database/              # Database files and schema
├── models/                # Data models
├── routes/                # Application routes
├── templates/             # HTML templates
├── static/                # CSS, JS, and uploads
├── utils/                 # Utility functions
└── tests/                 # Test files
```

## Database Management

### Reset Database

```bash
python database/init_db.py reset
```

### Create Admin User

```bash
flask create-admin
```

### Backup Database

```bash
cp database/baze_internship.db database/backup_$(date +%Y%m%d_%H%M%S).db
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Debug Mode

Set in `.env` file:

```
FLASK_ENV=development
```

## Deployment

### Production Checklist

1. Change `SECRET_KEY` in production
2. Set `FLASK_ENV=production`
3. Configure proper email settings
4. Set up regular database backups
5. Configure HTTPS
6. Set up proper file permissions

### Using Gunicorn (Production Server)

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Troubleshooting

### Database Issues

- Ensure database directory exists
- Check file permissions
- Run `python database/init_db.py` to reinitialize

### Upload Issues

- Check `MAX_CONTENT_LENGTH` in config
- Ensure upload directories exist
- Verify file permissions

### Email Issues

- Verify SMTP settings
- Check firewall rules
- Use app-specific passwords for Gmail

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security Considerations

- All passwords are hashed using Werkzeug's security functions
- Session cookies are HTTP-only and secure
- File uploads are restricted by type and size
- SQL injection protection through parameterized queries
- CSRF protection enabled for all forms

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Email: maryam8580@bazeuniversity.edu.ng
- Documentation: [README]([https://github.com/mamzy247/bids/readme.md](https://raw.githubusercontent.com/mamzy247/BIDS/refs/heads/main/README.md))
- Issues: [GitHub Issues](https://github.com/mamzy247/bids/issues)

## Acknowledgments

- Baze University IT Department
- Maryam (Me)
- All contributing developers and testers
