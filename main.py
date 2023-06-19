from email.mime.multipart import MIMEMultipart
import ssl
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory, request, url_for
from info import sender, password, subject

app = Flask(__name__)


def send_email():
    global selected_image, text_top, text_top_y, text_bottom, text_bottom_y, selected_color, email
    selected_image = request.form.get('image-selector')
    text_top = request.form.get('textTop')
    text_bottom = request.form.get('textBottom')
    text_top_y = request.form.get('textTop_y')
    text_bottom_y = request.form.get('textBottom_y')
    selected_color = request.form.get('color-selector')
    email = request.form.get('email')
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/result.html')

    with open(f'static/img/{selected_image}', 'rb') as f:
        image_data = f.read()
    image = MIMEImage(image_data, name=f'{selected_image}')

    rendered_template = template.render(
        selected_color=selected_color,
        text_top_y=text_top_y,
        text_top=text_top,
        selected_image=selected_image,
        text_bottom_y=text_bottom_y,
        text_bottom=text_bottom,
    )
    
    msg = MIMEMultipart()
    text = MIMEText(rendered_template, 'html')
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(text)
    msg.attach(image)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, email, msg.as_string())
    server.quit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        send_email()
        return render_template('index.html',
                               selected_image=selected_image,
                               text_top=text_top,
                               text_bottom=text_bottom,
                               text_top_y=text_top_y,
                               text_bottom_y=text_bottom_y,
                               selected_color=selected_color,
                               )
    else:
        return render_template('index.html', selected_image='logo.svg')


@app.route('/static/img/<path:path>')
def serve_images(path):
    return send_from_directory('static/img', path)


if __name__ == '__main__':
    app.run(debug=True)
