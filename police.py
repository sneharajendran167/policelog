import streamlit as st
import pandas as pd 
import pymysql
from streamlit_option_menu import option_menu
from datetime import datetime

def create_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        passwd="Sneharajendran@1672k",
        database="police_log"
    )
    return connection

def fetch_data(query):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result) 
                return df
        finally:
            connection.close()
    else:
        return pd.DataFrame()


#streamlit 
st.set_page_config(page_title="SecureCheck Police Dashboard",layout="wide")

st.title("🚨SecureCheck: A Python-SQL Digital Ledger for Police Post Logs")
st.markdown("View and analyze police post logs stored in MySQL database.")


with st.sidebar:
    select = option_menu("Main Menu",["Home","Police post log","Medium Insights","Complex Insights","Predict Outcome and Violation"])

# Fetch and display data
df = fetch_data("SELECT * FROM police_log_stops;")

if select == "Home":
    col1,col2=st.columns(2)
    with col1:
        st.header("Introduction of the Project")

        st.markdown("""
        **SecureCheck: Police Traffic Stop Analysis**

        This project analyzes real-world police stop data:
        - Driver demographics (gender, age, race)  
        - Types of violations (speeding, seatbelt, DUI, etc.)  
        - Stop outcomes (ticket, warning, arrest)  
        - Searches and drug-related stops  
        - Duration and time patterns of stops  

        ### Objectives
        - Identify trends in traffic stops and enforcement.  
        - Highlight potential risk factors leading to searches or arrests.  
        - Provide insights for safer roads and fairer enforcement.  

        ### Features
        - **Data Overview**- Browse raw police stop data.  
        - **Predictions**- Generate a narrative prediction of stop outcomes.  
        - **Insights Dashboard** -State-wise and vehicle-wise summaries.  

        """)

    with col2:
        st.image(r"D:/GUVI PRACTICE/traffic police.jpg")

    
elif select == "Police post log":
    st.dataframe(df, use_container_width=True)


#sql queries 
elif select == "Medium Insights":
    st.header("Medium Insights dashboard")

    select_query=st.selectbox("Select the question",
    ["1.What are the top 10 vehicle_Number involved in drug-related stops?",
    "2.Which vehicles were most frequently searched?",
    "3.Which driver age group had the highest arrest rate?",
    "4.What is the gender distribution of drivers stopped in each country?",
    "5.Which race and gender combination has the highest search rate?",
    "6.What time of day sees the most traffic stops?",
    "7.What is the average stop duration for different violations?",
    "8.Are stops during the night more likely to lead to arrests?",
    "9.Which violations are most associated with searches or arrests?",
    "10.Which violations are most common among younger drivers (<25)?",
    "11.Is there a violation that rarely results in search or arrest?",
    "12.Which countries report the highest rate of drug-related stops?",
    "13.What is the arrest rate by country and violation?",
    "14.Which country has the most stops with search conducted?"])

    if select_query=="1.What are the top 10 vehicle_Number involved in drug-related stops?":
        query1="""
        SELECT vehicle_number, COUNT(*) AS drug_related_stops
        FROM police_log_stops
        WHERE drugs_related_stop = TRUE
        GROUP BY vehicle_number
        ORDER BY drug_related_stops DESC
        LIMIT 10;
        """
        df1=fetch_data(query1)
        st.dataframe(df1,use_container_width=True)

    elif select_query=="2.Which vehicles were most frequently searched?":
        query2="""
        SELECT vehicle_number, COUNT(*) AS search_count
        FROM police_log_stops
        WHERE search_conducted = TRUE
        GROUP BY vehicle_number
        ORDER BY search_count DESC
        LIMIT 5;
        """
        df2=fetch_data(query2)
        st.dataframe(df2,use_container_width=True)

    elif select_query == "3.Which driver age group had the highest arrest rate?":
        query3="""
        SELECT 
            CASE 
                WHEN driver_age < 18 THEN '<18'
                WHEN driver_age BETWEEN 18 AND 24 THEN '18-24'
                WHEN driver_age BETWEEN 25 AND 34 THEN '25-34'
                WHEN driver_age BETWEEN 35 AND 44 THEN '35-44'
                WHEN driver_age BETWEEN 45 AND 54 THEN '45-54'
                WHEN driver_age BETWEEN 55 AND 64 THEN '55-64'
                ELSE '65+'
            END AS age_group,
            COUNT(*) AS total_stops,
            SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS arrests,
            ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate
        FROM police_log_stops
        GROUP BY age_group
        ORDER BY arrest_rate DESC;
        """
    
        df3 = fetch_data(query3)
        st.dataframe(df3, use_container_width=True)

    elif select_query == "4.What is the gender distribution of drivers stopped in each country?":
        query4="""
        SELECT driver_gender,country_name,COUNT(*) AS stop_count
        FROM police_log_stops
        GROUP BY country_name,driver_gender
        order BY country_name;"""

        df4=fetch_data(query4)
        st.dataframe(df4,use_container_width=True)

    elif select_query == "5.Which race and gender combination has the highest search rate?":
        query5="""
        SELECT 
        driver_race,
        driver_gender,
        COUNT(*) AS total_stops,
        SUM(search_conducted) AS total_searches,
        ROUND(SUM(search_conducted) / COUNT(*) * 100, 2) AS search_rate
        FROM police_log_stops
        GROUP BY driver_race, driver_gender
        ORDER BY search_rate DESC
        LIMIT 5;"""

        df5=fetch_data(query5)
        st.dataframe(df5,use_container_width=True)

    elif select_query == "6.What time of day sees the most traffic stops?":
        query6="""
        SELECT 
        CASE 
            WHEN HOUR(stop_time) BETWEEN 5 AND 11 THEN 'Morning (5AM-11AM)'
            WHEN HOUR(stop_time) BETWEEN 12 AND 16 THEN 'Afternoon (12PM-4PM)'
            WHEN HOUR(stop_time) BETWEEN 17 AND 20 THEN 'Evening (5PM-8PM)'
            ELSE 'Night (9PM-4AM)'
        END AS time_of_day,
        COUNT(*) AS stop_count
        FROM police_log_stops
        GROUP BY time_of_day
        ORDER BY stop_count DESC;"""

        df6=fetch_data(query6)
        st.dataframe(df6,use_container_width=True)

    elif select_query == "7.What is the average stop duration for different violations?":
        query7="""
        SELECT violation, ROUND(AVG(stop_duration), 2) AS avg_stop_duration_minutes
        FROM police_log_stops
        GROUP BY violation
        ORDER BY avg_stop_duration_minutes DESC
        LIMIT 10;"""

        df7=fetch_data(query7)
        st.dataframe(df7,use_container_width=True)

    elif select_query == "8.Are stops during the night more likely to lead to arrests?":
        query8="""
        SELECT
        CASE 
            WHEN HOUR(stop_time) BETWEEN 5 AND 11 THEN 'Morning (5AM-11AM)'
            WHEN HOUR(stop_time) BETWEEN 12 AND 16 THEN 'Afternoon (12PM-4PM)'
            WHEN HOUR(stop_time) BETWEEN 17 AND 20 THEN 'Evening (5PM-8PM)'
            ELSE 'Night (9PM-4AM)'
        END AS time_of_day,
        SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
        COUNT(*) AS total_stops,
        ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate
        FROM police_log_stops
        GROUP BY time_of_day
        ORDER BY arrest_rate DESC;"""

        df8=fetch_data(query8)
        st.dataframe(df8,use_container_width=True)

    elif select_query == "9.Which violations are most associated with searches or arrests?":
        query9="""
        SELECT
        violation,
        COUNT(*) AS total_stops,
        SUM(search_conducted) AS total_searches,
        SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
        ROUND(SUM(search_conducted) / COUNT(*) * 100, 2) AS search_rate,
        ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate
        FROM police_log_stops
        GROUP BY violation
        ORDER BY search_rate DESC, arrest_rate DESC
        LIMIT 10;"""

        df9=fetch_data(query9)
        st.dataframe(df9,use_container_width=True)

    elif select_query == "10.Which violations are most common among younger drivers (<25)?":
        query10="""
        SELECT violation, COUNT(*) AS stop_count
        FROM police_log_stops
        WHERE driver_age < 25
        GROUP BY violation
        ORDER BY stop_count DESC
        LIMIT 10;"""

        df10=fetch_data(query10)
        st.dataframe(df10,use_container_width=True)

    elif select_query == "11.Is there a violation that rarely results in search or arrest?":
        query11="""
        SELECT 
        violation,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN search_conducted = 1 OR stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS search_or_arrest,
        ROUND(SUM(CASE WHEN search_conducted = 1 OR stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS rate_percentage  
        FROM police_log_stops
        GROUP BY violation
        ORDER BY rate_percentage ASC;"""

        df11=fetch_data(query11)
        st.dataframe(df11,use_container_width=True)

    elif select_query== "12.Which countries report the highest rate of drug-related stops?":
        query12="""
        SELECT 
        country_name,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN violation LIKE '%DUI%' THEN 1 ELSE 0 END) AS drug_stops,
        ROUND(SUM(CASE WHEN violation LIKE '%DUI%' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS drug_stop_rate
        FROM police_log_stops
        GROUP BY country_name
        ORDER BY drug_stop_rate DESC;"""

        df12=fetch_data(query12)
        st.dataframe(df12,use_container_width=True) 

    elif select_query== "13.What is the arrest rate by country and violation?":
        query13="""
        SELECT country_name, violation,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
        ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate
        FROM police_log_stops
        GROUP BY country_name,violation
        ORDER BY arrest_rate DESC;"""

        df13=fetch_data(query13)
        st.dataframe(df13,use_container_width=True) 

    elif select_query== "14.Which country has the most stops with search conducted?":
        query14="""
        SELECT country_name,
        COUNT(*) AS total_stops
        FROM police_log_stops
        WHERE search_conducted = TRUE
        GROUP BY country_name
        ORDER BY total_stops DESC
        LIMIT 1;"""

        df14=fetch_data(query14)
        st.dataframe(df14,use_container_width=True) 

elif select=="Complex Insights":
    st.header("Complex Insights dashboard")
    
    select_query=st.selectbox("Select the question",
    ["1.Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions)",
     "2.Driver Violation Trends Based on Age and Race (Join with Subquery)",
     "3.Time Period Analysis of Stops (Joining with Date Functions) , Number of Stops by Year,Month, Hour of the Day",
     "4.Violations with High Search and Arrest Rates (Window Function)",
     "5.Driver Demographics by Country (Age, Gender, and Race)",
     "6.Top 5 Violations with Highest Arrest Rates"])

    if select_query=="1.Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions)":
        query1="""
        SELECT country_name,year,total_stops,total_arrests,
        ROUND((total_arrests * 1.0 / total_stops) * 100, 2) AS arrest_rate_percentage,
        RANK() OVER (PARTITION BY year ORDER BY total_arrests DESC) AS rank_by_arrests
        FROM 
        (SELECT country_name,
        EXTRACT(YEAR FROM stop_date) AS year,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests
        FROM police_log_stops
        GROUP BY country_name, EXTRACT(YEAR FROM stop_date)) AS yearly_data
        ORDER BY year, rank_by_arrests;"""
        
        df1=fetch_data(query1)
        st.dataframe(df1,use_container_width=True)

    elif select_query=="2.Driver Violation Trends Based on Age and Race (Join with Subquery)":
        query2="""
        SELECT 
        a.age_group,
        t.violation,
        t.driver_race,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN t.stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
        ROUND(SUM(CASE WHEN t.stop_outcome = 'Arrest' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate
        FROM police_log_stops t
        JOIN (
        SELECT 
        stop_id,
        CASE 
            WHEN driver_age BETWEEN 16 AND 25 THEN '16-25'
            WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
            WHEN driver_age BETWEEN 36 AND 50 THEN '36-50'
            WHEN driver_age BETWEEN 51 AND 65 THEN '51-65'
            ELSE '66+' 
        END AS age_group
        FROM police_log_stops) a
        ON t.stop_id = a.stop_id
        GROUP BY a.age_group, t.driver_race,t.violation
        ORDER BY total_stops DESC;"""

        df2=fetch_data(query2)
        st.dataframe(df2,use_container_width=True)

    elif select_query=="3.Time Period Analysis of Stops (Joining with Date Functions) , Number of Stops by Year,Month, Hour of the Day":
        query3="""
        SELECT
        YEAR(STR_TO_DATE(stop_date, '%Y-%m-%d')) AS year,
        MONTH(STR_TO_DATE(stop_date, '%Y-%m-%d')) AS month,
        HOUR(STR_TO_DATE(stop_time, '%H:%i:%s')) AS hour_of_day,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
        ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate
        FROM police_log_stops
        GROUP BY year, month, hour_of_day
        ORDER BY year, month, hour_of_day;"""

        df3=fetch_data(query3)
        st.dataframe(df3,use_container_width=True)

    elif select_query=="4.Violations with High Search and Arrest Rates (Window Function)":
        query4="""
        SELECT
        violation,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) AS total_searches,
        SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
        ROUND(SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS search_rate,
        ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate,
        RANK() OVER (ORDER BY ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) DESC) AS rank_by_arrest_rate,
        RANK() OVER (ORDER BY ROUND(SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) DESC) AS rank_by_search_rate
        FROM police_log_stops
        GROUP BY violation
        ORDER BY rank_by_arrest_rate ASC, rank_by_search_rate ASC;"""

        df4=fetch_data(query4)
        st.dataframe(df4,use_container_width=True)

    elif select_query=="5.Driver Demographics by Country (Age, Gender, and Race)":
        query5="""
        SELECT
        country_name,
        CASE 
            WHEN driver_age BETWEEN 16 AND 25 THEN '16-25'
            WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
            WHEN driver_age BETWEEN 36 AND 50 THEN '36-50'
            WHEN driver_age BETWEEN 51 AND 65 THEN '51-65'
            ELSE '66+'
        END AS age_group,
        driver_gender,
        driver_race,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
        ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate
        FROM police_log_stops
        GROUP BY country_name, age_group, driver_gender, driver_race
        ORDER BY country_name, total_stops DESC;"""

        df5=fetch_data(query5)
        st.dataframe(df5,use_container_width=True)

    elif select_query=="6.Top 5 Violations with Highest Arrest Rates":
        query6="""
        SELECT 
        violation,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
        ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate
        FROM police_log_stops
        GROUP BY violation
        ORDER BY arrest_rate DESC
        LIMIT 5;"""

        df6=fetch_data(query6)
        st.dataframe(df6,use_container_width=True)

elif select == "Predict Outcome and Violation":
    st.header("Log for Predict the outcome and Violation")
    with st.form("form"):
        stop_date = st.date_input("STOP DATE")
        stop_time = st.text_input("STOP TIME (HH:MM:SS)", value="00:00:00")
        try:
            stop_time = datetime.strptime(stop_time, "%H:%M:%S").time()
        except ValueError:
            st.error("Invalid time format. Use HH:MM:SS")
            stop_time = None

        driver_gender = st.selectbox("DRIVER GENDER", ["M", "F"])
        driver_age = st.number_input("DRIVER AGE", min_value=18, max_value=80)
        violation = st.selectbox("VIOLATION", ["Seatbelt", "Speeding", "Signal", "DUI", "Other"])
        search_conducted = st.selectbox("SEARCH CONDUCTED", ["0", "1"])
        stop_outcome = st.selectbox("STOP OUTCOME", ["Ticket", "Arrest", "Warning"])
        stop_duration = st.selectbox("STOP DURATION", df['stop_duration'].dropna().unique())
        drugs_related_stop = st.selectbox("DRUG RELATED", ["0", "1"])

        submit = st.form_submit_button("PREDICT THE STOP OUTCOME AND VIOLATION ")

    if submit and stop_time:
        searching = "A search was conducted" if int(search_conducted) else "No search was conducted"
        drug_txt = "was drugs related" if int(drugs_related_stop) else "was not drug related"
        pronoun = "he" if driver_gender == "Male" else "she"

        st.markdown(f"""
        A **{driver_age}**-years-old **{driver_gender}** driver was stopped for **{violation}** at **{stop_time.strftime('%I:%M %p')}**.
        {searching}, and {pronoun} received a **{stop_outcome}**.
        The stop lasted **{stop_duration}** and {drug_txt}.
        """)





    
    


    

