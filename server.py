from __future__ import annotations
from flask import Flask, render_template, request, redirect
from typing import Union, TYPE_CHECKING
import csv

if TYPE_CHECKING:
    from werkzeug.wrappers import Response as BaseResponse

app = Flask(__name__)


@app.route('/')
def my_home() -> str:
    """Renders the home page template."""
    return render_template('index.html')


def write_to_csv(data: dict[str, str]) -> None:
    """Writes the data dictionary passed into a database.csv file.

    Args:
        data - dictionary of values from contact form
            {'name': 'John Doe','email': 'jdoe@gmail.com','message': 'This is a message'}
    """
    with open('database.csv', newline='', mode='a') as database2:
        name = data['name']
        email = data['email']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form() -> Union[BaseResponse, str]:
    """Submits the form data to be stored into a csv file.

    Returns:
        A BaseResponse if the form data was successfully recorded otherwise a message is presented
        to the user.
    """
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/#thankyou')
        except:
            return 'Did not save to database'
    return 'Something went wrong. Try Again!'
