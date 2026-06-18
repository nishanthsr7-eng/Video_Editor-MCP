import os, sys
os.environ.setdefault("RESOLVE_SCRIPT_API",
    r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting")
os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"D:\DaVinci\fusionscript.dll")
sys.path.append(os.path.join(os.environ["RESOLVE_SCRIPT_API"], "Modules"))
import DaVinciResolveScript as dvr


def connect():
    resolve = dvr.scriptapp("Resolve")
    if resolve is None:
        raise RuntimeError(
            "Could not connect to Resolve. Is it running, and is scripting "
            "enabled in Preferences > System > General > External scripting using?")
    pm = resolve.GetProjectManager()
    proj = pm.GetCurrentProject()
    mp = proj.GetMediaPool() if proj else None
    return resolve, pm, proj, mp


if __name__ == "__main__":
    resolve, pm, proj, mp = connect()
    print("Connected:", resolve.GetProductName(), resolve.GetVersionString())
    print("Project:", proj.GetName() if proj else "(none)")
    tl = proj.GetCurrentTimeline() if proj else None
    print("Timeline:", tl.GetName() if tl else "(none)")
