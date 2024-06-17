import yaml
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Semester Tracker',layout='wide')
st.title("Credits Based Evaluation System")
# Load YAML data from a file
with open('conf.yaml') as file:
    data = yaml.safe_load(file)

# Access the YAML data
# print(data)
branchs = ['ComputerScienceEngineering(CSE)','InformationTechnology(IT)','Mechanical(MECH)','ElectricalAndCommunication(ECE)']
branch = st.selectbox("Select Your Branch",branchs)
sem = ['first_sem','second_sem','third_sem','fourth_sem','fifth_sem','sixth_sem','seventh_sem','eighth_sem']
semesters = st.multiselect("Select every semester you have appeared",sem)
# print(data[branch]['first_sem'])
cbcs = {}
subjects = []
credits = []
for semester in semesters :
    # st.success(type(data[branch][semester]['subjects']))
    # subs = data[branch][semester]['subjects']
    for subject in data[branch][semester]['subjects'] :
        # st.warning(subject)
        subjects.append(subject)
    for credit in data[branch][semester]['credits'] :
        # st.warning(credit)
        credits.append(credit)
    # cbcs[s] = data[branch][s]['credits']
# st.warning(subjects)
# st.success(credits)
for i in range(len(subjects)) :
    if credits[i] == 0 :
        continue
    else :
        cbcs[subjects[i]] = credits[i]
# st.info(cbcs)
# df = pd.DataFrame.from_dict(cbcs,orient='index',columns=['credits'])
df = pd.DataFrame(list(cbcs.items()), columns=['Subjects', 'Credits'],index=None)
# st.write(df)
st.sidebar.header('Sidebar Header')
with st.sidebar:
    st.write("S - 10")
    st.write("A - 9")
    st.write("B - 8")
    st.write("C - 7")
    st.write("D - 6")
    st.write("E - 5")
Grades = []
for subject in df['Subjects']:
    Grade = st.number_input(subject, min_value=5, max_value=10, step=1,key=subject)
    Grades.append(Grade)
df['Grades'] = Grades
st.dataframe(df)

tot_credits = 0
for i in range(len(df['Subjects'])):
    tot_credits += (df['Credits'][i]*df['Grades'][i])
st.write(f"Credits * Grade = ",tot_credits)
if df['Credits'].sum() or len(semesters) !=0 :
    st.write(f"CGPA =",tot_credits/df['Credits'].sum())
    st.write(f"No. of Credits =",df['Credits'].sum())
st.success("Total semesters : "+str(len(semesters)))
st.success("Total credits : "+str(df['Credits'].sum()))
st.warning("Total subjects : "+str(len(df['Subjects'])))