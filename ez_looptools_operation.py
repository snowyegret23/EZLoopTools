import bpy
import bmesh
from bpy.types import Operator

class EZLOOPTOOLS_OT_Operation(Operator):
    bl_idname = "mesh.ezlooptools_operation"
    bl_label = "EZ LoopTools Operation"
    bl_description = "Apply LoopTools Flatten, Relax, or Space to loops"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if 'mesh_looptools' not in bpy.context.preferences.addons:
            self.report({'ERROR'}, "LoopTools addon needs to be enabled")
            return {'CANCELLED'}

        obj = context.object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        context.tool_settings.mesh_select_mode = (False, True, False)

        selected_faces = [f for f in bm.faces if f.select]
        if not selected_faces:
            self.report({'ERROR'}, "No faces selected")
            return {'CANCELLED'}

        selected_edges = set()
        for face in selected_faces:
            selected_edges.update(face.edges)

        processed_edges = set()
        loops = []

        direction = context.scene.ezlooptools_direction
        operation = context.scene.ezlooptools_operation

        for edge in selected_edges:
            if edge in processed_edges:
                continue

            for e in bm.edges:
                e.select = False

            edge.select = True

            if direction == 'HORIZONTAL':
                bpy.ops.mesh.loop_multi_select(ring=False)
            elif direction == 'VERTICAL':
                bpy.ops.mesh.loop_multi_select(ring=True)
            else:
                self.report({'ERROR'}, "Invalid direction")
                return {'CANCELLED'}

            loop_edges = [e for e in bm.edges if e.select and e in selected_edges]

            if loop_edges:
                loops.append(loop_edges.copy())
                processed_edges.update(loop_edges)

        for loop_edges in loops:
            for e in bm.edges:
                e.select = False
            for e in loop_edges:
                e.select = True

            if operation == 'FLATTEN':
                bpy.ops.mesh.looptools_flatten()
            elif operation == 'RELAX':
                bpy.ops.mesh.looptools_relax()
            elif operation == 'SPACE':
                bpy.ops.mesh.looptools_space()
            else:
                self.report({'ERROR'}, "Invalid operation")
                return {'CANCELLED'}

        bmesh.update_edit_mesh(obj.data)

        self.report({'INFO'}, f"Applied {operation} to {len(loops)} loops")

        return {'FINISHED'}
