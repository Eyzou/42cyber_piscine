##  GDB Useful 

###  Basic Debugging Steps

```gdb
disassemble main         # Disassemble the main function
break strcmp             # Set a breakpoint at strcmp
break *0xXXXX
b *0xXXXXX
run                      # Run the program
info registers           # Show register states
info functions           # List all functions
or x/s *(int)(*$xxx)     # Inspect memory (alternative syntax)
p &xxx                   # Print address of variable
```

### Breakpoint Management

```gdb
info breakpoints         # See active breakpoints
d                        # Delete breakpoints
```

##  Useful Reference (x86)

| Register | Name           | Description |
|----------|----------------|-------------|
| `esp`    | Stack Pointer  | Points to the **top of the stack**, where function arguments (like those passed to `strcmp`) are stored. |
| `ebp`    | Base Pointer   | Used to access **local variables**, like `-0x7a(%ebp)`, but not function arguments. |

## Some tools

gdb used in level 1
IDA Pro used in level 2

---

## LEVEL 1

### Option 1 — Break at `strcmp` Call

<details>
<summary>Spoiler Alert</summary>
- The password is passed via the **stack** (through `%esp`).
- You can inspect the memory at:

```gdb
x/s *(int*)($esp)        # Read the value at the address pointed to by esp
```

</details>

---

### Option 2 — Break at Beginning

<details>
<summary>Spoiler Alert</summary>

Set a breakpoint early when password chunks are loaded into memory.  
These values are later used in `strcmp`.  
Check memory where data is stored:

```gdb
x/s $ebp -0xXXXXXX          # Inspect memory at offset from base pointer
```

</details>


## LEVEL 2


### Break at `strcmp` Call
### Decomposing the code

<details>
<summary>Spoiler Alert</summary>
- The string is passed via the **stack** (through `%esp`).
- You can inspect the memory at:

```gdb
x/s *(int*)($esp+4)        # Read the value at the address pointed to by esp to have the needed string
```
Then we notice that the key should begin with 00
Then a 'd' is hardcoded on the buffer at the first place.
Then using the word we discover we disregard the first letter which is a "d"
And convert the letter into ASCII number
we got the final key to input

</details>
