import os
import json
import argparse
import numexpr as ne
import datetime

class Calculator():
    def __init__(self, context_path, username):
        self.context_path = context_path
        self.context = {"history": []}
        self.username = username
    
    def load_context(self):
        if not os.path.exists(self.context_path):
            print(f"The context file doesn't exist. Generating one: {self.context_path}")
            with open(self.context_path, mode="w") as r:
                json.dump(self.context, r)
        else:
            try:
                with open(self.context_path, mode="r") as r:
                    self.context = json.load(r)
            except Exception as e:
                print(f"Error: {e}. The file {self.context_path} isn't a json file or it's corupted")
        print("Context loaded")
        return self.context
    
    def write_context(self, v=False): # v is for verbose
        with open(self.context_path, mode="w") as r:
            json.dump(self.context, r)
        if v:
            print(f"Context writed in {self.context_path}")
    
    def execute_command(self, command):
        match command:
            case "help" | "h":
                print('You can write a calculation here. Furthermore, you can also write these command: ')
                print("help: show this help")
                print("history: show your history")
                print("clear: clear the history")
                print("save: save the context(history) in the context path")
                print("quit: save and quit the program")
            case "quit":
                self.write_context()
                print(f"See you soon, {self.username}")
                exit()
            case "clear":
                self.context["history"] = []
                print("History cleared")
            case "save":
                self.write_context(v=True)
            case "history":
                for element in self.context["history"]:
                    try: 
                        print(f"Calculated: {element['calculation']}, with result {element['result']}. By user {element['user']} at {element['datetime']}")
                    except Exception as e:
                        print(f"Error: {e}. There may be a flaw in the history.")
                if not self.context["history"]:
                    print("History is empty :(")
            case _:
                self._compute_calculation(command)
    
    def _compute_calculation(self, calculation):
        try:
            result = ne.evaluate(calculation)
        except Exception as e:
            print(f"Error. Your calculation is maybe malformed? Please retry. Error code: {e}")
            return "Error"
        self.context["history"].append({"calculation": calculation, "result": str(result), "user": self.username, "datetime": str(datetime.datetime.now().isoformat())})
        print(result)

if __name__=="__main__":
    parser = argparse.ArgumentParser("A simple interactive calculator with history")
    parser.add_argument("--context-file", "-c", default="context.json", help="Path of the json context file")
    parser.add_argument("--username", "-u", default=os.getlogin(), help="Your username. By default, the session's username")
    args = parser.parse_args()
    
    context_path = args.context_file
    USERNAME = args.username
    
    calculator = Calculator(context_path=context_path, username=USERNAME)
    calculator.load_context()
    
    print(f"Welcome in your caclulator, dear {USERNAME}")
    print('You can type "help" to get the help')
    
    while True:
        command = input(">>> ")
        calculator.execute_command(command)