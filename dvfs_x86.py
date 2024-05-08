import os
from m5.objects import *

system = System()

# Create a DVFS handler
dvfs_handler = DVFSHandler()

# Create a voltage domain
voltage_domain = VoltageDomain()
voltage_domain.voltage = "1.0V"

# Associate the voltage domain with the DVFS handler
dvfs_handler.domains = [voltage_domain]

# Assign the DVFS handler to the system
system.dvfs_handler = dvfs_handler

# Create a clock domain and associate it with the voltage domain
system.clk_domain = SrcClockDomain(
    voltage_domain=voltage_domain,
    init_perf_level=2,  # Set the initial performance level (2GHz)
    frequencies=[
        Frequency(1000, "1GHz"),
        Frequency(1500, "1.5GHz"),
        Frequency(2000, "2GHz"),
    ]
)
system.clk_domain.clock = "2.0GHz"

system.mem_mode = "atomic"
system.mem_ranges = [AddrRange("512MB")]
system.cpu = X86AtomicSimpleCPU()

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
    "/home/said/GEM5/ARM/gem5/fs_images/disks/workload/x86_workloads/dist/fabinnaci"
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