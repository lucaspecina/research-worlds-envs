"""Verificacion gratis (sin LLM, sin red) de los ejemplos del doc
docs/research/2026-11-15-reformulacion-descubrir-es-encontrar-un-atajo.md

Cada chequeo muestra tres cosas: (a) el camino obvio (simular / enumerar) no entra en ningun
presupuesto para preguntas lejanas, (b) existe un atajo, (c) el atajo es EXACTO contra la
simulacion en las distancias donde simular si se puede.

Correr:  python docs/research/2026-11-15-atajos-verificacion.py     (tarda unos segundos; necesita numpy solo para el chequeo 6)
"""
import itertools
import math
import random
import time


# ---------- 1. SUPERPOSICION: regla 90 (cada celda = XOR de sus dos vecinas) ----------
def check_1_rule90():
    def sim(t_max, x):
        """celda x en el paso t_max, simulando paso a paso desde una sola celda negra en 0"""
        row = {0: 1}
        for _ in range(t_max):
            new = {}
            for c in set(itertools.chain.from_iterable((k - 1, k + 1) for k in row)):
                if row.get(c - 1, 0) ^ row.get(c + 1, 0):
                    new[c] = 1
            row = new
        return row.get(x, 0)

    def jump(t, x):
        """atajo: la celda (t,x) vale 1 sii (t+x) es par y C(t,(t+x)/2) es impar (teorema de Lucas:
        el binomio es impar sii j & (t-j) == 0)"""
        if (t + x) % 2 or abs(x) > t:
            return 0
        j = (t + x) // 2
        return 1 if (j & (t - j)) == 0 else 0

    ok = all(sim(t, x) == jump(t, x) for t in range(0, 70) for x in range(-t - 1, t + 2))
    t0 = time.time()
    _ = [jump(10**18 + k, 2 * k - 10**18) for k in range(1000)]
    dt = time.time() - t0
    t0 = time.time()
    sim(1500, 0)
    dsim = time.time() - t0
    print(f"1. SUPERPOSICION (regla 90): atajo == simulacion en los 70 primeros pasos completos: {ok}")
    print(f"   1000 preguntas en el paso 10^18: {dt * 1000:.1f} ms; simular solo 1.500 pasos tarda {dsim:.2f} s y crece con t^2")


# ---------- 2. REPETICION: automata en un anillo de N celdas con regla al azar ----------
def check_2_cycle():
    N = 14

    def step(state, rule):
        return tuple(rule[(state[(i - 1) % N], state[i], state[(i + 1) % N])] for i in range(N))

    def find_cycle(state, rule, limit=10**6):
        seen = {state: 0}
        s = state
        for t in range(1, limit):
            s = step(s, rule)
            if s in seen:
                return seen[s], t - seen[s]  # (preperiodo, periodo)
            seen[s] = t
        return None

    random.seed(7)
    found = []
    for _ in range(40):
        rule = {k: random.randint(0, 1) for k in itertools.product((0, 1), repeat=3)}
        s0 = tuple(random.randint(0, 1) for _ in range(N))
        c = find_cycle(s0, rule)
        if c and c[1] > 50:
            found.append((rule, s0, c))
    rule, s0, (mu, lam) = max(found, key=lambda z: z[2][1])
    T = 10**15
    T2 = mu + 3 * lam + 17  # distancia accesible para verificar
    a = s0
    for _ in range(T2):
        a = step(a, rule)
    b = s0
    for _ in range(mu + (T2 - mu) % lam):
        b = step(b, rule)
    print(f"2. REPETICION (anillo de {N} celdas, regla al azar): preperiodo {mu}, periodo {lam}")
    print(f"   atajo verificado contra simulacion directa a distancia {T2}: {a == b}; "
          f"el estado en el paso 10^15 sale con {mu + (T - mu) % lam} pasos")


# ---------- 3. CONSERVACION: el acertijo MU (Hofstadter) ----------
def check_3_mu():
    # reglas: xI->xIU ; Mx->Mxx ; III->U ; UU->(nada).  Pregunta: desde MI, se llega a MU?
    def nxt(s):
        out = set()
        if s.endswith("I"):
            out.add(s + "U")
        out.add("M" + s[1:] * 2)
        for i in range(len(s) - 2):
            if s[i:i + 3] == "III":
                out.add(s[:i] + "U" + s[i + 3:])
        for i in range(len(s) - 1):
            if s[i:i + 2] == "UU":
                out.add(s[:i] + s[i + 2:])
        return out

    frontier = {"MI"}
    seen = {"MI"}
    sizes = []
    for _ in range(1, 9):
        frontier = {n for s in frontier for n in nxt(s) if len(n) <= 40 and n not in seen}
        seen |= frontier
        sizes.append(len(seen))
    inv_ok = all(s.count("I") % 3 != 0 for s in seen)
    print(f"3. CONSERVACION (acertijo MU): cadenas alcanzables por profundidad: {sizes}; 'MU' encontrado: {'MU' in seen}")
    print(f"   'la cantidad de I nunca es multiplo de 3' se cumple en las {len(seen)} cadenas: {inv_ok} -> MU es imposible, en una linea")


# ---------- 4. GEMELO SIN ATAJO: regla 30, columna central ----------
def check_4_rule30():
    row = {0: 1}
    col = []
    for t in range(1200):
        col.append(row.get(0, 0))
        new = {}
        for c in range(-t - 1, t + 2):
            if row.get(c - 1, 0) ^ (row.get(c, 0) | row.get(c + 1, 0)):
                new[c] = 1
        row = new
    ones = sum(col) / len(col)
    best = max(range(1, 200), key=lambda p: sum(col[i] == col[i - p] for i in range(p, len(col))))
    agree = sum(col[i] == col[i - best] for i in range(best, len(col))) / (len(col) - best)
    print(f"4. GEMELO SIN ATAJO (regla 30, columna central, 1200 pasos): fraccion de unos {ones:.3f}")
    print(f"   el mejor 'periodo' encontrado acierta solo {agree:.3f} (azar = 0.5) -> lo correcto es decir 50/50")


# ---------- 5. DISFRAZ: una regla lineal escondida detras de un renombre de simbolos ----------
def check_5_disguise():
    P, N = 5, 23            # 5 simbolos, anillo de 23 celdas (5^23 ~ 1.2e16 estados)
    A, B, C = 2, 1, 4       # regla lineal: nueva[i] = 2*izq + 1*centro + 4*der (mod 5)
    triples = list(itertools.product(range(P), repeat=3))
    base = {(l, m, r): (A * l + B * m + C * r) % P for l, m, r in triples}

    def step(s, table):
        return tuple(table[(s[i - 1], s[i], s[(i + 1) % N])] for i in range(N))

    def is_affine(table):
        """prueba estandar de superposicion, admitiendo una constante: g = f - f(0) es aditiva"""
        f0 = table[(0, 0, 0)]
        for x in triples:
            for y in triples:
                z = tuple((x[k] + y[k]) % P for k in range(3))
                if (table[z] - f0) % P != (table[x] - f0 + table[y] - f0) % P:
                    return False
        return True

    def is_linear(table):
        return table[(0, 0, 0)] == 0 and is_affine(table)

    def conjugate(table, perm):
        """la misma regla con los simbolos renombrados (perm[viejo] = nuevo)"""
        inv = [0] * P
        for old, new in enumerate(perm):
            inv[new] = old
        return {(l, m, r): perm[table[(inv[l], inv[m], inv[r])]] for l, m, r in triples}

    # algebra del atajo: una regla lineal es una convolucion ciclica; t pasos = nucleo^t
    def conv(u, v):
        out = [0] * N
        for i, ui in enumerate(u):
            if ui:
                for j, vj in enumerate(v):
                    if vj:
                        out[(i + j) % N] = (out[(i + j) % N] + ui * vj) % P
        return out

    def kpow(kernel, t):
        result = [1] + [0] * (N - 1)
        while t:
            if t & 1:
                result = conv(result, kernel)
            kernel = conv(kernel, kernel)
            t >>= 1
        return result

    def kernel_of(table):
        k = [0] * N
        k[1], k[0], k[N - 1] = table[(1, 0, 0)], table[(0, 1, 0)], table[(0, 0, 1)]
        return k

    def jump_linear(s0, table, t):
        return tuple(conv(kpow(kernel_of(table), t), list(s0)))

    random.seed(11)
    s0 = tuple(random.randrange(P) for _ in range(N))

    # 5.0 sin disfraz
    sim = s0
    ok0 = True
    for t in range(1, 301):
        sim = step(sim, base)
        if t in (1, 2, 7, 100, 300):
            ok0 &= jump_linear(s0, base, t) == sim
    print(f"5. DISFRAZ. Sin disfraz: prueba de superposicion = {is_linear(base)}; atajo == simulacion en t=1,2,7,100,300: {ok0}")

    # cuanto dura el ciclo de verdad (orden exacto del nucleo)
    def prime_factors(n):
        f, d = [], 2
        while d * d <= n:
            if n % d == 0:
                f.append(d)
                while n % d == 0:
                    n //= d
            d += 1
        if n > 1:
            f.append(n)
        return f

    ident = [1] + [0] * (N - 1)
    order = P**22 - 1       # el orden divide a 5^22 - 1 (5 tiene orden 22 modulo 23)
    assert kpow(kernel_of(base), order) == ident
    for q in prime_factors(order):
        while order % q == 0 and kpow(kernel_of(base), order // q) == ident:
            order //= q
    period = order          # periodo exacto del estado inicial usado (divide al orden del sistema)
    for q in prime_factors(order):
        while period % q == 0 and conv(kpow(kernel_of(base), period // q), list(s0)) == list(s0):
            period //= q
    print(f"   este estado inicial recien se repite a los {period:,} pasos: detectar el ciclo simulando es inviable")

    # 5.1 con disfraz: renombre NO afin
    def is_affine_perm(perm):
        g = [(perm[x] - perm[0]) % P for x in range(P)]
        return all(g[(x + y) % P] == (g[x] + g[y]) % P for x in range(P) for y in range(P))

    perms = list(itertools.permutations(range(P)))
    disguise = random.choice([p for p in perms if not is_affine_perm(p)])
    hidden = conjugate(base, disguise)
    seen = {s0}
    s = s0
    repeated = False
    for _ in range(200000):
        s = step(s, hidden)
        if s in seen:
            repeated = True
            break
        seen.add(s)
    print(f"   Con disfraz {disguise}: prueba de superposicion sobre la tabla visible = {is_affine(hidden)}; "
          f"simulando 200.000 pasos, se repitio algun estado: {repeated}")

    # 5.2 buscador mecanico: probar los 120 renombres hasta que la prueba estandar pase
    lin = [(i + 1, c) for i, c in enumerate(perms) if is_linear(conjugate(hidden, c))]
    aff = [(i + 1, c) for i, c in enumerate(perms) if is_affine(conjugate(hidden, c))]
    print(f"   buscador mecanico: de {len(perms)} renombres, {len(aff)} destapan la estructura "
          f"({len(lin)} la dejan lineal exacta); el primero aparece en el intento {aff[0][0]}")

    # 5.3 el atajo recuperado es exacto contra la simulacion del sistema DISFRAZADO
    dec = lin[0][1]
    inv_dec = [0] * P
    for old, new in enumerate(dec):
        inv_dec[new] = old
    decoded = conjugate(hidden, dec)

    def jump_hidden(state, t):
        z = jump_linear(tuple(dec[x] for x in state), decoded, t)
        return tuple(inv_dec[x] for x in z)

    sim = s0
    ok1 = True
    for t in range(1, 1501):
        sim = step(sim, hidden)
        if t in (1, 3, 50, 777, 1500):
            ok1 &= jump_hidden(s0, t) == sim
    t0 = time.time()
    jump_hidden(s0, 10**18)
    dt = time.time() - t0
    print(f"   atajo recuperado == simulacion del sistema disfrazado en t=1,3,50,777,1500: {ok1}; "
          f"estado en el paso 10^18 en {dt * 1000:.0f} ms")

    # 5.4 nota de diseno: que renombres NO esconden nada, segun el alfabeto
    def affine_mod(p):
        cnt = 0
        for perm in itertools.permutations(range(p)):
            g = [(perm[x] - perm[0]) % p for x in range(p)]
            cnt += all(g[(x + y) % p] == (g[x] + g[y]) % p for x in range(p) for y in range(p))
        return cnt

    def affine_bits(nbits):
        n, cnt = 1 << nbits, 0
        for perm in itertools.permutations(range(n)):
            g = [perm[x] ^ perm[0] for x in range(n)]
            cnt += all(g[x ^ y] == g[x] ^ g[y] for x in range(n) for y in range(x))
        return cnt

    print("   nota de diseno - renombres que NO esconden nada (afines) / renombres totales:")
    for p in (3, 5, 7):
        print(f"     {p} simbolos: {affine_mod(p)} / {math.factorial(p)}")
    for nb in (2, 3):
        print(f"     bloques de {nb} bits: {affine_bits(nb)} / {math.factorial(1 << nb)}")


# ---------- 6. TRAMPA: un patron que se repite muchisimas veces... y despues se rompe ----------
def check_6_trap():
    """Regla 110 en un anillo de 300 casillas, arranque al azar (semilla fija). La casilla 279 repite
    el mismo dibujo de 7 pasos durante cientos de pasos y despues deja de hacerlo (le llega una
    estructura que venia viajando por el anillo). Quien induce 'se repite cada 7' mirando solo esa
    casilla, se equivoca en las preguntas lejanas."""
    import numpy as np

    N, T, seed, cell, period, t0 = 300, 2400, 32, 279, 7, 400
    rng = np.random.default_rng(seed)
    s = rng.integers(0, 2, N, dtype=np.uint8)
    col = []
    for _ in range(T):
        col.append(int(s[cell]))
        left, right = np.roll(s, 1), np.roll(s, -1)
        s = ((s | right) & ~(left & s & right)) & 1      # regla 110
    pattern = col[t0:t0 + period]
    t = t0 + period
    while t < T and col[t] == col[t - period]:
        t += 1
    reps = (t - t0) // period
    predicted = [pattern[(k - t0) % period] for k in range(t, t + 14)]
    print(f"6. TRAMPA (regla 110, anillo de {N}, casilla {cell}): desde el paso {t0} repite el dibujo "
          f"{''.join(map(str, pattern))} durante {t - t0} pasos ({reps} repeticiones seguidas)")
    print(f"   y se rompe en el paso {t}: el patron predecia {''.join(map(str, predicted))}, "
          f"salio {''.join(map(str, col[t:t + 14]))}")


if __name__ == "__main__":
    check_1_rule90()
    check_2_cycle()
    check_3_mu()
    check_4_rule30()
    check_5_disguise()
    check_6_trap()
