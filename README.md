# Bollywood DancePro

**Learn Bollywood dance with AI-powered guidance and a community of dancers!**

A Django-based web application for the Bollywood DancePro platform—connecting beginner and advanced Bollywood dancers with AI-generated tutorials, a song library, community performances, and subscription-based access.

## Features

- **User Profiles**: Beginner and Advanced dancer levels
- **Song Library**: Pre-loaded Bollywood songs with user request support
- **Choreographies**: Advanced dancers upload dance videos; AI converts them to step-by-step tutorials
- **Learning Modules**: AI-generated tutorials with step-by-step breakdowns
- **Community Forum**: Connect with fellow dancers
- **Monthly Performances**: Virtual community showcases
- **Subscription Model**: $9.99/month for full access

## Quick Start

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed sample data (optional)
python manage.py seed_data

# Start the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser.

**Demo login**: `demo` / `demo123`

## Project Structure

```
bollywood_dancepro/     # Django project settings
core/                   # Main application
  models.py             # UserProfile, Song, Choreography, LearningModule, etc.
  views.py              # Page views
  urls.py               # URL routing
templates/              # HTML templates
  base.html             # Base layout
  core/                 # Page-specific templates
```

## Admin

Create a superuser to access the admin panel:

```bash
python manage.py createsuperuser
```

Then visit **http://127.0.0.1:8000/admin**

## Design Document

Based on the Bollywood DancePro design document—a subscription-based platform with AI-powered dance tutorials, interactive feedback, and community engagement.
