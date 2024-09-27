import bpy
import bmesh
from bpy.types import Operator

class EZLOOPTOOLS_OT_Operation(Operator):
    bl_idname = "mesh.ezlooptools_operation"
    bl_label = "EZ LoopTools Operation"
    bl_description = "Apply LoopTools Flatten, Relax, or Space to loops"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        import bmesh

        # LoopTools 애드온이 활성화되어 있는지 확인
        if 'mesh_looptools' not in bpy.context.preferences.addons:
            self.report({'ERROR'}, "LoopTools addon needs to be enabled")
            return {'CANCELLED'}

        obj = context.object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}

        # 에디트 모드에서 bmesh 가져오기
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)

        # Edge Select 모드로 전환
        context.tool_settings.mesh_select_mode = (False, True, False)

        # 선택된 면 가져오기
        selected_faces = [f for f in bm.faces if f.select]
        if not selected_faces:
            self.report({'ERROR'}, "No faces selected")
            return {'CANCELLED'}

        # 선택된 면에서 엣지 수집
        selected_edges = set()
        for face in selected_faces:
            selected_edges.update(face.edges)

        # 이미 처리된 엣지를 추적하기 위한 집합
        processed_edges = set()
        loops = []

        # 방향 및 작업 가져오기
        direction = context.scene.ezlooptools_direction
        operation = context.scene.ezlooptools_operation

        for edge in selected_edges:
            if edge in processed_edges:
                continue

            # 모든 엣지 선택 해제
            for e in bm.edges:
                e.select = False

            # 엣지 선택
            edge.select = True

            # 루프 또는 링 선택
            if direction == 'HORIZONTAL':
                bpy.ops.mesh.loop_multi_select(ring=False)
            elif direction == 'VERTICAL':
                bpy.ops.mesh.loop_multi_select(ring=True)
            else:
                self.report({'ERROR'}, "Invalid direction")
                return {'CANCELLED'}

            # 선택된 루프 엣지 수집
            loop_edges = [e for e in bm.edges if e.select and e in selected_edges]

            if loop_edges:
                loops.append(loop_edges.copy())
                processed_edges.update(loop_edges)

        # 각 루프에 선택된 작업 적용
        for loop_edges in loops:
            # 루프의 엣지 선택
            for e in bm.edges:
                e.select = False
            for e in loop_edges:
                e.select = True

            # 작업 적용
            if operation == 'FLATTEN':
                bpy.ops.mesh.looptools_flatten()
            elif operation == 'RELAX':
                bpy.ops.mesh.looptools_relax()
            elif operation == 'SPACE':
                bpy.ops.mesh.looptools_space()
            else:
                self.report({'ERROR'}, "Invalid operation")
                return {'CANCELLED'}

        # 메쉬 업데이트
        bmesh.update_edit_mesh(obj.data)

        self.report({'INFO'}, f"Applied {operation} to {len(loops)} loops")

        return {'FINISHED'}
