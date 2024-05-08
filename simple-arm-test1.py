import m5
from m5.objects import *

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "2.0GHz"

# Create a Voltage Domain object
voltage_domain = VoltageDomain()
voltage_domain.voltage = "1.0V"  # Set the voltage value (in Volts)

# Assign the voltage domain to the clock domain
system.clk_domain.voltage_domain = voltage_domain

system.mem_mode = "atomic"
system.mem_ranges = [AddrRange("512MB")]
system.cpu = ArmAtomicSimpleCPU()

system.membus = SystemXBar()

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

system.cpu.createInterruptController()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    thispath,
    "/home/said/GEM5/ARM/gem5/fs_images/disks/workload/fabionnaci"
)

system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause()))

