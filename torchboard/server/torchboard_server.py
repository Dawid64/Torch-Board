import flask
from flask_cors import CORS, cross_origin
from flask_session import Session
from werkzeug.serving import make_server

import webbrowser

from threading import Thread

import os
from torchboard.server.utils import wipe_dir, transform_history_dict

from typing import Any, List
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class TorchBoardServer():
    port:int
    host:str
    static_path:str
    
    listener_state:dict[str, List[Any]]
    variable_state:dict[str, Any]
    
    app:flask.Flask
    
    def __init__(self, port:int=8080, host:str='127.0.0.1', name:str='TorchBoard', static_path:str='static', board:Any=None) -> None:
        self.port = port
        self.host = host
        self.static_path = static_path        
        
        self.variable_state = dict()
        
        self.app = flask.Flask(name)
        self.__flask_process = None
        
        self.app.config["SECRET_KEY"] = "duparomana123" #TODO: Change secret key
        self.app.config['SESSION_TYPE'] = 'filesystem'
        
        CORS(self.app, resources={r"/*": {"origins": "*"}}) #TODO: Change origins to specific domain
        Session(self.app)
        self.board = board

        @self.app.route('/')
        def index():
            return flask.send_from_directory(self.static_path, 'index.html')
        
        @self.app.route('/<path:path>')
        def static_proxy(path):
            return flask.send_from_directory(self.static_path, path)
        
        self.app.add_url_rule('/get_changes','get_changes', self.__get_changes_session, methods=['GET'])
        self.app.add_url_rule('/get_history','get_history', self.__get_history, methods=['GET'])
        self.app.add_url_rule('/get_variables','get_variables', self.__get_variables, methods=['GET'])
        self.app.add_url_rule('/update_variable','update_variable', self.__update_variable, methods=['PUT'])
        
        self.server = make_server(self.host, self.port, self.app, threaded=True)
        self.server.daemon_threads = True
        
    @cross_origin()
    def __get_changes_session(self) -> flask.Response:
        changes_list = self.board.history.get_since_last_change()
        return flask.jsonify(transform_history_dict(changes_list)),200

    @cross_origin()
    def __get_history(self) -> flask.Response:
        history_list = self.board.history.get_all()
        return flask.jsonify(transform_history_dict(history_list)),200
    
    @cross_origin()
    def __get_variables(self) -> flask.Response:
        return flask.jsonify({key:value for key,value in self.variable_state.items()}),200
    
    @cross_origin()
    def __update_variable(self) -> flask.Response:
        data = flask.request.json
        if any([key not in data for key in ['name','value']]):
            return flask.jsonify({'status': 'error', 'message': 'Invalid request'}),400
            
        name,value = data['name'],data['value']
        
        if not name in self.variable_state:
            return flask.jsonify({'status': 'error', 'message': f'Variable {name} not found'}),404
            
        self.update_changeable_value(name, value)
        return flask.jsonify({'status': 'success'}),200
    
    def start(self, start_browser=False) -> None:
        if self.__flask_process:
            return
        self.__flask_process = Thread(target=self.server.serve_forever)
        self.__flask_process.daemon = True
        self.__flask_process.start()
        
        if os.path.exists('flask_session'):
            wipe_dir('flask_session')
        
        if start_browser:
            webbrowser.open(f'http://{self.host}:{self.port}') #Force open browser to dashboard
    
    def stop(self) -> None:
        self.__flask_process.join()
        self.__flask_process = None     
        
    def register_changeable_value(self,name:str,default_value:Any) -> None:
        self.variable_state[name] = default_value
        
    def update_changeable_value(self,name:str,value:Any) -> None:
        self.variable_state[name] = value
        
    def get_changeable_value(self,name:str) -> Any | None:
        if name in self.variable_state:
            return self.variable_state[name]
        else:
            return None
    
    def get_changeable_values(self) -> dict[str, Any]:
        return {k:v for k,v in self.variable_state.items()}