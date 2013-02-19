#! /usr/bin/python
import cgi, os, re, math

def sortV(values):
   temp = list()
   for i in range(len(values)):
      menor = 0
      for j in range(len(values)):
         if values[j][0] > values[menor][0]:
            menor = j
      temp.append(values.pop(menor))
   return temp

def page_header(values):
   print  ("""
<!doctype html>
<html>
<head>
  <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
  <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
  <title>Tarea de Max :)</title>
  <style>
    html, body {
    height: 100%;
    margin: 0;
    padding: 0;
    }

    #mapa {
    height: 70%;
    }

    @media print {
    html, body {
    height: auto;
    }

    #mapa {
    height: 650px;
    }
}
  </style>

  <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false&language=es"></script>
  <script type="text/javascript" src="http://localhost/wifi-signal.js"></script>
  <script type="text/javascript">
  function draw_signals(){""")
   values = sortV(values)
   for i in values:
      print ('      draw_circle('+str(round(i[0], 2))+', "'+str(i[2])+'", '+str(i[1])+');')
   print ("""  };
  </script>

</head>
<body onload="main()">
  <div id="mapa" width="450" height="400"></div>
  <br/>
  <p>
  <div id="description"></div>
  </p>
""")

def page_footer():
    print """
</body>
</html>
"""

def calculate_distance(signal_level):
    return ((10.0 ** ((18.0-(signal_level))/20.0) )/(41.88*2442.0))

def get_wifi_points():
    fl = open("wireless_list.dat", "r")
    text = fl.read()
    fl.close()
    text = text.split("Cell")
    wifi_points = list()
    for i in text:
        i = i.split("\n")
        temp = list()
        for j in i:
            if j.find("ESSID:") != -1:
                j = j.replace(" ", "")
                j = j.split('"')
                temp.append(j[1])
            elif j.find("Signal level") != -1:
                j = j.replace(" ", "")
                j = j.split('Signallevel=')
                signal_level = float( re.findall(r"[-]?[0-9]+", j[1])[0] )
                temp.append(calculate_distance(signal_level))
                temp.append(signal_level)

        if len(temp) > 0:
            wifi_points.append(temp)
    return wifi_points

def main():
    os.system("sudo iwlist wlan0 scan > wireless_list.dat")
    
    print "Content-Type: text/html\n"
    page_header(get_wifi_points())
    page_footer()

main()
