import os, sys
print("python:", sys.version.split()[0], "bits=", 8*__import__("struct").calcsize("P"))
print("RESOLVE_SCRIPT_API:", os.getenv("RESOLVE_SCRIPT_API"))
print("RESOLVE_SCRIPT_LIB:", os.getenv("RESOLVE_SCRIPT_LIB"))
print("lib exists:", os.path.exists(os.getenv("RESOLVE_SCRIPT_LIB") or ""))
import DaVinciResolveScript as m
print("module loaded:", m)
print("has scriptapp:", hasattr(m, "scriptapp"))
r = m.scriptapp("Resolve")
print("scriptapp('Resolve') ->", r)
if r:
    print("product:", r.GetProductName(), r.GetVersionString())
