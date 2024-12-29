import flask
from flask_cors import CORS, cross_origin
from flask_session import Session
from werkzeug.serving import make_server
import secrets

import webbrowser

from threading import Thread

import os
from torchboard.server.utils import wipe_dir, transform_history_dict

from typing import Any, Iterable, List
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def type_mapping(value:Any) -> str:
    if isinstance(value, bool):
        return 'bool'
    elif isinstance(value, int):
        return 'int'
    elif isinstance(value, float):
        return 'float'
    elif isinstance(value, Iterable):
        if isinstance(value[0], int):
            return 'list_int'
        elif isinstance(value[0], float):
            return 'list_float'
        else:
            return 'list'
    else:
        return 'unknown'

class TorchBoardServer():
    port:int
    host:str
    static_path:str

    variable_state:dict[str, Any]

    app:flask.Flask
    
    def __init__(self, port:int=8080, host:str='127.0.0.1', name:str='TorchBoard', static_path:str='torchboard/dist', board:Any=None) -> None:
        static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')
        from torchboard.base.board import Board
        self.port = port
        self.host = host
        self.static_path = static_path        
        
        self.board: Board = board
        self.variable_state = dict()
        
        self.app = flask.Flask(name)
        self.__flask_process = None
        
        self.app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
        self.app.config['SESSION_TYPE'] = 'filesystem'

        CORS(self.app, resources={r"/*": {"origins": "*"}}) #TODO: Change origins to specific domain
        Session(self.app)

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
        self.app.add_url_rule('/do_action','do_action', self.__do_action, methods=['POST'])
        
        self.server = make_server(self.host, self.port, self.app, threaded=True)
        self.server.daemon_threads = True
    
    
    def start(self, start_browser=False) -> None:
        if self.__flask_process:
            return
        self.__flask_process = Thread(target=self.server.serve_forever)
        self.__flask_process.daemon = True
        self.__flask_process.start()
        
        if os.path.exists('flask_session'):
            wipe_dir('flask_session')
        
        print(f'Started TorchBoard server at http://{self.host}:{self.port}')
        if start_browser:
            webbrowser.open(f'http://{self.host}:{self.port}') #Force open browser to dashboard
    
    def stop(self) -> None:
        self.__flask_process.join()
        self.__flask_process = None
    
    @cross_origin()
    def __get_changes_session(self) -> flask.Response:
        return flask.jsonify(self.board.history.get_since_last_change()),200

    @cross_origin()
    def __get_history(self) -> flask.Response:
        history = self.board.history.get_all()
        return flask.jsonify(history), 200
    
    @cross_origin()
    def __get_variables(self) -> flask.Response:
        variables = [{'name':key,'value':value,'type':type_mapping(value)}
         for key, value in self.board.optim_operator.get_current_parameters().items()]
        return flask.jsonify(variables),200
    
    @cross_origin()
    def __update_variable(self) -> flask.Response:
        data = flask.request.json
        if 'name' not in data or 'value' not in data:
            return flask.jsonify({'status': 'error', 'message': 'Invalid request'}),400
            
        name,value = data['name'],data['value']
        
        # if not name in self.variable_state:
        #     return flask.jsonify({'status': 'error', 'message': f'Variable {name} not found'}),404
        
        self.board.optim_operator.update_parameters(name, value)
        
        return flask.jsonify({'status': 'success'}),200
    
    @cross_origin()
    def __do_action(self) -> None:
        data = flask.request.json
        if any([key not in data for key in ['action']]):
            return flask.jsonify({'status': 'error', 'message': 'Invalid request'}),400
        
        action = data['action']
        match action:
            case 'toggle_training':
                
                self.board.toggle_training()
                return flask.jsonify({'status': 'success'}),200
            case 'save_model':
                self.board.save_model()
                return flask.jsonify({'status': 'success'}),200
            case _:
                return flask.jsonify({'status': 'error', 'message': 'Invalid action'}),400
    
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