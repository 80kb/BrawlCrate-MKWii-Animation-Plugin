__author__ = "BillyNoodles"
__version__ = "2.0.0"

from BrawlCrate.API import BrawlAPI
from System.IO import Path
from System.IO import Directory

preset_name = "MKW Boost"
preset_path = Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", preset_name)

if BrawlAPI.ShowYesNoWarning("Are you sure you want to delete this preset?", "Delete Preset"):
    Directory.Delete(preset_path, True)
    BrawlAPI.RootNode._mainForm.reloadPluginsToolStripMenuItem_Click(None, None)