# E-commerce API - Phase 2

A simple Django REST Framework API for managing products in an e-commerce system.

## Features
- **Product Management**: Create and retrieve products having name, price, and description
- **Categegory Management**: Create and retrieve category having name and description
- **REST API**: Clean endpoints for product and category operations
- **Database Relationship**: Each product now have category field by referring to Category Model as Foreign key
- **Slug field**: SEO-friendly urls using slugs for both products and categories
- **Admin Panel**:  Enabled Django admin panel to manage data via web interface.

## API Endpoints
### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create a new product
- `GET /api/products/<slug:slug>` - Retrieve a product using it's slug name
- `PUT /api/products/<slug:slug>` - Update a product, lookup based on slug field
- `DELETE /api/products/<slug:slug>` - Delete a product, lookup based on slug field
### Categories
- `GET /api/products/categories/` - List all categories
- `POST /api/products/categories/` - Create a new category
- `GET /api/products/categories/<slug:slug>` - Retrieve a category using it's slug name
- `PUT /api/products/categories/<slug:slug>` - Update a category, lookup based on slug field
- `DELETE /api/products/categories/<slug:slug>` - Delete a category, lookup based on slug field

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