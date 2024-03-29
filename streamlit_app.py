# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customize Your Smoothie 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get the current credentials

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe
)

submit_button = st.button("Submit Order")

if ingredients_list:
    ingredients_str = ''

    for fruit_chosen in ingredients_list:
        ingredients_str += fruit_chosen + ' '
        st.subheader(f"{fruit_chosen} Nutrition Information")
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen}")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

if submit_button:
    ingredients_str = ''
    for fruit_chosen in ingredients_list:
        ingredients_str += fruit_chosen + ' '
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_str + """', '""" + name_on_order + """')"""

    session.sql(my_insert_stmt).collect()
    
    st.success(f'Your Smoothie is ordered!, {name_on_order}', icon="✅")
