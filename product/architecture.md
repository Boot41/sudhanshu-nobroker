# Architecture

For the tech stack we will be using :

1. Postgres for the backend database
2. Fast API for backend APIs 
3. SQLAlchemy for ORM mapping
4. Alembic for managing Data Migrations
5. React for front-end

# Database Structure

Below is the proposed database schema based on the product requirements. The structure is normalized to reduce data redundancy and improve data integrity.

### Normalization Notes
- **Amenities**: The `property_amenities` table is a join table that links properties to a master list of amenities. This is a many-to-many relationship and avoids storing a comma-separated list in the `properties` table.
- **Media**: The `property_media` table allows each property to have multiple images or videos without cluttering the main `properties` table.
- **Shortlists**: The `shortlisted_properties` table manages the many-to-many relationship between users and their favorited properties.

### Schema Diagram

```
+-------------------------+           +-------------------------+           +-------------------------+
|          users          |           |   shortlisted_properties|           |      applications       |
|-------------------------|           |-------------------------|           |-------------------------|
| id (PK)                 |---------->| user_id (FK)            |           | id (PK)                 |
| full_name               |           | property_id (FK)        |---------->| property_id (FK)        |
| email                   |           +-------------------------+           | tenant_id (FK)          |
| password_hash           |                                                 | status                  |
| phone_number            |                                                 | created_at              |
| role ('tenant'/'owner') |                                                 +-------------------------+
| created_at              |
+-------------------------+
             |
             |
             v
+-------------------------+           +-------------------------+           +-------------------------+
|       properties        |           |     property_media      |           |  property_amenities     |
|-------------------------|           |-------------------------|           |-------------------------|
| id (PK)                 |---------->| property_id (FK)        |---------->| property_id (FK)        |
| owner_id (FK -> users)  |           | media_url               |           | amenity_id (FK)         |
| title                   |           | media_type ('image'/'vr') |           +-------------------------+
| description             |           +-------------------------+                        ^
| address                 |                                                                |
| rent_price              |                                                                |
| status                  |                                                      +-------------------------+
| created_at              |                                                      |        amenities        |
+-------------------------+                                                      |-------------------------|
                                                                               | id (PK)                 |
                                                                               | name                    |
                                                                               +-------------------------+

```

### Detailed Table Schema

Below is a detailed description of each table, its columns, and their corresponding data types.

#### `users`
Stores information about both tenants and property owners.

| Column Name     | Data Type                  | Notes                                  |
|:----------------|:---------------------------|:---------------------------------------|
| `id`            | `SERIAL PRIMARY KEY`       | Unique identifier for each user        |
| `full_name`     | `VARCHAR(255)`             | User's full name                       |
| `email`         | `VARCHAR(255) UNIQUE`      | User's email, must be unique           |
| `password_hash` | `VARCHAR(255)`             | Hashed password for security           |
| `phone_number`  | `VARCHAR(20)`              | User's contact number                  |
| `role`          | `ENUM('tenant', 'owner')`  | Defines the user's role on the platform|
| `created_at`    | `TIMESTAMP WITH TIME ZONE` | Timestamp of user account creation     |

#### `properties`
Contains all the details about the properties listed on the platform.

| Column Name  | Data Type                     | Notes                                     |
|:-------------|:------------------------------|:------------------------------------------|
| `id`         | `SERIAL PRIMARY KEY`          | Unique identifier for each property       |
| `owner_id`   | `INTEGER`                     | Foreign key referencing `users.id`        |
| `title`      | `VARCHAR(255)`                | Title of the property listing             |
| `description`| `TEXT`                        | Detailed description of the property      |
| `address`    | `TEXT`                        | Full address of the property              |
| `rent_price` | `DECIMAL(10, 2)`              | Monthly rent amount                       |
| `status`     | `ENUM('available', 'rented')` | Current status of the property            |
| `created_at` | `TIMESTAMP WITH TIME ZONE`    | Timestamp of when the property was listed |

#### `amenities`
A master list of all possible amenities.

| Column Name | Data Type            | Notes                             |
|:------------|:---------------------|:----------------------------------|
| `id`        | `SERIAL PRIMARY KEY` | Unique identifier for each amenity|
| `name`      | `VARCHAR(100)`       | Name of the amenity (e.g., 'Wi-Fi')|

#### `property_amenities`
Links properties to their available amenities in a many-to-many relationship.

| Column Name   | Data Type | Notes                                  |
|:--------------|:----------|:---------------------------------------|
| `property_id` | `INTEGER` | Foreign key referencing `properties.id`|
| `amenity_id`  | `INTEGER` | Foreign key referencing `amenities.id` |

#### `property_media`
Stores URLs for property photos and virtual tours.

| Column Name   | Data Type                   | Notes                                     |
|:--------------|:----------------------------|:------------------------------------------|
| `id`          | `SERIAL PRIMARY KEY`        | Unique identifier for the media file      |
| `property_id` | `INTEGER`                   | Foreign key referencing `properties.id`   |
| `media_url`   | `TEXT`                      | URL of the image or video                 |
| `media_type`  | `ENUM('image', 'vr')`       | Type of media (e.g., standard image, VR tour) |

#### `shortlisted_properties`
Tracks which properties a user has shortlisted.

| Column Name   | Data Type | Notes                                  |
|:--------------|:----------|:---------------------------------------|
| `user_id`     | `INTEGER` | Foreign key referencing `users.id`     |
| `property_id` | `INTEGER` | Foreign key referencing `properties.id`|

#### `applications`
Manages tenant applications for properties.

| Column Name   | Data Type                                     | Notes                                     |
|:--------------|:----------------------------------------------|:------------------------------------------|
| `id`          | `SERIAL PRIMARY KEY`                          | Unique identifier for each application    |
| `property_id` | `INTEGER`                                     | Foreign key referencing `properties.id`   |
| `tenant_id`   | `INTEGER`                                     | Foreign key referencing `users.id`        |
| `status`      | `ENUM('sent', 'viewed', 'accepted', 'rejected')`| Current status of the application         |
| `created_at`  | `TIMESTAMP WITH TIME ZONE`                    | Timestamp of when the application was sent|
