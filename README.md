# TRANSPORT-SPEDITION-LOGISTIC PROJECT

## Description

Transport-Spedition-Logistic Project provides a comprehensive solution for the Transport and Logistics (TSL) industry. Users can efficiently create, plan, and manage transportation orders for their company's trucks fleet.

## Requirements

All necessary requirements are listed in the `requirements.txt` file.

## Installation

1. Download project files.
2. Open your terminal and navigate to the project folder.
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
5. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```
5. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
6. Start the local server and begin using the project.
7. I will develop project on external server in future.

## How the Project Works

The project consists of four applications:

- **user_app**: Handles user registration, login, and logout. Users select their role (Logistician, Dispatcher, Driver) during registration, determining permissions for various project areas.
- **logistician_app**: Allows Logisticians to create, edit, and delete transportation orders, manage load/delivery places, and specify volumes for tanker trailer chambers. Both actual and archived orders can be monitored here.
- **dispatcher_app**: Enables Dispatchers to manage transportation orders and assign them to drivers.
- **driver_app**: Provides drivers with information about assigned orders. When a driver completes an order, an automatic email is sent to dispatchers for assignment of a new order.

## Models

### Custom User

#### Fields

- `username`: A unique username for each user.
- `first_name`: The user's first name.
- `last_name`: The user's last name.
- `email`: The user's email address (unique).
- `phone_number`: The user's contact phone number (unique).
- `role`: The role of the user within the system, chosen from predefined options.

### Transportation Order

#### Fields

- `date`: The date when the transportation order was created (defaulting to the current date).
- `trailer_type`: The type of trailer required for the transportation order, selected from predefined choices.
- `tanker_volume`: If applicable, the volume details for tanker trailers, linked to the `TankerTrailer` model.
- `load_weight`: The weight of the load being transported, ensuring it falls within a valid range.
- `load_place`: The place of loading, connected to the `LoadOrDeliveryPlace` model, representing the starting point.
- `delivery_place`: The destination of the delivery, associated with the `LoadOrDeliveryPlace` model.
- `driver`: The assigned driver for the transportation order, linked to the `CustomUser` model with the "Driver" role.
- `done`: Indicates whether the transportation order has been completed (defaulting to `False`).

### Load/Delivery Place

#### Fields

- `company`: The name of the company associated with the load or delivery place.
- `country`: The country where the place is located.
- `state`: The state or region within the country.
- `town`: The town or city name.
- `postal_code`: The postal code for the area.
- `street`: The street name.
- `street_number`: The street number.
- `contact_number`: A contact number for the place.

## Note

The frontend interface is currently under development and will be added in the future.

Enjoy using the Transport-Spedition-Logistic Project!
