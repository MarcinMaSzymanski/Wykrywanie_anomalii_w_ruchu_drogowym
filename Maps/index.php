<?php

require("dbinfo.php");

// Start XML file, create parent node

$dom = new DOMDocument("1.0");
$node = $dom->createElement("markers");
$parnode = $dom->appendChild($node);

// Opens a connection to a MySQL server

$connection=mysqli_connect ($host, $username, $password, $database);
if (!$connection) {
  die('Not connected : ' . mysqli_error());
}

// Select all the rows in the markers table

$query = "SELECT * FROM DetectedAnomalies WHERE count>193";
$result = mysqli_query($connection, $query);
if (!$result) {
  die('Invalid query: ' . mysql_error());
}

header("Content-type: text/xml");

// Iterate through the rows, adding XML nodes for each

while ($row = @mysqli_fetch_assoc($result)){
  // Add to XML document node
  $node = $dom->createElement("marker");
  $newnode = $parnode->appendChild($node);
  $newnode->setAttribute("lat", $row['latitude']);
  $newnode->setAttribute("lng", $row['longitude']);
}
echo $dom->saveXML();
$test = $dom->saveXML();
$dom->save('test1.xml');
?>


