from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/products/2')
def products2():
    data = open('static/products.txt', 'r').readlines()
    
    products_list = []
    id = 1;
    for line in data:
        products_list.append({'name': line.strip(), 'id': id})
        id = id + 1
    print(products_list)
    return render_template('products2.html', products=products_list)



if __name__ == '__main__':
    app.run(debug=True, port=5001)