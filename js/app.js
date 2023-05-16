// Update the date when app last run
var nowDate = new Date(); 
const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var updated_date = `Last Updated: ${nowDate.getDate()+'-'+(months[nowDate.getMonth()])+'-'+nowDate.getFullYear()}`; 
document.getElementById("last-updated").innerHTML = updated_date;

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
        // row.append("td").text(data.title);
        row.append("td").html(`<a href="${data.song_url}">${data.title}</a>`);
        row.append("td").text(data.artists_name);
        row.append("td").text(data.album_name);
        row.append("td").text(data.release_date);
        row.append("td").text(data.duration_min);
        row.append("td").text(data.popularity);
        // row.append("td").html(`<a href="${data.song_url}">${data.song_url}</a>`);

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

//---------- THANK YOU DORFNOX for the tutoring below ---------- //
// Search with multiple input
// -- 1. Figure out how to get text element for each search input
// -- 2. Figure out how do we architect the passing logic - passing logic should take into account whether user should provide value or not
function search() {
    var inputTitle, inputArtist, inputDate, table, tr, tdElements, i, count;
    inputTitle = document.getElementById("song-title").value.toUpperCase();
    inputArtist = document.getElementById("artist").value.toUpperCase();
    inputDate = document.getElementById("date-release").value;

    table = document.getElementById("song-table");
    tr = Array.from(table.getElementsByTagName("tr")).slice(1);
    console.log(tr);
    count = 0;

    for (i = 0; i < tr.length; i++) {
        tdElements = tr[i].getElementsByTagName("td");
        console.log(tdElements);
        console.log(tr);
        tdTitle = tdElements[0].textContent ||  tdElements[0].innerText;
        tdArtist = tdElements[1].textContent ||  tdElements[1].innerText;
        tdDate = tdElements[3].textContent ||  tdElements[3].innerText;
        
        // Whether there's input or not, pass will be true
        var pass = true;

        if (pass && inputTitle) {            
            pass = compare(tdTitle, inputTitle);
        }

        if (pass && inputArtist) {
            pass = compare(tdArtist, inputArtist);
        }
        
        if (pass && inputDate) {
            pass = compare(tdDate, inputDate);
        }

        if (pass) {
            tr[i].style.display = "";
            count = count + 1;  
        }
        else {
            tr[i].style.display = "none";
        }
        
    }
    updateResult(count);
}

// Compare if input from user is in text element
function compare(string1, string2) {
    return string1.toUpperCase().includes(string2.toUpperCase());
}

// Update result numbers
function updateResult(count) {
    var result = `There are ${count} result(s).`;
    document.getElementById("result").innerHTML = result;
} 

// Create search list -- Thank you w3schools.com <3 //
// // Search with title
// function searchTitle() {
//     var input, filter, table, tr, td, i, txtValue, count;
//     input = document.getElementById("song-title");
//     filter = input.value.toUpperCase();
//     table = document.getElementById("song-table");
//     tr = table.getElementsByTagName("tr");
//     count = 0;

//     for (i = 0; i < tr.length; i++) {
//         td = tr[i].getElementsByTagName("td")[0];
        
//         if (td) {
//             txtValue = td.textContent || td.innerText;
//             if (txtValue.toUpperCase().indexOf(filter) > -1) {
//                 tr[i].style.display = "";
//                 count = count + 1;
//                 console.log(count);               
//             }
//             else {
//                 tr[i].style.display = "none";
//             }
//         }    
        
//     }
// }