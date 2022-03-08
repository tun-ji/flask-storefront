from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
import models  # our custom defined models

#create a Blueprint variable named admin_page.
admin_page = Blueprint('admin_page', __name__, template_folder='templates/admin')

def logged_in():
    if 'username' not in session or 'admin' not in session['userroles']:
        return False
    else:
        return True


@admin_page.route("/admin/")
def admin():
    if not logged_in():
        return redirect(url_for('login', next='/admin/'))
    # username in session and user has admin role, continue
    return render_template('index.html', title="ADMIN", information="Here you can add new Products. Click on what you would like to do")


@admin_page.route("/admin/inventory/")
def inventory():
    if not logged_in():
        return redirect(url_for('login', next='/admin/inventory/'))

    # username in session, continue
    # get our registered products from the database
    produce = models.ProduceOluwatomilolaAdeniran.query.all()
    information = request.args.get('information', 'Here you can register new produce')
    css = request.args.get('css', 'normal')
    return render_template('inventory.html', title="Register Products", information=information, css=css,
                           produce=produce)


@admin_page.route("/admin/inventory/add-product/", methods=['POST','GET'])
def process_customer_add():
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session and admin role, continue

    if request.method != 'POST':
        # return to products-and-services.html page containing add form. Only POST method is allowed
        error = 'Please use the form to add new products'
        return render_template('inventory.html', title="REGISTER CUSTOMERS", information=error, css="error")

    # No problem so far, get the request object and the parameters sent from the form.
    Pname = request.form['Produce_Name']
    Pdesc = request.form['Produce_Description']
    URL = request.form['Photo_URL']
    WGT = request.form['Weight']
    PPU = request.form['price_per_unit']
    Qty = request.form['Quantity']

    # let's write to the database
    try:
        product = models.ProduceOluwatomilolaAdeniran(Produce_Name=Pname, Produce_Description=Pdesc, Photo_URL=URL,
                                                   Weight=WGT, price_per_unit=PPU, Quantity=Qty)
        models.db.session.add(product)
        models.db.session.commit()
    except Exception as e:
        error = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('inventory.html', title="REGISTER PRODUCT", information=error, css="error")
    # no error, continue
    return redirect(url_for('admin_page.inventory', information="Product Added!", css="success"))


@admin_page.route("/admin/inventory/edit/<int:id>/", methods=['POST', 'GET'])
def customers_edit(id):
    # check database for the product to edit
    product = models.ProduceOluwatomilolaAdeniran.query.filter_by(id=id).first()
    # send to the edit form
    return render_template('inventory-edit.html', produce=product)


@admin_page.route("/admin/inventory/process-inventory-edit/<int:id>/", methods=['POST', 'GET'])
def process_customer_edit(id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/inventory/'))
    # username in session and admin in role, continue
    if request.method != 'POST':
        # redirect to signup form. Only POST method is allowed
        error = 'Please use the form to edit customers'
        return render_template('inventory.html', title="REGISTER PRODUCE", information=error, css="error")
    # No problem so far, get the request object and the parameters sent.
    Pname = request.form['Produce_Name']
    Pdesc = request.form['Produce_Description']
    URL = request.form['Photo_URL']
    WGT = request.form['Weight']
    PPU = request.form['price_per_unit']
    Qty = request.form['Quantity']
    # let's update the database
    try:
        # Get the existing data from database as object
        product = models.ProduceOluwatomilolaAdeniran.query.filter_by(id=id).first()
        # Update the fields
        product.Produce_Name = Pname
        product.Produce_Description = Pdesc
        product.Photo_URL = URL
        product.Weight = WGT
        product.price_per_unit = PPU
        product.Quantity = Qty
        # commit
        models.db.session.commit()
    except Exception as e:
        error = 'Could not update produce. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.inventory', information="Update not successful", css="error"))
    return redirect(url_for('admin_page.inventory', information="Update successful", css="success"))


@admin_page.route("/admin/inventory/delete/<int:id>/", methods=['POST', 'GET'])
def customer_delete(id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/inventory/'))
        # username in session and admin role, continue
        # No problem so far
        # let's update the database
    try:
        # Get the existing data from database as object
        produce = models.ProduceOluwatomilolaAdeniran.query.filter_by(id=id).first()
        # Delete the record
        models.db.session.delete(produce)
        # commit
        models.db.session.commit()
    except Exception as e:
        error = 'Could not delete produce. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.inventory', information="Delete not successful", css="error"))
    return redirect(url_for('admin_page.inventory', information="Delete successful", css="success"))

