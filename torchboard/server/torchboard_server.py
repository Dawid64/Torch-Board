import flask
from flask_cors import CORS, cross_origin

class TorchBoardServer():
    port:int
    host:str
    static_path:str
    state_history:dict[str, list] #?
    changes:dict[str, list]
    app:flask.Flask
    
    def __init__(self, port=8080, host='127.0.0.1', name='TorchBoard', static_path='static'):
        self.port = port
        self.host = host
        self.state_history = {}
        self.changes = {}
        self.app = flask.Flask(name)
        CORS(self.app, resources={r"/*": {"origins": "*"}}) #TODO: Change origins to specific domain

        @self.app.route('/')
        def index():
            return flask.send_from_directory('static', 'index.html')
        
        @self.app.route('/<path:path>')
        def static_proxy(path):
            return flask.send_from_directory('static', path)
        
        self.app.add_url_rule('/get_changes','get_changes', self.__flush_changes, methods=['GET'])
        
    @cross_origin()
    def __flush_changes(self):
        json = flask.jsonify(self.changes)
        self.changes = {}          
        return json,200

    def run(self):
        self.app.run(port=self.port, host=self.host)
        
    def set_variable(self, name, value):
        self.changes[name] = self.changes.get(name,[]) + [value]
        self.state_history[name] = self.state_history.get(name, []) + [value]
    
    def get_variable_history(self, name):
        return self.state_history[name] if name in self.state_history else None
    
    def set_variables(self, variables:dict):
        for key, value in variables.items():
            self.set_variable(key, value)
        
        
if __name__ == '__main__':
    server = TorchBoardServer(static_path='../../static')
    server.set_variables({'test': 1, 'test2': 2})
    server.run()