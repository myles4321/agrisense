
from flask import jsonify, render_template, request, url_for, flash, redirect
from flask_login import current_user, login_user, login_manager
from itsdangerous import Serializer
from agrisense import app, db
from agrisense.forms import RegistrationForm, LoginForm, FarmingInfoForm
from agrisense.models import User, Post
import openai
import requests




@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')




@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


base_url = 'https://api.openai.com/v1'


@app.route('/generate')
def generate():
    # Set the request body
    data = {
        'prompt': 'a fish',
        'size': '1024x1024',
        'response_format': 'url'
    }

    # Send a request to OpenAI to generate the image
    response = requests.post(
        f'{base_url}/images/generations',
        headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
        json=data
    )

    if response.status_code == 200:
        image_url = response.json().get('url')

        # Render the HTML template with the image URL
        return render_template('image.html', image_url=image_url)
    else:
        return 'Error generating the image.'   
    
    
    
    
       
from flask import Flask, session, render_template, redirect, url_for, Markup
import openai
import os
import io
import base64
import matplotlib.pyplot as plt
from PIL import Image
from base64 import b64decode
from io import BytesIO
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask setup

app.secret_key = os.getenv('APPSECRET_KEY')

# OpenWeatherMap API Key
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')


@app.route('/weather')
def index():
    response = requests.get('http://ip-api.com/json/')

    if response.status_code != 200:
        return 'Could not get location information.'

    location_data = response.json()
    session['location'] = location_data

    lat = location_data.get('lat')
    lon = location_data.get('lon')

#fetching weather data.
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric'
    response = requests.get(weather_url)

    if response.status_code != 200:
        return 'Could not get weather information.'

    weather_data = response.json()
    #print(weather_data)  # Print out the data to understand the structure

  #fetching soil data.
    AMBEEDATA_API_KEY=os.getenv('AMBEEDATA_API_KEY')
    soil_url = f'https://api.ambeedata.com/latest/by-lat-lng?lat={lat}&lng={lon}'
    headers = {"x-api-key": AMBEEDATA_API_KEY}
    response = requests.get(soil_url, headers=headers)
    #print("Soil API Response: ", response.text)  # Add this line to print the response.

    if response.status_code != 200:
        return 'Could not get soil information.'
    else:
        soil_data = response.json()
        #print(soil_data )

    return render_template('display.html', weather_data=weather_data, soil_data=soil_data)



# Your OpenAI API token
openai_token = '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'

base_url = "https://api.openai.com/v1/"
url = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2'


    
def generate_image(api_key, text):
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {api_key}"}

    data = {"inputs": text}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        # Check if the response contains image data
        if 'image' in response.headers.get('Content-Type', '').lower():
            return response.content
    except Exception as e:
        print("Error occurred:", e)

    return None


# Route for the home page
@app.route('/openai', methods=['GET', 'POST'])
def dalle():
    image_data = None
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        size = request.form.get('size')
        image = DallEImage().get_image_from_dalle(prompt, size)
        
        # Convert the image to bytes and encode it in base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return render_template('openai.html', image_data=image_data) 


hf_api_key = "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"

@app.route('/huggingface', methods=['GET', 'POST'])
def huggingface():
    image_data = None
    if request.method == 'POST':
        text = request.form.get('text')
        image_bytes = generate_image(hf_api_key, text)

        if image_bytes:
            # Convert the image bytes to base64
            image_data = base64.b64encode(image_bytes).decode('utf-8')

    return render_template('huggingface.html', image_data=Markup(image_data))








OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY
chat_log = []

class DallEImage:
    def get_image_from_dalle(self, prompt, size):
 
        data = {
            "prompt": prompt,
            "size": size,
            # Fill in this line, (prompt)
            # Fill in this line, (size)
            'response_format': 'b64_json',
        }

        # download and transform the image
        response = requests.post(
            base_url + '/images/generations',
            headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
            json=data
        )
        b64_image_data = response.json().get('data', [])[0].get('b64_json', '')

        decoded_image = base64.b64decode(b64_image_data)
        image = Image.open(BytesIO(decoded_image))

        return image  # fill in this line

chat_log = []
@app.route('/farminginfo', methods=['GET', 'POST'])
def farminginfo():
    
    response = requests.get('http://ip-api.com/json/')

    if response.status_code != 200:
        return 'Could not get location information.'

    location_data = response.json()
    session['location'] = location_data

    lat = location_data.get('lat')
    lon = location_data.get('lon')

#fetching weather data.
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric'
    response = requests.get(weather_url)

    if response.status_code != 200:
        return 'Could not get weather information.'

    weather_data = response.json()
    #print(weather_data)  # Print out the data to understand the structure

  #fetching soil data.
    AMBEEDATA_API_KEY=os.getenv('AMBEEDATA_API_KEY')
    soil_url = f'https://api.ambeedata.com/latest/by-lat-lng?lat={lat}&lng={lon}'
    headers = {"x-api-key": AMBEEDATA_API_KEY}
    response = requests.get(soil_url, headers=headers)
    #print("Soil API Response: ", response.text)  # Add this line to print the response.

    if response.status_code != 200:
        return 'Could not get soil information.'
    else:
        soil_data = response.json()
        #print(soil_data )
    
    form = FarmingInfoForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Retrieve user responses from the form
        q1 = form.q1.data
        q2 = form.q2.data
        q3 = form.q3.data
        q4 = form.q4.data
        q5 = form.q5.data
        q6 = form.q6.data


        # Create a message for the GPT-4 model
        user_message = f"based on this weather data: {weather_data} and this soil information:{soil_data}, suggest four crops to plant that will grow well with such weather conditions and soil information."
        #user_message = f"name one crop"
        # Append the user's message to the chat log
        chat_log.append({"role": "user", "content": user_message})
        

        # Send the message to the GPT-4 model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )

        # Extract the assistant's response
        assistant_response = response['choices'][0]['message']['content']

        # Append the assistant's response to the chat log
        chat_log.append({"role": "assistant", "content": assistant_response})
        #chat_log.append(assistant_response)
        
        first_crop = f"give only the names of the first four crop suggestion, names only: {assistant_response}"
        response2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_log + [{"role": "user", "content": first_crop}]
        )
        firstt_crop = response2['choices'][0]['message']['content']
        chat_log.append({"role": "assistant", "content": firstt_crop})
        #chat_log.append(firstt_crop)
        
        
        image_data = None
        prompt = f"generate four seperate different realistic seed images of each of the crops in: {firstt_crop}"
        size = "512x512"
        image = DallEImage().get_image_from_dalle(prompt, size)
        
        # Convert the image to bytes and encode it in base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Render the 'gpt.html' template with the form and response
        return render_template('farminginfo.html', title='farminginfo', form=form, assistant_response=assistant_response,firstt_crop=firstt_crop, image_data=image_data)

    # Render the 'gpt.html' template with the form when the page is initially loaded
    return render_template('farminginfo.html', title='farminginfo', form=form)



@app.route('/get_pest_control', methods=['POST'])
def get_pest_control_advice():
    data = request.get_json()
    assistant_response = data.get('assistantResponse')

    # Initialize chat log with the assistant's response and a question about pests
    chat_log = [{"role": "user", "content": assistant_response},
                {"role": "assistant", "content": "for each one of the crops, what pests affect them and suggest two ways to protect ech of those crops?"}]

    try:
        # Send the chat log to the GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_log,
        )

        # Extract the assistant's response from the model's output
        assistant_response = response['choices'][0]['message']['content']

        # Return the pest control advice generated by the model
        pest_control_advice = f"Here is some pest control advice for the suggested crops: ..."

        return jsonify({"pestControlAdvice": assistant_response})

    except Exception as e:
        # Handle errors appropriately
        return jsonify({"error": str(e)})

