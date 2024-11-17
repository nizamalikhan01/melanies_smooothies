# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
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
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
#st.dataframe(data=my_dataframe, use_container_width=True)
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
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    time_to_insert = st.button("Submit")
    if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered,' + name_on_order + '!!', icon="✅")
    st.write(my_insert_stmt)

