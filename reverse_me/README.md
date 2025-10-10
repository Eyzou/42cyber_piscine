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

**gdb**: used for all 3 levels (dynamic debugging)
**IDA Pro**: used to visualize assembly code (optional)
**objdump**: tool for analyzing binary sections

### objdump usage example:
```bash
objdump -s -j .rodata ./level1 | grep -A1 "5f73"
```
- `-s`: Display raw content of all sections
- `-j .rodata`: Target only the `.rodata` section (read-only data, contains string constants)
- `grep -A1 "5f73"`: Search for specific offset (e.g., `5f73` corresponds to first bytes of `_stack_check`)
- `-A1`: Display 1 additional line after the matched pattern

---

## LEVEL 1 - Simple strcmp

**Goal**: Find the hardcoded password compared with `strcmp`.

### Context
The program (see `level1/source.c:10`) uses `strcmp(key, input)` to compare your input with a hardcoded string `"__stack_check"`.

<details>
<summary>Spoiler Alert - Method 1: Breakpoint on strcmp</summary>

### Steps:
1. Launch GDB:
   ```bash
   gdb ./level1
   ```

2. Set a breakpoint on `strcmp` function:
   ```gdb
   break strcmp
   ```

3. Run the program:
   ```gdb
   run
   ```
   Enter anything when prompted (e.g., "test")

4. Inspect `strcmp` arguments on the stack:
   ```gdb
   x/s *(int*)($esp)      # 1st argument (hardcoded key)
   x/s *(int*)($esp+4)    # 2nd argument (your input)
   ```

**Expected result**: `"__stack_check"`

</details>

---

<details>
<summary>Spoiler Alert - Method 2: Assembly code analysis</summary>

### Steps:
1. Disassemble the main function:
   ```gdb
   gdb ./level1
   disassemble main
   ```

2. Identify where the string is loaded into memory (before the `strcmp` call)

3. Set a breakpoint at that address:
   ```gdb
   break *0xXXXX
   ```

4. Run and inspect memory:
   ```gdb
   run
   x/s $ebp-0xXX    # Offset according to disassembly
   ```

**Note**: This method requires reading assembly to find the exact offset.

</details>

---

## LEVEL 2 - ASCII Conversion

**Goal**: The binary checks that input starts with "00", then converts following digits into ASCII characters.

<details>
<summary>Spoiler Alert</summary>

### Resolution Steps:

#### 1. Analyze source code (`source.c:21-22`):
The program checks:
```c
if (input[0] != '0' || input[1] != '0')
    no();
```
→ **Input must start with "00"**

#### 2. Hardcoded buffer (`source.c:27`):
```c
result_buffer[0] = 'd';  // First character forced to 'd'
```

#### 3. Find the expected string:
```bash
gdb ./level2
break strcmp
run
# Enter "00" to pass initial checks
x/s *(int*)($esp+4)    # Displays "delabere"
```

#### 4. ASCII Conversion:
- We want to get `"delabere"` but `'d'` is already there
- We need to convert `"elabere"` to ASCII codes:
  ```
  e = 101
  l = 108
  a = 097
  b = 098
  e = 101
  r = 114
  e = 101
  ```

#### 5. Final input:
```
00101108097098101114101
```

### Explanation:
- `00` → passes initial check
- `101108097098101114101` → converted to `"elabere"`
- Final buffer: `'d' + "elabere"` = `"delabere"` ✓

</details>


---

## LEVEL 3 - Level 2 Variation

**Goal**: Similar to Level 2, but with different initial check and hardcoded character.

<details>
<summary>Spoiler Alert</summary>

### Differences from Level 2:
| Aspect | Level 2 | Level 3 |
|--------|---------|---------|
| Initial check | `"00"` | `"42"` |
| Hardcoded character | `'d'` | `'*'` |
| Expected string | `"delabere"` | `"********"` (8 asterisks) |

### Resolution Steps:

#### 1. Analyze source code (`source.c:25`):
```c
if (input[0] != '4' || input[1] != '2')
    no();
```
→ **Input must start with "42"**

#### 2. Hardcoded buffer (`source.c:31`):
```c
result_buffer[0] = '*';  // First character forced to '*'
```

#### 3. Find the expected string:
```bash
gdb ./level3
break strcmp
run
# Enter "42" to pass initial checks
x/s 0xXXXXXXXX    # Find address in disassembly, displays "********"
```

#### 4. ASCII Conversion:
- We want to get `"********"` (8 asterisks) but first `'*'` is already there
- We need to convert 7 remaining `'*'` to ASCII codes:
  ```
  * = 042 (ASCII decimal)
  ```
  → `042042042042042042042` (7 times)

#### 5. Final input:
```
42042042042042042042042
```

### Explanation:
- `42` → passes initial check
- `042042042042042042042` → converted to 7 `'*'` characters
- Final buffer: `'*' + "*******"` = `"********"` ✓

</details>


---

###  Patch 1 — Bypass `strcmp` failure (Level 1)

<details>
<summary>Click to expand</summary>

**Context**: After `strcmp` returns, the binary uses a `JNE` (Jump if Not Equal) instruction to jump to the "Nope" failure path when passwords don't match.

**Goal**: Replace `JNE` with an unconditional jump (`JMP`) to always reach the "Good job" success path.

####  Replace `JNE` with a short unconditional jump (`JMP +4`)

**Patch command:**

```bash
echo -ne '\xEB\x04' | dd of=./level1 bs=1 seek=$((0x1244)) conv=notrunc count=2
```

#### Breakdown:
- `echo -ne`:
  - `-n` avoids adding a newline
  - `-e` interprets escape sequences like `\xEB`
- `\xEB\x04`:
  - `\xEB` = opcode for `JMP` (short relative jump)
  - `\x04` = jump +4 bytes forward
- `dd`:
  - `of=./level1`: output file to patch
  - `bs=1`: write 1 byte at a time
  - `seek=$((0x1244))`: move to offset 0x1244 (location of `JNE` instruction)
  - `conv=notrunc`: prevents file truncation (only modify specified bytes)
  - `count=2`: write 2 bytes total

#### Instruction Reference:
- `JNE (0x75)` — Jump if Not Equal (conditional)
- `JMP (0xEB)` — Unconditional Short Jump

> This patch makes the program always jump to the success branch, regardless of password correctness.

</details>

---

###  Patch 2 — Jump directly to "Good job" (Level 2)

<details>
<summary>Click to expand</summary>

**Context**: Level 2 has multiple checks before reaching the success message. We want to skip all intermediate logic and jump directly from the first check to the "Good job" block.

**Goal**: Replace the first `JE` (Jump if Equal) with a long jump directly to the success message.

#### Insert a near jump (`JMP rel32`) with calculated offset

**Patch command:**

```bash
echo -ne '\xE9\x53\x01\x00\x00' | dd of=./level2 bs=1 seek=$((0x131e)) conv=notrunc
```

#### Offset Calculation:
A near jump uses a **relative** 32-bit offset from the instruction AFTER the jump:

```
rel32 = destination_address - (jump_instruction_address + 5)
      = 0x1476 - (0x131e + 5)
      = 0x1476 - 0x1323
      = 0x153
```

**Why +5?** The jump instruction itself is 5 bytes (`\xE9` + 4 bytes offset), so the CPU calculates from the next instruction.

#### Breakdown:
- `\xE9` = opcode for near `JMP` (32-bit relative)
- `\x53\x01\x00\x00` = offset `0x153` in little-endian format
- `seek=$((0x131e))` = location to patch (first check)

> This patch redirects execution directly to the win message, bypassing all password checks.

</details>

---

### Patch 3 — Force success via correct `strcmp` match (Level 3)

<details>
<summary>Click to expand</summary>

**Context**: Level 3 has a check that verifies if `strcmp` returned 0 (strings match). We want to jump directly to the success path where this check passes.

**Goal**: Jump from an early point in the code directly to the block that executes when `strcmp == 0`.

####  Force `JMP` to the valid success block

**Patch command:**

```bash
echo -ne '\xE9\xE9\x01\x00\x00' | dd of=./level3 bs=1 seek=$((0x1370)) conv=notrunc
```

#### Relevant Assembly (target location):

```asm
0x14a2: mov -0x54(%rbp), %eax    # Load strcmp result
0x14a5: test %eax, %eax          # Test if result == 0
0x14a7: je   0x155e <main+574>   # Jump to success if zero
```

The `je` at `0x14a7` checks for `strcmp == 0` and jumps to the "Good job" message.

#### Offset Calculation:
```
rel32 = destination_address - (jump_instruction_address + 5)
      = 0x155e - (0x1370 + 5)
      = 0x155e - 0x1375
      = 0x1e9
```

#### Breakdown:
- `\xE9` = opcode for near `JMP`
- `\xE9\x01\x00\x00` = offset `0x1e9` in little-endian format
- `seek=$((0x1370))` = early location to patch

> This forces execution directly into the valid `strcmp` success path, bypassing all password validation.

</details>

---
