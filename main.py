import smtplib
from flask import Flask, render_template, send_from_directory, request
from jinja2 import Environment, FileSystemLoader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from info import sender, password, subject
from translate import Translator

# initialize flask app
app = Flask(__name__)


def send_email():
    try:
        # env settings
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('templates/result.html')

        # read an image
        with open(f'static/img/{selected_image}', 'rb') as f:
            image_data = f.read()
        image = MIMEImage(image_data, name=f'{selected_image}')

        # translate selected_color
        translator = Translator(to_lang='ru')
        translation = translator.translate(selected_color)

        # render template
        rendered_template = template.render(
            selected_color=translation,
            text_top_y=text_top_y,
            text_top=text_top,
            selected_image=selected_image,
            text_bottom_y=text_bottom_y,
            text_bottom=text_bottom,
            email=email
            )

        # settings
        msg = MIMEMultipart()
        text = MIMEText(rendered_template, 'html')
        msg['From'] = sender
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(text)
        msg.attach(image)

        # server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, email, msg.as_string())
        server.quit()
    except Exception as e:
        # error handling
        return f'An error occurred! The error is {e}'


@app.route('/', methods=['GET', 'POST'])
def index():
    # global variables
    global selected_image, text_top, text_top_y, text_bottom, text_bottom_y, selected_color, email
    if request.method == 'POST':
        # function send_email
        send_email()

        # get values from index.html
        selected_image = request.form.get('image-selector')
        text_top = request.form.get('textTop')
        text_bottom = request.form.get('textBottom')
        text_top_y = request.form.get('textTop_y')
        text_bottom_y = request.form.get('textBottom_y')
        selected_color = request.form.get('color-selector')
        email = request.form.get('email')
        
        # return index.html
        return render_template('index.html',
                               selected_image=selected_image,
                               text_top=text_top,
                               text_bottom=text_bottom,
                               text_top_y=text_top_y,
                               text_bottom_y=text_bottom_y,
                               selected_color=selected_color,
                               )
    else:
        # return index.html with default values
        return render_template('index.html', selected_image='logo.svg')


@app.route('/static/img/<path:path>')
def serve_images(path):
    # select an image
    return send_from_directory('static/img', path)


if __name__ == '__main__':
    app.run(debug=True)
