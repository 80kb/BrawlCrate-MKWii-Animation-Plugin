__author__ = "BillyNoodles"
__version__ = "2.0.0"

from BrawlCrate.API import BrawlAPI
from BrawlLib.SSBB.ResourceNodes import *

from System.IO import Directory
from System.IO import Path
from System.IO import StreamWriter

# TODO: Add proper error messages
# TODO: Create dynamic import preset script

textures = []

def check_textures(material, preset_name):
    tex_refs = material.GetChildrenRecursive()

    # find texture nodes for corresponding material texture references
    for reference in tex_refs:
        for texture in BrawlAPI.NodeListOfType[TEX0Node]():
            if texture.Name == reference.Name:

                # unique name export texture
                texture.Name = preset_name + "-tex" + str(len(textures))

                # unique name export reference
                reference.Name = texture.Name

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

def export_animations(target, preset_name):
    # verify and gather target material data
    for material in BrawlAPI.NodeListOfType[MDL0MaterialNode]():
        if material.Name == target:

            # unique export material
            export_mat = material

            if check_textures(export_mat, preset_name) and check_animations(export_mat):

                # create preset directory
                path = Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", preset_name)
                Directory.CreateDirectory(path)

                # export material
                export_mat.Export(Path.Combine(path, export_mat.Name + ".mdl0mat"))

                # export textures
                for texture in textures:
                    texture.Export(Path.Combine(path, texture.Name + ".tex0"))

                # export animation
                for srt in BrawlAPI.NodeListOfType[SRT0Node]():
                    for srt_subnode in srt.Children:
                        if srt_subnode.Name == export_mat.Name:
                            srt.Export(Path.Combine(path, srt.Name + ".srt0"))
                            break

    return "Material name not found"

preset = BrawlAPI.UserStringInput("New Preset Name", "")
if preset != None:

    # check if preset already exists
    if not Directory.Exists(Path.Combine(BrawlAPI.PluginPath, "MKWii Animations", preset)):

        target = BrawlAPI.UserStringInput("Target Material", "")
        if target != None:

            export_animations(target, preset)

    else:

        BrawlAPI.ShowMessage("Preset name already used", "")
