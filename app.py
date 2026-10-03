import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

st.set_page_config(page_title="Pigeon Post", page_icon="🐦")

st.title("🐦 Pigeon Post Express")
st.write("Write a digital letter, and our virtual pigeon will deliver it via email!")

# Sidebar for Mail Server configurations
st.sidebar.header("⚙️ Pigeon Settings (SMTP Configuration)")
st.sidebar.write("To send real emails, we need an SMTP server. For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833).")

smtp_server = st.sidebar.text_input("SMTP Server", value="smtp.gmail.com")
smtp_port = st.sidebar.number_input("SMTP Port", value=587, step=1)
sender_email = st.sidebar.text_input("Your Email (Sender)")
sender_password = st.sidebar.text_input("Your Email Password/App Password", type="password")

# Main Form
with st.form("pigeon_form"):
    recipient_email = st.text_input("Recipient's Email Address")
    subject = st.text_input("Letter Subject", value="A letter carried by a virtual pigeon ✉️")
    letter_content = st.text_area("Write your letter here...", height=200)
    
    submitted = st.form_submit_button("🕊️ Release the Pigeon!")

if submitted:
    if not sender_email or not sender_password:
        st.error("Please configure your Sender Email and Password in the sidebar settings first!")
    elif not recipient_email or not letter_content:
        st.error("Please provide both a recipient email and the letter content.")
    else:
        with st.spinner("🐦 The pigeon is preparing for flight..."):
            try:
                # Set up the email headers and body
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                
                # Stylize the email body
                pigeon_template = f"""
                Hello!
                
                A virtual carrier pigeon has delivered a letter for you:
                
                --------------------------------------------------
                {letter_content}
                --------------------------------------------------
                
                Best regards,
                Your Pigeon Post Service 🐦
                """
                msg.attach(MIMEText(pigeon_template, 'plain'))
                
                # Establish connection with the SMTP server
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls() # Secure the connection
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                server.quit()
                
                # Fun pigeon flight animation!
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(percent_complete + 1)
                
                st.balloons()
                st.success(f"✨ Success! The pigeon has successfully delivered your letter to {recipient_email}! 🕊️")
                
            except Exception as e:
                st.error(f"❌ The pigeon got lost! Error details: {e}")
