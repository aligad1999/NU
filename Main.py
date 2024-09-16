import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# App title and configuration
st.set_page_config(page_title="NU Course Search App", page_icon=":books:", layout="wide")
st.image("logos_new.png", width=400)
st.title("Search Courses by Group")
st.write("This tool helps you find the optimal course block for a set of selected courses. Simply choose your required courses, and the tool will analyze them to provide the best matching block, ensuring an efficient and well-organized schedule. With our recent update, it now supports AI groups, making it even easier for students and professionals in AI-related fields to find the ideal course combinations.")
file_path = "CS Groups.xlsx"

if 'course_input' not in st.session_state:
    st.session_state['course_input'] = ""

def display_clickable_courses(dataframe):
    courses = dataframe['Description (COURSES)'].str.split().explode().str.upper().unique()
    unique_courses = sorted(set(courses))
    
    st.subheader("Click on courses to add them")
    
    for i in range(0, len(unique_courses), 4):
        cols = st.columns(4)
        
        for j in range(4):
            if i + j < len(unique_courses):
                course_name = unique_courses[i + j]
                if isinstance(course_name, str):
                    if cols[j].button(course_name):
                        if st.session_state['course_input']:
                            st.session_state['course_input'] += f", {course_name}"
                        else:
                            st.session_state['course_input'] = course_name

if os.path.exists(file_path):
    data = pd.read_excel(file_path)
    st.success("Data file successfully loaded!")

    display_clickable_courses(data)

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

            # Set the height of the chart dynamically based on the number of rows
            num_rows = len(sorted_df)
            fig, ax = plt.subplots(figsize=(10, num_rows * 0.5)) 

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
