# Convert Me

A web application that converts Google Spreadsheet `.xlsx` files into a CSV format compatible with proprietary software. I built this to automate the migration of spreadsheet information. Uses Flask to create a web server, and the script was written in Python.

## Project Structure

```
google-to-nw-converter/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── converters/
│   │   ├── __init__.py
│   │   └── google_to_csv.py
│   ├── static/
│   │   └── index.css
│   └── templates/
│       └── index.html
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository:**

   ```sh
   git clone https://github.com/isaacjstriker/convapp
   cd google-to-nw-converter
   ```

2. **Create a virtual environment:**

   ```sh
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

4. **Install the required dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

5. **Set up environment variables (if needed):**
   Create a `.env` file in the root directory and add any necessary environment variables.

## Usage

1. **Run the application:**

   ```sh
   python3 app/main.py
   ```

2. **Access the web application:**
   Open your web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000).

3. **Upload a Google Spreadsheet (.xlsx) file:**
   Use the web interface to upload your file and convert it to NW Scheduler CSV format.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.
