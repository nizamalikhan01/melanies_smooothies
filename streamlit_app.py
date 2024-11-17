# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session for sis
from snowflake.snowpark.functions import col
# Write directly to the app
import requests
import pandas as pd
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """choose the fruit which u want in your custom smoothie.
    """
)


option = st.selectbox(
    "What is your favorite fruit?",
    ("Banana", "Starwberries", "Peaches"),
)
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be :  " + name_on_order)
#st.write("You selected:", option)
cnx = st.connection("snowflake")
session = cnx.session()
# snowpark dataframe
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"), col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
# pandas dataframe
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
ingredient_list = st.multiselect(
    "Chose upto 5 ingredients"
    ,my_dataframe
    ,max_selections = 5
)

if ingredient_list:
   # st.write(ingredient_list)
    ingredients_string = ''
    for each_fruit in ingredient_list:
        ingredients_string += each_fruit + " "
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', each_fruit,' is ', search_on, '.')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit)
    #st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    time_to_insert = st.button("Submit")
    if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered,' + name_on_order + '!!', icon="✅")
    st.write(my_insert_stmt)

    
