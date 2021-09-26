import json

from flask import Blueprint, Flask, request, Response
from flask_cors import CORS

from build_model import Model
from utils import get_coords_by_address


ml = Blueprint('ml', __name__)
CORS(ml)

model = Model()

@ml.route('/predict', methods=['GET'])
def predict():
    if request.method != 'GET':
        return Response(
            json.dumps({'status': 'error', 'message': 'Method not allowed.'}),
            status=405
        )

    data = request.args
    address = data['address']
    volume = float(data['volume'])
    date = data['date']
    dates = model.get_time(date, address, volume)

    return Response(
        json.dumps({'status': 'ok', 'data': dates}),
        status=200
    )    


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(ml, url_prefix='')
    app.run(host='0.0.0.0', port=8080, debug=True)
