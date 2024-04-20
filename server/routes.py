from flask import jsonify, request
from app import app, db
from models import Sweet, Vendor, VendorSweet

# GET /vendors
@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    vendors_list = [{'id': vendor.id, 'name': vendor.name} for vendor in vendors]
    return jsonify(vendors_list)

# GET /vendors/:id
@app.route('/vendors/<int:id>', methods=['GET'])
def get_vendor(id):
    vendor = Vendor.query.get(id)
    if vendor:
        vendor_data = {
            'id': vendor.id,
            'name': vendor.name,
            'vendor_sweets': [{
                'id': vs.id,
                'price': vs.price,
                'sweet': {'id': vs.sweet.id, 'name': vs.sweet.name},
                'sweet_id': vs.sweet_id,
                'vendor_id': vs.vendor_id
            } for vs in vendor.sweets]
        }
        return jsonify(vendor_data)
    else:
        return jsonify({'error': 'Vendor not found'}), 404

# GET /sweets
@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    sweets_list = [{'id': sweet.id, 'name': sweet.name} for sweet in sweets]
    return jsonify(sweets_list)

# GET /sweets/<int:id>
@app.route('/sweets/<int:id>', methods=['GET'])
def get_sweet(id):
    sweet = Sweet.query.get(id)
    if sweet:
        sweet_data = {'id': sweet.id, 'name': sweet.name}
        return jsonify(sweet_data)
    else:
        return jsonify({'error': 'Sweet not found'}), 404


# POST /vendor_sweets
@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.json

    price = data.get('price')
    sweet_id = data.get('sweet_id')
    vendor_id = data.get('vendor_id')

    if not price or not sweet_id or not vendor_id:
        return jsonify({'error': 'Missing required fields'}), 400

    sweet = Sweet.query.get(sweet_id)
    vendor = Vendor.query.get(vendor_id)

    if not sweet:
        return jsonify({'error': 'Sweet not found'}), 404

    if not vendor:
        return jsonify({'error': 'Vendor not found'}), 404

    vendor_sweet = VendorSweet(price=price, sweet_id=sweet_id, vendor_id=vendor_id)

    db.session.add(vendor_sweet)
    db.session.commit()

    return jsonify({
        'id': vendor_sweet.id,
        'price': vendor_sweet.price,
        'sweet_id': vendor_sweet.sweet_id,
        'vendor_id': vendor_sweet.vendor_id
    }), 201


# DELETE /vendor_sweets/<int:id>
@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def delete_vendor_sweet(id):
    # Check if the VendorSweet exists
    vendor_sweet = VendorSweet.query.get(id)
    if not vendor_sweet:
        return jsonify({'error': 'VendorSweet not found'}), 404

    # Delete the VendorSweet from the database session and commit the transaction
    db.session.delete(vendor_sweet)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'VendorSweet deleted successfully'}), 200
