import requests
from bs4 import BeautifulSoup
from flask import Flask, request
from flask_cors import CORS, cross_origin


# Set up FLASK with generous CORS permissions
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def resolve_urlString(yt_url):
  # Use requests to retrieve data from a given URL
  yt_response = requests.get(yt_url)

  # Parse the whole HTML page using BeautifulSoup
  yt_soup = BeautifulSoup(yt_response.text, 'html.parser')

  # Title of the parsed page
  # print(yt_soup.title.string)

  # Find all <script tags> from webpage
  data = yt_soup.find_all('script')
  id_found = False

  # Depending on the channel/webpage the Channel ID may be different.
  # Parse out Channel ID
  for count, value in enumerate(data):
    string_index = value.text.find('"externalId"')
    if string_index != -1 and id_found == False:
      id_found = True
      val = value.text[string_index:string_index+38].split(":")[1].strip('"')
      return 'https://www.youtube.com/playlist/?list=' + val[:1] + 'U' + val[2:]
    
  if id_found == False and id_found == False:
    for count, value in enumerate(data):
      string_index = value.text.find('"externalChannelId"')

      if string_index != -1:
        id_found = True
        val = value.text[string_index:string_index+46].split(":")[1].strip('"')
        return 'https://www.youtube.com/playlist/?list=' + val[:1] + 'U' + val[2:]

  if id_found == False:
    for count, value in enumerate(data):
      string_index = value.text.find('"browseId"')

      if string_index != -1 and id_found == False:
        id_found = True
        val = value.text[string_index:string_index+37].split(":")[1].strip('"')
        return 'https://www.youtube.com/playlist/?list=' + val[:1] + 'U' + val[2:]
  
  raise ValueError('URL NOT FOUND')


# Decently Robust set of test cases.
def tests():
  assert(resolve_urlString('https://www.youtube.com/watch?v=hkZEpNsw6zA')) == 'https://www.youtube.com/playlist/?list=UUw7SNYrYei7F5ttQO3o-rpA'
  assert(resolve_urlString('https://www.youtube.com/user/shadowbeatzinc/videos')) == 'https://www.youtube.com/playlist/?list=UUhzdk2cqwRe1zKP_y6BJx6w'
  assert(resolve_urlString('https://www.youtube.com/watch?v=K8XHmv3ok4Y&list=UUmuobr4DmrmLI1BaGZD3p5w&index=114')) == 'https://www.youtube.com/playlist/?list=UUmuobr4DmrmLI1BaGZD3p5w'
  assert(resolve_urlString('https://www.youtube.com/channel/UCw7SNYrYei7F5ttQO3o-rpA')) == 'https://www.youtube.com/playlist/?list=UUw7SNYrYei7F5ttQO3o-rpA'
  assert(resolve_urlString('https://m.youtube.com/jawed')) == 'https://www.youtube.com/playlist/?list=UU4QobU6STFB0P71PMvOGN5A'
  assert(resolve_urlString('https://www.youtube.com/playlist?list=PLaAVDbMg_XAr-xrZw7wJp1XDXY9HDS1vm')) == 'https://www.youtube.com/playlist/?list=UUFKDEp9si4RmHFWJW1vYsMA'
  assert(resolve_urlString('https://www.youtube.com/channel/UCSF_aFGIIIoWY30GVV19TKA')) == 'https://www.youtube.com/playlist/?list=UUSF_aFGIIIoWY30GVV19TKA'
  assert(resolve_urlString('https://www.youtube.com/channel/UCzAypSoOFKCZUts3ULtVT_g')) == 'https://www.youtube.com/playlist/?list=UUzAypSoOFKCZUts3ULtVT_g'
  assert(resolve_urlString('https://www.youtube.com/user/LoLChampSeries')) == 'https://www.youtube.com/playlist/?list=UUvqRdlKsE5Q8mf8YXbdIJLw'
  assert(resolve_urlString('https://www.youtube.com/channel/UCWWZjhmokTbezUQr1kbbEYQ')) == 'https://www.youtube.com/playlist/?list=UUWWZjhmokTbezUQr1kbbEYQ'
  assert(resolve_urlString('https://www.google.com')) == 'URL NOT FOUND'

# Default Route
@app.route("/")
@cross_origin()
def testFunction():
    try:
      res = resolve_urlString('https://www.youtube.com/watch?v=d3b2Lz2yh5c&list=UUrUlBg1aGGDFpIIFT7AISCA')
      return res
    except:
      return 'ERROR URL NOT FOUND'

# Route to grab Channel Playlist URL
@app.route("/grab", methods=['POST'])
@cross_origin()
def fetchFunction():
    try:
      resp = resolve_urlString(request.json['URL'])
      return resp
    except:
      return 'ERROR URL NOT FOUND'

# Comment this out if you don't want to run in debug mode/if you want to run on a server
if __name__ == '__main__':
    app.run(debug=True)