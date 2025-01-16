import {io,Socket} from "socket.io-client";
import StoreValue from "./StoreValue";

//Helper function. Sets key and triggers reactivity
import { setMapKey } from "./StoreValue";

export interface ServerToClientMessage {
    chartValueUpdate: (variable:{key:string,values:number[]}) => void;
    boardValueUpdate: (data:{key:string, values: number | boolean | string}) => void;
    getOptimizerVariables: (variables:[{name:string,value: number | boolean | number[],type:OptimizerVariableType}]) => void;
}

export interface ClientToServerMessage {
    optimizerValueUpdate: (key:string,value: number) => void;
    actionTrigger: (key:string,args:any) => void;
}

export enum ActionType {
    "toggle_training",
    "save_model",
}

enum OptimizerVariableType {
    "int",
    "float",
    "bool",
    "list_int",
    "list_float",
    "list"
}

class SocketHandler {
    private socket: Socket<ServerToClientMessage,ClientToServerMessage> ;

    constructor(connectionUrl: string) {
        this.socket = io(connectionUrl,{
            autoConnect: false,
            withCredentials: true,
        });
    }

    public connect() {
        this.socket.connect();
    }

    public disconnect() {
        this.socket.disconnect();
    }

    public onConnect(callback: () => void) {
        this.socket.on("connect", callback);
    }

    public onDisconnect(callback: () => void) {
        this.socket.on("disconnect", callback);
    }

    public onChartValueUpdate(callback: (variable:{key:string,values:number[]}) => void) {
        this.socket.on("chartValueUpdate", callback);
    }

    public onBoardValueUpdate(callback: (data:{key:string, values: number | boolean | string}) => void) {
        this.socket.on("boardValueUpdate", callback);
    }

    public onGetOptimizerVariables(callback: (variables:[{name:string,value: number | boolean | number[],type:OptimizerVariableType}]) => void) {
        this.socket.on("getOptimizerVariables", callback);
    }

    public emitOptimizerValueUpdate(key:string,value: number) {
        this.socket.emit("optimizerValueUpdate", key, value);
    }

    public emitActionTrigger(key:string,args:any) {
        this.socket.emit("actionTrigger", key, args);
    }
}

export class ServerState{
    private socketHandler: SocketHandler;

    //These are StoreValues so that the UI can subscribe to them and be reactive
    private __chartValues:StoreValue<Map<string, number[]>> = new StoreValue(new Map());
    private __boardValues:StoreValue<Map<string, string | boolean | number>> = new StoreValue(new Map());
    private __optimizerVariables:StoreValue<Map<string,number | boolean | number[]>> = new StoreValue(new Map());
    
    constructor(connectionUrl: string) {
        this.socketHandler = new SocketHandler(connectionUrl);
        setMapKey(this.__boardValues, "connected", false);

        this.socketHandler.onConnect(() => {
            setMapKey(this.__boardValues, "connected", true);
        });
        this.socketHandler.onDisconnect(() => {
            setMapKey(this.__boardValues, "connected", false);
        });

        this.socketHandler.onChartValueUpdate((variable:{key:string,values:number[]}) => {
            this.onChartValueUpdate(variable.key,variable.values);
        });

        this.socketHandler.onBoardValueUpdate((data:{key:string, values: number | boolean | string}) => {
            this.onBoardValueUpdate(data.key,data.values);
        });
        this.socketHandler.onGetOptimizerVariables((variables) => {
            this.onGetOptimizerVariables(variables);
        });

        this.socketHandler.connect();
    }

    get chartValues(): StoreValue<Map<string, number[]>> {
        return this.__chartValues;
    }

    get boardValues(): StoreValue<Map<string, string | boolean | number>> {
        return this.__boardValues;
    }

    get optimizerVariables(): StoreValue<Map<string,number | boolean | number[]>> {
        return this.__optimizerVariables;
    }

    private onChartValueUpdate(key:string, values:number[]) {
        if (!this.__chartValues.value.has(key)) {
            setMapKey(this.__chartValues,key,values);
        }
        else {
            const prev_values = this.__chartValues.value.get(key);
            if (prev_values === undefined) {
                console.error("Undefined values");
                return;
            }
            if (typeof prev_values[0] === typeof values[0]) {
                switch (typeof prev_values[0]) {
                    case "number":
                        setMapKey(this.__chartValues,key,prev_values.concat(values));
                        break;
                    default:
                        console.error("Type mismatch in values");
                }
            }
            else {
                console.error("Type mismatch in values");
            }
        }
    }

    private onGetOptimizerVariables(variables:[{name:string,value: number | boolean | number[],type:OptimizerVariableType}]) {
        this.__optimizerVariables.value = new Map();
        for (const variable of variables) {
            setMapKey(this.__optimizerVariables,variable.name,variable.value);
        }
    }

    private onBoardValueUpdate(key:string, value: string | boolean | number) {
        setMapKey(this.__boardValues,key,value);
    }

    public getBoardValue(key:string) {
        return this.__boardValues.value.get(key);
    }   

    public chartKeys() {
        return Array.from(this.__chartValues.value.keys());
    }

    public getChartValueHistory(key:string) {
        return this.__chartValues.value.get(key);
    }

    public updateOptimizerValue(key:string,value: number) {
        this.socketHandler.emitOptimizerValueUpdate(key,value);
    }

    public triggerAction(key:string,args:any) {
        this.socketHandler.emitActionTrigger(key,args);
    }
}