import connexion
from flask import request, jsonify
from Src.Logics.reference_service import reference_service

app = connexion.FlaskApp(__name__)
ref_service = reference_service()

@app.route("/api/accessibility", methods=['GET'])
def formats():
    return "SUCCESS"

@app.route("/api/<reference_type>/<string:item_id>", methods=['GET'])
def get_reference(reference_type, item_id):
    try:
        item = ref_service.get(reference_type, item_id)
        if item is None:
            return jsonify({"error": "Not found"}), 404
        return jsonify(item)
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@app.route("/api/<reference_type>", methods=['PUT'])
def add_reference(reference_type):
    try:
        data = request.json
        item = ref_service.add(reference_type, data)
        return jsonify(item), 201
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@app.route("/api/<reference_type>/<string:item_id>", methods=['PATCH'])
def update_reference(reference_type, item_id):
    try:
        data = request.json
        item = ref_service.update(reference_type, item_id, data)
        return jsonify(item)
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@app.route("/api/<reference_type>/<string:item_id>", methods=['DELETE'])
def delete_reference(reference_type, item_id):
    try:
        result = ref_service.delete(reference_type, item_id)
        return jsonify({"success": result})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
