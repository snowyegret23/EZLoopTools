bl_info = {
    "name": "EZLooptools",
    "author": "Snowyegret",
    "version": (1, 0, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > EZLooptools",
    "description": "Apply LoopTools Flatten, Relax, or Space to faces",
    "category": "Mesh",
}

import bpy
from bpy.props import EnumProperty
from .ez_looptools_operation import EZLOOPTOOLS_OT_Operation
from .ez_looptools_panel import EZLOOPTOOLS_PT_Panel

def register():
    bpy.utils.register_class(EZLOOPTOOLS_OT_Operation)
    bpy.utils.register_class(EZLOOPTOOLS_PT_Panel)

    bpy.types.Scene.ezlooptools_direction = EnumProperty(
        name="Direction",
        description="Choose whether to operate on Horizontal or Vertical loops",
        items=[
            ('HORIZONTAL', "Horizontal", "Operate on horizontal loops"),
        ],
        default='HORIZONTAL'
    )

    bpy.types.Scene.ezlooptools_operation = EnumProperty(
        name="Operation",
        description="Choose the LoopTools operation",
        items=[
            ('FLATTEN', "Flatten", "Flatten the loops"),
            ('RELAX', "Relax", "Relax the loops"),
            ('SPACE', "Space", "Space the loops evenly"),
        ],
        default='FLATTEN'
    )

def unregister():
    del bpy.types.Scene.ezlooptools_direction
    del bpy.types.Scene.ezlooptools_operation

    bpy.utils.unregister_class(EZLOOPTOOLS_PT_Panel)
    bpy.utils.unregister_class(EZLOOPTOOLS_OT_Operation)

if __name__ == "__main__":
    register()
