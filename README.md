# HomeBless - Property Listing Platform

HomeBless is a property listing platform that helps users explore, filter, compare, and search for residential properties in Thailand.

## Tech Stack

### Frontend
- HTML5, Tailwind CSS, JavaScript – Modern and responsive design
- Django Templating Language – Dynamic content rendering

### Backend
- Django – Robust and scalable framework
- PostgreSQL – Reliable database for property listings

## Installation & Setup

Clone the repository:
```bash
git clone https://github.com/HomeBless/HomeBless.git
cd HomeBless
```

Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements
```

Run migrations and start the server:
```bash
python manage.py migrate
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.
