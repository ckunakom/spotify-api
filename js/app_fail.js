// --------------- Creating a table --------------- //
// Get a reference to the table body
var tbody = d3.select("tbody");

// Load data from clean_top_tracks.json
d3.json("./data/clean_top_tracks.json").then(function(trackData) {

    // console.log(trackData);
    
    // Iterate over json data object and just pull out the columns of interest
    // .....??? how....

    // Is there a way to do things simimalrly like in python's map?
    //// This seems excessive... I could already see Brendan cringing.

    // Pull out data of interest and make them into arrays     
    var titleArray =  trackData.map(data => data.title);
    var artistArray =  trackData.map(data => data.artists_name);
    var albumArray =  trackData.map(data => data.album_name);
    var releaseDateArray =  trackData.map(data => data.release_date);
    var durationArray =  trackData.map(data => data.duration_min);
    var populationArray =  trackData.map(data => data.popularity);
    var songUrlArray =  trackData.map(data => data.song_url);

    // Piece them up into object... 
    var newTrackData = {
        title: titleArray,
        artist: artistArray,
        album: albumArray,
        releaseDate: releaseDateArray,
        duration: durationArray,
        popularity: populationArray,
        songUrl: songUrlArray
    };

    console.log(newTrackData);

    // console.log(titleArray);
    // Loop through data...

    // THESE DON'T WORK
    // for (var i = 0; i < newTrackData.length; i++) {
    //     // D3: append `tr` for each trackData object
    //     var row = tbody.append("tr");

    //     // Get the values within each key of JSON
    //     Object.entries(data).forEach(([key, value]) => {
    //         // Append `td` to the row for each value in JSON
    //         var cell = row.append("td");
    //         // D3:update each cell's text with values in trackData object
    //         cell.text(value);
    //     });
    // }

    // newTrackData won't work... why...
    trackData.forEach((data) => {
    
        // D3: append `tr` for each trackData object
        var row = tbody.append("tr");

        Object.values(data).forEach((value) => {
            // Append `td` to the row for each value in JSON
            var cell = row.append("td");
            // Append each cell
            cell.text(value);
            // cell.text(data.artists_name);
            // cell.text(data.album_name);
            // cell.text(data.release_date);
            // cell.text(data.duration_min);
            // cell.text(data.popularity);
            // cell.text(data.song_url);
        });
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
