<!DOCTYPE html>

<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>MyIot - Temperature</title>
</head>
<body>
<?php
$topErr = "";
$top = "20";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
   if (empty($_POST["str_top"])) {
     $topErr = "top is required!";
   } else {
     $top = value_input($_POST["str_top"]);
     if (!preg_match("/^[0-9 ]*$/",$top)) {
       $topErr = "Only allow number"; 
     }
   }
}

function value_input($data) {
   $data = trim($data);
   $data = stripslashes($data);
   $data = htmlspecialchars($data);
   return $data;
}
?>

<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
Top:<input type="text" name="str_top" value="<?php echo $top;?>">
<input type="submit" name="submit" value="Submit"> 
<br>
</form>
<?php
$mysql_conf = array(
    'host'    => 'localhost', 
    'db'      => 'myiot', 
    'db_user' => 'admin', 
    'db_pwd'  => 'Osram9809', 
    );

$mysqli = @new mysqli($mysql_conf['host'], $mysql_conf['db_user'], $mysql_conf['db_pwd']);
if ($mysqli->connect_errno) {
    die("could not connect to the database:\n" . $mysqli->connect_error);
}
$mysqli->query("set names 'utf8';");
$select_db = $mysqli->select_db($mysql_conf['db']);
if (!$select_db) {
    die("could not connect to the db:\n" .  $mysqli->error);
}$sql = "select *  from tb_temperature order by id desc limit $top;";
$res = $mysqli->query($sql);
if (!$res) {
    die("sql error:\n" . $mysqli->error);
}

echo "<table border='1'>
<tr>
<th>hostname</th>
<th>location</th>
<th>room_temp_c</th>
<th>room_humidity</th>
<th>cpu_temp</th>
<th>gpu_temp</th>
<th>cpu_use</th>
<th>ram_total</th>
<th>ram_used</th>
<th>ram_free</th>
<th>disk_total</th>
<th>disk_used</th>
<th>disk_used_perc</th>
<th>creation_datetime</th>
</tr>";

 while ($row = $res->fetch_assoc()) {
	echo "<tr>";
        ///var_dump($row);
        ///echo "<td>" . $row["hostname"] . "</td>";
  echo "<td>" . $row['hostname'] . "</td>";
  echo "<td>" . $row['location'] . "</td>";
  if ($row['room_temp_c'] >= 30) {
    echo "<td style='color:yellow' bgcolor='red'>" . $row['room_temp_c'] . "</td>";
  } elseif($row['room_temp_c'] > 25 and $row['room_temp_c'] < 30 ) { 
    echo "<td bgcolor='yellow'>" . $row['room_temp_c'] . "</td>";
  } else {
    echo "<td bgcolor='#00FF00'>" . $row['room_temp_c'] . "</td>";
  }

  //echo "<td>" . $row['room_temp_f'] . "</td>";  
  echo "<td>" . $row['room_humidity'] . "</td>";   
  echo "<td>" . $row['cpu_temp'] . "</td>";
  echo "<td>" . $row['gpu_temp'] . "</td>";
  if ($row['cpu_use'] >= '50%') {
    echo "<td style='color:yellow' bgcolor='red'>" . $row['cpu_use'] . "</td>";
  } else {
    echo "<td>" . $row['cpu_use'] . "</td>";
  }
  echo "<td>" . $row['ram_total'] . "</td>";
  echo "<td>" . $row['ram_used'] . "</td>";
  echo "<td>" . $row['ram_free'] . "</td>";
  echo "<td>" . $row['disk_total'] . "</td>";
  echo "<td>" . $row['disk_used'] . "</td>";
  echo "<td>" . $row['disk_used_perc'] . "</td>";
  //echo "<td>" . $row['creation_year'] . "</td>";
  echo "<td>" . $row['creation_datetime'] . "</td>";   
  echo "</tr>";
  }
echo "</table>";

$res->free();
$mysqli->close();
?>
</body>
</html>