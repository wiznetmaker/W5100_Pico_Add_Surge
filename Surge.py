from usocket import socket
from machine import Pin, SPI, ADC
import network
import time
import ujson

led = Pin(25, Pin.OUT)
response = ""


# W5x00 chip initialization
def w5x00_init():
    spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
    nic = network.WIZNET5K(spi, Pin(17), Pin(20))  # spi, cs, reset pin
    nic.active(True)

    # None DHCP
    nic.ifconfig(('192.168.0.20', '255.255.255.0', '192.168.0.1', '8.8.8.8'))

    # DHCP
    # nic.ifconfig('dhcp')
    print('IP address:', nic.ifconfig())

    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())

def web_page():
    html = """

    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pico Probe</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>  <!-- Plotly library -->
    <script>
        function updateChart() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    var data = JSON.parse(this.responseText);

                    var trace = {
                        <!-- x: data.time, -->
                        x: 0,
                        y: data.value,
                        mode: 'lines',
                        type: 'scatter'
                    };

                    var layout = {
                        title: 'Analog Data',
                        xaxis: {
                            title: 'Time'
                        },
                        yaxis: {
                            title: 'Value',
                            range: [0, 7]  // Set the y-axis range from 0 to 5
                        }
                    };

                    var chartData = [trace];
                    Plotly.newPlot('chart', chartData, layout);
                    <!-- document.getElementById("adc_value").innerHTML = data.value; -->
                    document.getElementById("adc_value").innerHTML = data.value.slice(-1)[0];
                }
            };
            xhttp.open("GET", "/adc", true);
            xhttp.send();
        }

        setInterval(updateChart, 5);
    </script>
    </head>
    <body>
    <div align="center">
    <h1>Add Surge</h1>
    <h2>Voltage & Current measurement</h2>
    Voltage Level : <strong id="adc_value">""" + response + """</strong>
    <p><a href="/?mode_change"><button class="button">Mode Change</button></a><br>
    </p>
    <div id="chart"></div>
    </div>
    </body>
    </html>
    """
    return html


def main():
    w5x00_init()
    s = socket()
    s.bind(('192.168.0.20', 80))
    s.listen(5)

    data = {
        'time': [],
        'value': []
    }
    MAX_DATA_POINTS = 100

    while True:
        conn, addr = s.accept()
        print('Connect from', str(addr))
        request = conn.recv(1024)
        request = str(request)
        led_on = request.find('/?led=on')
        led_off = request.find('/?led=off')
        adc_request = request.find('/adc')

        if led_on == 6:
            print("Voltage Mode")
            led.value(1)
        if led_off == 6:
            print("Current Mode")
            led.value(0)
        if adc_request >= 0:
            adc = ADC(Pin(28))
            adc_value = adc.read_u16()
            response = "{:.2f}".format(adc_value / 65535 * 3.3 * 2.4)

            data['time'].append(time.time())
            data['value'].append(response)

            if len(data['time']) > MAX_DATA_POINTS:
                data['time'] = data['time'][1:]
                data['value'] = data['value'][1:]

            json_data = ujson.dumps(data)

            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: application/json\n')
            conn.send('Content-Length: %d\n' % len(json_data))
            conn.send('\n')
            conn.send(json_data)
        else:
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Content-Length: %s\n\n' % len(response))
            conn.send(response)
        conn.close()

if __name__ == "__main__":
    main()

