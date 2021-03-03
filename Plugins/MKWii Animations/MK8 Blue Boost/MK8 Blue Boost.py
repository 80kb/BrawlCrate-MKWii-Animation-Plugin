__author__ = "BillyNoodles"
__version__ = "1.1"

import BrawlLib
import BrawlCrate
from BrawlCrate.API import BrawlAPI
from System.IO import Path

def CreateShader():
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".mdl0" in wrapper.ExportFilter:
            if wrapper.Resource.Name == "course":
                shader = wrapper.NewShader()
                shader.Replace(Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", "MK8 Blue Boost", "mk8BlueShader.mdl0shade"))
                return shader.Name

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
                wrapper.Resource.Replace(Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", "mk8BlueBumpS.tex0"))
                wrapper.Resource.Name = "mk8BlueBumpS"
                return

def ImportTextures():
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".brres" in wrapper.ExportFilter:
            g_node = BrawlLib.SSBB.ResourceNodes.NodeFactory.FromFile(None, Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", "mk8BlueGradS.tex0"))
            wrapper.Resource.GetOrCreateFolder[BrawlLib.SSBB.ResourceNodes.TEX0Node]().AddChild(g_node)
            r_node = BrawlLib.SSBB.ResourceNodes.NodeFactory.FromFile(None, Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", "mk8BlueRainbow.tex0"))
            wrapper.Resource.GetOrCreateFolder[BrawlLib.SSBB.ResourceNodes.TEX0Node]().AddChild(r_node)
            c_node = BrawlLib.SSBB.ResourceNodes.NodeFactory.FromFile(None, Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", "mk8BlueBoost.srt0"))
            wrapper.Resource.GetOrCreateFolder[BrawlLib.SSBB.ResourceNodes.SRT0Node]().AddChild(c_node)

def CheckUse(shader):
    amount = 0
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".mdl0mat" in wrapper.ExportFilter:
            if wrapper.Resource.Shader == shader:
                amount += 1
    if amount == 1:
        return True
    else:
        return False

def SearchAndDestroy(mat):
    children = mat.GetChildrenRecursive()
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".png" in wrapper.ExportFilter:
            for i in range(len(children)):
                if wrapper.Resource.Name == children[i].Name:
                    if i > 0:
                        wrapper.Delete()
                        break
        if ".mdl0shade" in wrapper.ExportFilter:
            if CheckUse(mat.Shader) == True and wrapper.Resource.Name == mat.Shader:
                wrapper.Delete()
        if ".srt0" in wrapper.ExportFilter:
            for i in range(len(wrapper.Resource.Children)):
                if wrapper.Resource.Children[i].Name == mat.Name:
                    wrapper.Delete()

def ReplaceMaterial(x):
    CurrentIndex = 0
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".mdl0mat" in wrapper.ExportFilter:
            CurrentIndex += 1
            if wrapper.Resource.Name == x:
                SearchAndDestroy(wrapper.Resource)
                ReplaceTextureRef(wrapper.Resource)
                ImportTextures()
                wrapper.Resource.Replace(Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", "mk8BlueBoost.mdl0mat"))
                for i in range(MatAmount() - CurrentIndex):
                    wrapper.Resource.DoMoveDown()
                wrapper.Resource.Shader = CreateShader()
                wrapper.Resource.Name = "mk8BlueBoost"
                return
    BrawlAPI.ShowMessage("No material with the name \"" + x + "\" exists", "Error")

#main function
input = BrawlAPI.UserStringInput("Material Name")
if input != None:
    ReplaceMaterial(input)
