# Import python packages
import streamlit as st
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

if submit_button:
    ingredients_str = ",".join(ingredients_list)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_str + """', '""" + name_on_order + """')"""

    session.sql(my_insert_stmt).collect()
    
    st.success(f'Your Smoothie is ordered!, {name_on_order}', icon="✅")
