import eventlet
from flask_socketio import SocketIO

commands = [
    # {"output": "sample output 1"},
    # {"output": "hello  this is cecilia agatha tolentino the cecestr cat"},
    # {"input": "this is a prompt, enter number 1: "},
    # {"output": "cece again"},
    # {"output": "i ate sock"},
    # {"input": "Enter number how many cats u like (1 and its cece): "},
    # {"output": "i ate sock"},
]

class wait_flag_container:
    wait = False
    

def run_loop(socketio: SocketIO):
    user_response = {}

    def loop():
        for item in commands:
            if "input" in item:
                wait_flag_container.wait = True
                socketio.emit('request_input', { "type": "input_request", "prompt": item["input"] })

                while wait_flag_container.wait:
                    eventlet.sleep(0.1)

                print("User entered:", user_response["value"])

            elif "output" in item:
                socketio.emit('print_output', { "type": "output", "value": item["output"] })

        socketio.emit("done", { "type": "output", "value": "[Loop Finished]" })

    return loop, user_response, lambda: setattr(wait_flag_container, "wait", False)
