__author__ = "BillyNoodles"
__version__ = "2.0.0"

from BrawlCrate.API import BrawlAPI
from BrawlCrate.UI import MainForm
from BrawlLib.SSBB.ResourceNodes import *

from System.IO import Directory
from System.IO import Path
from System.IO import File
from System.IO import StreamWriter

# TODO: Add proper error messages

def check_textures(material):
    tex_refs = material.GetChildrenRecursive()

    # find texture nodes for corresponding material texture references
    for reference in tex_refs:
        for texture in BrawlAPI.NodeListOfType[TEX0Node]():
            if texture.Name == reference.Name:
                textures.append(texture)
                break

    return True if len(textures) == len(tex_refs) else False

def check_animations(material):
    # find corresponding srt0 nodes
    for srt in BrawlAPI.NodeListOfType[SRT0Node]():
        for srt_subnode in srt.Children:
            if srt_subnode.Name == material.Name:
                return True
    
    return False

def export_animations():
    # verify and gather target material data
    for material in BrawlAPI.NodeListOfType[MDL0MaterialNode]():
        if material.Name == target:
            if check_textures(material) and check_animations(material):

                # create preset directory
                Directory.CreateDirectory(path)

                # export material
                material.Export(Path.Combine(path, material.Name + ".mdl0mat"))

                # export shader
                material.ShaderNode.Export(Path.Combine(path, material.Name + ".mdl0shade"))

                # export textures
                for texture in textures:
                    texture.Export(Path.Combine(path, texture.Name + ".tex0"))

                # export animation
                for srt in BrawlAPI.NodeListOfType[SRT0Node]():
                    for srt_subnode in srt.Children:
                        if srt_subnode.Name == material.Name:
                            srt.Export(Path.Combine(path, srt.Name + ".srt0"))
                            break
                
                # only once
                break

if BrawlAPI.RootNode != None:

    # prompt for preset name
    preset = BrawlAPI.UserStringInput("New Preset Name", "")
    if preset != None:

        # check if preset already exists
        path = Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", preset)
        if not Directory.Exists(path):

            # prompt for target material
            target = BrawlAPI.UserStringInput("Target Material", "")
            if target != None:

                textures = []
                export_animations()

                # edit and include import and delete script to preset folder
                import_script = File.ReadAllText(Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", "Import Preset.txt"))
                import_script = import_script.Replace("preset_name = \"\"", "preset_name = \"" + preset + "\"")

                delete_script = File.ReadAllText(Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", "Remove Preset.txt"))
                delete_script = delete_script.Replace("preset_name = \"\"", "preset_name = \"" + preset + "\"")

                with StreamWriter(Path.Combine(path, "Import " + preset + ".py")) as writer:
                    writer.Write(import_script)

                with StreamWriter(Path.Combine(path, "Remove " + preset + ".py")) as writer:
                    writer.Write(delete_script)

                BrawlAPI.RootNode._mainForm.reloadPluginsToolStripMenuItem_Click(None, None)
        else:

            BrawlAPI.ShowMessage("Preset name already in use", "")
