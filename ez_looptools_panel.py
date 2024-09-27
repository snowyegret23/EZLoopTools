import bpy
from bpy.types import Panel

class EZLOOPTOOLS_PT_Panel(Panel):
    bl_label = "EZ LoopTools"
    bl_idname = "VIEW3D_PT_ez_looptools_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EZLooptools'

    def draw(self, context):
        layout = self.layout

        layout.label(text="Apply to Loops:")
        layout.prop(context.scene, 'ezlooptools_direction', expand=True)
        layout.prop(context.scene, 'ezlooptools_operation', expand=True)
        layout.operator('mesh.ezlooptools_operation', text='Apply')
