# Print every untagged ASCII diagram of a topic with its override hash key.
# Usage: python3 extract.py <topic-number>
import re, hashlib, sys, pathlib, glob
ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).parent))
n = int(sys.argv[1])
try:
    import mag
    f = str(ROOT / mag.cfg_by_n(n)["file"])      # resolves subfolder files (AI-ML/, DSA/, …)
except Exception:
    f = sorted(glob.glob(str(ROOT / f"{n:02d}-*.md")))[0]
txt = pathlib.Path(f).read_text(encoding="utf-8")
blocks = [b for l, b in re.findall(r"```([\w+-]*)\n(.*?)```", txt, re.DOTALL) if not l.strip()]
print(f"# {len(blocks)} ASCII diagrams in {pathlib.Path(f).name}\n")
for i, b in enumerate(blocks, 1):
    c = b.strip("\n").strip()
    key = hashlib.md5(c.encode()).hexdigest()[:12]
    print(f"\n================= DIAGRAM #{i}  key={key}  ({len(c.splitlines())} lines) =================")
    print(c)
