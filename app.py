import re, json, urllib2

from flask import Flask, render_template, redirect, Response

app = Flask(__name__)
app.url_map.strict_slashes = False


redline = [
    {
        "name": "Alewife",
        "stop_ids": [
            70061
        ]
    },
    {
        "name": "Davis",
        "stop_ids": [70063]
    }
]


# Path data for red line
paths_red_base_to_alewife = ["70062", "70064", "70066", "70068", "70070", "70072", 
        "70074", "70076", "70078", "70080", "70082", "70084", "70086"]
paths_from_ashmont_to_alewife = paths_red_base_to_alewife + ["70088", "70090","70092", "70094"]
paths_from_braintree_to_alewife = paths_red_base_to_alewife + ["70098", "70100","70102", "70104", "70106"]

paths_red_base_to_ashmont_braintree = ["70085", "70083", "70081", "70079", "70077",
        "70075", "70073", "70071", "70069", "70067", "70065", "70063", "70061"]
paths_from_alewife_to_ashmont = paths_red_base_to_ashmont_braintree + ["70093", "70091", "70089", "70087", "70085"]
paths_from_alewife_to_braintree = paths_red_base_to_ashmont_braintree + ["70105", "70103", "70101", "70099", "70097"]

def normalize_stop(stop_id):
    # some stops have multiple platforms. we don't care about platforms, so normalize to stops
    if stop_id in ['70096']: #jfk, destination alewife
        return '70086'
    elif stop_id in ['70095']: #jfk, destination braintree
        return '70085'
    else:
        return stop_id

def get_current_stop(next_stop_id, destination):
    
    print next_stop_id
    index = paths_red_base_alewife_bound.index(next_stop_id)
    
    print index
    
    if index > 0:
        return paths_red_base_alewife_bound[index - 1]
    else:
        return paths_red_base_alewife_bound[index]
    




"""redline_stop_main = [{'Alewife': [70061]}, {'Davis': [70063]}, {'Porter': [70065]}, 'Harvard', 'Central', 'Kendall_MIT',
                     'Charles_MGH', 'Park', 'Downtown_Crossing', 'South_Station', 'Broadway',
                     'Andrew', 'JFK_UMass',]
redline_ashmot = [redline_stop_main, 'Savin_Hill', 'Fields_Corner', 'Shawmut', 'Ashmont']
redline_braintree = [redline_stop_main, 'North_Quincy', 'Wollaston', 'Quincy_Center',
                     'Quincy_Adams', 'Braintree']"""


"""redline_stop_main = ['Alewife', 'Davis', 'Porter', 'Harvard', 'Central', 'Kendall_MIT',
                     'Charles_MGH', 'Park', 'Downtown_Crossing', 'South_Station', 'Broadway',
                     'Andrew', 'JFK_UMass',]
redline_ashmot = [redline_stop_main, 'Savin_Hill', 'Fields_Corner', 'Shawmut', 'Ashmont']
redline_braintree = [redline_stop_main, 'North_Quincy', 'Wollaston', 'Quincy_Center',
                     'Quincy_Adams', 'Braintree']"""

@app.route('/')
def landing():
    return render_template('index.html', num_millisecs=0)
    
@app.route('/humans.txt')
def humans():
    return render_template('humans.txt')

@app.route('/api/')
def api():
    
    #response = urllib2.urlopen('http://developer.mbta.com/lib/rthr/red.json')
    #red_line_data = response.read()
    
    #deserialized_json = json.loads(red_line_data)
    
    #tripid tracks one train
    #from this, we choose the first element in the predictions array, we use its stopid and its seconds as the transition time

    mock_data = {
        "TripList": {
            "CurrentTime": 1375565923,
            "Line": "Red",
            "Trips": [
                {
                    "TripID": "R9831FA4F",
                    "Destination": "Ashmont",
                    "Predictions": [
                        {
                        "StopID": "70063",
                        "Stop": "Davis",
                        "Seconds": 913
                        },
                        {
                        "StopID": "70065",
                        "Stop": "Porter Square",
                        "Seconds": 1037
                        }
                    ]
                },
                {
                    "TripID": "R9831FBA2",
                    "Destination": "Ashmont",
                    "Predictions": [
                        {
                        "StopID": "70065",
                        "Stop": "Porter Square",
                        "Seconds": 54
                        },
                        {
                        "StopID": "70067",
                        "Stop": "Harvard Square",
                        "Seconds": 182
                        }
                    ]
                }

            ]
            
            
        }
    }

    # add data and logic for all redline stops
    # filter trains that haven't started yet?

    
    repackaged_trips = []
    
    for trip in mock_data["TripList"]["Trips"]:#deserialized_json['TripList']['Trips']:
        
        next_stop = trip['Predictions'][0]['StopID']
        current_stop = get_current_stop(next_stop, 'some')
        
        repackaged_trips.append({'trip_id': trip['TripID'],
                    'current_stop': 's' + current_stop, 'next_stop': 's' + next_stop,
                    'est_time': trip['Predictions'][0]['Seconds'] * 1000 })
    
    data = json.dumps(repackaged_trips)
    return Response(data, status=200, mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)