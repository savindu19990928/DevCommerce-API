# DevCommerce API

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-6.1-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.18-red.svg)](https://www.django-rest-framework.org/)
[![Database](https://img.shields.io/badge/database-MySQL-informational.svg)](https://www.mysql.com/)
[![Deployment](https://img.shields.io/badge/deployment-Cloud%20Run-blueviolet.svg)](https://cloud.google.com/run)

A production-ready, feature-rich E-Commerce RESTful API built with **Django 6.1** and **Django REST Framework (DRF)**. DevCommerce features a hybrid Role-Based and Attribute-Based Access Control system, full product catalog management, serial-number-level inventory tracking, registered and guest checkout flows with automated PDF receipt generation, customer care ticketing, and Google Cloud Storage / Cloud Run deployment readiness.

---

## Table of Contents

- [Features](#features)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Project Structure](#project-structure)
- [User Roles & Permissions](#user-roles--permissions)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
  - [Environment Configuration](#environment-configuration)
  - [GCP Service Account Configuration](#gcp-service-account-configuration)
  - [Database Migrations & Dummy Data](#database-migrations--dummy-data)
  - [Running the Application](#running-the-application)
- [Docker & Containerization](#docker--containerization)
- [Google Cloud Deployment (Cloud Run & Cloud Build)](#google-cloud-deployment-cloud-run--cloud-build)
- [API Overview & Documentation](#api-overview--documentation)
- [Security & Public Repository Guidelines](#security--public-repository-guidelines)
- [License](#license)

---

## Features

- **Authentication & User Management:**
  - JWT authentication (`access` & `refresh` tokens via `djangorestframework-simplejwt`).
  - Contact verification via 6-digit OTPs (Email and SMS simulation).
  - Multi-address book management (Billing & Shipping).
- **Hybrid RBAC + ABAC Permission Engine:**
  - Granular model-level and object-level permissions with peer-to-peer permission delegation.
- **Catalog & Storefront:**
  - Brands, hierarchical categories, and product listings with filtering & pagination.
  - Pre-order management, cost/price margins, and product reviews.
  - Dynamic homepage curation (popular, trending, sale, recommendations).
- **Order Management & Fulfillment:**
  - Registered and guest checkout workflows.
  - Automated PDF receipt generation (`ReportLab`).
  - Secure public tracking via unguessable guest tokens.
  - Packing workflow with physical serial number binding.
  - Cart, Wishlist, and Coupon validation engine.
- **Support & Customer Care:**
  - Warranty registration with serial number verification.
  - Customer care support tickets with threaded communications.
  - Refund requests and customer phone callback requests.
- **Inventory & Stock Management:**
  - Serial-number-level lifecycle tracking (`IN_STOCK`, `RESERVED`, `PACKED`, `SOLD`).
  - Stock movements audit trail (additions, damages, removals, adjustments).
- **Reports & Analytics:**
  - Administrative dashboard reporting on revenue, orders, catalog size, and low-stock alerts.

For a comprehensive feature breakdown, see [FEATURES.md](FEATURES.md).

---

## Architecture & Tech Stack

- **Backend Framework:** Django 6.1 & Django REST Framework 3.18
- **Authentication:** SimpleJWT (JSON Web Tokens)
- **Database:** MySQL (via `mysqlclient`)
- **Cloud Storage:** Google Cloud Storage (`django-storages[google]`, `google-cloud-storage`)
- **PDF Generation:** ReportLab
- **Admin Interface:** Django Jazzmin
- **WSGI / Production Server:** Gunicorn
- **Containerization & CI/CD:** Docker, Google Cloud Build, Google Cloud Run

---

## Project Structure

```text
DevCommerce-API/
├── catalog/          # Products, Categories, Brands, Reviews
├── core/             # Granular permissions engine, PDF generators, audit logs
├── devcommerce/      # Project root: settings, URLs, WSGI/ASGI, storage backends
├── inventory/        # Serial numbers, stock movements, stock levels
├── marketing/        # Dynamic recommendations and tagging
├── orders/           # Cart, Orders, Checkout, Receipts, Coupons, Warranties
├── support/          # Customer care cases, communications, call requests
├── users/            # Custom User model, JWT auth, OTP verification, addresses
├── Dockerfile        # Container build definition
├── cloudbuild.yaml   # Google Cloud Build deployment pipeline
├── manage.py         # Django management CLI
├── requirements.txt  # Python package dependencies
├── .env.example      # Environment variables template
└── gcp_service_account_key.json.example # GCP service account key template
```

---

## User Roles & Permissions

DevCommerce implements a multi-tier permission architecture:

| Role | Code | Description |
| :--- | :--- | :--- |
| **Superuser** | `is_superuser=True` | Unrestricted authority; role management and permission elevation. |
| **Administrator** | `ADMIN` | Global access across catalog, inventory, orders, support, and reports. Can assign granular permissions. |
| **Customer** | `CUSTOMER` | Scoped to own data: browsing, cart, orders, reviews, warranties, and support tickets. |
| **Assistant** | `ASSISTANT` | Customer service staff; requires granular permissions to inspect orders, handle tickets, and process refunds. |
| **Stock Manager** | `STOCK` | Manages products, categories, brands, stock movements, and serial numbers based on assigned permissions. |
| **Order Packer** | `PACKING` | Warehouse fulfillment; views active orders and marks items packed with serial numbers. |

For full permission delegation mechanics, see [USER_ROLES.md](USER_ROLES.md).

---

## Getting Started

### Prerequisites

- **Python:** 3.13 or newer
- **MySQL:** 8.0 or newer
- **Git**
- *(Optional)* **Google Cloud Platform account** with a Cloud Storage bucket for media/static hosting.

---

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/DevCommerce-API.git
   cd DevCommerce-API
   ```

2. **Create and activate a virtual environment:**
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv devenv
     .\devenv\Scripts\Activate.ps1
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

### Environment Configuration

Copy the example environment template to `.env`:

```bash
cp .env.example .env
```

Open `.env` and fill in your settings:

```env
# Django Configuration
SECRET_KEY=your-secure-django-secret-key
DEBUG=True
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
SITE_URL=http://localhost:8000

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=devcomdb
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306

# Google Cloud Storage Configuration
USE_GCP=False
GS_BUCKET_NAME=your_gcs_bucket_name
GS_CREDENTIALS_FILE=gcp_service_account_key.json
```

> [!TIP]
> If you are testing locally without Google Cloud Storage, set `USE_GCP=False`. Django will serve static and media files locally.

---

### GCP Service Account Configuration

If you enable Google Cloud Storage (`USE_GCP=True`):

1. Obtain a service account key JSON from your GCP Project IAM console with **Storage Admin** or **Storage Object Admin** permissions.
2. Place the file in the project root as `gcp_service_account_key.json` (or reference its path via `GS_CREDENTIALS_FILE` in `.env`).
3. A reference template is provided in `gcp_service_account_key.json.example`.

> [!IMPORTANT]
> Both `.env` and `gcp_service_account_key.json` are strictly excluded in `.gitignore` and `.dockerignore`. Never commit private keys to version control.

---

### Database Migrations & Dummy Data

1. **Create the MySQL database:**
   ```sql
   CREATE DATABASE devcomdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

4. *(Optional)* **Seed sample data:**
   You can populate demo products, categories, brands, and test accounts:
   ```bash
   mysql -u your_user -p devcomdb < dummy_data.sql
   ```

---

### Running the Application

Start the local Django development server:

```bash
python manage.py runserver
```

- **API Base:** [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
- **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Health Check:** [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/)

---

## Docker & Containerization

A production-ready [Dockerfile](Dockerfile) is included.

1. **Build the Docker image:**
   ```bash
   docker build -t devcommerce-api .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8080:8080 --env-file .env devcommerce-api
   ```

The application runs using Gunicorn on port `8080`.

---

## Google Cloud Deployment (Cloud Run & Cloud Build)

A sample deployment pipeline is provided in [cloudbuild.yaml](cloudbuild.yaml).

Before triggering a build, substitute the placeholders with your actual GCP details:
- `[GCP region]` (e.g., `us-central1`, `asia-southeast1`)
- `[GCP project ID]` (e.g., `my-cloud-project`)
- `[Artifact Registry repository]` (e.g., `cloud-run-source-deploy`)
- `[service name]` (e.g., `devcommerce-api`)

Trigger a build via Cloud SDK:
```bash
gcloud builds submit --config=cloudbuild.yaml
```

When running in **Cloud Run**, set `DEBUG=False` and configure database connection parameters and cloud storage environment variables in Cloud Run Secret Manager. Cloud Run automatically leverages the attached service account without requiring a JSON key file.

---

## API Overview & Documentation

| Endpoint Prefix | Description |
| :--- | :--- |
| `/api/users/` | Registration, JWT token obtain/refresh, OTP contact verification, profile, address book, permission delegation |
| `/api/catalog/` | Categories, Brands, Products, homepage curation, product reviews |
| `/api/inventory/` | Serial numbers, stock level tracking, physical stock movements |
| `/api/orders/` | Orders, Cart, Wishlist, Coupons, guest checkout, receipt PDF downloads |
| `/api/support/` | Customer care cases, message thread communications, warranty claims, refunds, call requests |
| `/api/marketing/` | Recommendation tags |
| `/api/reports/` | Executive and admin reporting metrics |
| `/health/` | Liveness health check |

### Detailed Documentation Guides

- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) – Complete reference of all endpoints.
- [ADMIN_API_DOCUMENTATION.md](ADMIN_API_DOCUMENTATION.md) – Endpoints and flows for Admin users.
- [CUSTOMER_API_DOCUMENTATION.md](CUSTOMER_API_DOCUMENTATION.md) – Customer storefront and self-service endpoints.
- [STOCK_API_DOCUMENTATION.md](STOCK_API_DOCUMENTATION.md) – Inventory and stock tracking endpoints.
- [PACKING_API_DOCUMENTATION.md](PACKING_API_DOCUMENTATION.md) – Warehouse order packing and fulfillment endpoints.
- [ASSISTANT_API_DOCUMENTATION.md](ASSISTANT_API_DOCUMENTATION.md) – Customer support assistant workflows.
- [SUPERUSER_API_DOCUMENTATION.md](SUPERUSER_API_DOCUMENTATION.md) – Superuser role promotion and user administration.
- [COMMON_API_DOCUMENTATION.md](COMMON_API_DOCUMENTATION.md) – Shared schemas and general endpoints.

---

## Security & Public Repository Guidelines

This repository is configured for safe open-source and public deployment:

1. **Ignored Files:** All real credential files (`.env`, `.env.*`, `gcp_service_account_key.json`, and all `*service_account*.json` files) are listed in `.gitignore` and `.dockerignore`.
2. **Template Files:** Only `.env.example` and `gcp_service_account_key.json.example` are committed.
3. **Container Safety:** `.dockerignore` blocks sensitive files and virtual environments from leaking into Docker images during build time.

---

## License

This project is licensed under the [MIT License](LICENSE) (or your chosen organization license).
