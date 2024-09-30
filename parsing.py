from openai import OpenAI
import streamlit as st
import base64

client = OpenAI( api_key= "")

# Function to convert image to base64
def convert_image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode()

st.title("Cheque Information Extractor")

uploaded_image = st.file_uploader("Upload a cheque image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Convert the image to base64
    base64_image = convert_image_to_base64(uploaded_image)

    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "image_url",
            "image_url": {
                "url": "data:image/png;base64,"+base64_image}
            },
            {
            "type": "text",
            "text": "This is a Cheque. You need to find the following things: Bank Name, Account Number, IFSC Code, Branch, Cheque Number (it should be in the bottom, and enclosed by 〞〞. dont give "" in the table), Date (Top right side DD MM YYYY), Payee Name, Amount in Figures, Amount in Words, Drawer's Name, Whether signature is present or not. Give the response in Table Format. Only give the table and nothing else."
            }
        ]
        }
    ]

    # Send the request to OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0,
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Display the response
    response_message = response.choices[0].message.content

    # Display the response
    st.write("Extracted Information:")
    st.markdown(response_message)
