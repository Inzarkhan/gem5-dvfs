# Import the m5 (gem5) library created when gem5 is built
import m5
import os

# Import all of the SimObjects
from m5.objects import *

# Import TensorFlow for the machine learning workload
import tensorflow as tf
import numpy as np

# Define a simple machine learning workload
def matrix_multiply():
    a = tf.constant(np.random.rand(100, 100), name='a')
    b = tf.constant(np.random.rand(100, 100), name='b')
    c = tf.matmul(a, b, name='c')

    with tf.Session() as sess:
        result = sess.run(c)

    return result

# Run the simulation thrice
for i in range(3):
    print(f"Beginning simulation {i + 1}!")

    # Instantiate only on the first iteration
    if i == 0:
        # create the system we are going to simulate
        system = System()

        # Set the clock frequency of the system (and all of its children)
        system.clk_domain = SrcClockDomain(clock="1GHz", voltage_domain=VoltageDomain(voltage="1V"))

        # Set up the system
        system.mem_mode = "timing"  # Use timing accesses
        system.mem_ranges = [AddrRange("512MB")]  # Create an address range

        # Create a more advanced CPU model with DVFS support
        system.cpu = TimingSimpleCPU()
        system.cpu.clk_domain = SrcClockDomain(clock="1GHz", voltage_domain=VoltageDomain(voltage="1V"))

        # Specify the available frequency levels (in Hz)
        freq_levels = [1e9, 800e6, 600e6]
        system.cpu.clk_domain.setDVFSLevels(freq_levels)

        # Additional DVFS setup
        dvfs_controller = DVFSController()
        system.cpu.addDVFSController(dvfs_controller)

        # Create a memory bus, a system crossbar, in this case
        system.membus = SystemXBar()

        # Hook the CPU ports up to the membus
        system.cpu.icache_port = system.membus.cpu_side_ports
        system.cpu.dcache_port = system.membus.cpu_side_ports

        # create the interrupt controller for the CPU and connect to the membus
        system.cpu.createInterruptController()

        # Create a DDR3 memory controller and connect it to the membus
        system.mem_ctrl = MemCtrl()
        system.mem_ctrl.dram = DDR3_1600_8x8()
        system.mem_ctrl.dram.range = system.mem_ranges[0]
        system.mem_ctrl.port = system.membus.mem_side_ports

        # Connect the system up to the membus
        system.system_port = system.membus.cpu_side_ports

        # Load machine learning workload
        ml_binary = "ml_workload.py"
        ml_cmd = ["python", ml_binary]
        ml_process = Process()
        ml_process.cmd = ml_cmd
        system.cpu.workload = ml_process
        system.cpu.createThreads()

        # ...

    # Run gem5 simulation
    m5.instantiate()
    exit_event = m5.simulate()
    print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause()))

# Print a statement after 3 times of execution
print("Simulation completed 3 times.")
