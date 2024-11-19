import streamlit as st
import yaml
from common import Background, Authenticator, InitializeLogin, encrypt_users
import yagmail
from cryptography.fernet import Fernet

st.set_page_config(page_title='Home Workout Generator', page_icon='💪')
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)
Background()
InitializeLogin()
config = Authenticator()

with open("email.yaml", "r") as f:
    email = yaml.safe_load(f)

encrypted_password = email["encrypted_password"].encode()
cipher_suite = Fernet(st.secrets['key'])
decrypted_password = cipher_suite.decrypt(encrypted_password).decode()

try:
    username_forgot_username, email_forgot_username = st.session_state['authenticator'].forgot_username(location='main')
    if username_forgot_username:
        yag = yagmail.SMTP('homeworkoutgenerate@gmail.com', decrypted_password, host='smtp.gmail.com', port=587, smtp_starttls=True, smtp_ssl=False)
        yag.send(
            to=email_forgot_username,
            subject='Username',
            contents=f'Your username is: {username_forgot_username}'
        )
        st.success(f'Username sent securely to {email_forgot_username}') # Username to be transferred to user securely
        config['credentials']['usernames'] = encrypt_users(config['credentials']['usernames'], st.secrets['key'])
        with open('config.yaml', 'w') as file: 
            yaml.dump(config, file, default_flow_style=False)
    else:
        st.error('Email not found')
except Exception as e:
    st.error(e)

col1, col2, col3 = st.columns([1,1,4])
with col1:
    if st.button('**Exit**', type='primary', use_container_width=True):
        st.switch_page('Workout_Generator.py')
with col2:
    if st.button('**Login**', type='primary', use_container_width=True):
        st.switch_page('pages/1_Login.py')