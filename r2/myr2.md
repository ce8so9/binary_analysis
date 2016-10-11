# Basic Commands

## r2 command line options
```
-h # get help message
-a <arch> # specify architecture (RAsm Plugin name)
-b <bits> # specify 8, 16, 32, 64 register size in bits
-c <cmd> # run command
-d <bin> # start debugging
-i <script> # include/interpret script
-n # do not load rbin info
-L # list io plugins
```

## In the shell
Syntax of the commands:
> [repeat][command] [args] [@ tmpseek] [; ...] [# comment]
> 3x # perform 3 hexdumps
> pd 3 @ entry0 # disasm 3 instructions at entrypoint
> x@rsp;pd@rip # show stack and code


## Printing Bytes
R2 is an block-based hexadecimal editor. Change the block
size with the ‘b’ command.
p8 print hexpairs
px print hexdump
pxw/pxq dword/qword dump
pxr print references
pxe emojis

## Structures
pf - define function signatures
Can load include files with the t command.
010 templates can be loaded using 010 python script.
Load the bin with r2 -nn to load the struct/headers
definitions of the target bin file.
Use pxa to visualize them in colorized hexdump.

# Disassembling and printing bytes

## rasm2
Disassembling and assembling code can be done with pa/pad or
using the rasm2 commandline tool.
$ rasm2 -L
$ rasm2 -a x86 -b 64 nop

## Disassembling Code
There are different commands to get the instructions at a
specific address.
pd/pD disassemble N bytes/instructions.
pi/pI just print the instructions
pid print address, bytes and instruction
pad disassemble given hexpairs
pa assemble instruction

> e asm.emu=true emulates the code with esil and
> agv/agf. render ascii art or graphviz graph
Seek History
s- (undo)
s+ (redo)
Use u and U keys to go back/forward in the visual seek
history.

## Patching Code

The ‘w’ command allows us to write stuff:

* Open with r2 -w (by default is readonly except debugger)
* VA/PA translations are transparent
* Sometimes we will need to use r2 -nw to patch headers
* The w command also allows to write assembly
* Wx in hexpairs
* wxf

## Dumping and Restoring

Dump to file
> pr 1K > file
> wt file 1K
> y 1K
Restoring
> wf file @ dst
> yy @ dst
Copy
> yt 1K @ dst

# Decompilation

## Better disassembly

There are other disassembler modes in r2.
> e asm.emustr=true
> e asm.pseudo=true
> pds : summary
> pdc : decompil incomplete

```
aa/aac/af
#!pipe retdec
```

# User Interface

## Colors

> e scr.color=true
> e scr.rgb=true
> e scr.truecolor=true
> e scr.utf8=true
> ecr # Random colors
> eco X # Color palette
> VE # visual color theme editor

## Visual Mode

Type V and then change the view with ‘p’ and ‘P’
Visual Panels : Press ‘!’ in the Visual mode # NICE

### Visualization
* Toggle Colors (C)
* Highlight stuff with (/)
* Setting new commands on top and right with = and |
* <space> toggle between graph and disasm

### Navigation
* Cursor Mode (Vc)
* HUD (V_)
* Resize Hexdump with []
* Add comments (;)
* Undo/Redo seek (u/U)
* Find next/prev hit/func/.. With n/N
* Basic Block Graphs

### Debugger integration
* Seek to PC (.)
* Step (s) or StepOver (S)
* Set breakpoints with ‘b’
* Change stack settings
*
### Editing stuff

* Bit Editor (Vd1)
* Increment/Decrement bytes (Cursor + +/- keys)
* Select ranges bytes to copy/paste
* Define flags
* Interactive writes
** A : rewrite assembly in place
** I : insert hex/ascii stuff

## Web User Interface

Start the webserver with =h
Launch the browser with =H
See /m /p /t and /enyo

# Binary Info (parsing file formats)

## RBin Information

$ rabin2 -s
> is
> fs symbols;f
Symbols Relocs Classes Entrypoints
Imports Strings Demangling Exports
Sections Libraries SourceLines ExtraInfo

All this info can be exported in JSON by appending a ‘j’.
$ r2 -nn /bin/ls
> e scr.hexflags=9999
> pxa

## Sections

Some of them are mapped and some others don’t. Executables
use to provide the information duplicated. One simplified
for the loader and another for analysis, exposing dwarf
information, annotations, etc
> iS
> .iS*
> S=
> S-*

## Hashing Sections

Rahash2 allows us to compute a variety of checksums to a
portion of a file, a full file or by blocks.
$ rahash2 -a md5 -s “hello world”
$ rahash2 -a all /bin/ls
$ rabin2 -SK md5 /bin/ls
$ rahash2 -L
* Also supports encryption/decryption
* As well as encoding/decoding

## Entropy

The entropy is computed by the amount of different values in
a specific block of data.

* Low entropy = plain/text
* Middle entropy = code
* High entropy = compressed / encrypted

There are other methods to identify
* p=e
* p=p
* p=0

## Strings

So we have different commands depending on that:
$ rabin2 -z # strings from .rodata (default in r2)
$ rabin2 -zz # strings in full file
$ rabin2 -zzz # dont map once, useful for huge files like 1TB
Radare2 will load the strings by default, which is sometimes not
desired, see the following vars:
> e bin.strings=false
> e bin.maxstrbuf=32M

# Scripting - Automation

## Using R2Pipe For Automation

R2 provides a very basic interface to use it based on the cmd()
api call which accepts a string with the command and returns the
output string.
$ pip install r2pipe
$ r2 -qi names.py /bin/ls
$ cat names.py

# Analyzing Code

## Analyzing From The Metal

R2 provides tools for analyzing code at different levels.
* ae emulates the instruction (microinstructions)
* ao provides information about the current opcode
* afb enumerate basic blocks of function
* af analyzes the function (or a2f)
* ax code/data references/calls

## Analyzing the Whole Thing
Many people is used to the IDA way: load the bin, expect all
xrefs, functions and strings to magically appear in there.
This is the default behaviour, which can be slow, tedious,
and 99% of the time we can solve the problem quicker with
direct and manual analysis.
Run `r2 -A` or use the ‘aa’ subcommands to achieve this.
* aa
* aaa
* aaaa

## Low Level Anal Tweaks
Use the anal hints command to modify instruction behaviours
by hand.
> ahs 1 @ 0x100001175

## Searching for code

We can search for some specific code in a binary or memory.
* /R [expr] # search for ROP gadgets
* /r sym.imp.printf # find references to this address
* /m # search for magic headers
* Yara # identify crypto algorithms
* /a [asm] #assemble code and search bytes
* /A [type] #find instructions of this type
* /c [code] #find strstr matching instructions
* /v4 1234 #search for this number in memory
* pxa #disasm all possible instructions
* e asm.emustr=true #pD $SS @ $S~Hello

## Graphing Code

Functions can be rendered as an
ascii-art graph using the ‘ag’.
Enter visual mode using the V key
Then press V again (or spacebar) to
get the graph view.

The graph view is the result of the agf command and it
permits to:
* Move nodes
* Zoom in/out
* Relayout
* Switch between different graph modes
○ Callgraph
○ Overview

R2 can also use graphviz, xdot or web graph to show this
graph to the user, not just in ascii art.
> agv
> ag $$ > a.dot
