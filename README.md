**DATA CLEANING WITH PYTHON:**

![](/images/img.png)

**Goal**: Calculate the messiness of a given CSV file, and make suggestions/perform cleaning on some attributes

**Platforms & Tools:**
Python Django for HTML/JavaScript web application and interface

Pandas for working with the CSV files

Plotly for radar charts and visualizations


This project began as a machine learning prediction model for salary data in the USA. After obtaining data from the U.S. Bureau of Labor Statistics website,
I quickly realized that the data needed a lot of cleaning reformatting to be useful for an exploratory analysis.

My professor and I decided to segue into an application that can clean and detect the cleanliness of datasets, and make suggestions for users. It was targeted
at non-coders who deal with large amounts of data, and need to do large-scale statistical analysis.


In its current state, the code can detect the number of duplicates, the consistency of type within a column, and also the amount of missing/null values within 
the dataset.


**Future Expansions:**

**Time-Series Data Handling:**
Extend the capabilities to handle time-date data more effectively. This could involve automated recognition of time-related variables, and being able to 
reformat those accordingly, in different date-time formats.


**User-Friendly Configuration Options:**
Develop a user-friendly configuration interface to allow users to customize data cleaning and formatting processes based on their specific requirements. 
This could include the ability to define rules, preferences, and thresholds.


**Integration with Cloud Services:**
Explore integration with cloud-based services for scalable processing of large datasets. This would allow users to leverage cloud computing resources for
faster and more efficient data cleaning and analysis. The cleaned datasets could also be uploaded to a cloud system rather than locally.
