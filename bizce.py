from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import random
import requests
import time

# IP izleme tablosu
ip_request_count = {}
REQUEST_LIMIT = 6
BLOCK_DURATION = 24 * 60 * 60  # 1 gün (saniye)
token = requests.get("https://raw.githubusercontent.com/hoqk4baz/ryuga/refs/heads/main/token.json").json()["token"]
class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')

        # İstek sayısını kontrol et
        current_time = time.time()
        if client_ip in ip_request_count:
            count, first_request_time = ip_request_count[client_ip]
            if count >= REQUEST_LIMIT and (current_time - first_request_time) < BLOCK_DURATION:
                self.send_response(429)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()

                error_page = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>who is RYUGA</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            min-height: 100vh;
                            margin: 0;
                            background: url('https://i.pinimg.com/736x/e6/f7/e8/e6f7e823c92d72aea836f3f6ffc30622.jpg') no-repeat center center fixed;
                            background-size: cover;
                        }}
                        h1 {{
                            color: #fff;
                            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
                        }}
                        .result-box {{
                            max-width: 90%;
                            width: auto;
                            padding: 15px;
                            background: rgba(255, 255, 255, 0.9);
                            border: 1px solid #ddd;
                            border-radius: 5px;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                            margin-top: 20px;
                            text-align: center;
                            word-wrap: break-word;
                        }}
                    </style>
                </head>
                <body>
                    <h1>who is RYUGA</h1>
                    <div class="result-box">
                        <strong>LİMİTLERİ AŞTIN</strong>
                        <p>Kanka bugünlük senin için bu kadar yeterli, fazlası zarar!</p>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(error_page.encode('utf-8'))
                return
            elif (current_time - first_request_time) >= BLOCK_DURATION:
                # Zaman aşımı olduğunda sayaç sıfırlanır
                ip_request_count[client_ip] = (1, current_time)
            else:
                ip_request_count[client_ip] = (count + 1, first_request_time)
        else:
            ip_request_count[client_ip] = (1, current_time)

        # API işlemleri ve HTML oluşturma işlemleri burada yer alacak
        try:
            # Rastgele MSISDN oluştur
            msisdn = str(random.randint(100000000, 999999999))  # 10 haneli rastgele sayı

            # API Request
            url = "https://api.dnatech.io/v1/Action/6709/IssueCode"
            url2 = "https://api.dnatech.io/v1/Action/4208/IssueCode"
            payload = {"Msisdn": "5" + msisdn}
            headers = {
                'User-Agent': user_agent,
                'Accept': "application/json",
                'Content-Type': "application/json",
                'authorization': token,
                'sec-fetch-site': "same-site",
                'accept-language': "tr-TR,tr;q=0.9",
                'sec-fetch-mode': "cors",
                'origin': "https://gnc.dnatech.io",
                'referer': "https://gnc.dnatech.io/",
                'sec-fetch-dest': "empty"
            }
            response = requests.post(url, json=payload, headers=headers)
            response2 = requests.post(url2, json=payload, headers=headers)
            if response.status_code and response2.status_code == 200:
                baslik = "YEMEK SEPETİ / CARİBOU"
                api_result = f"YEMEK SEPETİ 300/170: {response.json()['Data']['ReturnMessage']}"
                api_result2 = f"Caribou KAHVE: {response2.json()['Data']['ReturnMessage']}"
            elif response.status_code == 401:
                baslik = "TOKEN PATLADI"
                api_result = "SÜRE DOLDU ADMİNİN AÇMASI GEREKLİ"
                api_result2 = ""
            else:
                baslik = "HATA ADMİNE BİLDİRİN"
                api_result = f"Bir hata oluştu: {response.status_code}"
                api_result2 = ""

            # HTML Content
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>who is RYUGA</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        margin: 0;
                        background: url('https://i.pinimg.com/736x/e6/f7/e8/e6f7e823c92d72aea836f3f6ffc30622.jpg') no-repeat center center fixed;
                        background-size: cover;
                    }}
                    h1 {{
                        color: #fff;
                        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
                    }}
                    .result-box {{
                        max-width: 90%;
                        width: auto;
                        padding: 15px;
                        background: rgba(255, 255, 255, 0.9);
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin-top: 20px;
                        text-align: center;
                        word-wrap: break-word;
                    }}
                </style>
            </head>
            <body>
                <h1>who is RYUGA</h1>
                <h1>TG: @whoisryuga</h1>
                <div class="result-box">
                    <strong>{baslik}</strong>
                    <p>{api_result}</p>
                    <p>{api_result2}</p>
                </div>
            </body>
            </html>
            """

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Wow Denemeler Yapıyorsun anlaşılan :) ==> {e}".encode('utf-8'))


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """Çoklu iş parçacığı destekli HTTP Sunucusu"""
    pass


def run(server_class=ThreadingHTTPServer, handler_class=MyRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run(port=3169)
