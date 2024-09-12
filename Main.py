import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# App title and configuration
st.set_page_config(page_title="NU Course Search App", page_icon=":books:", layout="wide")
st.image("logo.png", width=200)
st.title("Search Courses by Group")


file_path = "CS Groups.xlsx"

# Initialize the session state for course input
if 'course_input' not in st.session_state:
    st.session_state['course_input'] = ""

# Function to display courses as clickable buttons
def display_clickable_courses(dataframe):
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
    
    # Display courses as clickable buttons
    st.subheader("Click on courses to add them")
    for col in range(course_table.shape[1]):
        for row in course_table[col]:
            # Ensure row is a valid string before creating a button
            if isinstance(row, str):
                if st.button(row):
                    if st.session_state['course_input']:
                        st.session_state['course_input'] += f", {row}"
                    else:
                        st.session_state['course_input'] = row

# Ensure the file exists
if os.path.exists(file_path):
    data = pd.read_excel(file_path)
    st.success("Data file successfully loaded!")

    # Display the clickable courses table
    display_clickable_courses(data)

    # Display the current course_input text field
    st.text_input("Selected Courses (comma-separated):", value=st.session_state['course_input'], key='course_input', disabled=False)

    def search_courses(course_list, dataframe):
        course_list = [course.strip().upper() for course in course_list.split(',')]
        results = []
        for index, row in dataframe.iterrows():
            courses = row['Description (COURSES)'].split()
            ratio = sum(course in courses for course in course_list) / len(course_list)
            if ratio > 0:
                results.append({'GroupName': row['GroupName'], 'Ratio': ratio})
        return pd.DataFrame(results)

    if st.session_state['course_input']:
        results_df = search_courses(st.session_state['course_input'], data)

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
            st.warning("No matching groups found for the selected courses.")
else:
    st.error(f"Data file '{file_path}' not found. Please ensure the file is placed in the correct directory.")
