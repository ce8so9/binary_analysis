from miasm2.core.bin_stream                 import bin_stream_str
from miasm2.analysis.machine import Machine
from miasm2.jitter.csts import PAGE_READ, PAGE_WRITE

# Binary path and offset of the target function
offset = 0x660
fname = "out"

# Get Miasm's binary stream
bin_file = open(fname).read()
bin_stream = bin_stream_str(bin_file)

# Disassembling target func at offset
machine = Machine('x86_64')

# link the disasm engine to the bin_stream
mdis = machine.dis_engine(bin_stream)

# Disassemble basic blocks
blocs = mdis.dis_multibloc(offset)

#for b in blocs:
#    print b

# Initializing the Jit engine with a stack
jitter = machine.jitter(jit_type='python')
jitter.init_stack()

# Add the shellcode in an arbitrary memory location
run_addr = 0x400000
jitter.vm.add_memory_page(run_addr, PAGE_READ | PAGE_WRITE, bin_file)

# Trace registers values and mnemonics
jitter.jit.log_regs = True
jitter.jit.log_mn = True

def code_sentinelle(jitter):
    jitter.run = False
    jitter.pc = 0
    return True

jitter.push_uint64_t(0x1337beef)
# Add a breakpoint to special address 0x1337BEEF to stop emulation
jitter.add_breakpoint(0x1337beef, code_sentinelle)

# Initialize and starts the emulator
jitter.init_run(run_addr+offset)
jitter.continue_run()
