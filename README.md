# Google to NW Scheduler Converter

This project is a web application that converts Google Spreadsheet `.xlsx` files into a CSV format compatible with NW Scheduler. The application is built using Flask and provides a user-friendly interface for file uploads and conversions.

## Project Structure

```
google-to-nw-converter
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── converters
│   │   ├── __init__.py
│   │   └── google_to_csv.py
│   ├── static
│   └── templates
│       └── index.html
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd google-to-nw-converter
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   Create a `.env` file in the root directory and add any necessary environment variables.

## Usage

1. **Run the application:**
   ```
   python app/main.py
   ```

2. **Access the web application:**
   Open your web browser and go to `http://127.0.0.1:5000`.

3. **Upload a Google Spreadsheet (.xlsx) file:**
   Use the provided interface to upload your file and initiate the conversion to CSV.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.