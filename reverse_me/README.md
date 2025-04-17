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

### Patch 1 

<details>
identifier localisation de strcmp
JNE jump quand strcmp != 0 alors il faut bypass et donc on remplace par un JMP vers le succes.
modifier JNE par JPM + 4 Octets.

PATCH: echo -ne '\xEB\x04' | dd of=./level1 bs=1 seek=$((0x1244)) conv=notrunc (count=2)

- ecrit sur la sortie standard , -n sans le saut a la ligne final, -e active interpretation des sequences d'echappement
- l'OPCODE voulue
- dd pour copier les donnes binaires, sur le binaire, bs ecrit 1 octet a la fois, seek deplace le curseurs a l'adresse voulu, empeche trunc du fichier

JNE = 75 - Jump short if not zero/not equal (ZF=0)
JMP = E9 - Jump
remplacer le saut conditionel par un saut 

</details>

---

### Patch 2

<details>
jump from the first je to the final good job one.
PATCH:  echo -ne '\xE9\x53\x01\x00\x00' | dd of=./level2 bs=1 seek=$((0x131e)) conv=notrunc

Calcul de l'offset:
rel32 = (destination - (adresse_saut + 5))
offset = 0x1476 - (0x131e + 5) = 0x1476 - 0x1323 = 0x153

</details>

---

### Patch 3

<details>
jump from the first je to the final good job one.
PATCH: echo -ne '\xE9\xE9\x01\x00\x00' | dd of=./level3 bs=1 seek=$((0x1370)) conv=notrunc
Trouver la function success among all the different comparison.
the one correct is the one comparing the answer of strcmp to 0
comparaison between the answer of strcmp twice so it matchs then correct succes pass is at 0x155e
   0x00000000000014a2 <+386>:   mov    -0x54(%rbp),%eax
   0x00000000000014a5 <+389>:   test   %eax,%eax
   0x00000000000014a7 <+391>:   je     0x155e <main+574>
Calcul de l'offset:
rel32 = (destination - (adresse_saut + 5))
offset = 0x155e - (0x1370 + 5) = 0x155e - 0x1375 =  0x1e9

</details>

