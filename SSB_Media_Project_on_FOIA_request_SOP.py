#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandas')
get_ipython().system('pip install selenium')
get_ipython().system('pip install requests')
get_ipython().system('pip install bs4')
import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[77]:


file_path = r"C:\Users\Administrator\Downloads\test.xlsx"
def read_excel(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Extract relevant columns
        agency_name_col = df["Agency Name"]
        report_number_col = df["Incident Case Number"]
        arrest_date_col = df["Incident Date"]
        subject_info_col1 = df["Subject Age"]
        subject_info_col2 = df["Subject Race/Ethnicity"]
        subject_info_col3 = df["Subject Gender"]

        # Process the data (we can customize this part based on our requirements)
        for i in range(len(df)):
            agency_name = agency_name_col[i]
            report_number = report_number_col[i]
            arrest_date = arrest_date_col[i]
            subject_info = subject_info_col1[i], subject_info_col2[i], subject_info_col3[i]

            # our logic for requesting public records goes here
            # we can print or process the relevant information as needed

            print(f"Requesting records from {agency_name} (Report/Case/Booking Number: {report_number})")
            print(f"Arrest/Booking Date: {arrest_date}")
            print(f"Subject Age/Gender: {subject_info}\n")

        # Return the DataFrame for further use (optional)
        return df

    except FileNotFoundError:
        print("Error: File not found. Please provide the correct file path.")

        #Example usage
file_path = r"C:\Users\Administrator\Downloads\test.xlsx"
df = pd.read_excel(file_path)
print(df.head())


# In[79]:


def find_foia_request_form_or_email(police_agency_name, state):
    # Step 1: Identify the Police Agency
    # We can provide the police agency name and state as input parameters.
    # Example: police_agency_name = "New Jersey PD", state = "New Jersey"
    
    # Construct the search query
    search_query = f"{police_agency_name} FOIA request form"
    
    # Search for the police agency's FOIA page
    search_results = requests.get(f"https://www.google.com/search?q={search_query}")
    soup = BeautifulSoup(search_results.content, "html.parser")
    
    # Extract relevant links from search results
    foia_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and ("foia" in href.lower() or "public records" in href.lower()):
            foia_links.append(href)
    
    if not foia_links:
        return "No FOIA request form or contact information found."
    
    # Step 2: Verify the state
    # Check if any of the links match the state provided
    for link in foia_links:
        if state.lower() in link.lower():
            return f"FOIA request form or contact information found: {link}"
    
    return "No FOIA request form or contact information found for the specified state."

# Example usage:
police_agency = "New Jersey PD"
state = "New Jersey"
result = find_foia_request_form_or_email(police_agency, state)
print(result)


# In[95]:


def get_agency_info(agency_name):
    base_url = "https://opramachine.com/api/v1/requests/"
    params = {"q": f"agency:{agency_name}"}

    try:
        response = requests.get(base_url, params=params)
        response_data = response.json()

        if "results" in response_data:
            # Assuming the first result contains the relevant agency information
            agency_info = response_data["results"][0]
            return agency_info
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    agency_name = "Morris Twp PD"
    agency_info = get_agency_info(agency_name)

    if agency_info:
        print(f"Agency Name: {agency_info.get('agency')}")
        print(f"Request Count: {agency_info.get('count')}")
        print(f"Last Updated: {agency_info.get('last_updated')}")
    else:
        print(f"Agency '{agency_name}' not found or API request failed.")


# In[91]:


def make_get_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Print the response content (data)
            print(response.text)
        else:
            print(f"Error: Status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Error making the request: {e}")

if __name__ == "__main__":
    # Replace this URL with the actual API endpoint we want to query
    api_url = "https://app.clickup.com/t/86cv3115q"
    make_get_request(api_url)


# In[93]:


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_foia_request():
    # Email configuration
    sender_email = "your_email@example.com"
    recipient_email = "recipient@example.com"
    subject = "FOIA/Public Records Request"
    body = """
    Dear Records Officer,

    I am writing to submit a Freedom of Information Act (FOIA) request for the following information:

    [Include specific details about the records we are requesting.]

    Please find my contact information below:
    Name: Your Name
    Address: Your Address
    Phone: Your Phone Number
    Email: Your Email Address

    Thank you for your attention to this matter. I look forward to your prompt response.

    Sincerely,
    [Your Full Name]
    """

    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login(sender_email, "your_email_password")
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("FOIA request email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_foia_request()


# In[94]:


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_follow_up_email():
    # Email configuration
    sender_email = "your_email@example.com"
    recipient_email = "recipient@example.com"
    subject = "Follow-Up on FOIA/Public Records Request"
    body = """
    Dear Records Officer,

    I hope this email finds you well. I am writing to follow up on my Freedom of Information Act (FOIA) request submitted on [date of initial request]. As I have not yet received an acknowledgment or tracking number, I wanted to inquire about the status of my request.

    Request Details:
    [Include any relevant details about your original request.]

    Please let me know if there are any updates or if additional information is needed from my end. I appreciate your attention to this matter and look forward to your response.

    Sincerely,
    [Your Full Name]
    """

    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login(sender_email, "your_email_password")
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Follow-up email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_follow_up_email()


# In[81]:


def make_opra_request(police_department_name, incident_case_number, incident_date, your_name):
    # Step 3.1: Signup for OPRAmachine.com (Already assumed we have an account)
    # Step 3.2: Click on "Make A Request" (Assuming we are logged in)
    
    # Step 3.3: Find the Police Department (we can search for it on OPRAmachine)
    # Example: police_department_name = "Morris Twp PD"
    
    # Step 3.4: After Finalizing the PD, click on "Make Request"
    
    # Step 3.5: Fill the Form
    request_text = f"""
    Dear {police_department_name},
    This is a request for public records made under OPRA and the common law right of access.
    I am not required to fill out an official form. Please acknowledge receipt of this message.
    
    Records requested:
    Arrest Reports of Incident case #{incident_case_number}
    Date: {incident_date}
    
    Please include all available documents related to this incident, including but not limited to the
    arrest report, booking information, and any charges filed.
    
    Respectfully Submitted,
    {your_name}
    """
    
    # Print the request text (you can also save it to a file or send it via email)
    print(request_text)

    # Step 3.6: Publish the Report & Update It on the Clickup Database (Customize this part as needed)

# Example usage:
make_opra_request(
    police_department_name="Morris Twp PD",
    incident_case_number="2022-45695",
    incident_date="4/11/2022",
    your_name="SaRa"
)


# In[82]:


def generate_opra_request_template(name, gender, age, reason_for_arrest, incident_date, your_name):
    request_text = f"""
    Dear Public Records Officer,
    I am requesting a copy of the arrest report(s) for the following individual:
    
    Name: {name}
    Gender: {gender}
    Age: {age}
    Arrested For: {reason_for_arrest}
    
    Incident Date (Approx): {incident_date}
    
    Please include all available documents related to this incident, including but not limited to the
    arrest report, booking information, and any charges filed.
    
    Respectfully Submitted,
    {your_name}
    """
    
    print(request_text)

# Example usage:
generate_opra_request_template(
    name="John Doe",
    gender="Male",
    age="30",
    reason_for_arrest="Suspicion of theft",
    incident_date="2024-04-09",
    your_name="Jane Smith"
)


# In[84]:


import requests

# ClickUp API token
API_TOKEN = "pk_84844841_MZG47YDF5W54TNFUNRMS9YF7GMO2EZ0I"

# ClickUp workspace ID and list ID 
WORKSPACE_ID = "https://app.clickup.com/9016274016/home"
LIST_ID = "86cv3115q"

# Create a new task
def create_clickup_task():
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    headers = {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json",
    }
    payload = {
        "name": "Case XYZ",  # Replace with the case number or suspect name
        "status": "Filled",
        # Add other necessary fields (description, due date, etc.)
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        task_id = response.json()["id"]
        print(f"Task created successfully! Task ID: {task_id}")
        return task_id
    else:
        print(f"Error creating task. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    task_id = create_clickup_task()
    if task_id:
        # Update custom fields (e.g., "Via," "Police Department," etc.) for the task
        # Implement the logic to wait for the report and update the status accordingly
        pass

