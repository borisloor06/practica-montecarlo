from flask import Flask, request
from flask.templating import render_template
from calc.Montecarlo import Montecarlo

monte = Montecarlo()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/montecarlo')
def correccionMontecarlo():
    if request.method == 'GET':
        return render_template('montecarlo.html',
        data    = monte.probabilidadAuto(),
        data2    = monte.probabilidadDia(),
        data3    = monte.tablaProbabilidades()[0],
        data4    = monte.simulacion6(monte.tablaProbabilidades()[1]),
        data5    = monte.simulaciones(monte.tablaProbabilidades()[1]),
        data6    = monte.ganancia()[0],
        image    = monte.ganancia()[1],
        )

if __name__ == '__main__':
    app.run( host="0.0.0.0", port=3000,debug=True)
