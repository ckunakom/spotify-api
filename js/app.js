// --------------- Creating a table --------------- //
// Get a reference to the table body
var tbody = d3.select("tbody");

// Load data from clean_top_tracks.json
d3.json("./data/clean_top_tracks.json").then(function(trackData) {

    // console.log(trackData);
    
    // Iterate over json data object and just pull out the columns of interest
    trackData.forEach((data) => {
    
        // D3: append `tr` for each trackData object
        var row = tbody.append("tr");
        // Append `td` to the row for each value in JSON and append each cell
        row.append("td").text(data.title);
        row.append("td").text(data.artists_name);
        row.append("td").text(data.album_name);
        row.append("td").text(data.release_date);
        row.append("td").text(data.duration_min);
        row.append("td").text(data.popularity);
        row.append("td").html(`<a href="${data.song_url}">${data.song_url}</a>`);

    });
 
// Error handler: log error to console when loading data
}).catch(function(error) {
console.log(error);
});

// --------------- Creating Search Box --------------- //
// Select the form & filter button
var form = d3.select("form");
var button = d3.select("#filter-btn");

// Create event handlers 
form.on("submit", filterEvent);
button.on("click", filterEvent);

// Complete the event handler function for the form
function filterEvent() {
    // Prevent the page from refreshing
    d3.event.preventDefault();


};