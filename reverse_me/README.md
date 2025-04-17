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
objdump -s -j .rodata ./your_binary | grep -A1 42cd

##  Useful Reference (x86)

| Register | Name           | Description |
|----------|----------------|-------------|
| `esp`    | Stack Pointer  | Points to the **top of the stack**, where function arguments (like those passed to `strcmp`) are stored. |
| `ebp`    | Base Pointer   | Used to access **local variables**, like `-0x7a(%ebp)`, but not function arguments. |

## Some tools

gdb used in level 1
IDA Pro used in level 2/3
objdump (outil pour analyse de fichiers binaires):

```bash
objdump -s -j .rodata ./level1/2/3 | grep -A1 XXXX
```
-s contenue brut
-A1 1 ligne apres le motif trouve
-XX l'offset

---

## LEVEL 1

#### Option 1 — Break at `strcmp` Call

<details>
<summary>Spoiler Alert</summary>
- The password is passed via the **stack** (through `%esp`).
- You can inspect the memory at:

```gdb
x/s *(int*)($esp)        # Read the value at the address pointed to by esp
```

</details>

---

#### Option 2 — Break at Beginning

<details>
<summary>Spoiler Alert</summary>

Set a breakpoint early when password chunks are loaded into memory.  
These values are later used in `strcmp`.  
Check memory where data is stored:

```gdb
x/s $ebp -0xXXXXXX          # Inspect memory at offset from base pointer
```

</details>

---

## LEVEL 2


<details>
<summary>Spoiler Alert</summary>
- The string is passed via the **stack** (through `%esp`).
- You can inspect the memory at:

- 1st we need to check and notice that the key should begin with 00
- then add at least 00 to by pass the 2 first no function and put the breakpoint at strcmp
```gdb
x/s *(int*)($esp+4)        # Read the value at the address pointed to by esp to have the needed string
```
- Then a 'd' is hardcoded on the buffer at the first place.
- Then using the word we discover we disregard the first letter which is a "d"
- And convert the letter into ASCII number
- We got the final key to input

</details>


---

## LEVEL 3


<details>
<summary>Spoiler Alert</summary>
- The string is passed via the **stack**.
- You can inspect the memory at:

- 1st we need to check and notice that the key should begin with 00
- then add at least 42 to by pass the 2 first no function and put the breakpoint at strcmp
```gdb
x/s 0xXXXXXXXX        # Read the value at the address pointed to by esp to have the needed string
```
- Then a '*' is hardcoded on the buffer at the first place.
- Then using the word we discover we disregard the first letter which is a "*"
- And convert the letter into ASCII number
- We got the final key to input

</details>


---

###  Patch 1 — Bypass `strcmp` failure

<details>
<summary>Click to expand</summary>

We locate a `JNE` (Jump if Not Equal) instruction that follows a `strcmp` call.  
Since `JNE` jumps when `strcmp != 0`, we want to **bypass** this and force the success path.

####  Replace `JNE` with a short unconditional jump (`JMP +4`)

**Patch command:**

```bash
echo -ne '\xEB\x04' | dd of=./level1 bs=1 seek=$((0x1244)) conv=notrunc count=2
```

#### Breakdown:
- `echo -ne`: `-n` avoids newline, `-e` interprets escape sequences.
- `\xEB\x04`: opcode for `JMP` with +4 bytes offset.
- `dd`:
  - `bs=1`: write 1 byte at a time,
  - `seek=0x1244`: move to the target instruction offset,
  - `conv=notrunc`: prevents file truncation.

#### Instruction Reference:
- `JNE (75)` — Jump if Not Equal
- `JMP (EB)` — Unconditional Short Jump

> This patch makes the program always jump to the success branch.

</details>

---

###  Patch 2 — Jump directly to "Good job"

<details>
<summary>Click to expand</summary>

We want to skip intermediate logic and jump from the **first `JE`** directly to the final "Good job" success block.

#### Insert a near jump (`JMP rel32`) with calculated offset

**Patch command:**

```bash
echo -ne '\xE9\x53\x01\x00\x00' | dd of=./level2 bs=1 seek=$((0x131e)) conv=notrunc
```

#### Offset Calculation:
```
rel32 = destination - (jump_address + 5)
      = 0x1476 - (0x131e + 5)
      = 0x1476 - 0x1323
      = 0x153
```

> `\xE9` is the opcode for a 4-byte relative jump. This redirects execution to the win message.

</details>

---

### Patch 3 — Force success via correct `strcmp` match

<details>
<summary>Click to expand</summary>

We find the comparison that checks if `strcmp == 0`, and patch the binary to jump there directly.

####  Force `JMP` to the valid success block

**Patch command:**

```bash
echo -ne '\xE9\xE9\x01\x00\x00' | dd of=./level3 bs=1 seek=$((0x1370)) conv=notrunc
```

#### Relevant Assembly:

```asm
0x14a2: mov -0x54(%rbp), %eax
0x14a5: test %eax, %eax
0x14a7: je   0x155e <main+574>
```

We target the `je` at `0x14a7` which checks for `strcmp == 0`.

#### Offset Calculation:
```
rel32 = 0x155e - (0x1370 + 5)
      = 0x155e - 0x1375
      = 0x1e9
```

> This forces execution directly into the valid `strcmp` success path.

</details>

---
