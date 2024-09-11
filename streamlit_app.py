# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")
#aucune idee de ce que je dois changer

#option = st.selectbox("What is your favorite fruit?", ("Banana", "Strawberries", "Peaches"))

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie")
#st.write("The name on your Smoothie is", name_on_order)

ingredients_list = st.multiselect('Choose up to 5 ingredients: ', my_dataframe, max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    ingredients_string = ''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '

    #st.write(ingredients_string)

    my_insert_stmt = "insert into SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS,NAME_ON_ORDER) values ('" + ingredients_string + "','"+name_on_order+"')"
    #st.write(my_insert_stmt)
    #st.stop
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+' !', icon="✅")
