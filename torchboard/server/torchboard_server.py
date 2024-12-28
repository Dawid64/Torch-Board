import flask
from flask_cors import CORS, cross_origin
from flask_session import Session

from multiprocessing import Process

import webbrowser

from torchboard.base.listener import Listener

from typing import Any, List
class TorchBoardServer():
    port:int
    host:str
    static_path:str
    listener_state:dict[str, Listener]
    changes:dict[str, list]
    app:flask.Flask
    
    def __init__(self, port:int=8080, host:str='127.0.0.1', name:str='TorchBoard', static_path:str='static') -> None:
        self.port = port
        self.host = host
        
        self.listener_state = {}
        
        self.app = flask.Flask(name)
        self.__flask_process = None
        
        self.app.config["SECRET_KEY"] = "duparomana123" #TODO: Change secret key
        self.app.config['SESSION_TYPE'] = 'filesystem'
        
        CORS(self.app, resources={r"/*": {"origins": "*"}}) #TODO: Change origins to specific domain
        Session(self.app)

        @self.app.route('/')
        def index():
            return flask.send_from_directory('static', 'index.html')
        
        @self.app.route('/<path:path>')
        def static_proxy(path):
            return flask.send_from_directory('static', path)
        
        self.app.add_url_rule('/get_changes','get_changes', self.__get_changes_session, methods=['GET'])
        self.app.add_url_rule('/get_history','get_history', self.__get_history, methods=['GET'])
        
    @cross_origin()
    def __get_changes_session(self) -> flask.Response:
        history_indexes = flask.session.get('history_indexes', dict())
        changes = dict()
        for key,listener in self.listener_state.items():
            idx = history_indexes.get(key, 0)
            updates = listener.history[idx:]
            if updates:
                changes[key] = updates
                history_indexes[key] = len(listener.history)
        flask.session['history_indexes'] = history_indexes
        return flask.jsonify(changes),200

    @cross_origin()
    def __get_history(self) -> flask.Response:
        ret = dict()
        for key in self.listener_state:
            ret[key] = self.listener_state[key].get_all()
            if not 'history_indexes' in flask.session:
                flask.session['history_indexes'] = dict()
            flask.session['history_indexes'][key] = len(self.listener_state[key].history)
        return flask.jsonify(ret),200

    def __run_flask(self) -> None:
        self.app.run(port=self.port, host=self.host)
    
    def run(self) -> None:
        if self.__flask_process:
            return
        self.__flask_process = Process(target=self.__run_flask, name=self.app.name) #Non blocking
        self.__flask_process.start()
        #webbrowser.open(f'http://{self.host}:{self.port}') #Force open browser to dashboard
    
    def stop(self) -> None:
        self.__flask_process.terminate()
        self.__flask_process.join()
        self.__flask_process = None
    
    def add_listener_variable(self, name:str, value:Any) -> None:
        if name not in self.listener_state:
            self.listener_state[name] = Listener()
        self.listener_state[name].add(value)
    
    def add_listener_variables(self, variables:dict[str, Any]) -> None:
        for key, value in variables.items():
            self.add_listener_variable(key, value)
    
    def get_listener_variable_history(self, name:str) -> List[Any] | None:
        if name in self.listener_state:
            return self.listener_state[name].get_all()
        else:
            return None        
    
        
        
if __name__ == '__main__':
    server = TorchBoardServer(static_path='../../static')
    server.add_listener_variables({'test': 1, 'test2': 2})
    server.run()