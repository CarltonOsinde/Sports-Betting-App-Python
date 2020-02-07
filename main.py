from flask import Flask, render_template
import requests

app = Flask(__name__)

url = "https://therundown-therundown-v1.p.rapidapi.com/sports"

headers = {
    'x-rapidapi-host': "therundown-therundown-v1.p.rapidapi.com",
    'x-rapidapi-key': "1864f18133msh86532f0f8b12109p19ea0djsn2751fafa167d"
    }

#Endpoints
nba_events = "sports/4/events"

def get_lines(line_periods):
    bets = {}
    bets = ["moneylines"] = []
    bets = ["spreads"] = []
    bets = ["totals"] = []

    for line_index in line_periods:
        line = line_periods[line_index]['period_full_game']
        affiliate  = line['affiliate']['affiliate_name']
        bets["moneylines"].append("{0} : {1} {2}".format(line['moneyline']['moneyline_home'], line['moneyline']['moneyline_away'], affiliate))
        bets["spreads"].append("{0} : {1} {2}".format(line['spread']['point_spread_home'], line['spread']['point_spread_away'], affiliate))
        bets["totals"].append("over {0}; under {1} {2}".format(line['total']['total_over'], line['total']['total_under'], affiliate))
    return bets

@app.route("/")
def get_events():
        querystring = {"include":["all_periods", "scores"]}
        response = requests.request("GET", url + nba_events, headers=headers, params=querystring).json()
        events = []
        for event in response['events']:
            event_data = {}
            event_data['time'] = event['event_date']
            event_data['place'] = "{0}, {1}".format(event['score']['venue_name'], event['score']['venue_location'])
            event_data['teams'] = "{0} - {1}".format(event['teams'][1]['name'], event['teams'][0]['name'])
            event_data['bets'] = get_lines(event['line_periods'])
            events.append(event_data)

        return render_template('index.html', events=events)
if __name__ == "__main__":
    app.run(debug=True)