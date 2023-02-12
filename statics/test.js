let reader = new FileReader();


// Set the onload event for the reader
reader.onload = function() {
  // Get the contents of the file
  let csvData = reader.result;

  // Parse the CSV data
  let parsedData = Papa.parse(csvData, {
    header: true
  });

  // Build the HTML table
  let table = document.createElement("table");
  let headers = parsedData.meta.fields;

  let headerRow = document.createElement("tr");
  headers.forEach(function(header) {
    let headerCell = document.createElement("th");
    headerCell.textContent = header;
    headerRow.appendChild(headerCell);
  });
  table.appendChild(headerRow);

  parsedData.data.forEach(function(row) {
    let tableRow = document.createElement("tr");
    headers.forEach(function(header) {
      let cell = document.createElement("td");
      cell.textContent = row[header];
      tableRow.appendChild(cell);
    });
    table.appendChild(tableRow);
  });

  // Add the table to the page
  document.body.appendChild(table);
};

// Read the contents of the file
reader.readAsText(fileInput.files[0]);


