// receive mappings from api. draw current trains. 
// 

var stations = [
	{"station": "alewife", "id": "s70061"},
	{"station": "alewife", "id": "s70062"},
	{"station": "davis", "id": "s70063"},
	{"station": "davis", "id": "s70064"},
	{"station": "porter", "id": "s70065"},
	{"station": "porter", "id": "s70066"},
	{"station": "harvard", "id": "s70067"},
	{"station": "harvard", "id": "s70068"},
	{"station": "central", "id": "s70069"},
	{"station": "central", "id": "s70070"},
	{"station": "kendall_mit", "id": "s70071"},
	{"station": "kendall_mit", "id": "s70072"},
	{"station": "charles_mgh", "id": "s70073"},
	{"station": "charles_mgh", "id": "s70074"},
	{"station": "park", "id": "s70075"},
	{"station": "park", "id": "s70076"},
	{"station": "downtown_crossing", "id": "s70077"},
	{"station": "downtown_crossing", "id": "s70078"},
	{"station": "south_station", "id": "s70079"},
	{"station": "south_station", "id": "s70080"},
	{"station": "broadway", "id": "s70081"},
	{"station": "broadway", "id": "s70082"},
	{"station": "andrew", "id": "s70083"},
	{"station": "andrew", "id": "s70084"},
	{"station": "jfk_umass", "id": "s70085"},
	{"station": "jfk_umass", "id": "s70086"},
	
	{"station": "savin_hill", "id": "s70087"},
	{"station": "savin_hill", "id": "s70088"},
	{"station": "fields_corner", "id": "s70089"},
	{"station": "fields_corner", "id": "s70090"},
	{"station": "shawmut", "id": "s70091"},
	{"station": "shawmut", "id": "s70092"},
	{"station": "ashmont", "id": "s70093"},
	{"station": "ashmont", "id": "s70094"},
	
	{"station": "north_quincy", "id": "s70097"},
	{"station": "north_quincy", "id": "s70098"},
	{"station": "wollaston", "id": "s70099"},
	{"station": "wollaston", "id": "s70100"},
	{"station": "quincy_center", "id": "s70101"},
	{"station": "quincy_center", "id": "s70102"},
	{"station": "quincy_adams", "id": "s70103"},
	{"station": "quincy_adams", "id": "s70104"},
	{"station": "braintree", "id": "s70105"},
	{"station": "braintree", "id": "s70106"}
	
];

var station_lookup = {
	"s70061": {"x_axis": 315, "y_axis": 243},
	"s70062": {"x_axis": 315, "y_axis": 257},
	"s70063": {"x_axis": 365, "y_axis": 243},
	"s70064": {"x_axis": 365, "y_axis": 257},
	"s70065": {"x_axis": 437, "y_axis": 252},
	"s70066": {"x_axis": 430, "y_axis": 264},
	"s70067": {"x_axis": 473, "y_axis": 284},
	"s70068": {"x_axis": 462, "y_axis": 295},
	"s70069": {"x_axis": 502, "y_axis": 308},
	"s70070": {"x_axis": 493, "y_axis": 317},
	"s70071": {"x_axis": 531, "y_axis": 332},
	"s70072": {"x_axis": 520, "y_axis": 342},
	"s70073": {"x_axis": 555, "y_axis": 352},
	"s70074": {"x_axis": 545, "y_axis": 362},
	"s70075": {"x_axis": 595, "y_axis": 385},
	"s70076": {"x_axis": 585, "y_axis": 398},
	"s70077": {"x_axis": 683, "y_axis": 456},
	"s70078": {"x_axis": 673, "y_axis": 468},
	"s70079": {"x_axis": 707, "y_axis": 490},
	"s70080": {"x_axis": 692, "y_axis": 490},
	"s70081": {"x_axis": 707, "y_axis": 525},
	"s70082": {"x_axis": 692, "y_axis": 525},
	"s70083": {"x_axis": 707, "y_axis": 560},
	"s70084": {"x_axis": 692, "y_axis": 560},
	"s70085": {"x_axis": 707, "y_axis": 595},
	"s70086": {"x_axis": 692, "y_axis": 595},
	
	// Ashmont
	"s70087": {"x_axis": 628, "y_axis": 725},
	"s70088": {"x_axis": 612, "y_axis": 725},
	"s70089": {"x_axis": 628, "y_axis": 765},
	"s70090": {"x_axis": 612, "y_axis": 765},
	"s70091": {"x_axis": 628, "y_axis": 805},
	"s70092": {"x_axis": 612, "y_axis": 805},
	"s70093": {"x_axis": 628, "y_axis": 845},
	"s70094": {"x_axis": 612, "y_axis": 845},

	// Braintree	
	"s70097": {"x_axis": 764, "y_axis": 709},
	"s70098": {"x_axis": 754, "y_axis": 719},
	"s70099": {"x_axis": 820, "y_axis": 759},
	"s70100": {"x_axis": 809, "y_axis": 770},
	"s70101": {"x_axis": 879, "y_axis": 813},
	"s70102": {"x_axis": 869, "y_axis": 824},
	"s70103": {"x_axis": 928, "y_axis": 860},
	"s70104": {"x_axis": 912, "y_axis": 864},
	"s70105": {"x_axis": 928, "y_axis": 945},
	"s70106": {"x_axis": 912, "y_axis": 945}
};

var directions = {	
	"alewife": {"name": "Alewife", "right": "davis", "down": "davis", "fill": "white", "stroke": "red"},
	"davis": {"name": "Davis", "right": "porter", "down": "porter", "left": "alewife", "up": "alewife", "fill": "white", "stroke": "red"},
	"porter": {"name": "Porter", "right": "harvard", "down": "harvard", "left": "davis", "up": "davis", "fill": "white", "stroke": "red"},
	"harvard": {"name": "Harvard", "right": "central", "down": "central", "left": "porter", "up": "porter", "fill": "white", "stroke": "red"},
	"central": {"name": "Central", "right": "kendall", "down": "kendall", "left": "harvard", "up": "harvard", "fill": "white", "stroke": "red"},
	"kendall_mit": {"name": "Kendall/MIT", "right": "charles_mgh", "down": "charles_mgh", "left": "central", "up": "central", "fill": "white", "stroke": "red"},
	"charles_mgh": {"name": "Charles/MGH", "right": "park", "down": "park", "left": "kendall", "up": "kendall", "fill": "white", "stroke": "red"},
	"park": {"name": "Park Street", "right": "park", "down": "park", "left": "charles_mgh", "up": "charles_mgh", "fill": "white", "stroke": "red"}
};

var svcontainer = d3.select("svg");

var stations = svcontainer.selectAll("stations")
	.data(stations)
	.enter()
	.append("circle")
	.attr("cx", function (d) { return station_lookup[d.id].x_axis; })
	.attr("cy", function (d) { return station_lookup[d.id].y_axis; })
	.attr("r", 4)
	.attr("fill", 'blue');
	//.attr("id", function (d) { return d.id; });

/*var texts = svcontainer.selectAll("text")
    .data(station_names)
    .enter()
    .append("text")
    .attr("x", function (d) { return d.x_axis; })
    .attr("y", function (d) { return d.y_axis; })
    .attr("dy", ".1em")
    .attr("transform", function (d) { return "rotate(-45 " + Math.round(d.x_axis + 20) + "," + Math.round(d.y_axis - 10) + ")"; })
    .attr("text-anchor", "right")
    .style("font", "18px Helvetica Neue")
    .text(function (d) { return directions[d.id].name; });*/

var update_trains = function() {
    // add all stops to map
    
    d3.json("/api", function(error, json) {
        console.log(json);
        if (error) return console.warn(error);
        var data = json;

        data.forEach(function(d, i) {
            console.log('looking at ' + d.current_stop);
            svcontainer
            	.append("circle")
            	.attr("cx", station_lookup[d.current_stop].x_axis)	
            	.attr("cy", station_lookup[d.current_stop].y_axis)
            	.attr("r", 5)
            	.attr("fill", '#fff')
            	.transition()
            	.duration(d.est_time)
            	.attr("cx", station_lookup[d.next_stop].x_axis)
            	.attr("cy", station_lookup[d.next_stop].y_axis );
            });	
    });
	
};

update_trains();