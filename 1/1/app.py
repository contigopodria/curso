from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/hola')
def hello_word():
    return 'Hola mundo Flask'


@app.route('/test')
def hello_word2():
    return 'Hola mundo Flask test'


@app.route('/saludar')
@app.route('/saludar/<hi>')
@app.route('/saludar/<hi>/<lang>')
def saludar(hi='Andrés', lang='español'):
    return 'Hola mundo: '+hi+' '+lang


@app.route('/primer_html')
@app.route('/primer_html/<name>')
def primer_html(name='Andrés'):
    return '''
        <html>
            <body>
                <h1>Hola Flask</h1>
                <p>Hola %s</p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                    <li>Item 3</li>
                    <li>Item 4</li>
                </ul>
            </body>
        </html>
    ''' % name

@app.route('/static_file')
def static_file():
    #return "<img src='/static/img/Hola.png'>"
    return "<img src='"+url_for("static",filename="img/Hola.png")+"'>"

@app.route('/mi_primer_template')
@app.route('/mi_primer_template/<name>')
def mi_primer_template(name='Andrés'):
    return render_template('view.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
