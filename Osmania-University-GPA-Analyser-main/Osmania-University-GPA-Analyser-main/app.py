import yaml
import streamlit as st
import pandas as pd
from st_on_hover_tabs import on_hover_tabs
from LineChart import LineChart

# loading the Yaml File
with open('engineering_curriculum2.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Hide the "Made with Streamlit" footer
# Define a CSS style for the text
hide_streamlit_style="""
    <style>
    #MainMenu{visibility:hidden;}
    footer{visibility:hidden;}
    h1 {
        color: #01FFB3 ;
    }
    h2 {
        color: darkorange;
    }
    </style>
    """
# st.markdown(hide_streamlit_style,unsafe_allow_html=True)
# setting the side bar
with st.sidebar:
    tabs = on_hover_tabs(tabName=['SGPA Calculator','CGPA Calculator',], 
                         iconName=['calculate', 'monitoring'], default_choice=0,
                         styles = {'navtab': {'background-color':'#272731',
                                                  'color': '#818181',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                    'tabOptionsStyle': {':hover :hover': {'color': 'orangered',
                                                                      'cursor': 'pointer'}},              
                                                  
                                                  },
                         )
    text = r'''\small \color{orangered}\text{SGPA = } \frac{\text{Grade Points} \times \text{Credits}}{ \sum \text{credits} } '''
    st.divider()
    st.latex(text)
    st.divider()
    helpertext= r'''\large \color{gray}\\ S : 10 \\ A :9 \\ B :8 \\ C :7 \\ D :6 \\ E :5'''
    st.latex(helpertext)
#number of semester appeared
def sgpa(branch:str,semesters:str):
    subjects = [] 
    credits = []
    cbcs = {}
    Grades = []
    GradePoints = 0
    for sub in data[branch][semesters]['subjects']:
            values = list(sub.values())
            subjects.append(values[0])
            credits.append(values[1])
    for i in range(len(subjects)) :
        cbcs[subjects[i]] = credits[i]


    df = pd.DataFrame.from_dict(cbcs,orient='index',columns=['credits'])
    df = pd.DataFrame(list(cbcs.items()), columns=['Subjects', 'Credits'],index=None)
    for i in range(len(df)):
        subject = df.iloc[i]['Subjects']
        Grade = st.number_input(subject, min_value=5, max_value=10, step=1,key=subject)
        Grades.append(Grade)
    df['Grades'] = Grades
    st.dataframe(df,use_container_width=True,hide_index=True)
    for i in range(len(df['Subjects'])):
        GradePoints += (df['Credits'][i]*df['Grades'][i])
    # st.warning(/df['Credits'].sum())
    
    Sgpa = GradePoints/df['Credits'].sum()
    st.divider()
    sub = r'''\large \color{limegreen} \text{Total Subjects = } \color{darkorange}'''+str(len(df))
    cred = r'''\large \\ \color{red} \text{Total Credits \color{skyblue} = } \color{orange}''' + str(df['Credits'].sum())
    st.latex(sub)
    st.latex(cred)
    info = r'''\huge \color{orange}\text{SGPA} = ''' + str(round(Sgpa,2))
    st.latex(info)
    st.divider()
def sgpa1(branch:str,semester:str):
    subjects = [] 
    credits = []
    cbcs = {}
    Grades = []
    GradePoints = 0
    # st.warning(data[branch][semester]['subjects']['theory'])
    for sub in data[branch][semester]['subjects']['theory']:
            values = list(sub.values())
            subjects.append(values[0])
            credits.append(values[1])
    for i in range(len(subjects)) :
        cbcs[subjects[i]] = credits[i]

    for sub in data[branch][semester]['subjects']['practical']:
            values = list(sub.values())
            subjects.append(values[0])
            credits.append(values[1])
    for i in range(len(subjects)) :
        cbcs[subjects[i]] = credits[i]


    df = pd.DataFrame.from_dict(cbcs,orient='index',columns=['credits'])
    df = pd.DataFrame(list(cbcs.items()), columns=['Subjects', 'Credits'],index=None)
    for i in range(len(df)):
        subject = df.iloc[i]['Subjects']
        Grade = st.number_input(subject, min_value=5, max_value=10, step=1,key=subject)
        Grades.append(Grade)
    df['Grades'] = Grades
    st.dataframe(df,use_container_width=True,hide_index=True)
    for i in range(len(df['Subjects'])):
        GradePoints += (df['Credits'][i]*df['Grades'][i])
    # st.warning(df['Credits'].sum())
    
    Sgpa = GradePoints/df['Credits'].sum()
    theory = len(data[branch][semester]['subjects']['theory'])
    practical = len(data[branch][semester]['subjects']['practical'])
    st.divider()
    sub = r'''\large \color{limegreen} \text{Total Subjects = } \color{darkorange}'''+str(len(df))
    sub1 = r'''\large \color{limegreen} \text{Total Theory Subjects = } \color{darkorange}'''+str(theory)
    sub2 = r'''\large \color{limegreen} \text{Total Practical Subjects = } \color{darkorange}'''+str(practical)
    cred = r'''\large \\ \color{red} \text{Total Credits \color{skyblue} = } \color{orange}''' + str(df['Credits'].sum())
    st.latex(sub)
    st.latex(sub1)
    st.latex(sub2)
    st.latex(cred)
    info = r'''\huge \color{orange}\text{SGPA} = ''' + str(round(Sgpa,2))
    st.latex(info)
    st.divider()

def cgpa(branch,semesters):
    semCredits = []
    grades = []
    n = len(semesters)
    TotCredits = 0
    TotSubjects = 0
    gpas = 0
    for semester in semesters:
        semCredits.append(data[branch][semester]['sem_credits'])
        TotCredits += data[branch][semester]['sem_credits']
        TotSubjects += len(data[branch][semester]['subjects'])
    # st.warning(type(data[branch][semester]['subjects']))
    for i in range(n):
        grades.append(float(st.number_input(f'Enter semester {i+1} SGPA. ',min_value=5.0,max_value=10.0,step=0.001)))
    for i in range(n) :
        gpas += grades[i]*semCredits[i]
    Cgpa = gpas/TotCredits
    st.divider()
    info1 = r'''\large \color{orange} \text{Total Subjects} = \color{darkorange}'''+str(TotSubjects)
    st.latex(info1)
    info2 = r'''\large \color{orange} \text{Total Credits} = \color{darkorange}'''+str(TotCredits)
    st.latex(info2)
    stringg = r'''\huge \color{skyblue} \text{ Expected GPA } =  \color{darkorange} '''+str(round(Cgpa, 3))
    st.latex(stringg)
    SemesterGrades = [{"x": i + 1, "y": grades[i]} for i in range(n)]
    LineChart(SemesterGrades=SemesterGrades)

def cgpa1(branch,semesters):
    semCredits = []
    grades = []
    n = len(semesters)
    TotCredits = 0
    # TotSubjects = 0
    TotTheorySubjects = 0
    TotPracticalSubjects = 0
    gpas = 0
    # st.warning(semesters)
    for semester in semesters:
        #  st.warning(data[branch][semester]['sem_credits'])
        semCredits.append(data[branch][semester]['sem_credits'])
        TotCredits += data[branch][semester]['sem_credits']
        TotTheorySubjects += len(data[branch][semester]['subjects']['theory'])
        TotPracticalSubjects += len(data[branch][semester]['subjects']['practical'])
    TotSubjects = TotTheorySubjects + TotPracticalSubjects
    # st.warning(type(data[branch][semester]['subjects']))
    for i in range(n):
        grades.append(float(st.number_input(f'Enter semester {i+1} SGPA. ',min_value=5.0,max_value=10.0,step=0.001)))
    for i in range(n) :
        gpas += grades[i]*semCredits[i]
    Cgpa = gpas/TotCredits
    st.divider()
    info1 = r'''\large \color{orange} \text{Total Subjects} = \color{darkorange}'''+str(TotSubjects)
    st.latex(info1)
    infoT = r'''\large \color{orange} \text{Total Theory Subjects} = \color{darkorange}'''+str(TotTheorySubjects)
    st.latex(infoT)
    infoP = r'''\large \color{orange} \text{Total Practical Subjects} = \color{darkorange}'''+str(TotPracticalSubjects)
    st.latex(infoP)
    info2 = r'''\large \color{orange} \text{Total Credits} = \color{darkorange}'''+str(TotCredits)
    st.latex(info2)
    stringg = r'''\huge \color{skyblue} \text{ Expected GPA } =  \color{darkorange} '''+str(round(Cgpa, 3))
    st.latex(stringg)
    SemesterGrades = [{"x": i + 1, "y": grades[i]} for i in range(n)]
    LineChart(SemesterGrades=SemesterGrades)
if tabs == 'SGPA Calculator':
    st.title(":orange[SGPA Calculator]",anchor=False)
    branches = list(data.keys())
    # st.warning(branches)
    branch = st.selectbox("Select Your Branch",branches)
    sems = list(data[branch].keys())
    semester = st.selectbox("Select a semester for which you want to calculate the SGPA",sems)
    sgpa1(branch=branch,semester=semester)

if tabs == 'CGPA Calculator':
    st.title(":red[CGPA Calculator]",anchor=False)
    branches = list(data.keys())
    branch = st.selectbox("Select Your Branch",branches)
    sems = list(data[branch].keys())
    semesters = st.multiselect("Select every Semester That You Have aapeared so far",sems)
    if semesters == [] or branches == []:
        msg = r'''\huge \color{orangered} \text{ Please Select at least one Semester}  \color{darkorange} '''
        st.latex(msg)
    else:
        cgpa1(branch,semesters)
