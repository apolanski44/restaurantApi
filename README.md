# Restaurant Management Application

## Introduction

The Restaurant Management Application is a web-based platform designed to streamline the management of restaurant operations. It provides functionality for both administrators and guests.

### Key Features:

- **Guest Interface:**
  - Adding reservations by specifying table ID and last name.
  - Adding reservations by specifying the number of guests and last name.
  - Checking available tables for a specific date and time.
  - Browsing the menu.
  - Canceling reservations.

- **Administrator Interface:**
  - Adding new tables to the system.
  - Deleting tables from the system.
  - Updating table information (e.g., number of seats).
  - Adding new dishes to the menu.
  - Removing dishes from the menu.
  - Editing existing dishes in the menu.
  - Viewing all reservations for a selected date.
  - Deleting reservations.

# Database Structure

The application uses an SQL database to manage its data. Below is a description of the database structure, including all tables, their columns, and relationships.

---
## Login and password for admin user in database: admin admin 

## Tables

### 1. `Tables`
This table stores information about the restaurant's tables.

| Column Name  | Data Type    | Constraints              | Description                     |
|--------------|--------------|--------------------------|---------------------------------|
| `ID`         | `INT`        | Primary Key, Auto-Increment | Unique identifier for each table. |
| `Seats`      | `INT`        | Not Null                | Number of seats available at the table. |

---

### 2. `Reservations`
This table stores reservation details.

| Column Name          | Data Type        | Constraints               | Description                               |
|----------------------|------------------|---------------------------|-------------------------------------------|
| `ID`                 | `INT`           | Primary Key, Auto-Increment | Unique identifier for each reservation.    |
| `TableID`            | `INT`           | Foreign Key (References `Tables(ID)`) | Table associated with the reservation.    |
| `ReservationTime`    | `DATETIME`      | Not Null                  | Date and time of the reservation.         |
| `Guests`             | `INT`           | Not Null                  | Number of guests for the reservation.     |
| `ClientLastName`     | `VARCHAR(255)`  | Not Null                  | Last name of the client making the reservation. |

---

### 3. `Menu`
This table stores information about the restaurant's menu items.

| Column Name  | Data Type        | Constraints              | Description                             |
|--------------|------------------|--------------------------|-----------------------------------------|
| `ID`         | `INT`           | Primary Key, Auto-Increment | Unique identifier for each menu item.    |
| `Name`       | `VARCHAR(255)`  | Not Null                | Name of the menu item.                  |
| `Category`   | `VARCHAR(100)`  | Not Null                | Category of the menu item (e.g., Soup, Drink, Main Course). |
| `Price`      | `DECIMAL(10, 2)` | Not Null                | Price of the menu item in PLN.          |

---

### 4. `Users`
This table stores information about the application's users (admins).

| Column Name  | Data Type        | Constraints              | Description                             |
|--------------|------------------|--------------------------|-----------------------------------------|
| `ID`         | `INT`           | Primary Key, Auto-Increment | Unique identifier for each user.        |
| `Username`   | `VARCHAR(255)`  | Not Null, Unique         | Username for the user.                  |
| `Password`   | `VARCHAR(255)`  | Not Null                | Hashed password for authentication.     |

---

## Relationships

- The `Reservations` table has a **foreign key relationship** with the `Tables` table through the `TableID` column.
  - This enforces referential integrity, ensuring that each reservation is associated with an existing table.
- The `Users` table operates independently and is used for admin authentication.
- There are no direct relationships between the `Menu` table and the other tables as it functions independently to manage menu items.

---

## Database Use Cases

1. **Manage Tables:**
   - Add, update, delete, and retrieve restaurant tables from the `Tables` table.
2. **Manage Reservations:**
   - Add, cancel, or retrieve reservations using the `Reservations` table.
3. **Manage Menu:**
   - Add, update, delete, and retrieve menu items from the `Menu` table.
4. **Manage Users:**
   - Authenticate admin users via the `Users` table.

---
# Restaurant Management API Documentation

This API provides endpoints for managing restaurant functionalities such as authentication, reservations, menu management, and table management. The following sections describe the routes and their purposes.

---

## Authentication (`auth.py`)

This module handles user authentication, including login, JWT token generation, and route protection.

### Routes

#### 1. `/adminlogin`
- **Method:** `GET`
- **Description:** Serves the admin login HTML page.

#### 2. `/api/adminlogin`
- **Method:** `POST`
- **Description:** Authenticates admin users by verifying credentials and returns a JWT token.
- **Request Body:**
  ```json
  {
    "username": "admin",
    "password": "password123"
  }
  ```
- **Response:**
  - **200 OK:**
    ```json
    {
      "message": "Login successful.",
      "token": "<JWT_TOKEN>"
    }
    ```
  - **400 Bad Request:**
    ```json
    {
      "error": "Username and password are required."
    }
    ```
  - **401 Unauthorized:**
    ```json
    {
      "error": "Invalid username or password."
    }
    ```

#### 3. `/api/adminindex`
- **Method:** `GET`
- **Description:** Returns a welcome message for the admin.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  - **200 OK:**
    ```json
    {
      "message": "Welcome to the admin index."
    }
    ```
  - **401 Unauthorized:**
    ```json
    {
      "error": "Unauthorized. Token is missing."
    }
    ```

#### 4. `/adminindex`
- **Method:** `GET`
- **Description:** Serves the admin index HTML page.

#### 5. `/userindex`
- **Method:** `GET`
- **Description:** Serves the user index HTML page.

#### 6. `/api/logout`
- **Method:** `POST`
- **Description:** Logs out the user by invalidating the session on the client side.
- **Response:**
  - **200 OK:**
    ```json
    {
      "message": "Logout successful."
    }
    ```

### Helper Functions

#### `require_api_key`
- **Purpose:** Middleware to protect routes using JWT authentication.
- **Behavior:**
  - Validates the `Authorization` header for a valid JWT token.
  - Returns a 401 Unauthorized response for missing or invalid tokens.
- **Usage:** Apply this decorator to any route requiring authentication.


## Menu Management (`menuRoutes.py`)

This module provides endpoints for managing the restaurant menu, including adding, editing, deleting, and retrieving menu items.

### Routes

#### 1. `/api/menu`
- **Method:** `GET`
- **Description:** Retrieves all menu items or filters by category.
- **Query Parameters:**
  - `category` (optional): The category to filter menu items by.
- **Response:**
  - **200 OK:**
    ```json
    {
      "menu_items": [
        {
          "id": 1,
          "name": "Tomato Soup",
          "category": "Soup",
          "price": 12.99
        }
      ]
    }
    ```
  - **500 Internal Server Error:**
    ```json
    {
      "error": "<Error message>"
    }
    ```

#### 2. `/api/menu`
- **Method:** `POST`
- **Description:** Adds a new menu item.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "name": "Grilled Chicken",
    "category": "Main Course",
    "price": 24.99
  }
  ```
- **Response:**
  - **201 Created:**
    ```json
    {
      "message": "Menu item added successfully."
    }
    ```
  - **400 Bad Request:**
    ```json
    {
      "error": "Name and category are required."
    }
    ```

#### 3. `/api/menu/<int:item_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific menu item by its ID.
- **Response:**
  - **200 OK:**
    ```json
    {
      "menu_item": {
        "id": 1,
        "name": "Tomato Soup",
        "category": "Soup",
        "price": 12.99
      }
    }
    ```
  - **404 Not Found:**
    ```json
    {
      "error": "Menu item not found."
    }
    ```

#### 4. `/api/menu/<int:item_id>`
- **Method:** `PUT`
- **Description:** Updates a specific menu item by its ID.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "name": "Chicken Salad",
    "category": "Main Course",
    "price": 19.99
  }
  ```
- **Response:**
  - **200 OK:**
    ```json
    {
      "message": "Menu item updated successfully."
    }
    ```
  - **400 Bad Request:**
    ```json
    {
      "error": "Name and category are required."
    }
    ```

#### 5. `/api/menu/<int:item_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific menu item by its ID.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  - **200 OK:**
    ```json
    {
      "message": "Menu item deleted successfully."
    }
    ```
  - **404 Not Found:**
    ```json
    {
      "error": "Menu item not found."
    }
    ```

#### 6. `/menuindex`
- **Method:** `GET`
- **Description:** Serves the menu index HTML page.

#### 7. `/manageMenu`
- **Method:** `GET`
- **Description:** Serves the manage menu HTML page for admin users.

#### 8. `/editMenuItem/<int:item_id>`
- **Method:** `GET`
- **Description:** Serves the edit menu item HTML page for a specific item.
- **Response:**
  - **200 OK:** Renders the edit page with item details.
  - **404 Not Found:** Renders a 404 page if the item does not exist.


---

## Reservation Management (`reservationsRoutes.py`)

This module provides endpoints for managing reservations, including checking availability, creating, editing, and deleting reservations.

### Routes

#### 1. `/api/reservations/check_availability`
- **Method:** `POST`
- **Description:** Checks table availability for a specific date and time.
- **Request Body:**
  ```json
  {
    "reservation_date": "2025-01-01",
    "reservation_time": "18:00"
  }
  ```
- **Response:**
  - **200 OK:**
    ```json
    {
      "available_tables": [
        { "id": 1, "seats": 4 }
      ]
    }
    ```
  - **400 Bad Request:**
    ```json
    {
      "error": "Please select both date and time."
    }
    ```

#### 2. `/api/reservations/auto_reserve`
- **Method:** `POST`
- **Description:** Automatically reserves a table based on the number of guests and availability.
- **Request Body:**
  ```json
  {
    "reservation_date": "2025-01-01",
    "reservation_time": "18:00",
    "guests": 2,
    "lastname": "Smith"
  }
  ```
- **Response:**
  - **201 Created:**
    ```json
    {
      "message": "Table reserved successfully.",
      "reservation_details": {
        "table_id": 1,
        "reservation_datetime": "2025-01-01 18:00:00",
        "guests": 2,
        "lastname": "Smith"
      }
    }
    ```
  - **400 Bad Request:**
    ```json
    {
      "error": "Reservation date and time are required."
    }
    ```

#### 3. `/api/reservations/manual_reserve`
- **Method:** `POST`
- **Description:** Manually reserves a specific table.
- **Request Body:**
  ```json
  {
    "reservation_date": "2025-01-01",
    "reservation_time": "18:00",
    "table_id": 1,
    "lastname": "Smith"
  }
  ```
- **Response:**
  - **201 Created:**
    ```json
    {
      "message": "Reservation confirmed.",
      "reservation_details": {
        "table_id": 1,
        "reservation_datetime": "2025-01-01 18:00:00",
        "lastname": "Smith"
      }
    }
    ```
  - **404 Not Found:**
    ```json
    {
      "error": "Table 1 is not available at the selected time."
    }
    ```

#### 4. `/api/reservations/cancel_reservation`
- **Method:** `POST`
- **Description:** Cancels an existing reservation.
- **Request Body:**
  ```json
  {
    "table_id": 1,
    "reservation_date": "2025-01-01",
    "reservation_time": "18:00",
    "lastname": "Smith"
  }
  ```
- **Response:**
  - **200 OK:**
    ```json
    {
      "message": "Reservation cancelled successfully."
    }
    ```
  - **404 Not Found:**
    ```json
    {
      "error": "Reservation does not exist."
    }
    ```

#### 5. `/api/reservations/manage`
- **Method:** `GET`
- **Description:** Retrieves all reservations for a specific date.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Query Parameters:**
  - `reservation_date` (required): The date to filter reservations.
- **Response:**
  - **200 OK:**
    ```json
    {
      "reservations": [
        { "id": 1, "table_id": 1, "reservation_time": "18:00", "guests": 2, "lastname": "Smith" }
      ]
    }
    ```
  - **404 Not Found:**
    ```json
    {
      "message": "No reservations found for the selected date."
    }
    ```

#### 6. `/manageReservation`
- **Method:** `GET`
- **Description:** Serves the manage reservations HTML page for admin users.

#### 7. `/userReservation`
- **Method:** `GET`
- **Description:** Serves the user reservations HTML page for customers.

#### 8. `/cancelreservation`
- **Method:** `GET`
- **Description:** Serves the cancel reservation HTML page for customers.



## Table Management (`tables.py`)

This module provides endpoints for managing restaurant tables, including adding, editing, deleting, and retrieving table information.

### Routes

#### 1. `/api/tables`
- **Method:** `POST`
- **Description:** Adds a new table to the system.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "seats": 4
  }
  ```
- **Response:**
  - **201 Created:**
    ```json
    {
      "message": "Table added successfully."
    }
    ```
  - **400 Bad Request:**
    ```json
    {
      "error": "Seats must be a positive integer."
    }
    ```

#### 2. `/api/tables`
- **Method:** `GET`
- **Description:** Retrieves all tables.
- **Response:**
  - **200 OK:**
    ```json
    {
      "tables": [
        { "id": 1, "seats": 4 },
        { "id": 2, "seats": 6 }
      ]
    }
    ```
  - **200 OK (No Tables):**
    ```json
    {
      "message": "No tables found."
    }
    ```

#### 3. `/api/tables/<int:table_id>`
- **Method:** `GET`
- **Description:** Retrieves information about a specific table.
- **Response:**
  - **200 OK:**
    ```json
    {
      "table": { "id": 1, "seats": 4 },
      "reservations": [
        { "id": 1, "reservation_time": "18:00", "lastname": "Smith" }
      ]
    }
    ```
  - **404 Not Found:**
    ```json
    {
      "error": "Table not found."
    }
    ```

#### 4. `/api/tables/<int:table_id>`
- **Method:** `PUT`
- **Description:** Updates the number of seats for a specific table.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "seats": 6
  }
  ```
- **Response:**
  - **200 OK:**
    ```json
    {
      "message": "Table updated successfully."
    }
    ```
  - **400 Bad Request:**
    ```json
    {
      "error": "Seats must be a positive integer."
    }
    ```
  - **404 Not Found:**
    ```json
    {
      "error": "Table not found."
    }
    ```

#### 5. `/api/tables/<int:table_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific table.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  - **200 OK:**
    ```json
    {
      "message": "Table deleted successfully."
    }
    ```
  - **404 Not Found:**
    ```json
    {
      "error": "Table not found."
    }
    ```

#### 6. `/api/tables/occupied`
- **Method:** `POST`
- **Description:** Retrieves all occupied tables for a specific date and time.
- **Request Body:**
  ```json
  {
    "reservation_date": "2025-01-01",
    "reservation_time": "18:00"
  }
  ```
- **Response:**
  - **200 OK:**
    ```json
    {
      "occupied_tables": [
        { "id": 1, "seats": 4 }
      ]
    }
    ```
  - **200 OK (No Occupied Tables):**
    ```json
    {
      "message": "No occupied tables for the selected date and time."
    }
    ```

#### 7. `/manageTables`
- **Method:** `GET`
- **Description:** Serves the manage tables HTML page for admin users.

# Security Features

## 1. **JWT-Based Authentication**
- Admin and secured API routes use JSON Web Tokens (JWT) for authentication.
- Tokens are issued after a successful login and must be included in the `Authorization` header for protected routes.
- Tokens include expiration time to enhance security (`exp` claim).

---

## 2. **Session-Based Authentication for Admin Panel**
- The admin panel uses session-based authentication for secure access to admin routes.
- Session cookies are signed with a secret key (`SECRET_KEY`) to prevent tampering.

---

## 3. **Role-Based Access Control**
- Role differentiation:
  - **Admin:** Access to all resources via JWT and session.
  - **Guest Users:** Limited access, such as viewing menu or reservations.
- Admin-exclusive routes include token verification (`@require_api_key`) and ensure only authorized users perform operations.

---

## 4. **Data Validation**
- Input validation on all endpoints ensures that invalid or malicious data is not processed.
  - Example: Validating positive integers for `seats` or `guests` and regex checks for valid last names.
- Returns clear error messages for invalid inputs.

---

## 5. **Error Handling**
- Custom error responses:
  - **400 Bad Request** for invalid user input.
  - **404 Not Found** for missing resources.
  - **500 Internal Server Error** for unexpected issues.
- Prevents exposure of sensitive stack traces.

---

## 6. **Parameterized Database Queries**
- All database interactions use parameterized queries to prevent SQL injection.

---

## 7. **Access Control on API Routes**
- Protected routes require a valid JWT (`Authorization: Bearer <token>`).
- Ensures unauthorized users cannot access or manipulate resources.

---

## 8. **CSRF Protection**
- Session-based admin routes are secured with server-side validation against Cross-Site Request Forgery (CSRF).

---

## 9. **Appropriate HTTP Status Codes**
- Uses industry-standard HTTP response codes for consistent API behavior:
  - `200 OK` for successful requests.
  - `201 Created` for resource creation.
  - `400 Bad Request` for invalid user input.
  - `401 Unauthorized` for missing/invalid tokens.
  - `404 Not Found` for non-existing resources.
  - `500 Internal Server Error` for server issues.

---

## 10. **Environment-Specific Secret Management**
- The `SECRET_KEY` for JWT and sessions should be stored securely in environment variables for production.

---



