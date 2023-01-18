import machine
import neopixel
import uweb


led_strip = neopixel.NeoPixel(machine.Pin(13, machine.Pin.OUT), 120, bpp=4)


COLOR_MAP = (
    ('off', '#000', (0, 0, 0, 0)),
    ('red', '#e00', (150, 0, 0, 0)),
    ('yellow', '#ee0', (80, 50, 0, 5)),
    ('green', '#0e0', (0, 100, 0, 0)),
    ('cyan', '#0ee', (0, 70, 40, 0)),
    ('blue', '#00e', (0, 0, 60, 5)),
    ('pink', '#e0e', (100, 0, 40, 5)),
    ('white', '#eee', (30, 20, 0, 100)),
)


HTML = """<html>
    <head>
        <title>ESP Web Server</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,">
        <style>
            html {{
                font-family: Helvetica;
                display:inline-block;
                margin: 0px auto;
                text-align: center;
                background-color: #333;}}
            h1 {{
                color: #ddd;
                padding: 2vh;}}
            .button {{
                display: inline-block;
                background-color: #888;
                border: solid;
                border-color: #000;
                border-radius: 4px;
                color: #fff;
                padding: 16px 40px;
                text-decoration: none;
                font-size: 30px;
                margin: 2px;
                cursor: pointer;
                width: 40pt;
                height: 40pt;}}
            .selected {{border-color: #fff;}}
        </style>
    </head>
    <body>
        <h1>ESP32 LED</h1>
        <p>
{lines}
        </p>
    </body>
</html>"""


def send_response(client):
    current_color = led_strip[0]
    lines = ''
    for name, html_color, led_color  in COLOR_MAP:
        lines += f'            <a href="/{name}"><button class="button {" selected" if current_color == led_color else ""}" style="background-color: {html_color};"></button></a>\n'
    html = HTML.format(lines=lines)
    uweb.response(client, data=html)

def main():
    sock = uweb.web_server()

    while True:
        web_res = uweb.web_wait(sock)
        if web_res:
            client, addr, method, url, headers = web_res
            print(f'{addr[0]:s}:{addr[1]:d} {method:s} {url:s}')
            if method == 'GET':
                color = url.strip('/')
                for name, html_color, led_color in COLOR_MAP:
                    if color == name:
                        led_strip.fill(led_color)
                        led_strip.write()
                        uweb.response_redirect(client, '/')
                        break
                else:
                    send_response(client)

if __name__ == '__main__':
    main()