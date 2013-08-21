import re, json, urllib2
from math import fabs

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


############################################################
# We want to get a 'cannonical' stopid from our station
# Store those lookups here
############################################################

# Alewife to JFK, before it splits to two paths
paths_red_base_alewife_to_braintree_ashmont = {"Alewife": "70061", "Davis": "70063", "Porter Square": "70065",
        "Harvard Square": "70067", "Central Square": "70069", "Kendall/MIT": "70071", "Charles/MGH": "70073",
        "Park Street": "70075", "Downtown Crossing": "70077", "South Station": "70079", "Broadway": "70081",
        "Andrew": "70083", "JFK/UMass": "70085"}
        
# Alewife to ashmont
paths_red_savin_hill_to_ashmont = {"Savin Hill": "70087", "Fields Corner": "70089", "Shawmut": "70091", "Ashmont": "70093"}
paths_red_alewife_to_ashmont = dict(paths_red_base_alewife_to_braintree_ashmont.items() + paths_red_savin_hill_to_ashmont.items())

# Alewife to braintree
paths_red_n_quincy_to_braintree = {"North Quincy": "70097", "Wollaston": "70099", "Quincy Center": "70101", 
    "Quincy Adams": "70103", "Braintree": "70105"}
paths_red_alewife_to_braintree = dict(paths_red_base_alewife_to_braintree_ashmont.items() + paths_red_n_quincy_to_braintree.items())


# JFK to Alewife, before it splits to two paths
paths_red_base_braintree_ashmont_to_alewife = {"Alewife": "70062", "Davis": "70064", "Porter Square": "70066",
        "Harvard Square": "70068", "Central Square": "70070", "Kendall/MIT": "70072", "Charles/MGH": "70074",
        "Park Street": "70076", "Downtown Crossing": "70078", "South Station": "70080", "Broadway": "70082",
        "Andrew": "70084", "JFK/UMass": "70086"}
        
# Ashmont to Alewife
paths_red_ashmont_to_savin_hill = {"Savin Hill": "70088", "Fields Corner": "70090", "Shawmut": "70092", "Ashmont": "70094"}
paths_red_ashmont_to_alewife = dict(paths_red_base_braintree_ashmont_to_alewife.items() + paths_red_ashmont_to_savin_hill.items())

# Braintree to Alewife
paths_red_braintree_to_n_quincy = {"North Quincy": "70098", "Wollaston": "70100", "Quincy Center": "70102", 
    "Quincy Adams": "70104", "Braintree": "70106"}
paths_red_braintree_to_alewife = dict(paths_red_base_braintree_ashmont_to_alewife.items() + paths_red_braintree_to_n_quincy.items())

############################################################
# End of station lookup data
############################################################


def get_starting_station(desination):
    # Pass in destination, receive starting station
    if destination == "Braintree" or destination == "Ashmont":
        return "Alewife"
    elif destination in paths_red_ashmont_to_savin_hill.keys():
        return "Ashmont"
    elif destination in paths_red_braintree_to_n_quincy.keys():
        return "Braintree"        
        
def get_current_stop_id(next_stop, destination):
    
    if destination == 'Ashmont':
        if int(paths_red_alewife_to_ashmont[next_stop]) + 2 <= int(paths_red_alewife_to_ashmont['Ashmont']):
            return int(paths_red_alewife_to_ashmont[next_stop]) + 2
        else:
            return int(paths_red_alewife_to_ashmont[next_stop])
            
    elif destination == 'Braintree':
        if int(paths_red_alewife_to_braintree[next_stop]) + 2 <= int(paths_red_alewife_to_braintree['Braintree']):
            return int(paths_red_alewife_to_braintree[next_stop]) + 2
        else:
            return int(paths_red_alewife_to_braintree[next_stop])
            
    elif destination == 'Alewife':
        if next_stop in paths_red_ashmont_to_savin_hill.keys():
            current_stop_id = int(paths_red_ashmont_to_savin_hill[next_stop])
        elif next_stop in paths_red_braintree_to_n_quincy.keys():
            current_stop_id = int(paths_red_braintree_to_n_quincy[next_stop])
        else:
            current_stop_id = int(paths_red_base_braintree_ashmont_to_alewife[next_stop])

        if current_stop_id - 2 >= int(paths_red_base_braintree_ashmont_to_alewife['Alewife']):
            return current_stop_id - 2
        else:
            return current_stop_id
    
    
def get_next_stop_id(next_stop, destination):
    if destination == 'Ashmont':
        next_stop_id = int(paths_red_alewife_to_ashmont[next_stop])
    elif destination == 'Braintree':
        next_stop_id = int(paths_red_alewife_to_braintree[next_stop])
    elif destination == 'Alewife':
        if next_stop in paths_red_ashmont_to_savin_hill.keys():
            next_stop_id = int(paths_red_ashmont_to_savin_hill[next_stop])
        elif next_stop in paths_red_braintree_to_n_quincy.keys():
            next_stop_id = int(paths_red_braintree_to_n_quincy[next_stop])
        else:
            next_stop_id = int(paths_red_base_braintree_ashmont_to_alewife[next_stop])
            
    return next_stop_id

@app.route('/')
def landing():
    return render_template('index.html', num_millisecs=0)
    
@app.route('/humans.txt')
def humans():
    return render_template('humans.txt')

@app.route('/api/')
def api():
    
    response = urllib2.urlopen('http://developer.mbta.com/lib/rthr/red.json')
    red_line_data = response.read()
    
    print red_line_data
    
    deserialized_json = json.loads(red_line_data)
    
    
    
    #tripid tracks one train
    #from this, we choose the first element in the predictions array, we use its stopid and its seconds as the transition time

    """mock_data = {
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
    }"""

    # add data and logic for all redline stops
    # filter trains that haven't started yet?

    
    repackaged_trips = []
    
    for trip in deserialized_json['TripList']['Trips']: #mock_data["TripList"]["Trips"]:
        
        next_stop = trip['Predictions'][0]['Stop']
        current_stop_id = get_current_stop_id(next_stop, trip['Destination'])
        next_stop_id = get_next_stop_id(next_stop, trip['Destination'])
        
        repackaged_trips.append({'trip_id': trip['TripID'],
                    'current_stop': 's' + str(current_stop_id), 'next_stop': 's' + str(next_stop_id),
                    'est_time': fabs(trip['Predictions'][0]['Seconds'] * 1000) })
    
    data = json.dumps(repackaged_trips)
    return Response(data, status=200, mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)