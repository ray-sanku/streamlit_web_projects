import streamlit as st

## Streamllit form fucntions
st.header("Streamlit Form Functions!")

with st.form(key="user_info_form"):
    name = st.text_input("Your Name:")
    age = st.number_input("Your Age")
    
    st.form_submit_button("Submit form",icon="🚨")
    
st.text_area("Your name:", name)
st.text_area("Your age:", age)

input_values = {
    "Name":None,
    "Age":None,
    "Gender":None,
    "Height":None
}

with st.form(key="validation_form"):
    input_values["Name"] = st.text_input("Enter your name: ")
    input_values["Age"] = st.number_input("Enter your age: ")
    input_values["Gender"] = st.selectbox("Select your gender",["Male","Female","Other"])
    input_values["Height"] = st.number_input("Enter your heights(cm): ")
    
    submit_button = st.form_submit_button("Submit Form")
    if submit_button:
        if not all(input_values.values()):
            st.warning("Please enter all the fields!")
        else:
            st.balloons()
            for key, value in input_values.items():
                st.write(f"{key}:{value}")
    
