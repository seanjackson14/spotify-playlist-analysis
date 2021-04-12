from flask import Flask, render_template
from io import BytesIO
import base64
from Code.code import mostPopularArtists,explicitPct,favAlbums,mostPopularYears,longestAndShortest

app = Flask(__name__)

import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('agg')

@app.route('/')
def mostPopArtists():

    img = BytesIO()
    mostPopularArtists()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('home.html',plot_url=plot_url,artists=mostPopularArtists())

@app.route('/favalbums')
def popAlbums():
    img = BytesIO()
    favAlbums()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('favalbums.html', plot_url=plot_url,albums=favAlbums())

@app.route('/mostcommonyears')
def yrs():
    img = BytesIO()
    mostPopularYears()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('commonyears.html', plot_url=plot_url,years=mostPopularYears())

@app.route('/explicit')

def explicit():
    img = BytesIO()
    explicitPct()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('explicit.html', plot_url=plot_url,exp=explicitPct())

@app.route('/longestandshortest')
def longandshort():
    return render_template('longshort.html',longshort=longestAndShortest())

@app.route('/about')
def about():
    return render_template('about.html',title='ABOUT')

if __name__ == "__main__":
    app.run(debug=True)