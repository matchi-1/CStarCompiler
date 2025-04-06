import eventlet
from flask_socketio import SocketIO

commands = [
    {"output": "just print this in frontend"},
    {"output": "just print this in frontend"},
    {"input": "this is a prompt, enter number 1: "},
    {"output": "just print this in frontend"},
    {"output": "just print this in frontend"},
    {"input": "Enter number 2: "}
]

class wait_flag_container:
    wait = False

def run_loop(socketio: SocketIO):
    user_response = {}

    def loop():
        for item in commands:
            if "input" in item:
                wait_flag_container.wait = True
                socketio.emit('request_input', {"prompt": item["input"]})

                while wait_flag_container.wait:
                    eventlet.sleep(0.1)

                print("User entered:", user_response["value"])

            elif "output" in item:
                socketio.emit('print_output', {"text": item["output"]})
                eventlet.sleep(0.1)

        socketio.emit("done", {"msg": "Done looping."})

    return loop, user_response, lambda: setattr(wait_flag_container, "wait", False)
