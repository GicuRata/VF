# VF

Proiectul nostru cu MiniSat SAT Solver

## Compilare

```bash
# Compilează solver-ul core
cd minisat/core && export MROOT=$(pwd)/.. && make

# Compilează solver-ul simp
cd minisat/simp && export MROOT=$(pwd)/.. && make

# Curăță compilarea
make clean
```

## Utilizare

### Comenzi de bază

```bash
# Rulează pe un fișier CNF (afișare în terminal)
./minisat/core/minisat problema.cnf

# Salvează soluția într-un fișier
./minisat/core/minisat problema.cnf solutie.txt

# Folosește solver-ul simp cu preprocesare
./minisat/simp/minisat problema.cnf solutie.txt
```

### Opțiuni avansate

```bash
# Rulează cu nivel de verbozitate
./minisat/core/minisat problema.cnf -verb=2

# Rulează cu euristici compatibile MiniSat 2.0
./minisat/core/minisat problema.cnf -no-luby -rinc=1.5 -phase-saving=0 -rnd-freq=0.02

# Setează limita de timp CPU (în secunde)
./minisat/core/minisat problema.cnf -cpu-lim=60

# Setează limita de memorie (în MB)
./minisat/core/minisat problema.cnf -mem-lim=2048

# Mod silențios
./minisat/core/minisat problema.cnf -verb=0
```

## Ajutor

```bash
./minisat/core/minisat --help
./minisat/simp/minisat --help
```
