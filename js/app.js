// --------------- Creating a table --------------- //
// Get a reference to the table body
var tbody = d3.select("tbody");

// Load data from clean_top_tracks.json
d3.json("./data/clean_top_tracks_v2.json").then(function(trackData) {

    // console.log(trackData);


    trackData.forEach((data) => {
        // D3: append `tr` for each trackData object
        var row = tbody.append("tr");

        // Get the values within each key of JSON
        Object.entries(data).forEach(([key, value]) => {
            // Append `td` to the row for each value in JSON
            var cell = row.append("td");
            // D3:update each cell's text with values in trackData object
            cell.text(value);
        })
    });

 
// Error handler: log error to console when loading data
}).catch(function(error) {
console.log(error);
});


        // // Get the values within each key of JSON
        // Object.entries(data).forEach(([key, value]) => {
        //     // Append `td` to the row for each value in JSON
        //     var cell = row.append("td");
        //     // D3:update each cell's text with values in trackData object
        //     cell.text(value);
        // });