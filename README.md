# Dash Data Analysis Application

## Overview
This Python script implements a Dash web application for data analysis and visualization. The application allows users to dynamically filter and visualize data through interactive graphs. The primary features include the selection of region, year, and tenure to analyze key product frequency and patient type distribution.

## Application Features
1. **Select Region:** Choose between "All India" and "My Region" to focus the analysis on specific geographical areas.
2. **Select Year:** Filter data by year, including an option for analyzing data across all available years.
3. **Select Tenure:** Choose from different tenure options such as "Overall," "First Quarter," "Second Quarter," "Third Quarter," and "Fourth Quarter" to refine the analysis.

## Data Source
The application uses data from the provided Excel file (`datasheets.xlsx`) with sheets named "India_SA_Implants_Data" and "My Region."

## Prerequisites
Ensure you have the required Python packages installed. You can install them using the following:
```bash
pip install -r requirements.txt
```

## How to Run the Application
1. Clone the repository or download the script (`dash_app.py`) to your local machine.
2. Install the necessary Python packages using the command mentioned in the "Prerequisites" section.
3. Run the script using the following command:
   ```bash
   python dash_app.py
   ```
4. Open a web browser and go to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to access the Dash application.

## Live Demo
You can access a live demo of the application hosted on [https://freelance-dash-app.onrender.com](https://freelance-dash-app.onrender.com).

## Code Structure
The script is organized as follows:
- **Import Statements:** Import necessary libraries and modules.
- **Data Loading:** Load data from the Excel file (`datasheets.xlsx`).
- **Dash App Layout:** Define the layout of the Dash application using Bootstrap components.
- **Callback Function:** Implement a callback function to update the graphs based on user input.
- **Graph Update Function:** Define a function (`update_graph`) to update the graphs based on selected filters.
- **Run the App:** Start the Dash app and run it.

## Note
- The script uses Dash for creating the web application, Plotly for graph plotting, and Pandas for data manipulation.
- Ensure the Excel file (`datasheets.xlsx`) is in the same directory as the script.

Feel free to customize the script to suit your specific data analysis requirements or integrate it into your project.
