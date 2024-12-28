import flask
from flask_cors import CORS, cross_origin

from torchboard.base.listener import Listener

from typing import Any, List
class TorchBoardServer():
    port:int
    host:str
    static_path:str
    state_history:dict[str, Listener]
    changes:dict[str, list]
    app:flask.Flask
    
    def __init__(self, port:int=8080, host:str='127.0.0.1', name:str='TorchBoard', static_path:str='static') -> None:
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
    def __flush_changes(self) -> flask.Response:
        changes = dict()
        for key,listener in self.state_history.items():
            updates = listener.get()
            if updates:
                changes[key] = updates
        return flask.jsonify(changes),200

    def run(self) -> None:
        self.app.run(port=self.port, host=self.host)
        
    def add_variable(self, name:str, value:Any) -> None:
        if name not in self.state_history:
            self.state_history[name] = Listener()
        self.state_history[name].add(value)
    
    def add_variables(self, variables:dict[str, Any]) -> None:
        for key, value in variables.items():
            self.add_variable(key, value)
    
    def get_variable_history(self, name:str) -> List[Any] | None:
        if name in self.state_history:
            return self.state_history[name].get_all()
        else:
            return None
        
        
if __name__ == '__main__':
    server = TorchBoardServer(static_path='../../static')
    server.set_variables({'test': 1, 'test2': 2})
    server.run()