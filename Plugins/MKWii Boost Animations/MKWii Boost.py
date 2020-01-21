__author__ = "BillyNoodles"
__version__ = "0.0.1"

import BrawlLib
import BrawlCrate
from BrawlCrate.API import BrawlAPI
from System.IO import Path

def CreateShader():
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".mdl0" in wrapper.ExportFilter:
            if wrapper.Resource.Name == "course":
                wrapper.NewShader().Replace(Path.Combine(BrawlAPI.PluginPath, "MKWii Boost Animations", "mkwShader"))

def MatAmount():
    StatInt = 0
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".mdl0mat" in wrapper.ExportFilter:
            StatInt += 1
    return StatInt

def ReplaceTextureRef(x):
    children = x.GetChildrenRecursive()
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".png" in wrapper.ExportFilter:
            if wrapper.Resource.Name == children[0].Name:
                wrapper.Resource.Replace(Path.Combine(BrawlAPI.PluginPath, "MKWii Boost Animations", "mkwBumpS.tex0"))
                wrapper.Resource.Name = "ef_arrowBumpS"
                return

def ImportTextures():
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".brres" in wrapper.ExportFilter:
            g_node = BrawlLib.SSBB.ResourceNodes.NodeFactory.FromFile(None, Path.Combine(BrawlAPI.PluginPath, "MKWii Boost Animations", "ef_arrowGradS.tex0"))
            wrapper.Resource.GetOrCreateFolder[BrawlLib.SSBB.ResourceNodes.TEX0Node]().AddChild(g_node)
            r_node = BrawlLib.SSBB.ResourceNodes.NodeFactory.FromFile(None, Path.Combine(BrawlAPI.PluginPath, "MKWii Boost Animations", "ef_rainbowRed2.tex0"))
            wrapper.Resource.GetOrCreateFolder[BrawlLib.SSBB.ResourceNodes.TEX0Node]().AddChild(r_node)
            c_node = BrawlLib.SSBB.ResourceNodes.NodeFactory.FromFile(None, Path.Combine(BrawlAPI.PluginPath, "MKWii Boost Animations", "course.srt0"))
            wrapper.Resource.GetOrCreateFolder[BrawlLib.SSBB.ResourceNodes.SRT0Node]().AddChild(c_node)

def ReplaceMaterial(x):
    CurrentIndex = 0
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".mdl0mat" in wrapper.ExportFilter:
            CurrentIndex += 1
            if wrapper.Resource.Name == x:
                ReplaceTextureRef(wrapper.Resource)
                ImportTextures()
                wrapper.Resource.Replace(Path.Combine(BrawlAPI.PluginPath, "MKWii Boost Animations", "mkwMat"))
                for i in range(MatAmount() - CurrentIndex):
                    wrapper.Resource.DoMoveDown()
                CreateShader()
                wrapper.Resource.Shader = "Shader 1"
                wrapper.Resource.Name = "ef_dushBoard"
                return
    BrawlAPI.ShowMessage("No material with the name \"" + x + "\" exists", "Error")

#main function
ReplaceMaterial(BrawlAPI.UserStringInput("Boost Material Name"))
