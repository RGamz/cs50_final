# AMS SWAP
#### Video Demo:  <https://youtu.be/UCArW3LnNCY?si=Sn_-JPBsdjni-f1F>

# Optimizing Workflow for Repair Requests: A Flask Application
## Introduction
For my final project in CS50, I developed an application tailored to streamline and organize the workflow of administrators handling repair requests from both stores and end customers at my current workplace. The backend of the application is built using Python and the Flask framework, along with Jinja templating. The frontend employs HTML, CSS, and JavaScript based on Bootstrap 5 as well as some open source JavaScript code for specific functions.
## Version Control and Dependencies
Git is used as the version control system, accompanied by a well-defined .gitignore file to exclude unnecessary packages from commits. Additionally, I have set up virtual environment and there is corresponding requirements.txt file specifies the stack used in the project. 
## Problem Statement
The core challenge addressed by this application is the heterogeneous nature of repair requests processed by administrators. Each request, depending on the client it pertains to, may require a different handling approach. The goal is to optimize the processing time by structuring existing processes and presenting a list of requests based on a unified logic for each process.
## Database
Two technologies are employed for the database: SQLite3 and the Pandas library. The local version of the application utilizes this stack, whereas the working version connects directly to the database to address corporate security considerations. In the db folder you will find 2 SQL files that contain requests that I did to our corporate MySQL database. Data from these requests was then manually imported as 2 csv files. Then, in local_db.py I will create SQLite3 database and corresponding tickets and logs tables. These tables will be alimented by Pandas module from csv. It means that I will read csv file and then by using pd.read_csv and pd.to_sql transfer data to SQL database. Once again in production code I will directly connect to corporate MySQL database.
## Flask Application Structure
The Flask application consists of several routes used for sorting and displaying various types of repair requests. Built-in route handling methods like before_request and teardown_request manage database connections before and after requests.
## Data Handling and Templating
The database is initially populated based on a CSV file, utilizing the Pandas library. Specific queries are then employed based on each application's requirements, varying in complexity. Data retrieved from the cursor after each query is passed to an HTML template using Jinja and Flask's render_template function.
New variables are created as needed to calculate required data on the backend or in Jinja.
## Error Handling
Each route incorporates error handling using the try-except principle. In case of an error, the built-in logging module displays relevant messages on the HTML page, pinpointing the issue. I use a page404.html for this as well as corresponding css file called error.css
## Template Structure
The templates follow a hierarchical structure with a master template and child templates inheriting from it. The master template includes the site header and essential links, while route-specific elements are displayed in corresponding child templates. Each route-specific template will have the following structure :
    - {% extends "layout.html" %} that is used to get main layout
    - title and main blocks
    - nav-tabs ul that will display tabs if needed
    - tables that correspond to each tab
    - each table will have:
        * th headers with jinja counters of tickets
        * td lines with the dynamic content with jinja templates


## Application Functions
Several functions are extracted to the application header, aiming to simplify and condense the code. Notable functions include calculating the difference in days between the current date and the request date (calculate_days_since), and appending cursor content to a list (tickets_to_list).

## Styling
Bootstrap templates are largely retained, with adaptations made for improved readability, reduced spacing between lines, and the addition of specific functions for content search and sorting. These functions are based on open source JavaScript functions because learning JS is a horrible experience. Bootstrap and css styles are connectected to the layout.html and thus they are available on all templates.

## Conclusion 
In conclusion, the developed Flask application efficiently organizes and streamlines the repair request processing workflow for administrators, addressing the diverse nature of requests and enhancing overall productivity.

