import pandas as pd
import re
import urllib.parse
import streamlit as st

st.set_page_config(page_title="Lead Cleaner", layout="wide")
st.title("Lead Scoring & Validation Tool")

# Upload CSV
uploaded_file = st.file_uploader("Upload your leads CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    
    # Let user select how to deduplicate
    st.sidebar.subheader("🔁 Deduplication Options")
    dedup_column = st.sidebar.selectbox(
        "Remove duplicates based on:",
        options=['Company', 'Owner Email', 'Owner Phone', 'Company + Owner Email']
    )

# Deduplicate before processing
    if dedup_column == 'Company + Owner Email':
        df_before = df.copy()
        df = df.drop_duplicates(subset=['Company', 'Owner Email'])
    elif dedup_column:
        df_before = df.copy()
        df = df.drop_duplicates(subset=[dedup_column])

    duplicates_removed = len(df_before) - len(df)
    if duplicates_removed > 0:
        st.sidebar.success(f"✅ Removed {duplicates_removed} duplicates.")
    else:
        st.sidebar.info("No duplicates found.")


    #FUNCTION FOR Processing The Dataset for DUPLICATE DATA,FREE DOMAIN,LINKEDIN SEARCH URLS
    def process_leads(df):
        #df = df.drop_duplicates(subset=['Company', 'Owner Email'])

        def is_valid_email(email):
            if pd.isna(email):
                return False
            regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return re.match(regex, email) is not None

        df['Valid Email'] = df['Owner Email'].apply(is_valid_email)

        free_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        def is_free_email(email):
            if pd.isna(email) or not is_valid_email(email):
                return False
            return email.split('@')[-1] in free_domains

        df['Free Email'] = df['Owner Email'].apply(is_free_email)

        df['Missing Website'] = df['Website'].isna() | (df['Website'] == '')
        df['Missing Phone'] = df['Owner Phone'].isna() | (df['Owner Phone'] == '')

        def generate_linkedin_search_url(company_name):
            if pd.isna(company_name) or company_name.strip() == '':
                return ''
            query = f"{company_name} site:linkedin.com/company"
            return f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"

        linkedin_column = 'Owner LinkedIn'
        def fill_missing_linkedin(row):
            if pd.isna(row[linkedin_column]) or row[linkedin_column].strip() == '':
                return generate_linkedin_search_url(row['Company'])
            return row[linkedin_column]

        df[linkedin_column] = df.apply(fill_missing_linkedin, axis=1)

        def revenue_score(revenue):
            try:
                num = int(str(revenue).replace('Cr', '').replace(',', '').strip())
                return 2 if num >= 5000 else 0
            except:
                return 0

        def employee_score(count):
            try:
                return 2 if int(count) > 10000 else 0
            except:
                return 0

        def lead_score(row):
            score = 0
            if row['Valid Email']:
                score += 2
            if not row['Free Email'] and row['Valid Email']:
                score += 2
            score += revenue_score(row['Revenue'])
            score += employee_score(row['Employees Count'])
            if row['Missing Website']:
                score -= 1
            if row['Missing Phone']:
                score -= 1
            return score

        df['Lead Score'] = df.apply(lead_score, axis=1)

        def categorize(score):
            if score > 6:
                return 'High'
            elif score >= 3:
                return 'Medium'
            else:
                return 'Low'

        df['Lead Priority'] = df['Lead Score'].apply(categorize)

        return df
    


    cleaned_df = process_leads(df)

    # DISPLAYING THE DATA
    st.subheader("📊 Lead Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Leads", len(cleaned_df))
    col2.metric("Valid Emails", cleaned_df['Valid Email'].sum())
    col3.metric("High Priority", sum(cleaned_df['Lead Priority'] == 'High'))

    # PRIORITY FILTER
    st.subheader("📋 Filtered Leads")
    priority_filter = st.selectbox("Select Priority", ["All", "High", "Medium", "Low"])
    if priority_filter == "All":
        st.dataframe(cleaned_df)
    else:
        filtered = cleaned_df[cleaned_df['Lead Priority'] == priority_filter]
        st.dataframe(filtered)

    # DOWNLOAD BUTTON
    csv = cleaned_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv,
        file_name='cleaned_df.csv',
        mime='text/csv'
    )
