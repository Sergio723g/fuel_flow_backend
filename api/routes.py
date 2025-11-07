from flask import Blueprint, request, jsonify
from database import (
    get_pedidos, get_pedido_by_id, create_pedido, update_pedido,
    delete_pedido, cambiar_estado_pedido, get_estadisticas,
    buscar_pedidos, verificar_usuario
)

pedidos_bp = Blueprint('pedidos', __name__)
auth_bp = Blueprint('auth', __name__)

@pedidos_bp.route('/pedidos', methods=['GET'])
def obtener_pedidos():
    estado = request.args.get('estado')
    pedidos = get_pedidos(estado=estado)
    return jsonify(pedidos)

@pedidos_bp.route('/pedidos/estado/<estado>', methods=['GET'])
def obtener_pedidos_por_estado(estado):
    pedidos = get_pedidos(estado=estado)
    return jsonify(pedidos)

@pedidos_bp.route('/pedidos/<int:id>', methods=['GET'])
def obtener_pedido(id):
    pedido = get_pedido_by_id(id)
    if pedido:
        return jsonify(pedido)
    return jsonify({'error': 'Pedido no encontrado'}), 404

@pedidos_bp.route('/pedidos', methods=['POST'])
def crear_pedido():
    try:
        datos = request.json
        campos_requeridos = ['nombre_cliente', 'direccion', 'tipo_combustible', 'cantidad', 'telefono']
        for campo in campos_requeridos:
            if campo not in datos or not datos[campo]:
                return jsonify({'error': f'Campo {campo} es obligatorio'}), 400
        
        pedido = create_pedido(datos)
        if pedido:
            return jsonify(pedido), 201
        return jsonify({'error': 'Error al crear el pedido'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pedidos_bp.route('/pedidos/<int:id>', methods=['PUT'])
def actualizar_pedido(id):
    try:
        datos = request.json
        pedido = update_pedido(id, datos)
        if pedido:
            return jsonify(pedido)
        return jsonify({'error': 'Pedido no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@pedidos_bp.route('/pedidos/<int:id>', methods=['DELETE'])
def eliminar_pedido(id):
    if delete_pedido(id):
        return jsonify({'message': 'Pedido eliminado correctamente'})
    return jsonify({'error': 'Error al eliminar el pedido'}), 500

@pedidos_bp.route('/pedidos/<int:id>/estado', methods=['PATCH'])
def cambiar_estado(id):
    try:
        data = request.json
        nuevo_estado = data.get('estado')
        if not nuevo_estado:
            return jsonify({'error': 'El estado es requerido'}), 400
        
        pedido = cambiar_estado_pedido(id, nuevo_estado)
        if pedido:
            return jsonify(pedido)
        return jsonify({'error': 'Error al cambiar el estado'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@pedidos_bp.route('/pedidos/buscar', methods=['GET'])
def buscar():
    termino = request.args.get('q', '')
    if not termino:
        return jsonify([])
    pedidos = buscar_pedidos(termino)
    return jsonify(pedidos)

@pedidos_bp.route('/pedidos/estadisticas', methods=['GET'])
def estadisticas():
    stats = get_estadisticas()
    return jsonify(stats)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400
        
        usuario = verificar_usuario(username, password)
        if usuario:
            return jsonify({
                'token': 'simple-token-placeholder',
                'user': usuario
            })
        return jsonify({'error': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/auth/verify', methods=['GET'])
def verify():
    return jsonify({'valid': True})
