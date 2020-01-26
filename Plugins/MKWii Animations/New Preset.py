__author__ = "BillyNoodles"
__version__ = "1.0.0"

from BrawlCrate.API import BrawlAPI
from System.IO import Directory
from System.IO import Path
from System.IO import StreamWriter

textureNames = []

def CheckMaterial(mat):
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".mdl0mat" in wrapper.ExportFilter:
            if wrapper.Resource.Name == mat:
                if CheckTextures(wrapper.Resource) and CheckAnimation(mat):
                    return True
                else:
                    return False
    BrawlAPI.ShowMessage("No material with the name " + mat + " exists", "Missing Material")

def CheckTextures(mat):
    index = 0
    children = mat.GetChildrenRecursive()
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".png" in wrapper.ExportFilter:
            for i in range(len(children)):
                if wrapper.Resource.Name == children[i].Name:
                    index = index + 1
                    break
    if index == len(children):
        return True
    else:
        BrawlAPI.ShowMessage("Material contains texture reference to non-existent textures\n" + str(len(children)) + " : " + str(index), "Missing Textures")

def CheckAnimation(mat):
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".srt0" in wrapper.ExportFilter:
            for i in range(len(wrapper.Resource.Children)):
                if wrapper.Resource.Children[i].Name == mat:
                    return True
    BrawlAPI.ShowMessage("No srt0 corresponds to the material", "Missing Animation")

def ExportItems(path, name, mat):
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".mdl0mat" in wrapper.ExportFilter:
            if wrapper.Resource.Name == mat:
                wrapper.Resource.Export(Path.Combine(path, name + ".mdl0mat"))
                ExportAnimations(path, name, wrapper.Resource)
                ExportShaders(path, name, wrapper.Resource)
                CreateScripts(path, name, wrapper.Resource, ExportTextures(path, name, wrapper.Resource))

def ExportTextures(path, name, mat):
    children = mat.GetChildrenRecursive()
    wrappers = BrawlAPI.NodeWrapperList
    textureText = ""
    for wrapper in wrappers:
        if ".tex0" in wrapper.ExportFilter:
            for i in range(len(children)):
                if wrapper.Resource.Name == children[i].Name:
                    wrapper.Resource.Export(Path.Combine(path, wrapper.Resource.Name + ".tex0"))
                    if i > 0:
                        textureText += "            node" + str(i) + " = BrawlLib.SSBB.ResourceNodes.NodeFactory.FromFile(None, Path.Combine(BrawlAPI.PluginPath, \"MKWii Animations\", \"" + name + "\", \"" + wrapper.Resource.Name + ".tex0\"))\n            wrapper.Resource.GetOrCreateFolder[BrawlLib.SSBB.ResourceNodes.TEX0Node]().AddChild(node" + str(i) + ")\n"
                    else:
                        textureNames.append(wrapper.Resource.Name)
    textureText += "            node" + str(len(children)) + " = BrawlLib.SSBB.ResourceNodes.NodeFactory.FromFile(None, Path.Combine(BrawlAPI.PluginPath, \"MKWii Animations\", \"" + name + "\", \"" + name + ".srt0\"))\n            wrapper.Resource.GetOrCreateFolder[BrawlLib.SSBB.ResourceNodes.SRT0Node]().AddChild(node" + str(len(children)) + ")\n"
    return textureText

def ExportAnimations(path, name, mat):
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".srt0" in wrapper.ExportFilter:
            for i in range(len(wrapper.Resource.Children)):
                if wrapper.Resource.Children[i].Name == mat.Name:
                    wrapper.Resource.Export(Path.Combine(path, name + ".srt0"))

def ExportShaders(path, name, mat):
    wrappers = BrawlAPI.NodeWrapperList
    for wrapper in wrappers:
        if ".mdl0shade" in wrapper.ExportFilter:
            if wrapper.Resource.Name == mat.Shader:
                wrapper.Resource.Export(Path.Combine(path, name + ".mdl0shade"))

def CreatePath(name):
    Directory.CreateDirectory(Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", name))
    return Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", name)

def CreateScripts(path, name, mat, textureText):
    with StreamWriter(Path.Combine(path, "Import.py")) as sr:
        sr.Write("import BrawlLib\n"
        "import BrawlCrate\n"
        "from BrawlCrate.API import BrawlAPI\n"
        "from System.IO import Path\n\n"
        "def CreateShader():\n"
        "    wrappers = BrawlAPI.NodeWrapperList\n"
        "    for wrapper in wrappers:\n"
        "        if \".mdl0\" in wrapper.ExportFilter:\n"
        "            if wrapper.Resource.Name == \"course\":\n"
        "                shader = wrapper.NewShader()\n"
        "                shader.Replace(Path.Combine(BrawlAPI.PluginPath, \"MKWii Animations\", \"" + name + "\", \"" + name + ".mdl0shade\"))\n"
        "                return shader.Name\n\n"
        "def MatAmount():\n"
        "    StatInt = 0\n"
        "    wrappers = BrawlAPI.NodeWrapperList\n"
        "    for wrapper in wrappers:\n"
        "        if \".mdl0mat\" in wrapper.ExportFilter:\n"
        "            StatInt += 1\n"
        "    return StatInt\n\n"
        "def ReplaceTextureRef(x):\n"
        "    children = x.GetChildrenRecursive()\n"
        "    wrappers = BrawlAPI.NodeWrapperList\n"
        "    for wrapper in wrappers:\n"
        "        if \".png\" in wrapper.ExportFilter:\n"
        "            if wrapper.Resource.Name == children[0].Name:\n"
        "                wrapper.Resource.Replace(Path.Combine(BrawlAPI.PluginPath, \"MKWii Animations\", \"" + name + "\", \"" + textureNames[0] + ".tex0\"))\n"
        "                wrapper.Resource.Name = \"" + textureNames[0] + "\"\n"
        "                return\n\n"
        "def ImportTextures():\n"
        "    wrappers = BrawlAPI.NodeWrapperList\n"
        "    for wrapper in wrappers:\n"
        "        if \".brres\" in wrapper.ExportFilter:\n" + textureText +
        "\ndef CheckUse(shader):\n"
        "    amount = 0\n"
        "    wrappers = BrawlAPI.NodeWrapperList\n"
        "    for wrapper in wrappers:\n"
        "        if \".mdl0mat\" in wrapper.ExportFilter:\n"
        "            if wrapper.Resource.Shader == shader:\n"
        "                amount += 1\n"
        "    if amount == 1:\n"
        "        return True\n"
        "    else:\n"
        "        return False\n\n"
        "def SearchAndDestroy(mat):\n"
        "    children = mat.GetChildrenRecursive()\n"
        "    wrappers = BrawlAPI.NodeWrapperList\n"
        "    for wrapper in wrappers:\n"
        "        if \".png\" in wrapper.ExportFilter:\n"
        "            for i in range(len(children)):\n"
        "                if wrapper.Resource.Name == children[i].Name:\n"
        "                    if i > 0:\n"
        "                        wrapper.Delete()\n"
        "                        break\n"
        "        if \".mdl0shade\" in wrapper.ExportFilter:\n"
        "            if CheckUse(mat.Shader) == True and wrapper.Resource.Name == mat.Shader:\n"
        "                wrapper.Delete()\n"
        "        if \".srt0\" in wrapper.ExportFilter:\n"
        "            for i in range(len(wrapper.Resource.Children)):\n"
        "                if wrapper.Resource.Children[i].Name == mat.Name:\n"
        "                    wrapper.Delete()\n\n"
        "def ReplaceMaterial(x):\n"
        "    CurrentIndex = 0\n"
        "    wrappers = BrawlAPI.NodeWrapperList\n"
        "    for wrapper in wrappers:\n"
        "        if \".mdl0mat\" in wrapper.ExportFilter:\n"
        "            CurrentIndex += 1\n"
        "            if wrapper.Resource.Name == x:\n"
        "                SearchAndDestroy(wrapper.Resource)\n"
        "                ReplaceTextureRef(wrapper.Resource)\n"
        "                ImportTextures()\n"
        "                wrapper.Resource.Replace(Path.Combine(BrawlAPI.PluginPath, \"MKWii Animations\", \"" + name + "\", \"" + name + ".mdl0mat\"))\n"
        "                for i in range(MatAmount() - CurrentIndex):\n"
        "                    wrapper.Resource.DoMoveDown()\n"
        "                wrapper.Resource.Shader = CreateShader()\n"
        "                wrapper.Resource.Name = \"" + mat.Name + "\"\n"
        "                return\n"
        "    BrawlAPI.ShowMessage(\"No material with the name \" + x + \" exists\", \"Error\")\n\n"
        "#main function\n"
        "input = BrawlAPI.UserStringInput(\"Material Name\")\n"
        "if input != None:\n"
        "    ReplaceMaterial(input)")
    with StreamWriter(Path.Combine(path, "Delete Preset.py")) as sr:
        sr.Write("from System.IO import Directory\n"
        "from System.IO import Path\n"
        "from BrawlCrate.API import BrawlAPI\n\n"
        "if BrawlAPI.ShowYesNoWarning(\"Are you sure you want to delete this preset?\", \"Delete Preset\"):\n"
        "   Directory.Delete(Path.Combine(BrawlAPI.PluginPath, \"MKWii Animations\", \"" + name + "\"), True)")

#main function
name = BrawlAPI.UserStringInput("Preset Name", "")
if name != None:
    mat = BrawlAPI.UserStringInput("Material Name", "")
    if mat != None:
        if CheckMaterial(mat):
            ExportItems(CreatePath(name), name, mat)
