# dvfs_controller.py
from m5.params import *
from m5.proxy import *
from m5.objects import *
from m5.util import addToPath

class DvfsController(SimObject):
    type = 'DvfsController'
    cxx_header = "learning_gem5/dvfs/dvfs_controller.hh"

    sys = Param.System(Parent.any, "System that the DVFS controller belongs to")
    cpu = Param.BaseCPU(Parent.any, "CPU to control")

    def startup(self):
        # Your initialization code goes here
        pass

    def adjust_frequency_voltage(self, new_freq, new_voltage):
        # Method to adjust the CPU frequency and voltage
        self.cpu.clk_domain.clock = new_freq
        # You may need to set the voltage using appropriate gem5 classes

    def set_dvfs_policy(self, policy):
        # Method to set the DVFS policy (e.g., performance, power saving)
        if policy == "performance":
            # Set parameters for performance-oriented policy
            self.adjust_frequency_voltage("3GHz", "high_voltage_level")
        elif policy == "power_saving":
            # Set parameters for power-saving policy
            self.adjust_frequency_voltage("1GHz", "low_voltage_level")
        else:
            # Handle unknown or default policy
            print(f"Unknown DVFS policy: {policy}. Defaulting to performance.")
            self.set_dvfs_policy("performance")

# Include in gem5 script
addToPath('/home/said/GEM5/ARM/gem5/configs/learning_gem5/part1/dvfs_controller.py')
from dvfs_controller import DvfsController
