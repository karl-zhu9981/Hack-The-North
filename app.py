import json
import re
from flask import Flask, render_template, request

import BigQueryFunctions as BGF


app = Flask(__name__)


def to_geojson(row):
    point = {
            "type": "Feature",
            "properties": {
                "name": str(row['name']),
                "popupContent": '<b>{2}</b><br>Rebate: ${3}<br><a \
                href="{0}">{0}</a><br>{1}'.format(row['website'], row['phone'],
                    row['name'], row['estimated_rebate'])
            },
            "geometry": {
                "type": "Point",
                "coordinates": re.findall('-?\d+\.?\d+', row['geopoint'])
            }
        }
    return point


@app.route('/')
def htn():
    return render_template('htn.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/ewaste')
def ewaste():
    return render_template('ewaste.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recycle', methods=['GET', 'POST'])
def recycle():
    if request.method == 'POST':
        model = request.form.get('modelNumber')

        project_id = 'test-252915'
        dataset_id = 'run_1'
        table_id = model
        current_location = {
            'latitude': 43.4638888889,
            'longitude': -80.5258333333
        }
        dummy = [
                {"name": "Fake Company", "geopoint": "POINT(43.2750 -80.3133)", "rebate": True,
                    "estimated_rebate": 30, "email": "deadmoose@gmail.com" ,
                    "phone": "905-832-3423", "website": "https://www.google.com"},
                {"name": "Fake Company", "geopoint": "POINT(43.2752 -80.3133)", "rebate": True,
                    "estimated_rebate": 30, "email": "deadmoose@gmail.com" ,
                    "phone": "905-832-3423", "website": "https://www.google.com"}
                ]
        response = [to_geojson(row) for row in dummy]
        service = BGF.Bigquery_functions(project_id, dataset_id, table_id, current_location)
        row_iter = service.return_nearby_locations()
        response = [to_geojson(json.loads(row.values()[0])) for row in row_iter]
        return json.dumps(response)
    return render_template('recycle.html')

if __name__ == '__main__':
    app.run(debug=True)
