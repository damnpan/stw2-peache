from flask import Flask, render_template, request
from output.py import img_links, buy_links
# https://stackoverflow.com/questions/17255737/importing-variables-from-another-file

app = Flask(__name__)

# Home Page
@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == 'GET':
    image_links = img_links
    shop_links = buy_links
    return render_template('index.html', image_links=image_links, shop_links=shop_links)
  else:
    image_links = img_links
    shop_links = buy_links
    return render_template('index.html', image_links=image_links, shop_links=shop_links)    


@app.route('/bye')
def route():
  return render_template('thanks.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)






