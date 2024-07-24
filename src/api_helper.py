import requests
import models
import json

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

async def post_feel(feel: models.Feel):
    feel_dict = feel.to_dict()
    feel_dict['symptoms'] = feel.symptoms.value
    response = requests.post(url="http://127.0.0.1:8000/api/feel/", json=feel_dict)
