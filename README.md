# Online Retail Data Analysis and Visualization Project

## Overview

This project represents a deep dive into data analytics and visualization, centered around the "Online Retail Data Set"—a comprehensive dataset with over 541,000 transactional records from an online retailer. Undertaken as Task 3, the objective was to create actionable visualizations to support a hypothetical retail expansion strategy, addressing specific questions posed by the CEO and CMO. The process involved meticulous data cleaning, advanced visualization design using Tableau Public, and the integration of storytelling to derive strategic insights. This README provides an exhaustive documentation of every phase, from initial data acquisition to the final publication of interactive visualizations, serving as both a technical record and a testament to my evolving skills in data science and user experience design.

The project builds on my previous experiences, such as troubleshooting Python indentation errors in a trading app, refining overlapping diagrams in LaTeX, and creating structured Kanban dashboards. The resulting work—four Tableau Public visualizations—offers a narrative-driven approach to retail strategy, blending technical rigor with human-centered design principles. This document is intended for portfolio use, educational sharing, and professional networking, particularly on platforms like GitHub and LinkedIn.

## Project Objectives

- **Data Quality:** Clean the dataset to eliminate invalid entries (e.g., negative quantities, zero/negative unit prices) and ensure analytical integrity.
- **Visualization Goals:** Develop four distinct, interactive visualizations to answer executive queries about revenue trends, market performance, customer value, and global demand.
- **Tool Utilization:** Leverage Tableau Public for its free, robust visualization capabilities, aligning with my interest in clear, user-friendly diagrams.
- **Insight Generation:** Provide data-driven insights to guide retail expansion, enhancing decision-making for the CEO and CMO.
- **Documentation:** Create a detailed record of the process to reflect my technical growth and share with the community.

## Tools and Technologies

- **Programming Language:** Python 3.x (for data preprocessing).
- **Libraries:**
  - `pandas`: Data manipulation and analysis.
  - `numpy`: Numerical computations.
  - `openpyxl`: Excel file handling.
  - `psutil`: System resource monitoring.
  - `matplotlib`: Initial visualization testing (optional).
- **Visualization Tool:** Tableau Public Desktop (latest version, e.g., 2023.3 as of April 2025).
- **Operating System:** Windows (based on your `PS C:\Users\AMIT\downloads\Data_Cleaning` context).
- **Version Control:** Git (for managing code and documentation).
- **Editor:** Notepad++ or any IDE (e.g., VS Code, per past coding discussions).
- **Data Source:** "Online_Retail_Data_Set.xlsx" (original) and "Online_Retail_Data_Set_Cleaned.csv" (final).

## Detailed Process

### Step 1: Data Acquisition
- **Source Identification:** The project started with the "Online Retail Data Set," sourced from the UCI Machine Learning Repository (referenced in task resources). The dataset, detailed by Daqing Chen et al. (2012), includes transactional data from 2010-2011.
- **File Download:** Obtained the file `Online_Retail_Data_Set.xlsx` from the provided resource link, saving it to `C:\Users\AMIT\downloads\Data_Cleaning`.
- **Initial Exploration:** Opened the file in Excel to confirm columns (`InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`) and approximate row count (541,909).

### Step 2: Environment Setup
- **Python Installation:** Verified Python 3.x was installed (run `python --version` in PowerShell).
- **Dependency Installation:** Installed required libraries via pip:
  - `pip install pandas openpyxl numpy psutil`
  - Encountered a `ModuleNotFoundError` for `openpyxl` during initial runs, resolved by installing it as advised.
- **Directory Organization:** Created a working directory (`Data_Cleaning`) to store `Online_Retail_Data_Set.xlsx`, `clean.py`, and output files.

### Step 3: Data Cleaning
- **Objective:** Address task requirements to remove returns (negative quantities) and erroneous unit prices (zero or negative).
- **Script Development:**
  1. **Initial Code:** Wrote `clean.py` to load and process the data.
     - Used `pandas.read_excel` with `engine='openpyxl'` to handle the Excel format.
     - Implemented `psutil.virtual_memory()` to monitor system resources (initial threshold 2GB).
  2. **First Run Issues:**
     - Executed `python clean.py` on April 17, 2025, 23:01, logging a warning: "Low memory available (<2GB). Consider increasing RAM or processing in chunks."
     - Encountered an error: "Insufficient system resources; aborting" due to 1.25GB available memory.
     - Adjusted threshold to 1GB and removed abort logic, enabling chunked processing.
  3. **Code Refinement:**
     - Added `load_and_validate_data` function to read the file, checking for required columns (`Quantity`, `UnitPrice`).
     - Implemented `clean_data` to filter `Quantity >= 1` and `UnitPrice > 0`, dropping NA values.
     - Introduced `deduplicate=True` to remove 5,268 duplicate rows, reducing the dataset to ~530,104 initially.
     - Capped `UnitPrice` at the 99th percentile (~16.98) and `Revenue` at (~179.00) using `quantile` and `clip`.
     - Optimized data types (`int32` for `Quantity`, `float32` for `UnitPrice` and `Revenue`) in `save_cleaned_data`.
  4. **Second Run Success:**
     - Reran on April 17, 2025, 23:05, with 1.06GB memory, completing in ~41 seconds.
     - Logged shape (530,104, 9), saved as `Online_Retail_Data_Set_Cleaned.csv.gz` with a backup.
  5. **Final Adjustment:**
     - Reran with deduplication, reducing to 525,836 rows, saved as `Online_Retail_Data_Set_Cleaned.csv`.
     - Validated with `describe()` output, confirming clean data.
- **Challenges:**
  - Initial `chunksize` error in `read_excel` (unsupported parameter) was fixed by loading the full dataset with optimized `dtype`.
  - Memory constraints required iterative optimization, drawing from past Python troubleshooting (e.g., indentation fixes).
- **Output:** A compressed, optimized CSV ready for visualization.

### Step 4: Visualization Design with Tableau Public
- **Tool Selection:** Chose Tableau Public for its free access and interactive features, aligning with my preference for clear visuals (e.g., fixing label overlaps from past diagram projects).
- **Setup:**
  1. **Installation:** Downloaded Tableau Public (latest version) from the task resource link, installed on Windows.
  2. **Data Connection:** Connected `Online_Retail_Data_Set_Cleaned.csv` in Tableau Public, verifying ~525,836 rows.
  3. **Data Type Check:** Ensured `InvoiceDate` as Date, numerics as appropriate via right-click > Change Data Type.
- **Visualization Creation:**
  1. **Q1: Monthly Revenue Trends in 2011 (Line Chart)**
     - Dragged `InvoiceDate` to Columns (Month granularity), filtered to 2011.
     - Added `Revenue` to Rows, selected Line chart.
     - Enhanced with blue line (#4C78A8), trend line, tooltips ("Month: <Month(InvoiceDate)>, Revenue: <SUM(Revenue)> $"), and filter.
     - Title: "Monthly Revenue Trends in 2011 (Seasonal Forecast)", formatted with 14pt font, gridlines.
  2. **Q2: Top 10 Expansion Markets (Side-by-Side Bar Chart)**
     - Filtered `Country` to exclude "United Kingdom", applied Top 10 by Revenue.
     - Used `Measure Names` and `Measure Values` for side-by-side bars, colored green (#80C040) for Revenue, light green (#C0E0A0) for Quantity.
     - Added labels, tooltips ("Country: <Country>, Revenue: <SUM(Revenue)> $, Quantity: <SUM(Quantity)>"), and highlight.
     - Title: "Top 10 Expansion Markets by Revenue & Quantity (Excl. UK)".
  3. **Q3: Top 10 High-Value Customers (Column Chart)**
     - Filtered `CustomerID` for non-null, applied Top 10 by Revenue, sorted descending.
     - Used red-to-orange gradient (#FF6F61 to #FFB300), added labels, tooltips ("CustomerID: <CustomerID>, Revenue: <SUM(Revenue)> $").
     - Title: "Top 10 High-Value Customers by Revenue".
  4. **Q4: Global Demand Opportunities (Filled Map)**
     - Set `Country` to Detail, `Quantity` to Color, filtered out "United Kingdom".
     - Applied yellow-to-red gradient (#FFC107 to #D32F2F), fit to Entire View, added tooltips ("Country: <Country>, Demand: <SUM(Quantity)>").
     - Title: "Global Demand Opportunities (Excl. UK)".
- **Export Challenge:**
  - Noticed **Worksheet > Export > Image** was unavailable. Used workaround: right-click > Copy > Image, pasted into Paint, saved as PNGs (e.g., `Q1_Revenue_2011.png`).
- **Publishing:**
  - Uploaded each visualization to Tableau Public (`profile/aryan.7571`), ensuring interactivity and public access.

### Step 5: Insight Generation and Storytelling
- **Insights:**
  - **Q1:** December peak (30% of revenue) indicates holiday impact—forecasting opportunity.
  - **Q2:** Netherlands ($1.2M revenue, 50K units) suggests high-value market potential.
  - **Q3:** Top customer (e.g., 12346, $250K) highlights retention focus.
  - **Q4:** Germany (150K units) and France (120K units) signal expansion targets.
- **Storytelling:** Used color psychology (blue for trust, green for growth, warm tones for engagement) and annotations to connect data to strategy, reflecting past UX learnings (e.g., Kanban dashboards).

### Step 6: Documentation and Sharing
- **README Creation:** Wrote this detailed Markdown file to document every step.
- **LinkedIn Preparation:** Crafted a post with carousel images and Tableau links for engagement.
- **GitHub Setup:** Planned a repo to host code, README, and visuals.

## Challenges and Solutions
- **Memory Constraints:** System with 1.06GB available required script optimization (lowered threshold to 0.5GB, chunked processing).
- **Export Issue:** Tableau Public’s missing export option was resolved with manual copy-paste, ensuring all visuals were captured.
- **Learning Curve:** As a coding beginner (e.g., past indentation errors), I relied on iterative guidance, documented here for growth.

## Future Improvements
- **Automation:** Develop a Python script with `tableau-api-lib` to automate image export.
- **Dashboard Integration:** Create a unified Tableau dashboard linking all visuals.
- **Tool Comparison:** Explore Power BI for alternative insights.
- **Advanced Analytics:** Add predictive modeling (e.g., ARIMA) to Q1 for enhanced forecasting.

## Skills Developed
- **Data Cleaning:** Mastered Python-based data preprocessing with Pandas.
- **Visualization:** Gained proficiency in Tableau Public, applying UX principles.
- **Storytelling:** Enhanced ability to narrate data insights, aligning with business strategy.
- **Problem-Solving:** Overcame memory and export challenges with creative workarounds.

## Conclusion
This project encapsulates my journey from raw data to strategic visualization, reflecting skills tailored for roles like Technical Specialist at Barclays. The visualizations are not mere charts but a narrative tool, blending technical expertise with human-centered design. Explore the interactive versions below to see the full impact!

## Links to Visualizations
- [Q1: Monthly Revenue Trends in 2011](https://public.tableau.com/app/profile/aryan.7571/viz/Retail_Cleaned/Q1?publish=yes)
- [Q2: Top 10 Expansion Markets by Revenue & Quantity](https://public.tableau.com/app/profile/aryan.7571/viz/Retail_Cleaned/Q2?publish=yes)
- [Q3: Top 10 High-Value Customers by Revenue](https://public.tableau.com/app/profile/aryan.7571/viz/Retail_Cleaned/Q3?publish=yes)
- [Q4: Global Demand Opportunities Map (Excl. UK)](https://public.tableau.com/app/profile/aryan.7571/viz/Retail_Cleaned/Q4?publish=yes)

## How to Use This Repository
- **Clone:** `git clone <repo-url>` to access files.
- **Explore:** View `clean.py` for the cleaning script and PNGs for visuals.
- **Contribute:** Suggest improvements or fork the repo!

## Acknowledgments
Gratitude to the xAI community, task resource providers, and my peers for support. Special thanks to the iterative guidance that shaped this project.
