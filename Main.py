import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# App title and configuration
st.set_page_config(page_title="NU Course Search App", page_icon=":books:", layout="wide")
st.title("Search Courses by Group")

file_path = "CS Groups.xlsx"

# Function to extract and display unique courses
def display_unique_courses(dataframe):
    courses = dataframe['Description (COURSES)'].str.split().explode().str.upper().unique()

    unique_courses = sorted(set(courses))
    
    num_columns = 4
    course_table = pd.DataFrame([unique_courses[i:i+num_columns] for i in range(0, len(unique_courses), num_columns)])
    
    def highlight_similar(course_name):
        if pd.isnull(course_name):
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
            return 'background-color: lightcyan'  
        elif course_name.startswith('SSCI'):
            return 'background-color: lightgoldenrodyellow'
        else:
            return ''
    
    styled_table = course_table.style.applymap(highlight_similar)
    

    st.subheader("Unique Courses")
    st.dataframe(styled_table.hide(axis='index'))

if os.path.exists(file_path):
    data = pd.read_excel(file_path)

    st.success("Data file successfully loaded!")

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
            sorted_df = results_df.sort_values(by="Ratio", ascending=False)

            st.subheader("Search Results:")
            st.dataframe(sorted_df)
            st.subheader("Visualized Results:")

            fig, ax = plt.subplots()
            ax.barh(sorted_df['GroupName'], sorted_df['Ratio'], color='skyblue')
            ax.set_xlabel("Match Ratio")
            ax.set_ylabel("GroupName")
            ax.set_title("Course Match Ratios by Group")
            plt.gca().invert_yaxis() 
            st.pyplot(fig)
        else:
            st.warning("No matching groups found for the entered courses.")
else:
    st.error(f"Data file '{file_path}' not found. Please ensure the file is placed in the correct directory.")
