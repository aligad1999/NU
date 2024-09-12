import streamlit as st
import pandas as pd
import os

# App title and configuration
st.set_page_config(page_title="Course Search App", page_icon=":books:", layout="wide")
st.title("Search Courses by Group")

# Specify the path to the Excel file (located beside the main code)
file_path = "CS Groups.xlsx"

# Ensure the file exists
if os.path.exists(file_path):
    # Load data into a pandas dataframe
    data = pd.read_excel(file_path)

    st.success("Data file successfully loaded!")

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
        return sorted(results, key=lambda x: x['Ratio'], reverse=True)

    # Search and display results when input is provided
    if course_input:
        results = search_courses(course_input, data)

        if results:
            st.subheader("Search Results:")
            for result in results:
                st.write(f"GroupName: {result['GroupName']} | Match Ratio: {result['Ratio']:.2f}")
        else:
            st.warning("No matching groups found for the entered courses.")
else:
    st.error(f"Data file '{file_path}' not found. Please ensure the file is placed in the correct directory.")
