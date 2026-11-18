#!/usr/bin/env python3
"""sql2mermaid: converte CREATE TABLE em diagrama ER Mermaid."""
import re, sys
def parse(sql):
    tables, rels = {}, []
    for m in re.finditer(r"create\s+table\s+(?:if\s+not\s+exists\s+)?[`\"]?(\w+)[`\"]?\s*\((.*?)\);", sql, re.I | re.S):
        name, body, cols = m.group(1), m.group(2), []
        for line in re.split(r",\s*\n", body):
            line = line.strip()
            fk = re.search(r"foreign\s+key\s*\(\s*[`\"]?(\w+)[`\"]?\s*\)\s*references\s+[`\"]?(\w+)", line, re.I)
            if fk: rels.append((name, fk.group(2), fk.group(1))); continue
            c = re.match(r"[`\"]?(\w+)[`\"]?\s+(\w+)", line)
            if c and c.group(1).lower() not in ("primary", "unique", "constraint", "key", "index"):
                tag = " PK" if re.search(r"primary\s+key", line, re.I) else ""
                inl = re.search(r"references\s+[`\"]?(\w+)", line, re.I)
                if inl: rels.append((name, inl.group(1), c.group(1))); tag += " FK"
                cols.append((c.group(2), c.group(1), tag))
        tables[name] = cols
    return tables, rels
def render(sql):
    t, r = parse(sql); out = ["erDiagram"]
    for n, cols in t.items():
        out.append(f"  {n} {{"); out += [f"    {ty} {nm}{tg}" for ty, nm, tg in cols]; out.append("  }")
    out += [f"  {b} ||--o{{ {a} : \"{c}\"" for a, b, c in r]
    return "\n".join(out)
if __name__ == "__main__":
    print(render(open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()))
