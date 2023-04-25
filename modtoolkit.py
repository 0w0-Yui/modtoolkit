bl_info = {
    "name": "Yui's Modding Toolkit",
    "description": "Useful toolkit for modding",
    "author": "0w0-Yui <yui@lioat.cn>",
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "View 3D > Toolshelf",
    "doc_url": "https://github.com/0w0-Yui/modtoolkit",
    "tracker_url": "https://github.com/0w0-Yui/modtoolkit/issues",
    "category": "Object",
}

import bpy
from bpy.props import IntProperty, StringProperty, PointerProperty, CollectionProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, Menu, Scene, Armature, Mesh
from bl_operators.presets import AddPresetBase
import os


class ListItem(PropertyGroup):
    vg: StringProperty(name="vg", description="vertex group name", default="")
    bone: StringProperty(name="bone", description="target bone name", default="")


class MY_UL_List(UIList):
    bl_idname = "MY_UL_List"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        custom_icon = "FORWARD"
        mesh = bpy.data.objects[context.scene.mesh_pointer.name]
        armature = bpy.data.armatures.get(context.scene.armature_pointer.name)
        layout.prop_search(item, "vg", mesh, "vertex_groups", text="")
        layout.label(text=item.name, icon=custom_icon)
        layout.prop_search(item, "bone", armature, "bones", text="")


class LIST_OT_NewItem(Operator):
    bl_idname = "my_list.new_item"
    bl_label = "添加一项"

    def execute(self, context):
        context.scene.my_list.add()

        return {"FINISHED"}


class LIST_OT_DeleteItem(Operator):
    bl_idname = "my_list.delete_item"
    bl_label = "Deletes an item"

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
    bl_category = "My Addon"

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
    bl_category = "My Addon"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.label(text="Select an armature:")
        box.prop(scene, "armature_pointer", text="")
        box.label(text="Select an mesh:")
        box.prop(scene, "mesh_pointer", text="")

        box.operator("object.start_assignment", text="start assign")

        box1 = layout.box()

        box1.label(text=context.scene.vertex_group_string)

        box1.operator("object.next", text="next")

        row = box1.row()
        row.template_list(
            "MY_UL_List", "The_List", scene, "my_list", scene, "list_index"
        )

        row1 = box1.row()
        row1.operator("my_list.new_item", text="add")
        row1.operator("my_list.delete_item", text="remove")
        box1.operator(Done.bl_idname, text=Done.bl_label)

        box2 = layout.box()
        row = box2.row()
        row.menu(menu_presets.__name__, text=menu_presets.bl_label, icon="PRESET")
        row1 = box2.row(align=True)
        row1.operator("menu.add_preset", text="save")
        row1.operator("menu.add_preset", text="remove").remove_active = True
        row1 = box2.row(align=True)
        row1.operator(OpenPresetFolder.bl_idname, text=OpenPresetFolder.bl_label)


class Kit(Operator):
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
        obj = bpy.data.objects[obj.name]
        vg_list = []
        for vg in obj.vertex_groups:
            # 获取顶点组的名称和索引
            vg_list.append({"name": vg.name, "index": vg.index})
        return vg_list

    def select_vg(name):
        bpy.ops.object.vertex_group_set_active(group=name)

    def update_label_vg(context, string):
        context.scene.vertex_group_string = f"current vertex group: {string}"



class StartAssign(Operator):
    bl_idname = "object.start_assignment"
    bl_label = "start assign"

    def execute(self, context):
        vg_list = []
        selected_mesh = context.scene.mesh_pointer
        print(context.scene.assign_index)
        context.scene.assign_index = 0
        vg_list = Kit.get_all_vg(selected_mesh)
        Kit.select_vg(vg_list[context.scene.assign_index]["name"])
        Kit.update_label_vg(context, vg_list[context.scene.assign_index]["name"])
        return {"FINISHED"}


class Next(Operator):
    bl_idname = "object.next"
    bl_label = "next"

    def execute(self, context):
        selected_mesh = context.scene.mesh_pointer
        selected_bone = bpy.context.selected_pose_bones
        list = context.scene.my_list
        index = context.scene.assign_index
        vg_list = Kit.get_all_vg(selected_mesh)
        print(selected_bone[0].name, index, len(vg_list))
        if selected_bone != None and index >= 0 and index < len(vg_list):
            print("added")
            item = list.add()
            item.vg = vg_list[index]["name"]
            item.bone = selected_bone[0].name
            index += 1
        if index < len(vg_list):
            Kit.select_vg(vg_list[index]["name"])
            Kit.update_label_vg(context, vg_list[context.scene.assign_index]["name"])
        context.scene.assign_index = index
        return {"FINISHED"}


class Done(Operator):
    bl_idname = "object.done"
    bl_label = "rename"

    def execute(self, context):
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

        return {"FINISHED"}


def register():
    bpy.utils.register_class(MyAddonPanel)
    bpy.utils.register_class(StartAssign)
    bpy.utils.register_class(Next)
    bpy.utils.register_class(Done)
    bpy.utils.register_class(ListItem)
    bpy.utils.register_class(MY_UL_List)
    bpy.utils.register_class(LIST_OT_NewItem)
    bpy.utils.register_class(LIST_OT_DeleteItem)
    bpy.utils.register_class(menu_presets)
    bpy.utils.register_class(add_presets)
    bpy.utils.register_class(CreditPanel)
    bpy.utils.register_class(OpenPresetFolder)

    Scene.armature_pointer = PointerProperty(type=Armature)
    Scene.mesh_pointer = PointerProperty(type=Mesh)
    Scene.my_list = CollectionProperty(type=ListItem)
    Scene.list_index = IntProperty(name="list index", default=0)
    Scene.assign_index = IntProperty(name="global index", default=-1)
    Scene.vertex_group_string = StringProperty(
        name="vertex_group_string", default=f"current vertex group: {None}"
    )


def unregister():
    bpy.utils.unregister_class(MyAddonPanel)
    bpy.utils.unregister_class(StartAssign)
    bpy.utils.unregister_class(Next)
    bpy.utils.unregister_class(Done)
    bpy.utils.unregister_class(ListItem)
    bpy.utils.unregister_class(MY_UL_List)
    bpy.utils.unregister_class(LIST_OT_NewItem)
    bpy.utils.unregister_class(LIST_OT_DeleteItem)
    bpy.utils.unregister_class(menu_presets)
    bpy.utils.unregister_class(add_presets)
    bpy.utils.unregister_class(CreditPanel)
    bpy.utils.unregister_class(OpenPresetFolder)

    del Scene.armature_pointer
    del Scene.mesh_pointer
    del Scene.my_list
    del Scene.list_index
    del Scene.assign_index
    del Scene.vertex_group_string


if __name__ == "__main__":
    register()
