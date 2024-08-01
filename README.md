# PyCoffee

PyCoffee is a Flask-based application designed to manage a coffee shop's operations, including order processing, inventory management, and user authentication.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

## Introduction

PyCoffee is a web application that helps manage a coffee shop. It provides features such as order creation, inventory tracking, and user authentication (including roles for admin and client).

## Installation

### Requirements

- Python 3.7+
- Flask

### Installation Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/CaueGrassi7/PyCoffee.git
    ```
2. Navigate to the project directory:
    ```sh
    cd PyCoffee
    ```
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
5. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
6. Initialize the database:
    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```
7. Run the application:
    ```sh
    flask run
    ```

## Usage

The application will run at `http://127.0.0.1:5000/`.

### Endpoints

#### Products

- **POST /api/products**: Add a new product (Admin only).
    - Request body: `{ "name": "Product Name", "description": "Product Description", "price": 9.99 }`
    - Response: `201 Created` with the created product.

- **GET /api/products**: Get a list of all products.
    - Response: `200 OK` with a list of products.

- **GET /api/products/<id>**: Get a product by ID.
    - Response: `200 OK` with the product data, or `404 Not Found`.

- **PUT /api/products/<id>**: Update a product by ID (Admin only).
    - Request body: `{ "name": "New Name", "description": "New Description", "price": 19.99 }`
    - Response: `200 OK` with the updated product, or `404 Not Found`.

- **DELETE /api/products/<id>**: Delete a product by ID (Admin only).
    - Response: `200 OK` with a message of successful deletion, or `404 Not Found`.

#### Orders

- **POST /api/orders**: Create a new order.
    - Request body: `{ "products": [{"product_id": 1, "quantity": 2}] }`
    - Response: `201 Created` with the created order.

- **PUT /api/orders/<id>**: Update the status of an order.
    - Request body: `{ "status": "paid" }`
    - Response: `200 OK` with the updated order, or `404 Not Found`.

#### User Authentication

- **POST /api/register**: Register a new user.
    - Request body: `{ "username": "user", "email": "user@example.com", "password": "password" }`
    - Response: `201 Created` with a success message.

- **POST /api/login**: Log in a user.
    - Request body: `{ "email": "user@example.com", "password": "password" }`
    - Response: `200 OK` with a success message.

- **POST /api/logout**: Log out the current user.
    - Response: `200 OK` with a success message.

## Contributing

Contributions are welcome! Follow the steps below to contribute:

1. Fork the project.
2. Create a branch for your feature or bugfix (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
