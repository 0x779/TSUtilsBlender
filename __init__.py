# Very small add on to start from

bl_info = {
    "name" : "TSUtils",
    "description" : "A collection of one-click utilities for general automation",
    "author" : "0x779",
    "version" : (0, 1, 0),
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "https://github.com/0x779/TSUtilsBlender",
    "category" : "3D View"
}

import bpy
from bpy.props import (
                       PointerProperty,
                       EnumProperty,
                       FloatProperty,
                       )

from bpy.types import (
                       PropertyGroup,
                       )


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class TSUtilProperties(PropertyGroup):

    metallicValue : FloatProperty(
        name="Metallic",
        default=0.5,
        max=1,
        min=0,
    )
    specularValue : FloatProperty(
        name="Specular",
        default=0.5,
        max=1,
        min=0,
    )
    roughnessValue : FloatProperty(
        name="Roughness",
        default=0.5,
        max=1,
        min=0,
    )
    emissionValue : FloatProperty(
        name="Emissive strength",
        default=0.5,
        max=1,
        min=0,
    )
    bumpValue : FloatProperty(
        name="Bump strength",
        default=0.15,
        max=1,
        min=0,
    )

    blendModeValue: EnumProperty(
        items=(
            ("OPAQUE", "Opaque", ""),
            ("CLIP", "Alpha Clip", ""),
            ("HASHED", "Alpha Hashed", ""),
            ("BLEND", "Alpha Blend", ""),
        ),
        name="Blend modes",
        default="OPAQUE",
        description="Blend modes",
    )

# ------------------------------------------------------------------------
#    Panel in Properties
# ------------------------------------------------------------------------

class PropertiesPanelUI(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "TSUtils"
    bl_idname = "tsutils.propertiespanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        row = layout.row()
        row.scale_y = 2.0
        row.operator(Screenshot_OT_custom.bl_idname)



# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class TSUtils_panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TS Utils"


class TSUtils_PT_panel_1(TSUtils_panel, bpy.types.Panel):
    bl_idname = "TSUtils_PT_panel_1"
    bl_label = "TS Utils"

    def draw(self, context):
        layout = self.layout

class TSUtils_PT_panel_2(TSUtils_panel, bpy.types.Panel):
    bl_parent_id = "TSUtils_PT_panel_1"
    bl_label = "Geometry"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Geometry")
        box = layout.box()
        box.operator(RemoveSubd_OT_custom.bl_idname)
        box.operator(Quadrify_OT_custom.bl_idname)
        box.operator(ApplyAllTransforms_OT_custom.bl_idname)
        box.operator(ApplyAllModifiers_OT_custom.bl_idname)
        layout.label(text="Normals")
        box = layout.box()
        box.operator(ClearSplitNormals_OT_custom.bl_idname)
        box.operator(FlipNormals_OT_custom.bl_idname)
        box.operator(NormalsOutside_OT_custom.bl_idname)
        box.operator(ClearSharp_OT_custom.bl_idname)
        layout.label(text="Scene")
        box = layout.box()
        box.operator(SelectGeo_OT_custom.bl_idname)
        box.operator(RemoveCams_OT_custom.bl_idname)
        box.operator(RemoveLights_OT_custom.bl_idname)
        box.operator(RemoveDupeMats_OT_custom.bl_idname)

class TSUtils_PT_panel_3(TSUtils_panel, bpy.types.Panel):
    bl_parent_id = "TSUtils_PT_panel_1"
    bl_label = "Materials"

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        layout.label(text="Material values")
        box = layout.box()
        box.prop(context.scene.tsutil_tool, 'metallicValue', slider=True)
        box.operator(SetMetallic_OT_custom.bl_idname)
        box.prop(context.scene.tsutil_tool, 'specularValue', slider=True)
        box.operator(SetSpecular_OT_custom.bl_idname)
        box.prop(context.scene.tsutil_tool, 'roughnessValue', slider=True)
        box.operator(SetRoughness_OT_custom.bl_idname)
        box.prop(context.scene.tsutil_tool, 'emissionValue', slider=True)
        box.operator(SetEmission_OT_custom.bl_idname)
        box.prop(context.scene.tsutil_tool, 'bumpValue', slider=True)
        box.operator(SetBump_OT_custom.bl_idname)

        layout.label(text="Material settings")
        box = layout.box()
        box.prop(scn.tsutil_tool, "blendModeValue", text="Blend Mode")
        box.operator(SetBlendModes_OT_custom.bl_idname)

        


class ClearSplitNormals_OT_custom(bpy.types.Operator):
    """Clear Custom Split Normals for selected objects"""
    bl_idname = "object.clearsplitnormals"
    bl_label = "Clear Custom Split Normals"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    try:
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.mesh.customdata_custom_splitnormals_clear()
                    except:
                        self.report({"WARNING"}, "Object has no custom split normals: " + obj.name + ", skipping")
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}

class FlipNormals_OT_custom(bpy.types.Operator):
    """Flip normals for the selected object(s)"""
    bl_idname = "object.flipnormals"
    bl_label = "Flip Normals"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(type="FACE")
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set(mode='OBJECT')
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}
        

class NormalsOutside_OT_custom(bpy.types.Operator):
    """Recalculate normals outside for the selected object(s)"""
    bl_idname = "object.normalsoutside"
    bl_label = "Recalculate normals outside"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(type="FACE")
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.normals_make_consistent(inside=False)
                    bpy.ops.object.mode_set(mode='OBJECT')
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}

class ClearSharp_OT_custom(bpy.types.Operator):
    """Clear all sharp edges for the selected object(s)"""
    bl_idname = "object.clearsharp"
    bl_label = "Clear all sharp edges"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(type="EDGE")
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.mark_sharp(clear=True)
                    bpy.ops.object.mode_set(mode='OBJECT')
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}

class Quadrify_OT_custom(bpy.types.Operator):
    """Convert selected objects from triangles to quads"""
    bl_idname = "object.quadrify"
    bl_label = "Convert to quads"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    for vert in obj.data.vertices:
                        vert.select = True #ensure all vertices are selected
                    bpy.ops.object.mode_set(mode='EDIT') #switch to edit mode
                    bpy.ops.mesh.remove_doubles() #remove doubles
                    bpy.ops.mesh.tris_convert_to_quads() #tris to quads
                    bpy.ops.object.mode_set(mode='OBJECT') #switch to object mode
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}

class SelectGeo_OT_custom(bpy.types.Operator):
    """Select geometry objects only"""
    bl_idname = "object.selectgeo"
    bl_label = "Select geometry only"

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            obj.select_set(obj.type == "MESH")
            bpy.context.view_layer.objects.active = obj
        self.report({"INFO"}, "Success")
        return {'FINISHED'}

class RemoveCams_OT_custom(bpy.types.Operator):
    """Remove all cameras"""
    bl_idname = "object.removecams"
    bl_label = "Remove all cameras"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type == 'CAMERA':
                obj.select_set(True)
            else:
                obj.select_set(False)
            bpy.ops.object.delete() 
        self.report({"INFO"}, "Success")
        return {'FINISHED'}

class RemoveLights_OT_custom(bpy.types.Operator):
    """Remove all lights"""
    bl_idname = "object.removelights"
    bl_label = "Remove all lights"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type == 'LIGHT':
                obj.select_set(True)
            else:
                obj.select_set(False)
            bpy.ops.object.delete() 
        self.report({"INFO"}, "Success")
        return {'FINISHED'}
        
class ApplyAllTransforms_OT_custom(bpy.types.Operator):
    """Apply all transforms for the selected object(s)"""
    bl_idname = "object.applytransforms"
    bl_label = "Apply all Transforms"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    for vert in obj.data.vertices:
                        vert.co = obj.matrix_world.copy() @ vert.co
                    obj.matrix_world.identity()
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}
        
class ApplyAllModifiers_OT_custom(bpy.types.Operator):
    """Apply all modifiers for the selected object(s)"""
    bl_idname = "object.applymodifiers"
    bl_label = "Apply all Modifiers"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    for m in obj.modifiers:
                        try:
                            bpy.context.view_layer.objects.active = obj
                            bpy.ops.object.modifier_apply(modifier=m.name)
                        except RuntimeError:
                            print(f"Error applying {m.name} to {obj.name}, removing it instead.")
                            obj.modifiers.remove(m)
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}

class RemoveSubd_OT_custom(bpy.types.Operator):
    """Removes subdivision modifiers for the selected object(s)"""
    bl_idname = "object.removesubd"
    bl_label = "Remove subdivision modifiers"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                        for m in obj.modifiers:
                            if(m.type == "SUBSURF"):
                                obj.modifiers.remove(m)
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}
           

class SetMetallic_OT_custom(bpy.types.Operator):
    """Set the metallic value for the selected object(s)"""
    bl_idname = "object.metallicset"
    bl_label = "Set Metallic"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':  
                    setMaterialValue('Metallic', context.scene.tsutil_tool.metallicValue, obj)
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}
        
class SetEmission_OT_custom(bpy.types.Operator):
    """Set the emissive value for the selected object(s)"""
    bl_idname = "object.emissionset"
    bl_label = "Set Emission"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':  
                    setMaterialValue('Emission Strength', context.scene.tsutil_tool.emissionValue, obj)
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}


class SetBump_OT_custom(bpy.types.Operator):
    """Set the bump value for the selected object(s)"""
    bl_idname = "object.bumpset"
    bl_label = "Set Bump"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':  
                    setMaterialValue('BUMP', context.scene.tsutil_tool.bumpValue, obj)
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}


class SetSpecular_OT_custom(bpy.types.Operator):
    """Set the specular value for the selected object(s)"""
    bl_idname = "object.specularset"
    bl_label = "Set Specular"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':  
                    setMaterialValue('Specular', context.scene.tsutil_tool.specularValue, obj)
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}           

class SetRoughness_OT_custom(bpy.types.Operator):
    """Set the roughness value for the selected object(s)"""
    bl_idname = "object.roughnessset"
    bl_label = "Set Roughness"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':  
                    setMaterialValue('Roughness', context.scene.tsutil_tool.roughnessValue, obj)
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}

class SetBlendModes_OT_custom(bpy.types.Operator):
    """Set the blend mode for the selected object(s)"""
    bl_idname = "object.blendmodeset"
    bl_label = "Set Blend Mode"

    def execute(self, context):
        if (len(bpy.context.selected_objects) > 0):
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':  
                        for mat in obj.material_slots:
                            mat.material.blend_method = context.scene.tsutil_tool.blendModeValue
            self.report({"INFO"}, "Success")
            return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Nothing selected")
            return {'CANCELLED'}

class Screenshot_OT_custom(bpy.types.Operator):
    """Screenshot"""
    bl_idname = "object.screenshot"
    bl_label = "Take screenshots"

    def execute(self, context):
        if bpy.data.is_saved:
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            bpy.ops.screen.screenshot(filepath=bpy.path.abspath("//Screenshot_viewport.png"))
            for area in bpy.context.workspace.screens[0].areas:
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.overlay.show_wireframes = True
                        ctx = {
                            "window": context.window, # current window, could also copy context
                            "area": area, # our 3D View (the first found only actually)
                            "region": None # just to suppress PyContext warning, doesn't seem to have any effect
                        }
                        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                        if bpy.app.version > (3, 0, 0):
                            with context.temp_override(**ctx): 
                                bpy.ops.screen.screenshot_area(filepath=bpy.path.abspath("//Screenshot_wireframe.png"))
                        else:
                            bpy.ops.screen.screenshot(filepath=bpy.path.abspath("//Screenshot_wireframe.png"))  # Blender <2.83 doesn't support screenshot_area
                        space.overlay.show_wireframes = False
                        self.report({"INFO"}, "Success")
                        return {'FINISHED'}
        else:
            self.report({"WARNING"}, "Save the file first")
            return {'CANCELLED'}

class RemoveDupeMats_OT_custom(bpy.types.Operator):
    """Remove duplicate materials"""
    bl_idname = "object.removedupemats"
    bl_label = "Remove duplicate materials"

    def execute(self, context):
        i = 0
        while i < len(bpy.data.materials):
            
            og_material = bpy.data.materials[i]
            
            print("og material: " + og_material.name)
            
            # get duplicate materials
            duplicate_materials = get_duplicate_materials(og_material)
            
            # replace all duplicates
            for duplicate_material in duplicate_materials:
                replace_material(duplicate_material, og_material)
            
            # adjust name to no trailing numbers
            if og_material.name[-3:].isnumeric() and og_material.name[-4] == ".":
                og_material.name = og_material.name[:-4]
                
            i = i+1
        self.report({"INFO"}, "Success")
        return {'FINISHED'}


def replace_material(bad_mat, good_mat):
    bad_mat.user_remap(good_mat)
    bpy.data.materials.remove(bad_mat)
    
    
def get_duplicate_materials(og_material):
    
    common_name = og_material.name
    
    if common_name[-3:].isnumeric():
        common_name = common_name[:-4]
    
    duplicate_materials = []
    
    for material in bpy.data.materials:
        if material is not og_material:
            name = material.name
            if name[-3:].isnumeric() and name[-4] == ".":
                name = name[:-4]
            
            if name == common_name:
                duplicate_materials.append(material)
    
    text = "{} duplicate materials found"
    print(text.format(len(duplicate_materials)))
    
    return duplicate_materials


def setMaterialValue(type, value, obj):
    for mat in obj.material_slots:
        for n in mat.material.node_tree.nodes:
            if n.type == 'BSDF_PRINCIPLED' and not type == 'BUMP':
                n.inputs[type].default_value = value
            if n.type == 'BUMP' and type == 'BUMP':
                n.inputs['Strength'].default_value = value  # Modify the strength value as desired


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    TSUtilProperties,
    PropertiesPanelUI,
    ClearSplitNormals_OT_custom,
    FlipNormals_OT_custom,
    NormalsOutside_OT_custom,
    ClearSharp_OT_custom,
    TSUtils_PT_panel_1,
    TSUtils_PT_panel_2,
    TSUtils_PT_panel_3,
    Quadrify_OT_custom,
    SelectGeo_OT_custom,
    RemoveCams_OT_custom,
    RemoveLights_OT_custom,
    RemoveDupeMats_OT_custom,
    ApplyAllTransforms_OT_custom,
    ApplyAllModifiers_OT_custom,
    RemoveSubd_OT_custom,
    SetMetallic_OT_custom,
    SetSpecular_OT_custom,
    SetRoughness_OT_custom,
    SetEmission_OT_custom,
    SetBump_OT_custom,
    SetBlendModes_OT_custom,
    Screenshot_OT_custom,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.tsutil_tool = PointerProperty(type=TSUtilProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.tsutil_tool


if __name__ == "__main__":
    register()