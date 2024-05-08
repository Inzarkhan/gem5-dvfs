# Copyright (c) 2015 Jason Power
# (License information remains unchanged)

import m5
import os
from m5.objects import *

# Function to create a CPU with varying voltage and frequency
def create_cpu(freq, voltage):
    cpu = ArmTimingSimpleCPU()
    cpu.clk_domain = SrcClockDomain()
    cpu.clk_domain.clock = f"{freq}GHz"
    cpu.clk_domain.voltage_domain = VoltageDomain(voltage=f"{voltage}V")
    return cpu

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]
system.membus = SystemXBar()

# Create multiple instances of ArmTimingSimpleCPU with different frequencies and voltages
cpu_2GHz = create_cpu(2.0, 1.5)
cpu_2_5GHz = create_cpu(2.5, 2.0)
cpu_3GHz = create_cpu(3.0, 3.0)

# Connect CPUs to the system crossbar
system.cpu_2GHz = cpu_2GHz
system.cpu_2_5GHz = cpu_2_5GHz
system.cpu_3GHz = cpu_3GHz

system.cpu_2GHz.icache_port = system.membus.cpu_side_ports
system.cpu_2GHz.dcache_port = system.membus.cpu_side_ports
system.cpu_2_5GHz.icache_port = system.membus.cpu_side_ports
system.cpu_2_5GHz.dcache_port = system.membus.cpu_side_ports
system.cpu_3GHz.icache_port = system.membus.cpu_side_ports
system.cpu_3GHz.dcache_port = system.membus.cpu_side_ports

system.cpu_2GHz.createInterruptController()
system.cpu_2_5GHz.createInterruptController()
system.cpu_3GHz.createInterruptController()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# Specify the path to the ARM Linux program
thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    thispath,
    "../../../",
    "tests/test-progs/hello/bin/arm/linux/hello",
)

# Workload configuration
system.workload = SEWorkload.init_compatible(binary)

# Process configuration
process = Process()
process.cmd = [binary]

# Assign workloads to CPUs
system.cpu_2GHz.workload = process
system.cpu_2_5GHz.workload = process
system.cpu_3GHz.workload = process

# Create threads for each CPU
system.cpu_2GHz.createThreads()
system.cpu_2_5GHz.createThreads()
system.cpu_3GHz.createThreads()

# Root and instantiation
root = Root(full_system=False, system=system)
m5.instantiate()

# Run simulations with different CPUs
for i, cpu in enumerate([system.cpu_2GHz, system.cpu_2_5GHz, system.cpu_3GHz]):
    print(f"Beginning simulation {i + 1} with {cpu.clk_domain.clock} and {cpu.clk_domain.voltage_domain.voltage}!")

    # Assign the current CPU to the system
    system.cpu = cpu

    exit_event = m5.simulate()
    print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")

# Print a statement after all simulations
print("All simulations completed.")
