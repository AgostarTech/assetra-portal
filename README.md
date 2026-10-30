# Enterprise Asset Portfolio Tracking and Management System (APT)

## 1. Project Purpose & Features
A complete, secure, responsive Django-based application designed to track and manage diverse asset portfolios including Vehicles, Land, Houses, Stocks, and Government Bonds. Features include role-based access control (User, Manager, Admin), accurate financial calculation engines, and a secure document verification workflow.

## 2. Architecture
*   **Backend:** Python 3, Django 4.2 LTS, Django ORM
*   **Database:** MySQL (XAMPP compatible)
*   **Frontend:** Django Templates, Custom CSS, Responsive UI
*   **Authentication:** Session-based with custom role enforcement

## 3. Installation & Setup (Windows / PowerShell)

### Prerequisites
*   Python 3 installed and added to PATH.
*   XAMPP installed with MySQL running.

### Configuration Steps
1.  **Clone / Extract the project.**
2.  **Create and activate the virtual environment:**
    ```powershell
    py -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
3.  **Install dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```
4.  **Database Setup:**
    Open XAMPP, ensure MySQL is running, and create a database named `apt_db`.
5.  **Environment Variables:**
    Ensure the `.env` file exists in the root directory with the database credentials (default XAMPP uses `root` and a blank password).
6.  **Apply Migrations:**
    ```powershell
    py manage.py makemigrations
    py manage.py migrate
    ```
7.  **Create Administrator:**
    ```powershell
    py manage.py createsuperuser
    ```
8.  **Run Development Server:**
    ```powershell
    py manage.py runserver
    ```

## 4. Testing
To run the automated portfolio and model tests:
```powershell
py manage.py test
