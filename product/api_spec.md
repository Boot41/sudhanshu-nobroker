### API Summary

Here’s a simple list of what our API will do, with the corresponding endpoints:

#### 1. For Everyone (Authentication)
*   **Create a New Account** (`POST /auth/register`): Anyone can sign up as a tenant or a property owner.
*   **Log In** (`POST /auth/login`): Existing users can log in to get a secure access token.

#### 2. For Registered Users (User Profiles)
*   **Get My Profile** (`GET /users/me`): See your own account details.
*   **Update My Profile** (`PUT /users/me`): Change your name or phone number.

#### 3. For Finding a Home (Properties)
*   **Search Properties** (`GET /properties`): Anyone can search for properties, filtering by location and price.
*   **View Property Details** (`GET /properties/{property_id}`): Get all the information about a single property.

#### 4. For Property Owners
*   **List a New Property** (`POST /properties`): Owners can add a new property for rent.
*   **Update a Property** (`PUT /properties/{property_id}`): Owners can edit the details of their own properties.
*   **Remove a Property** (`DELETE /properties/{property_id}`): Owners can delete their own property listings.
*   **Manage Applications** (`PUT /applications/{application_id}`): Owners can view, accept, or reject applications for their properties.

#### 5. For Tenants
*   **Shortlist a Property** (`POST /me/shortlist`): Tenants can save properties they are interested in.
*   **View Shortlist** (`GET /me/shortlist`): Tenants can see all the properties they have saved.
*   **Remove from Shortlist** (`DELETE /me/shortlist/{property_id}`): Tenants can remove a property from their saved list.
*   **Apply for a Property** (`POST /applications`): Tenants can submit an application to rent a property.
*   **Check My Applications** (`GET /applications`): Tenants can see the status of their applications.

---

# REST API Specification

This document outlines the REST API endpoints for the NoBroker application, based on the features in `spec.md` and the database schema in `architecture.md`.

## General Concepts

*   **Base URL**: All endpoints are prefixed with `/api/v1`.
*   **Authentication**: Endpoints requiring authentication must include an `Authorization: Bearer <JWT>` header.
*   **Error Responses**: Failed requests will return a standard JSON error object:
    ```json
    { "detail": "A descriptive error message." }
    ```

--- 

### 1. Authentication (`/auth`)

#### `POST /register`
*   **Description**: Registers a new user as either a 'tenant' or 'owner'.
*   **Request Body**:
    ```json
    {
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "password": "strongpassword123",
      "phone_number": "+11234567890",
      "role": "tenant"
    }
    ```
*   **Success Response (201 Created)**: The new user object (without password).
*   **Error Responses**: `400 Bad Request` (Invalid data), `409 Conflict` (Email already exists).

#### `POST /login`
*   **Description**: Authenticates a user and returns a JWT.
*   **Request Body** (`application/x-www-form-urlencoded`):
    `username=john.doe@example.com&password=strongpassword123`
*   **Success Response (200 OK)**:
    ```json
    { "access_token": "...", "token_type": "bearer" }
    ```
*   **Error Responses**: `401 Unauthorized` (Invalid credentials).

--- 

### 2. Users & Profiles (`/users`)

#### `GET /me`
*   **Description**: Retrieves the profile of the currently authenticated user.
*   **Authentication**: Required.
*   **Success Response (200 OK)**: The full user object.

#### `PUT /me`
*   **Description**: Updates the profile of the currently authenticated user.
*   **Authentication**: Required.
*   **Request Body** (all fields optional):
    ```json
    { "full_name": "Johnathan Doe", "phone_number": "+19876543210" }
    ```
*   **Success Response (200 OK)**: The updated user object.

--- 

### 3. Properties (`/properties`)

#### `GET /`
*   **Description**: Searches for available properties with filters.
*   **Query Parameters**:
    *   `address` (string): For location-based text search.
    *   `min_price` (float): Minimum rent price.
    *   `max_price` (float): Maximum rent price.
*   **Success Response (200 OK)**: An array of property summary objects.

#### `POST /`
*   **Description**: Creates a new property listing.
*   **Authentication**: Required (Role: `owner`).
*   **Request Body**:
    ```json
    {
      "title": "Modern 2BHK in City Center",
      "description": "A spacious and well-lit apartment.",
      "address": "123 Central Park, Anytown",
      "rent_price": 2500.00,
      "amenity_ids": [1, 5, 8]
    }
    ```
*   **Success Response (201 Created)**: The full details of the newly created property.

#### `GET /{property_id}`
*   **Description**: Retrieves the full details of a single property.
*   **Success Response (200 OK)**: A detailed property object, including owner info, amenities, and media.
*   **Error Responses**: `404 Not Found`.

#### `PUT /{property_id}`
*   **Description**: Updates an existing property listing.
*   **Authentication**: Required (Role: `owner`, must be the owner of the property).
*   **Request Body**: Same as `POST /`, with all fields optional.
*   **Success Response (200 OK)**: The updated property object.
*   **Error Responses**: `403 Forbidden`, `404 Not Found`.

#### `DELETE /{property_id}`
*   **Description**: Deletes a property listing.
*   **Authentication**: Required (Role: `owner`, must be the owner of the property).
*   **Success Response (204 No Content)**.
*   **Error Responses**: `403 Forbidden`, `404 Not Found`.

--- 

### 4. Shortlisting (`/me/shortlist`)

#### `GET /`
*   **Description**: Retrieves the authenticated user's shortlisted properties.
*   **Authentication**: Required (Role: `tenant`).
*   **Success Response (200 OK)**: An array of property summary objects.

#### `POST /`
*   **Description**: Adds a property to the user's shortlist.
*   **Authentication**: Required (Role: `tenant`).
*   **Request Body**:
    ```json
    { "property_id": 123 }
    ```
*   **Success Response (201 Created)**.
*   **Error Responses**: `404 Not Found` (Property does not exist), `409 Conflict` (Already shortlisted).

#### `DELETE /{property_id}`
*   **Description**: Removes a property from the user's shortlist.
*   **Authentication**: Required (Role: `tenant`).
*   **Success Response (204 No Content)**.

--- 

### 5. Applications (`/applications`)

#### `POST /`
*   **Description**: Submits an application for a property.
*   **Authentication**: Required (Role: `tenant`).
*   **Request Body**:
    ```json
    { "property_id": 123 }
    ```
*   **Success Response (201 Created)**: The new application object.

#### `GET /`
*   **Description**: Retrieves applications. For tenants, it returns their own applications. For owners, it returns applications for their properties.
*   **Authentication**: Required.
*   **Success Response (200 OK)**: An array of application objects.

#### `PUT /{application_id}`
*   **Description**: Updates the status of an application.
*   **Authentication**: Required (Role: `owner`, must own the associated property).
*   **Request Body**:
    ```json
    { "status": "accepted" } // Or 'viewed', 'rejected'
    ```
*   **Success Response (200 OK)**: The updated application object.
*   **Error Responses**: `403 Forbidden`.