# E-commerce API - Phase 1

A simple Django REST Framework API for managing products in an e-commerce system.

## Features
- **Product Management**: Create and retrieve products having name, price, and description
- **REST API**: Clean endpoints for product operations
- **Slug field**: SEO-friendly urls using slugs

## API Endpoints
- `GET /api/products/` - List all products
- `POST /api/products/` - Create a new product
- `GET /api/products/<slug:slug>` - Retrieve a product using it's slug name
- `PUT /api/products/<slug:slug>` - Update a product, lookup based on slug field
- `DELETE /api/products/<slug:slug>` - Delete a product, lookup based on slug field

## Tech Stack
- Django 5.x
- Django REST Framework 3.16.x
- SQLite database

## Quick Start
- Clone the repository. 
- Create a virtual environment.
- Run following commands: 
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```