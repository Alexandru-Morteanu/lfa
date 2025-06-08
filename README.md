# Limbaje Formale și Automate

**Autor:** Morteanu Alexandru

Fișierele atașate sunt rezultatul următoarelor teme:

---

## 1. NFA

**Script:** [nfa.py](nfa.py)  
**Input:** [nfa]([nfa])

### Rulare
```bash
python3 nfa.py
```

---

## 2. Joc în DFA/NFA

**Script:** [game.py](game.py)  
**Input:** [game]([game])

Pentru joc am creat un script separat care acceptă inputul *symbol cu symbol* pentru a fi mai distractiv.

### Acțiuni posibile
- `n` - nord
- `e` - est  
- `s` - sud
- `w` - vest
- `p` - pick up

**Notă:** Pentru a castiga:
```bash
1. w         → GARDEN_MODULE
2. p         → pick up CARD1
3. p         → GARDEN_MODULE+CARD
4. e         → HUB+CARD
5. n         → AIRLOCK
6. n         → CENTRAL
7. n         → DINING_BAY
8. w         → KITCHEN
9. p         → pick up CARD2
10. p        → KITCHEN+CARD
11. e        → DINING_BAY+CARD
12. n        → CREW_QUARTERS+CARD
13. n        → POD ✅ YOU WIN!
```

### Rulare
```bash
python3 game.py "[game]"
```

---

## 3. PDA (Pushdown Automaton)

**Script:** [pda.py](pda.py)  
**Input:** [pda]([pda])

Acest PDA verifică dacă inputul este de forma:
```
{ 0ⁿ 1ᵐ | n ≥ 1, m ≥ 1, m > n + 2 }
```

### Rulare
```bash
python3 pda.py
```

---

## 4. Mașina Turing

**Script:** [turing.py](turing.py)  
**Input:** [turing]([turing])

Această mașină Turing verifică dacă inputul este de forma:
```
{ 0^n 1^n | n>0 }
```

### Rulare
```bash
python3 turing.py "[turing]"
```
