import sys
import os
from mhwp.mhwp_dashboard import openmhwpdashboard
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def openmhwp():
    openmhwpdashboard()