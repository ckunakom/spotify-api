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

    // Get the number of result
    var length = trackData.length;

    window.addEventListener('load', (event) => {
        var result = `There are ${length} result(s).`;
        document.getElementById("result").innerHTML = result;
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

    // Select the input element and get the raw HTML node; then get value property of input element
    var inputTitle = d3.select("#song-title");
    var inputTitleValue = inputTitle.property("value"); // let's lowercase the input too

};

// Homework solution -------------------------------------------------------------

// // Keep track of all filters
// var filters = {};

// function updateFilters() {

//     // Save the element, value, and id of the filter that was changed
//     var changedElement = d3.select(this).select("input");
//     var elementValue = changedElement.property("value");
//     var filterId = changedElement.attr("id");

//     // If a filter value was entered then add that filterId and value to the filters list
//     if (elementValue) {
//         filters[filterId] = elementValue;
//     }
//     // Otherwise, clear that filter from the filters object
//     else {
//         delete filters[filterId];
//     }

//     // Call function to apply all filters and rebuild the table
//     filterTable()

// }

// function filterTable() {

//     // Set the filteredData to the tableData
//     let filteredData = tableData;

//     // Loop through all of the filters and keep any data that matches the filter values
//     Object.entries(filters).forEach(([key, value]) => {
//         filteredData = filteredData.filter(row => row[key] === value);
//     });

//     // Rebuild the table using the fitlered data
//     buildTable(filteredData);

// }

// function buildTable () {
//     // uhhhhhhhhhhhhhhh what goes here....
// }

// // Attach an event to listen for changes to each filter
// d3.selectAll(".filter").on("change", updateFilters);

// // Build the table when the page loads
// buildTable(tableData);