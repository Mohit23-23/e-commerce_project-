from flask import Flask, render_template, request
from threading import Thread
from main import AmazonPriceTracker,FlipkartPriceTracker,MultipleStorePriceTracker
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prices.db'
db = SQLAlchemy(app)

class TrackedPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    timestamp = db.Column(db.String(20))
    platform = db.Column(db.String(20))
    price = db.Column(db.Integer)

@app.route('/tracked_prices')
def tracked_prices():
    tracked_data = TrackedPrice.query.all()
    return render_template('tracked_prices.html', tracked_data=tracked_data)




app = Flask(__name__,template_folder='template' )

# ... (existing code)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    try:
        product_name = request.form['product_name']
        product_url = request.form['product_url']
        desired_price = int(request.form['desired_price'])
        track_option = request.form['track_option']

        if track_option == 'amazon':
            azt = AmazonPriceTracker(product_name, product_url, desired_price)
            t = Thread(target=azt.run)
            t.start()
        elif track_option == 'flipkart':
            fkt = FlipkartPriceTracker(product_name, product_url, desired_price)
            t = Thread(target=fkt.run)
            t.start()
        elif track_option == 'both':
            azurl = request.form['amazon_url']
            fkturl = request.form['flipkart_url']
            mspt = MultipleStorePriceTracker(product_name, azurl, fkturl, desired_price)
            t = Thread(target=mspt.track_multiple)
            t.start()

        return render_template('tracking_started.html')

    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
