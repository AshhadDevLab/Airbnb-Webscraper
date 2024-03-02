import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import pandas as pd

comma = "\'"
data = {
    "Title": [],
    "Subtitle": [],
    "Price": [],
    "Rating": [],
    "Link": []
}

st.markdown("""
    <style>
        [data-testid="stDecoration"] {
            background-image: linear-gradient(90deg, rgb(255, 56, 92), rgb(255, 255, 255));
        }
    </style>
    """,
            unsafe_allow_html=True)

st.title("Airbnb Scraper")
st.write("This is an example web scraper for Airbnb made using Streamlit. Please note that this is not a complete model, but rather a demonstration of how web scraping can be done with Streamlit.")

st.image("./images/airbnb_scrapper_logo.jpg",
         caption=None, use_column_width=True)

location_radio = st.radio(
    "Search Type:", ["Search by location", "Search by region"], horizontal=True)

if location_radio == "Search by location":
    location = st.text_input("Enter the location", "New York, United States")
    location = ''.join(location.replace(",", "--").split())

elif location_radio == "Search by region":
    location = st.selectbox("Select Region", [
                            "I'm flexible", "Middle East", "United Arab Emirates", "Europe", "United Kingdom", "Southeast Asia"], index=0)
    location = '-'.join(location.split())

datecol1, datecol2 = st.columns([1, 1])

with datecol1:
    check_in_date = st.date_input("Check-in date")
with datecol2:
    check_out_date = st.date_input("Check-out date")

countcol1, countcol2, countcol3, countcol4 = st.columns([1, 1, 1, 1])

with countcol1:
    adults_count = st.number_input(
        "Number of adults", value=0, key="adults_count", step=1)
with countcol2:
    children_count = st.number_input(
        "Number of children", value=0, key="children_count", step=1)
with countcol3:
    infants_count = st.number_input(
        "Number of infants", value=0, key="infant_count", step=1)
with countcol4:
    pets_count = st.number_input(
        "Number of pets", value=0, key="pets_count", step=1)

output = st.radio("Output:", ["Markdown", "CSV", "Excel"], horizontal=True)

additional_search_filters = st.toggle("Additional Search Filters", value=False)

if additional_search_filters:
    stay_radio = st.radio(
        "Stay for a:", ["Weekend", "Week", "Month"], horizontal=True)
    if stay_radio == "Weekend":
        stay = "weekend_trip"
    elif stay_radio == "Week":
        stay = "one_week"
    elif stay_radio == "Month":
        stay = "one_month"
    pass

    pricecol1, pricecol2 = st.columns([1, 1])

    with pricecol1:
        min_price = st.number_input(
            "Minimum Price", value=10, key="min_price", step=1)
        st.write(f"Minimum Price {min_price} USD")
    with pricecol2:
        max_price = st.number_input(
            "Maximum Price", value=450, key="max_price", step=1)
        st.write(f"Maximum Price {max_price} USD")


if st.button("Scrape Data"):
    driver = webdriver.Chrome()

    driver.get(f'https://www.airbnb.com{"" if location == f"I{comma}m flexible" else f"/s/{location}"}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=6&checkin={check_in_date}&checkout={check_out_date}{f"&adults={adults_count}" if adults_count > 0 else ""}{f"&children={children_count}" if children_count > 0 else ""}{f"&infants={infants_count}" if infants_count > 0 else ""}{f"&pets={pets_count}" if pets_count > 0 else ""}&flexible_trip_lengths%5B%5D={"one_week" if additional_search_filters == False else stay}{f"&max_price={max_price}" if additional_search_filters else ""}{f"&min_price={min_price}" if additional_search_filters and min_price > 10 else ""}')

    titles = driver.find_elements(
        By.CSS_SELECTOR, 'div.t1jojoys.atm_g3_1kw7nm4.atm_ks_15vqwwr.atm_sq_1l2sidv.atm_9s_cj1kg8.atm_6w_1e54zos.atm_fy_1vgr820.atm_7l_18pqv07.atm_cs_qo5vgd.atm_w4_1eetg7c.atm_ks_zryt35__1rgatj2.dir.dir-ltr')
    subtitles = driver.find_elements(
        By.CSS_SELECTOR, 'span.t6mzqp7.atm_g3_1kw7nm4.atm_ks_15vqwwr.atm_sq_1l2sidv.atm_9s_cj1kg8.atm_6w_1e54zos.atm_fy_kb7nvz.atm_7l_12u4tyr.atm_am_qk3dho.atm_ks_zryt35__1rgatj2.dir.dir-ltr')
    prices = driver.find_elements(By.CSS_SELECTOR, 'span._tyxjp1')
    ratings = driver.find_elements(
        By.CSS_SELECTOR, 'span.r1dxllyb.atm_7l_18pqv07.atm_cp_1ts48j8.dir.dir-ltr')
    links = driver.find_elements(By.CSS_SELECTOR, 'a.l1ovpqvx.atm_1y33qqm_1ggndnn_10saat9.atm_17zvjtw_zk357r_10saat9.atm_w3cb4q_il40rs_10saat9.atm_1cumors_fps5y7_10saat9.atm_52zhnh_1s82m0i_10saat9.atm_jiyzzr_1d07xhn_10saat9.bn2bl2p.atm_5j_8todto.atm_9s_1ulexfb.atm_e2_1osqo2v.atm_fq_idpfg4.atm_mk_stnw88.atm_tk_idpfg4.atm_vy_1osqo2v.atm_26_1j28jx2.atm_3f_glywfm.atm_kd_glywfm.atm_3f_glywfm_jo46a5.atm_l8_idpfg4_jo46a5.atm_gi_idpfg4_jo46a5.atm_3f_glywfm_1icshfk.atm_kd_glywfm_19774hq.atm_uc_x37zl0_1w3cfyq_oggzyc.atm_70_thabx4_1w3cfyq_oggzyc.atm_uc_glywfm_1w3cfyq_pynvjw.atm_uc_x37zl0_18zk5v0_oggzyc.atm_70_thabx4_18zk5v0_oggzyc.atm_uc_glywfm_18zk5v0_pynvjw.dir.dir-ltr')

    for title, subtitle, price, rating, link in zip(titles, subtitles, prices, ratings, links):
        if output == "Markdown":
            data["Title"].append(title.text)
            data["Subtitle"].append(subtitle.text)
            data["Price"].append(price.text)
            data["Rating"].append(f"⭐{rating.text}")
            data["Link"].append(link.get_attribute("href"))

            df = pd.DataFrame(data)

        elif output == "CSV":
            data["Title"].append(title.text)
            data["Subtitle"].append(subtitle.text)
            data["Price"].append(price.text)
            data["Rating"].append(f"⭐{rating.text}")
            data["Link"].append(link.get_attribute("href"))

            df = pd.DataFrame(data)
            filename = "airbnb_data.csv"
            df.to_csv(filename, index=False)

        elif output == "Excel":
            data["Title"].append(title.text)
            data["Subtitle"].append(subtitle.text)
            data["Price"].append(price.text)
            data["Rating"].append(f"⭐{rating.text}")
            data["Link"].append(link.get_attribute("href"))

            df = pd.DataFrame(data)
            filename = "airbnb_data.xlsx"
            df.to_excel(filename, index=False)

    if output == "Markdown":
        st.table(df)
    elif output == "CSV":
        st.write(f"Data saved to :green[{filename}]")
    elif output == "Excel":
        st.write(f"Data saved to :green[{filename}]")

st.markdown("---")

st.markdown("Copyright © 2024 AshhadDevLab")
st.markdown("## About Me")
st.markdown("I specialize in 3D Model design and development, Machine Learning, Artificial Intelligence, and Chatbot Development. With extensive experience in academic research and practical applications, I provide comprehensive solutions from data preprocessing to deployment.")

st.markdown("**My expertise encompasses:**")
st.markdown("- Integration and optimization of GPT Models for diverse applications including API Integration, LangChain, and LLamaIndex.")
st.markdown("- Expertise in Data Preprocessing and Visualization techniques.")
st.markdown("- JavaScript development for dynamic web applications, utilizing frameworks such as Three.js for immersive 3D visualizations.")

st.markdown("**I employ a range of tools in my work, including:**")
st.markdown(
    "- Programming languages like Python for backend development and JavaScript for front end.")
st.markdown("- Utilization of CSV and Google Sheets for data management.")
st.markdown(
    "- Data manipulation libraries such as Pandas and NumPy and visualization tools like Matplotlib.")
st.markdown(
    "- Proficient in version control with Git and leveraging Github actions for seamless workflows.")

st.markdown("My recent projects have involved the development of a web scrapping tool, extracting complex location data from Airbnb using the Selenium library, the presentation of the project is based on the Python Streamlit library.")

st.markdown("GitHub: [AshhadDevLab](https://github.com/AshhadDevLab)")
st.markdown(
    "LinkedIn: [Ashhad Ahmed](https://www.linkedin.com/in/ashhad-ahmed-1230ab25a/)")
st.markdown(
    "Stack Overflow: [AshhadDevLab](stackoverflow.com/users/23106915/ashhaddevlab)")
