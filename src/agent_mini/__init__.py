
import os
import sys 

agent_path= os.path.abspath(os.path.join(os.path.dirname(__file__),"../../Agent"))
if agent_path not in sys.path:
    sys.path.insert(0, agent_path)

from main import main as start_agent
def main():
    start_agent()
