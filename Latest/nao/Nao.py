import subprocess
class Nao():
    def __init__(self,ip,nao_folder_path = ".\\Nao\\"):
        self.ip = ip 
        self.setCommands(nao_folder_path)
    
    def setCommands(self,nao_folder_path):
        self.commands = {
            # this command need to concatenate a string with the posture
            "posture": "python " + nao_folder_path + "\\setPosture.py --ip " + str(self.ip) + " " + "--posture ",
            # this command need to concatenate a string with the text that nao will say
            "speak": "python " + nao_folder_path + " ",
        }

    def runCommands(self,command, args):
        instruction = "".join(str(self.commands[command]))
        for arg in args:
            instruction = instruction + ""
            instruction = instruction + arg
        process = subprocess.Popen(instruction.split(), stdout=subprocess.PIPE)

    def set_ip(self,ip):
        self.ip = ip
    
    def set_port(self,port):
        self.port = port









nao = Nao("192.168.43.12",".")

nao.runCommands("posture", ["Sit"])
