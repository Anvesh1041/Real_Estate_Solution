# Real Estate Solution

## Overview
Real Estate Solution is a web-based application built using Flask to manage properties for buying, selling, and renting. The application has both user and admin functionalities. Regular users can view properties, apply for them, and make purchases or rent inquiries. Admins have a dashboard to handle property listings and receive notifications about user activities.

## Features
- **User Side:**
  - Browse properties available for buy and rent.
  - Apply or buy properties.
  - View property details with images and other relevant information.

- **Admin Side:**
  - Admin dashboard to manage properties.
  - Search properties by ID.
  - Receive notifications for user actions related to buying, renting, or selling properties.
  - Ability to update or delete properties.

- **Database:**
  - MySQL is used for the backend database.
  - Property and user information is stored in dedicated tables.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Anvesh1041/Real_Estate_Solution.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Real_Estate_Solution
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the MySQL database:
   - Create a MySQL database.
   - Import the SQL schema files from the `/database` folder to create the necessary tables.
     ```bash
     mysql -u username -p database_name < database/Property.sql
     mysql -u username -p database_name < database/User.sql
     ```

5. Configure your database connection in the `config.py` file:
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/database_name'
   ```

6. Run the application:
   ```bash
   python app.py
   ```

## `import.py` - Automated Data Import
The `import.py` script is designed to automate the process of importing data from an Excel (CSV) file into the MySQL database. It also uses the **Pexels API** to fetch images for the properties during the import process.

### How It Works:
1. **Reads data from CSV:**  
   The script reads property data from a CSV file (e.g., `mumbai.csv`), which contains property details such as name, location, price, etc.

2. **Connects to MySQL Database:**  
   It establishes a connection with the MySQL database to insert the property data.

3. **Fetches Images from Pexels API:**  
   Using the Pexels API, the script automatically fetches images based on the property name or location and saves the image URLs to the database.

4. **Inserts Data into Database:**  
   The property details, along with the fetched images, are inserted into the MySQL database.

### How to Use `import.py`:
1. **Set up your Pexels API key:**
   - Open `import.py` and add your Pexels API key.
     ```python
     API_KEY = 'your_pexels_api_key'
     ```

2. **Run the script:**
   ```bash
   python import.py
   ```
   - The script will automatically read the CSV file, fetch images using the Pexels API, and insert the data into the MySQL database.

### CSV File Format:
The CSV file should have the following columns (as an example):
| Property Name | Location | Price | Description | ... |
|---------------|----------|-------|-------------|-----|

Each row represents a property, and the script will import all rows into the MySQL database.

---

## Dependencies
- **Flask** - Web framework
- **SQLAlchemy** - ORM for interacting with MySQL
- **PyMySQL** - MySQL connector for Python
- **Pexels API** - For fetching property images
- **pandas** - For reading and processing CSV files

## Future Enhancements
- Add filtering options for users to search properties by price, location, or type.
- Improve the image-fetching mechanism to provide more accurate and relevant images.

## Contributing
Feel free to fork this repository and submit pull requests for any improvements or new features.

## License
This project is licensed under the MIT License.