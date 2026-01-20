import os
import matplotlib.pyplot as plt
import re

OLD_DIR = 'results/old'
NEW_DIR = 'results/new'

def parse_time(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            match = re.search(r'Execution Time:\s*([\d\.]+)s', content)
            if match:
                return float(match.group(1))
            
            match_timeout = re.search(r'Timeout after (\d+)s', content)
            if match_timeout:
                return float(match_timeout.group(1))
    except Exception as e:
        print(f"Eroare parsare {filepath}: {e}")
    return None

def main():
    results = []
    
    for filename in os.listdir(NEW_DIR):
        if not filename.endswith('.res'):
            continue
            
        new_path = os.path.join(NEW_DIR, filename)
        old_path = os.path.join(OLD_DIR, filename)

        t_new = parse_time(new_path)
        t_old = parse_time(old_path)

        if t_new is not None and t_old is not None:
            if t_old >= 300 and t_new >= 300:
                continue
            results.append((t_old, t_new))
            print(f"{filename}: Vechi={t_old}s, Nou={t_new}s")

    if not results:
        print("Nu s-au gasit comparatii valide.")
        return

    results.sort(key=lambda x: x[0])
    
    old_times = [r[0] for r in results]
    new_times = [r[1] for r in results]

    x_old = list(range(1, len(old_times) + 1))
    x_new = list(range(1, len(new_times) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(x_old, old_times, 'r-o', label='Solver Vechi')
    plt.plot(x_new, new_times, 'g-o', label='Solver Nou')
    plt.xlabel('Numar de instante rezolvate')
    plt.ylabel('Timp (s)')
    plt.title('Compararea rezultatelor (Liniar)')
    plt.legend()
    plt.grid(True)
    plt.savefig('plot_clasic_liniar.png')
    print("Plot liniar salvat in plot_clasic_liniar.png")

    plt.figure(figsize=(10, 6))
    plt.plot(x_old, old_times, 'r-o', label='Solver Vechi')
    plt.plot(x_new, new_times, 'g-o', label='Solver Nou')
    plt.xlabel('Numar de instante rezolvate')
    plt.ylabel('Timp (s)')
    plt.title('Compararea rezultatelor (Logaritmic)')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    plt.savefig('plot_clasic_log.png')
    print("Plot logaritmic salvat in plot_clasic_log.png")

if __name__ == "__main__":
    main()
