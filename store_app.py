from flask import Flask, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "change_me"  # In production, use a secure secret key

PRODUCTS = [
    {"id": 1, "name": "Product 1", "price": 10.0},
    {"id": 2, "name": "Product 2", "price": 15.0},
    {"id": 3, "name": "Product 3", "price": 20.0},
]

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Store</title>
</head>
<body>
    <h1>Products</h1>
    <ul>
    {% for product in products %}
        <li>
            {{ product.name }} - ${{ "%.2f"|format(product.price) }}
            <a href='{{ url_for("add_to_cart", product_id=product.id) }}'>Add to cart</a>
        </li>
    {% endfor %}
    </ul>

    <h2>Your Cart</h2>
    {% if cart_items %}
        <ul>
        {% for item in cart_items %}
            <li>
                {{ item.name }} - {{ item.qty }} x ${{ "%.2f"|format(item.price) }}
                <a href='{{ url_for("remove_from_cart", product_id=item.id) }}'>Remove</a>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Your cart is empty.</p>
    {% endif %}
</body>
</html>
"""

def _find_product(pid):
    for prod in PRODUCTS:
        if prod["id"] == pid:
            return prod
    return None

@app.route('/')
def index():
    cart = session.get('cart', {})
    cart_items = []
    for pid, qty in cart.items():
        product = _find_product(int(pid))
        if product:
            cart_items.append({"id": product["id"], "name": product["name"], "price": product["price"], "qty": qty})
    return render_template_string(INDEX_TEMPLATE, products=PRODUCTS, cart_items=cart_items)

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
