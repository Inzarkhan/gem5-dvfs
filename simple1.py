# import the m5 (gem5) library created when gem5 is built
import m5
import os

# import all of the SimObjects
from m5.objects import *

debugflags = ["-c", "1", "-b", "4", "--debug-flags=syscalls"]
# Run the simulation thrice
for i in range(100):
    print(f"Beginning simulation {i + 1}!")

    # Instantiate only on the first iteration
    if i == 0:
        # create the system we are going to simulate
        system = System()
            # 
        # Set the clock frequency of the system (and all of its children)
        system.clk_domain = SrcClockDomain()
        system.clk_domain.clock = "2500MHz"
        system.clk_domain.voltage_domain = VoltageDomain()

        # Set up the system
        system.mem_mode = "timing"  # Use timing accesses
        system.mem_ranges = [AddrRange("512MB")]  # Create an address range

        # Create a simple CPU
        system.cpu = ArmTimingSimpleCPU()

        # Create a memory bus, a system crossbar, in this case
        system.membus = SystemXBar()

        # Hook the CPU ports up to the membus
        system.cpu.icache_port = system.membus.cpu_side_ports
        system.cpu.dcache_port = system.membus.cpu_side_ports

        # create the interrupt controller for the CPU and connect to the membus
        system.cpu.createInterruptController()

        # For X86 only we make sure the interrupts care connect to memory.
        # Note: these are directly connected to the memory bus and are not cached.
        # For other ISA you should remove the following three lines.
        #system.cpu.interrupts[0].pio = system.membus.mem_side_ports
        #system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
        #system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

        # Create a DDR3 memory controller and connect it to the membus
        system.mem_ctrl = MemCtrl()
        system.mem_ctrl.dram = DDR3_1600_8x8()
        system.mem_ctrl.dram.range = system.mem_ranges[0]
        system.mem_ctrl.port = system.membus.mem_side_ports

        # Connect the system up to the membus
        system.system_port = system.membus.cpu_side_ports

        # Here we set the ARM "matrix" binary path.
        thispath = os.path.dirname(os.path.realpath(__file__))
        # binary = os.path.join(thispath, "/home/said/GEM5/ARM/gem5/fs_images/disks/workload/fabionnaci")
        binary = os.path.join(thispath, "/home/said/GEM5/ARM/gem5/fs_images/disks/workload/fabionnaci")
        system.workload = SEWorkload.init_compatible(binary)

        # Create a process for a simple "Hello World" application
        process = Process()
        # Set the command
        # cmd is a list which begins with the executable (like argv)
        process.cmd = [binary]
        # Set the cpu to use the process as its workload and create thread contexts
        system.cpu.workload = process
        system.cpu.createThreads()

        # set up the root SimObject
        root = Root(full_system=False, system=system)

        # instantiate all of the objects we've created above
        m5.instantiate()

        exit_event = m5.simulate()
        print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause()))
        # Reset the CPU state for the next iterations
        system.cpu = ArmTimingSimpleCPU()
        system.cpu.createThreads()

# Print a statement after 3 times of execution
print("Simulation completed 100 times.")