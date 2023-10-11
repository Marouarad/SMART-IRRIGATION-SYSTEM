<?php
ini_set('display_errors', 1);
// Connexion à la base de données
$dbh = new PDO("sqlite:/var/www/html/soft_project/Client/BD/farm_water.db");

// Requête de sélection des 100 dernières valeurs de niveau d'eau par jour
$sql1 = "SELECT * FROM water_level_table WHERE rowid>=(SELECT MAX(rowid)-100 FROM water_level_table);";
// Requête de sélection des dernières 7 valeurs (une semaine)
$sql2 = "SELECT time_of_launching_pump, COUNT(*) FROM pompe_table WHERE time_of_launching_pump>=(Date('now','-6 days')) GROUP BY time_of_launching_pump;";

$data2 = array(); // Tableau temporaire pour stocker les données modifiées

foreach ($dbh->query($sql2) as $row) {
    // Changer la quantité d'eau dans un temps de pompage, ici "750L"
    $newData = array(new DateTime($row[0]), (int) ($row[1] * 750));
    $data2[] = $newData; // Ajouter les données modifiées au tableau temporaire
}

$data2 = json_encode($data2); // Convertir le tableau temporaire en format JSON
?>

<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

      // Charger les graphiques et les packages LineChart et BarChart.
      google.charts.load('current', {'packages':['corechart']});

      // Dessiner le graphique en ligne et le graphique en barres lorsque les graphiques sont chargés.
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data1 = google.visualization.arrayToDataTable([
          ['Time of picking', 'water level', 'minimal threshold', 'maximal threshold'],
          <?php
          foreach ($dbh->query($sql1) as $row) {
            if ($row['water_level'] == NULL) {
              continue;
            }
            // Changer le seuil minimal à "86%" et le seuil maximal à "92%" :
            echo '[new Date("' . $row['time_of_picking'] . '"),' . $row['water_level'] . ',77.43,92.43],';
          }
          ?>
        ]);

   var data2 = new google.visualization.DataTable();
data2.addColumn('string', 'Time of Launching');
data2.addColumn('number', 'Count');

<?php
foreach ($dbh->query($sql2) as $row) {
  $newData = array($row[0], (int) ($row[1] * 750));
  echo 'data2.addRow(' . json_encode($newData) . ');';
}
?>

        var linechart_options = {
          title: 'Water Level Quantity',
          seriesType: 'line',
          series: {
            0: { color: '#7a056c' },
            1: { color: '#7df9ff' },
            2: { color: '#23bd29' }
          },
          width: 550,
          height: 400
        };

        var linechart = new google.visualization.LineChart(document.getElementById('linechart_div'));

        var barchart_options = {
          title: 'Pump Water Consumption',
          width: 600,
          height: 300,
          series: [
            { color: 'purple', visibleInLegend: true },
            { color: 'red', visibleInLegend: false }
          ],
          legend: { position: 'none' },
          chart: {
            title: 'Water Pump Consumption per Day',
            subtitle: 'Pump Water Consumption'
          },
          bars: 'horizontal',
          axes: {
            x: {
              0: { side: 'top', label: 'Percentage' }
            }
          },
          bar: { groupWidth: "90%" }
        };

        var barchart = new google.visualization.BarChart(document.getElementById('barchart_div'));

        linechart.draw(data1, linechart_options);
        barchart.draw(data2, barchart_options);
      }
    </script>


  </head>
  <body class="bg">
  <nav class="navbar">
        <div class="container">
            <div class="logo"></div>
            <ul class="nav">
             <li>
                    <a class="Home" href="home.html">Home</a>
                </li>
                <li>
                    <a class="work" href="http://localhost/soft_project/Client/Php/IHM.php">Work</a>
                </li>
                <li>
                    <a class=about href="about.html">About</a>
                </li>
                <li>
                    <a href="#">Contact me</a>
                </li>
            </ul>
        </div>
    </nav>
    
    <div>
      <div style="margin-top:13%;">
        <table class="columns" align="center">
          <tr>
            <td style="margin-top:40px;">
              <div id="linechart_div" style="border: 1px solid #ccc"></div>
              <form method="post">
                <input type="submit" name="start_pumping" class="button" value="Start Pumping" />
              </form>
            </td>
            <td style="width: 6%;"></td>
            <td>
              <div id="barchart_div" style="border: 1px solid #ccc"></div>
              <form method="post">
                <input type="submit" name="average" class="button" value="Show Average" />
              </form>
              <?php
 if (isset($_POST["start_pumping"])) {
    // Exécution du script Python pour enregistrer le statut de la pompe
    exec("sudo python /var/www/html/soft_project/Serveur/Python/C-bin/pumping_water.py start_pumping", $output, $return_value);
    
   if (isset($_POST["start_pumping"])) {
    // Exécution du script Python pour enregistrer le statut de la pompe
    exec("sudo python /var/www/html/soft_project/Serveur/Python/C-bin/pumping_water.py start_pumping", $output, $return_value);
    
}

// Récupérer la valeur de la pompe dans la base de données
$conn = new SQLite3('/var/www/html/soft_project/Client/BD/farm_water.db');
$result = $conn->query("SELECT pump_status FROM pompe_table WHERE time_of_launching_pump = (SELECT MAX(time_of_launching_pump) FROM pompe_table)");
$row = $result->fetchArray(SQLITE3_ASSOC);
$pump_status_db = $row['pump_status'];

if ($pump_status_db == 0) {
    echo "La pompe est en marche... ";
} else {
    echo "La pompe est éteinte... ";
}

// Vérifier le niveau d'eau
$file_path = '/var/www/html/soft_project/Serveur/Python/sensor_file_emulator.txt';
$water_level = file_get_contents($file_path);
define('HIGH_LEVEL_OF_WATER', 90.0);
if ($water_level > HIGH_LEVEL_OF_WATER) {
    echo "La pompe est éteinte car le niveau d'eau est trop élevé.";
}
}

          // Calculer la moyenne de consommation d'eau d'une semaine
          if (isset($_POST["average"])) {
            $sum = 0;
            $i = 0;
            foreach ($dbh->query($sql2) as $row) {
              $i++;
              $sum += $row[1];
            }
            $average = 0;

if ($i != 0) {
    $average = (int) (($sum / $i) * 750);
}
            echo '<div class="headline">Weekly water consumption average: <span class="subheadline">' . $average . ' liters/day</span></div>';
          }
          ?>
        </td>
      </tr>
    </table>
  </div>
</div>
</body>
</html>


   <style> 
    ul {
    list-style-type: none;
  }

  .container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 30px;
  }
  .navbar {
    color: #14044D;
    height: 60px;
  }
  .navbar a:hover {
    color: #37367b;
    text-decoration: underline;}
    
  .navbar .logo {
    font-size: x-large;
    font-weight: bold;
  }
  
  .navbar a {
    color: #14044D;
    text-decoration: none;
    font-size: 18px;
    font-weight: bold;
  }
  

  .navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
  }
  
  .navbar ul {
    display: flex;
  }
  
  .navbar ul li {
    margin-left: 20px;
  }
  
    body, html {
    position: relative;
    height: 100%;
    width: 100%;
    margin: 0;
    overflow-y: hidden;
  }

  .bg {
  font-family: 'Poppins', sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #333;
  background-image: url("img/back.png"); 
  }

  .headline {
    font-family: Georgia, "Times New Roman", Times, serif;
    font-size: 24px;
    margin-top: 5px;
    margin-bottom: 0px;
    font-weight: normal;
    color:  #716B94;
  }

  .subheadline {
    font-family: "Lucida Grande", Tahoma;
    font-size: 14px;
    font-weight: lighter;
    font-variant: normal;
    text-transform: uppercase;
    color: #000000;
    margin-top: 10px;
    text-align: center;
    letter-spacing: 0.3em;
  }

  .button {
    color: #1A202C;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
        border: 2px solid #716B94;
    
    
  }
  .button:hover {
    background-color: #716B94; 
    color: white;
  }
  </style>        
            
            
            
            
            
            
            
            
            
            
  
