bl_info = {
    "name": "Yui's Modding Toolkit",
    "description": "Useful toolkit for modding",
    "author": "0w0-Yui <yui@lioat.cn>",
    "version": (0, 2, 0),
    "blender": (2, 83, 0),
    "location": "View 3D > Toolshelf",
    "doc_url": "https://github.com/0w0-Yui/modtoolkit",
    "tracker_url": "https://github.com/0w0-Yui/modtoolkit/issues",
    "category": "Object",
}

import bpy
from bpy.props import IntProperty, StringProperty, PointerProperty, CollectionProperty
from bpy.types import (
    PropertyGroup,
    UIList,
    Operator,
    Panel,
    Menu,
    Scene,
    Object,
)
from bpy.utils import register_class, unregister_class
from bl_operators.presets import AddPresetBase
import os


class ListItem(PropertyGroup):
    vg: StringProperty(name="vg", description="vertex group name", default="")
    bone: StringProperty(name="bone", description="target bone name", default="")


class MY_UL_List(UIList):
    bl_idname = "MY_UL_List"
    bl_label = ""

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        custom_icon = "FORWARD"
        mesh = bpy.data.objects[context.scene.mesh_pointer.name]
        armature = bpy.data.objects[context.scene.armature_pointer.name].data
        layout.prop_search(item, "vg", mesh, "vertex_groups", text="")
        layout.label(text=item.name, icon=custom_icon)
        layout.prop_search(item, "bone", armature, "bones", text="")


class LIST_OT_NewItem(Operator):
    bl_idname = "my_list.new_item"
    bl_label = "add"

    def execute(self, context):
        context.scene.my_list.add()

        return {"FINISHED"}


class LIST_OT_DeleteItem(Operator):
    bl_idname = "my_list.delete_item"
    bl_label = "remove"

    @classmethod
    def poll(cls, context):
        return context.scene.my_list

    def execute(self, context):
        my_list = context.scene.my_list
        index = context.scene.list_index

        my_list.remove(index)
        context.scene.list_index = min(max(0, index - 1), len(my_list) - 1)

        return {"FINISHED"}


class menu_presets(Menu):
    bl_label = "presets"
    bl_icon = "PRESET"
    preset_subdir = "yuinomodtools"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


class add_presets(AddPresetBase, Operator):
    bl_idname = "menu.add_preset"
    bl_label = "Add Preset"
    bl_description = "Add Preset"
    preset_menu = "menu_presets"

    # variable used for all preset values
    preset_defines = ["s = bpy.context.scene"]

    # properties to store in the preset
    preset_values = ["s.my_list"]

    # where to store the preset
    preset_subdir = "yuinomodtools"


class CreditPanel(Panel):
    bl_label = "Credit"
    bl_idname = "OBJECT_PT_credit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "YuiのModToolkit"

    def draw(self, context):
        layout = self.layout
        name = "0w0-Yui"
        op = layout.operator("wm.url_open", text=f"Github: {name}")
        op.url = "https://github.com/0w0-Yui"


class OpenPresetFolder(Operator):
    bl_idname = "menu.open_preset_folder"
    bl_label = "open presets folder"

    def execute(self, context):
        os.system(
            "explorer "
            + bpy.utils.resource_path("USER")
            + "\\scripts\\presets\\yuinomodtools"
        )
        return {"FINISHED"}


class MyAddonPanel(Panel):
    bl_label = "Vertex Group Rename Tool"
    bl_idname = "OBJECT_PT_my_addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "YuiのModToolkit"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        armature = scene.armature_pointer
        mesh = scene.mesh_pointer

        box = layout.box()
        box.label(text="select an armature:")
        box.prop(scene, "armature_pointer", text="", icon="ARMATURE_DATA")
        box.label(text="select a mesh:")
        box.prop(scene, "mesh_pointer", text="", icon="MESH_DATA")

        msg = Kit.check_pointer(mesh, armature)

        if msg == "":
            row = box.row(align=True)
            row.operator(StartAssign.bl_idname, text=StartAssign.bl_label)
            row.operator(Stop.bl_idname, text=Stop.bl_label)

            box1 = layout.box()

            box1.label(text=context.scene.vertex_group_string)

            row = box1.row(align=True)
            row.operator(Next.bl_idname, text=Next.bl_label)
            row.operator(Skip.bl_idname, text=Skip.bl_label)

            row = box1.row()
            row.template_list(
                MY_UL_List.bl_idname, "The_List", scene, "my_list", scene, "list_index"
            )

            row1 = box1.row(align=True)
            row1.operator(LIST_OT_NewItem.bl_idname, text=LIST_OT_NewItem.bl_label)
            row1.operator(
                LIST_OT_DeleteItem.bl_idname, text=LIST_OT_DeleteItem.bl_label
            )
            box1.operator(Done.bl_idname, text=Done.bl_label)

            box2 = layout.box()
            row = box2.row()
            row.menu(
                menu_presets.__name__,
                text=menu_presets.bl_label,
                icon=menu_presets.bl_icon,
            )
            row1 = box2.row(align=True)
            row1.operator(add_presets.bl_idname, text="save")
            row1.operator(add_presets.bl_idname, text="delete").remove_active = True
            row1 = box2.row(align=True)
            row1.operator(OpenPresetFolder.bl_idname, text=OpenPresetFolder.bl_label)
        else:
            layout.label(text=msg, icon="ERROR")


class Kit(Operator):
    def check_pointer(obj, armature):
        if obj is None or armature is None:
            return "no armature/mesh selected"
        # 遍历每个修改器
        for modifier in obj.modifiers:
            # 判断修改器是否是骨骼修改器
            if modifier.type == "ARMATURE":
                if modifier.object == bpy.data.objects[armature.name]:
                    return ""
        return f'no modifier for "{armature.name}" found in "{obj.name}"'

    def add_armature_modifier(obj, armature):
        obj = bpy.context.selected_objects[0]
        # 遍历每个修改器
        for modifier in obj.modifiers:
            # 判断修改器是否是骨骼修改器
            if modifier.type == "ARMATURE":
                # 移除修改器
                obj.modifiers.remove(modifier)
        armature_modifier = obj.modifiers.new(name="Armature", type="ARMATURE")
        armature_modifier.object = bpy.data.objects[armature.name]

    def select(obj):
        bpy.data.objects[obj.name].select_set(True)

    def mode_set(mode):
        bpy.ops.object.mode_set(mode=mode)

    def report(message, title="INFO", icon="INFO"):
        def draw(self, context):
            self.layout.label(text=message)

        bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

    def get_all_vg(obj):
        vg_list = []
        for vg in obj.vertex_groups:
            # 获取顶点组的名称和索引
            vg_list.append({"name": vg.name, "index": vg.index})
        return vg_list

    def select_vg(name):
        bpy.ops.object.vertex_group_set_active(group=name)

    def update_label_vg(context, string):
        context.scene.vertex_group_string = f"current vertex group: {string}"

    def is_mesh(scene, obj):
        return obj.type == "MESH"

    def is_armature(scene, obj):
        return obj.type == "ARMATURE"


class StartAssign(Operator):
    bl_idname = "object.start_assignment"
    bl_label = "start assign"

    def execute(self, context):
        vg_list = []
        selected_mesh = context.scene.mesh_pointer
        print("start quick assign")
        context.scene.assign_index = 0
        vg_list = Kit.get_all_vg(selected_mesh)
        Kit.select_vg(vg_list[context.scene.assign_index]["name"])
        Kit.update_label_vg(context, vg_list[context.scene.assign_index]["name"])
        return {"FINISHED"}


class Next(Operator):
    bl_idname = "object.next"
    bl_label = "next"

    def execute(self, context):
        if bpy.context.object.mode != "WEIGHT_PAINT":
            Kit.report("please enter weight paint mode")
            return {"FINISHED"}
        selected_mesh = context.scene.mesh_pointer
        selected_bone = bpy.context.selected_pose_bones
        list = context.scene.my_list
        index = context.scene.assign_index
        vg_list = Kit.get_all_vg(selected_mesh)
        if len(selected_bone) == 0:
            Kit.report("no bone selected")
            return {"FINISHED"}
        if index >= 0 and index < len(vg_list):
            item = list.add()
            item.vg = vg_list[index]["name"]
            item.bone = selected_bone[0].name
            print("{item.vg} -> {item.bone} added")
            index += 1
        if index < len(vg_list):
            Kit.select_vg(vg_list[index]["name"])
            Kit.update_label_vg(context, vg_list[index]["name"])
        else:
            context.scene.vertex_group_string = f"current vertex group: {None}"
        context.scene.assign_index = index
        return {"FINISHED"}


class Skip(Operator):
    bl_idname = "object.skip"
    bl_label = "skip"

    def execute(self, context):
        if bpy.context.object.mode != "WEIGHT_PAINT":
            Kit.report("please enter weight paint mode")
            return {"FINISHED"}
        selected_mesh = context.scene.mesh_pointer
        index = context.scene.assign_index
        vg_list = Kit.get_all_vg(selected_mesh)
        if index >= 0 and index < len(vg_list):
            print("{item.vg} skipped")
            index += 1
        if index < len(vg_list):
            Kit.select_vg(vg_list[index]["name"])
            Kit.update_label_vg(context, vg_list[context.scene.assign_index]["name"])
        else:
            context.scene.vertex_group_string = f"current vertex group: {None}"
        context.scene.assign_index = index
        return {"FINISHED"}


class Stop(Operator):
    bl_idname = "object.stop"
    bl_label = "reset assign"

    def execute(self, context):
        index = 0
        context.scene.vertex_group_string = f"current vertex group: {None}"
        context.scene.assign_index = index
        print("stop quick assign")
        return {"FINISHED"}


class Done(Operator):
    bl_idname = "object.done"
    bl_label = "rename"

    def execute(self, context):
        if bpy.context.object.mode != "WEIGHT_PAINT":
            Kit.report("please enter weight paint mode")
            return {"FINISHED"}
        mesh = bpy.data.objects[context.scene.mesh_pointer.name]
        my_list = context.scene.my_list
        vg_list = Kit.get_all_vg(mesh)
        vertex_groups = mesh.vertex_groups
        for i in my_list:
            for vg in vg_list:
                if vg["name"] == i.bone:
                    old_name = vg["name"]
                    new_suffix = ".old.001"
                    vertex_group = vertex_groups.get(old_name)
                    new_name = old_name + new_suffix
                    index = 1
                    while new_name in vertex_groups:
                        index += 1
                        new_name = f"{old_name}.old.{str(index).zfill(3)}"
                    if vertex_group is not None:
                        vertex_group.name = new_name
                        print("{old_name} -> {new_name} renamed")
                    else:
                        print(f'No vertex group found with name "{old_name}"')

        duplicates_dict = {}
        for i, item in enumerate(my_list):
            if item.bone in duplicates_dict:
                duplicates_dict[item.bone].append(i)
            else:
                duplicates_dict[item.bone] = [i]

        # 从字典中提取出所有重复的键值对，即重复的bone属性的值和它们的位置
        duplicates = [[k, v] for k, v in duplicates_dict.items() if len(v) > 1]

        for dup in duplicates:
            merged_group_name = dup[0]
            my_list_index = dup[1]
            vertex_group_names = []
            for i in my_list_index:
                vertex_group_names.append(my_list[i].vg)
            vertex_group = mesh.vertex_groups.new(name=merged_group_name)

            for id, vert in enumerate(mesh.data.vertices):
                available_groups = [v_group_elem.group for v_group_elem in vert.groups]
                weights = []
                for vertex_group_name in vertex_group_names:
                    if mesh.vertex_groups[vertex_group_name].index in available_groups:
                        weights.append(mesh.vertex_groups[vertex_group_name].weight(id))
                print(f"{vertex_group_names} -> {merged_group_name} renamed with merge")
                sum = 0
                for num in weights:
                    sum += num
                if sum > 0:
                    vertex_group.add([id], sum, "REPLACE")

        for item in my_list:
            is_dup = False
            for dup in duplicates:
                if item.bone == dup[0]:
                    is_dup = True
            if is_dup:
                continue
            old_name = item.vg
            new_name = item.bone
            Kit.select_vg(old_name)
            bpy.ops.object.vertex_group_copy()
            vertex_groups[-1].name = new_name
            print(f"{old_name} -> {new_name} renamed")
        Kit.report("done!")
        print("done!")
        return {"FINISHED"}


classes = (
    MyAddonPanel,
    StartAssign,
    Next,
    Done,
    ListItem,
    MY_UL_List,
    LIST_OT_NewItem,
    LIST_OT_DeleteItem,
    menu_presets,
    add_presets,
    CreditPanel,
    OpenPresetFolder,
    Stop,
    Skip,
)


def register():
    for cls in classes:
        register_class(cls)

    Scene.armature_pointer = PointerProperty(type=Object, poll=Kit.is_armature)
    Scene.mesh_pointer = PointerProperty(type=Object, poll=Kit.is_mesh)
    Scene.my_list = CollectionProperty(type=ListItem)
    Scene.list_index = IntProperty(name="list index", default=0)
    Scene.assign_index = IntProperty(name="global index", default=-1)
    Scene.vertex_group_string = StringProperty(
        name="vertex_group_string", default=f"current vertex group: {None}"
    )


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    del Scene.armature_pointer
    del Scene.mesh_pointer
    del Scene.my_list
    del Scene.list_index
    del Scene.assign_index
    del Scene.vertex_group_string


if __name__ == "__main__":
    register()
