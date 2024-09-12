import streamlit as st
import pandas as pd
import os

# App title and configuration
st.set_page_config(page_title="Course Search App", page_icon=":books:", layout="wide")
st.title("Search Courses by Group")

# Specify the path to the Excel file (located beside the main code)
file_path = "CS Groups.xlsx"

# Function to extract and display unique courses
def display_unique_courses(dataframe):
    # Extract all the courses from the 'Description (COURSES)' column
    courses = dataframe['Description (COURSES)'].str.split().explode().unique()
    
    # Remove duplicates and sort the courses alphabetically
    unique_courses = sorted(set(courses))
    
    # Create a DataFrame for display with 4 columns for better visualization
    num_columns = 4
    course_table = pd.DataFrame([unique_courses[i:i+num_columns] for i in range(0, len(unique_courses), num_columns)])
    
    # Function to apply colors based on course name prefixes
    def highlight_similar(course_name):
        if pd.isnull(course_name):  # Check for None or NaN
            return ''
        elif course_name.startswith('CSCI'):
            return 'background-color: lightblue'
        elif course_name.startswith('ENGL'):
            return 'background-color: lightgreen'
        elif course_name.startswith('MATH'):
            return 'background-color: lightcoral'
        elif course_name.startswith('ECEN'):
            return 'background-color: lightyellow'
        elif course_name.startswith('PHYS'):
            return 'background-color: lightpink'
        elif course_name.startswith('HUMA'):
            return 'background-color: lightgray'
        elif course_name.startswith('NSCI'):
            return 'background-color: lightpurple'
        elif course_name.startswith('SSCI'):
            return 'background-color: lightorange'
        else:
            return ''
    
    # Style the DataFrame by applying color based on similar course names
    styled_table = course_table.style.applymap(highlight_similar)
    
    # Display the table with color styling and no index
    st.subheader("Unique Courses (No Duplicates, Sorted Alphabetically)")
    st.dataframe(styled_table.hide(axis='index'))  # Hide the index for a clean look

# Ensure the file exists
if os.path.exists(file_path):
    # Load data into a pandas dataframe
    data = pd.read_excel(file_path)

    st.success("Data file successfully loaded!")

    # Display the unique courses table
    display_unique_courses(data)

    # Text input for courses to search
    course_input = st.text_input("Enter the courses you want to search (comma-separated):")

    # Function to search courses
    def search_courses(course_list, dataframe):
        course_list = [course.strip().upper() for course in course_list.split(',')]
        results = []
        for index, row in dataframe.iterrows():
            courses = row['Description (COURSES)'].split()
            ratio = sum(course in courses for course in course_list) / len(course_list)
            if ratio > 0:
                results.append({'GroupName': row['GroupName'], 'Ratio': ratio})
        return pd.DataFrame(results)

    # Search and display results when input is provided
    if course_input:
        results_df = search_courses(course_input, data)

        if not results_df.empty:
            # Sort the results by Ratio in descending order
            sorted_df = results_df.sort_values(by="Ratio", ascending=False)

            st.subheader("Search Results (Sorted by Match Ratio):")
            st.dataframe(sorted_df)  # Display the sorted table

            # Plot the results
            st.subheader("Visualized Results:")

            fig, ax = plt.subplots()
