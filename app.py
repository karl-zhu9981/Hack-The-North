import json
from flask import Flask, render_template, jsonify

import BigQueryFunctions as BGF


app = Flask(__name__)

@app.route('/')
def index():
    project_id = 'test-252915'
    dataset_id = 'run_1'
    table_id = 'Model1'
    current_location = {
        'latitude': 45.2,
        'longitude': 10.42
    }
    service = BGF.Bigquery_functions(project_id, dataset_id, table_id, current_location)
    row_iter = service.return_nearby_locations()
    resp = [json.loads(row.values()[0]) for row in row_iter]
    print(resp)

    return render_template('index.html', resp=resp)

@app.route('/findLocations', methods=['POST'])
def findLocations():
    request = request.form
    return jsonify({"locations": ["Loc1", "Loc2"]}), 200


if __name__ == '__main__':
    app.run(debug=True)
