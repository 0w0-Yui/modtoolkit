bl_info = {
    "name": "Yui's Modding Toolkit",
    "description": "Useful toolkit for modding",
    "author": "0w0-Yui <yui@lioat.cn>",
    "version": (0, 5, 1),
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


class Localization:
    localizations = {
        "en": {
            # pointer panel
            "mainpanel.label": "Vertex Group Rename Tool",
            "mainpanel.armature_pointer": "select an armature:",
            "mainpanel.mesh_pointer": "select a mesh:",
            "mainpanel.start_assignment": "start assign",
            "mainpanel.start_assignment.tip": "Start assign bones' name to vertex groups",
            "mainpanel.stop": "reset assign",
            "mainpanel.stop.tip": "Stop and reset the assign process",
            # vertex group assignment panel
            "mainpanel.vertex_group_string": "current vertex group: ",
            "mainpanel.next": "next",
            "mainpanel.next.tip": "Add current selected bones and vertex group to rename list",
            "mainpanel.skip": "skip",
            "mainpanel.skip.tip": "Skip assignment for current bone",
            "ul_list.vg.tip": "vertex group name",
            "ul_list.bone.tip": "target bone name",
            "my_list.new_item": "add",
            "my_list.new_item.tip": "Add an item from list",
            "my_list.delete_item": "remove",
            "my_list.delete_item.tip": "Remove an item from list",
            "mainpanel.done": "start rename",
            "mainpanel.done.tip": "Start rename for the current rename list",
            # presets panel
            "menu_presets": "presets",
            "presets.save": "save",
            "presets.delete": "delete",
            "presets.tip": "Save or delete preset from local",
            "presets.open_folder": "open presets folder",
            "presets.open_folder.tip": "Open presets folder in the explorer",
            # misc panel
            "miscpanel.label": "Misc",
            "miscpanel.remove_empty": "Remove Empty VG",
            "miscpanel.remove_empty.tip": "Remove all empty vertex group for active mesh",
            "miscpanel.remove_unused": "Remove Unused VG",
            "miscpanel.remove_unused.tip": "Remove all unused vertex group for active mesh",
            "miscpanel.merge_mats": "Auto Merge Mats",
            "miscpanel.merge_mats.tip": "Merge materials with same texture for active mesh",
            "miscpanel.select_seams": "Select Seams",
            "miscpanel.select_seams.tip": "Select edges marked as seams for active mesh",
            # credit panel
            "creditpanel.label": "Credit",
            "creditpanel.github": "Github: 0w0-Yui",
            "creditpanel.bilibili": "bilibili: 0w0-Yui",
            # report
            "report.no_active_mesh": "no active mesh!",
            "report.no_active_bone": "no bone selected",
            "report.no_active": "no armature/mesh selected",
            "report.no_armature": "no amature found for active mesh!",
            "report.active_not_mesh": "active object is not a mesh!",
            "report.not_weight_mode": "please enter weight paint mode!",
            "report.name_collision": "name collision found, details see command prompt!",
            "report.done": "done!",
        },
        "zh": {
            # pointer panel
            "mainpanel.label": "顶点组重命名工具",
            "mainpanel.armature_pointer": "选择目标骨架:",
            "mainpanel.mesh_pointer": "选择目标模型:",
            "mainpanel.start_assignment": "开始指定",
            "mainpanel.start_assignment.tip": "开始将骨骼名称指定给顶点组",
            "mainpanel.stop": "重置指定",
            "mainpanel.stop.tip": "停止并重置指定流程",
            # vertex group assignment panel
            "mainpanel.vertex_group_string": "当前顶点组: ",
            "mainpanel.next": "下一个",
            "mainpanel.next.tip": "添加当前选中骨骼和顶点组到重命名列表并选择下一个顶点组",
            "mainpanel.skip": "跳过",
            "mainpanel.skip.tip": "跳过当前顶点组指定",
            "ul_list.vg.tip": "顶点组名称",
            "ul_list.bone.tip": "目标骨骼名称",
            "my_list.new_item": "添加",
            "my_list.new_item.tip": "添加一个重命名列表项",
            "my_list.delete_item": "删除",
            "my_list.delete_item.tip": "删除选中重命名列表项",
            "mainpanel.done": "开始重命名",
            "mainpanel.done.tip": "根据当前重命名列表开始批量重命名顶点组",
            # presets panel
            "menu_presets": "重命名列表预设",
            "presets.save": "保存",
            "presets.delete": "删除",
            "presets.tip": "保存或删除当前重命名列表预设",
            "presets.open_folder": "打开预设文件夹",
            "presets.open_folder.tip": "用资源管理器打开预设存储文件夹",
            # misc panel
            "miscpanel.label": "杂项",
            "miscpanel.remove_empty": "移除空顶点组",
            "miscpanel.remove_empty.tip": "为选中模型移除空顶点组",
            "miscpanel.remove_unused": "移除未使用顶点组",
            "miscpanel.remove_unused.tip": "根据选中模型的骨架修改器移除未使用的顶点组",
            "miscpanel.merge_mats": "自动合并材质",
            "miscpanel.merge_mats.tip": "遍历选中模型材质列表并合并相同贴图项",
            "miscpanel.select_seams": "选中缝合边",
            "miscpanel.select_seams.tip": "选中当前模型缝合边",
            # credit panel
            "creditpanel.label": "作者",
            "creditpanel.github": "Github: 0w0-Yui",
            "creditpanel.bilibili": "B站: 0w0-Yui",
            # report
            "report.no_active_mesh": "未选中模型",
            "report.no_active_bone": "未选中骨骼",
            "report.no_active": "未选中骨架或模型",
            "report.no_armature": "选中骨骼未找到正确的骨架修改器",
            "report.active_not_mesh": "选中物体不是模型",
            "report.not_weight_mode": "请进入权重模式",
            "report.name_collision": "名字冲突, 详情见控制台输出",
            "report.done": "完成! ",
        },
    }

    def get_localization(context):
        lang = None
        current = context.preferences.view.language
        if current == "zh_CN" or current == "zh_TW":
            lang = Localization.localizations["zh"]
        else:
            lang = Localization.localizations["en"]
        return lang


LANG = Localization.get_localization(bpy.context)


class ListItem(PropertyGroup):
    vg_tip = LANG["ul_list.vg.tip"]
    bone_tip = LANG["ul_list.bone.tip"]

    vg: StringProperty(name="vg", description=vg_tip, default="")
    bone: StringProperty(name="bone", description=bone_tip, default="")


class MY_UL_List(UIList):
    bl_idname = "mainpanel.ul_list"

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
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        context.scene.my_list.add()

        return {"FINISHED"}


class LIST_OT_DeleteItem(Operator):
    bl_idname = "my_list.delete_item"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

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
    bl_idname = "menu_presets"
    bl_label = LANG[bl_idname]
    bl_icon = "PRESET"

    preset_subdir = "yuinomodtools"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


class add_presets(AddPresetBase, Operator):
    bl_idname = "menu.add_preset"
    bl_sub_idname = "presets"
    bl_label = ""
    bl_description = LANG[bl_sub_idname + ".tip"]
    preset_menu = "menu_presets"

    # variable used for all preset values
    preset_defines = ["s = bpy.context.scene"]

    # properties to store in the preset
    preset_values = ["s.my_list"]

    # where to store the preset
    preset_subdir = "yuinomodtools"


class CreditPanel(Panel):
    bl_idname = "creditpanel"
    bl_label = LANG[bl_idname + ".label"]
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "YuiのModToolkit"

    def draw(self, context):
        layout = self.layout
        name = "0w0-Yui"
        op = layout.operator("wm.url_open", text=LANG["creditpanel.github"])
        op.url = "https://github.com/0w0-Yui"
        op1 = layout.operator("wm.url_open", text=LANG["creditpanel.bilibili"])
        op1.url = "https://space.bilibili.com/276237700"


class RemoveUnused(Operator):
    bl_idname = "miscpanel.remove_unused"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        object = bpy.context.object
        skeleton = object.find_armature()
        if object.type != "MESH":
            Kit.report(LANG["report.no_active_mesh"])
            return {"FINISHED"}
        if skeleton is None:
            Kit.report(LANG["report.no_armature"])
            return {"FINISHED"}
        if object.type == "MESH" and len(object.vertex_groups) > 0:
            for vGroup in object.vertex_groups:
                if skeleton.data.bones.get(vGroup.name) is None:
                    print(f"{vGroup.name} removed")
                    object.vertex_groups.remove(vGroup)
        return {"FINISHED"}


class RemoveEmpty(Operator):
    bl_idname = "miscpanel.remove_empty"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        obj = bpy.context.object
        if obj.type != "MESH":
            Kit.report(LANG["report.no_active_mesh"])
            return {"FINISHED"}
        try:
            vertex_groups = obj.vertex_groups
            groups = {r: None for r in range(len(vertex_groups))}

            for vert in obj.data.vertices:
                for vg in vert.groups:
                    i = vg.group
                    if i in groups:
                        del groups[i]

            lis = [k for k in groups]
            lis.sort(reverse=True)
            for i in lis:
                print(f"{vertex_groups[i].name} removed")
                vertex_groups.remove(vertex_groups[i])
        except Exception as e:
            print(e)
        return {"FINISHED"}


class MergeTextureMaterial(Operator):
    bl_idname = "miscpanel.merge_mats"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        obj = bpy.context.object
        mat_dict = {}
        if obj.type == "MESH":
            for mat_slot in obj.material_slots:
                if mat_slot.material:
                    if mat_slot.material.node_tree:
                        # print("material:" + str(mat_slot.material.name))
                        for x in mat_slot.material.node_tree.nodes:
                            if x.type == "TEX_IMAGE":
                                # print(" texture: "+str(x.image.name))
                                if mat_slot.slot_index in mat_dict:
                                    mat_dict[mat_slot.slot_index].append(x.image.name)
                                else:
                                    mat_dict[mat_slot.slot_index] = [x.image.name]
        # print(mat_dict)
        flipped = {}
        for key, value in mat_dict.items():
            value = tuple(value)
            value = tuple(
                [item for index, item in enumerate(value) if item not in value[:index]]
            )
            if value not in flipped:
                flipped[value] = [key]
            else:
                flipped[value].append(key)

        # print(flipped)
        # print(flipped.items())

        data_face = {}

        print("getting polygons data")
        polygons = obj.data.polygons
        for f in polygons:
            index_face = f
            index_mat = f.material_index
            if index_mat in data_face:
                data_face[index_mat].append(index_face)
            else:
                data_face[index_mat] = [index_face]
            # print("face", f.index, "material_index", f.material_index)

        # print(data_face)
        # print(flipped)
        # return {"FINISHED"}

        for key, value in flipped.items():
            # print(key,value)
            for index in value[1:]:
                print(f"{index} merge into {value[0]}")
                # continue
                for face in data_face[index]:
                    # print(faces)
                    face.material_index = value[0]
        bpy.ops.object.material_slot_remove_unused()

        return {"FINISHED"}


class SelectSeams(Operator):
    bl_idname = "miscpanel.select_seams"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type != "MESH":
            Kit.report(LANG["report.active_not_mesh"])
            return {"FINISHED"}
        bpy.ops.object.mode_set(mode="OBJECT")
        for e in obj.data.edges:
            e.select = e.use_seam
        return {"FINISHED"}


class MiscPanel(Panel):
    bl_idname = "miscpanel"
    bl_label = LANG[bl_idname + ".label"]
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "YuiのModToolkit"

    def draw(self, context):
        layout = self.layout
        layout.operator(RemoveEmpty.bl_idname, text=RemoveEmpty.bl_label)
        layout.operator(RemoveUnused.bl_idname, text=RemoveUnused.bl_label)
        layout.operator(
            MergeTextureMaterial.bl_idname, text=MergeTextureMaterial.bl_label
        )
        layout.operator(SelectSeams.bl_idname, text=SelectSeams.bl_label)


class OpenPresetFolder(Operator):
    bl_idname = "presets.open_folder"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        os.system(
            "explorer "
            + bpy.utils.resource_path("USER")
            + "\\scripts\\presets\\yuinomodtools"
        )
        return {"FINISHED"}


class MyAddonPanel(Panel):
    bl_idname = "mainpanel"
    bl_label = LANG[bl_idname + ".label"]
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "YuiのModToolkit"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        armature = scene.armature_pointer
        mesh = scene.mesh_pointer

        box = layout.box()
        box.label(text=LANG[self.bl_idname + ".armature_pointer"])
        box.prop(scene, "armature_pointer", text="", icon="ARMATURE_DATA")
        box.label(text=LANG[self.bl_idname + ".mesh_pointer"])
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
                menu_presets.bl_idname,
                text=menu_presets.bl_label,
                icon=menu_presets.bl_icon,
            )
            row1 = box2.row(align=True)
            row1.operator(
                add_presets.bl_idname, text=LANG[add_presets.bl_sub_idname + ".save"]
            )
            row1.operator(
                add_presets.bl_idname, text=LANG[add_presets.bl_sub_idname + ".delete"]
            ).remove_active = True
            row1 = box2.row(align=True)
            row1.operator(OpenPresetFolder.bl_idname, text=OpenPresetFolder.bl_label)
        else:
            layout.label(text=msg, icon="ERROR")


class Kit(Operator):
    def check_pointer(obj, armature):
        if obj is None or armature is None:
            return LANG["report.no_active"]
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

    def update_label_vg(string):
        context = bpy.context
        context.scene.vertex_group_string = (
            LANG["mainpanel.vertex_group_string"] + f"{string}"
        )
        return context.scene.vertex_group_string

    def is_mesh(scene, obj):
        return obj.type == "MESH"

    def is_armature(scene, obj):
        return obj.type == "ARMATURE"


class StartAssign(Operator):
    bl_idname = "mainpanel.start_assignment"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        vg_list = []
        selected_mesh = context.scene.mesh_pointer
        print("start quick assign")
        context.scene.assign_index = 0
        vg_list = Kit.get_all_vg(selected_mesh)
        Kit.select_vg(vg_list[context.scene.assign_index]["name"])
        Kit.update_label_vg(vg_list[context.scene.assign_index]["name"])
        return {"FINISHED"}


class Next(Operator):
    bl_idname = "mainpanel.next"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        if bpy.context.object.mode != "WEIGHT_PAINT":
            Kit.report(LANG["report.not_weight_mode"])
            return {"FINISHED"}
        selected_mesh = context.scene.mesh_pointer
        selected_bone = bpy.context.selected_pose_bones
        list = context.scene.my_list
        index = context.scene.assign_index
        vg_list = Kit.get_all_vg(selected_mesh)
        if len(selected_bone) == 0:
            Kit.report(LANG["report.no_active_bone"])
            return {"FINISHED"}
        if index >= 0 and index < len(vg_list):
            item = list.add()
            item.vg = vg_list[index]["name"]
            item.bone = selected_bone[0].name
            print(f"{item.vg} -> {item.bone} added")
            index += 1
        if index < len(vg_list):
            Kit.select_vg(vg_list[index]["name"])
            Kit.update_label_vg(vg_list[index]["name"])
        else:
            Kit.update_label_vg(str(None))
        context.scene.assign_index = index
        return {"FINISHED"}


class Skip(Operator):
    bl_idname = "mainpanel.skip"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        if bpy.context.object.mode != "WEIGHT_PAINT":
            Kit.report(LANG["report.not_weight_mode"])
            return {"FINISHED"}
        selected_mesh = context.scene.mesh_pointer
        index = context.scene.assign_index
        vg_list = Kit.get_all_vg(selected_mesh)
        if index >= 0 and index < len(vg_list):
            name = vg_list[index]["name"]
            print(f"{name} skipped")
            index += 1
        if index < len(vg_list):
            Kit.select_vg(vg_list[index]["name"])
            Kit.update_label_vg(vg_list[index]["name"])
        else:
            Kit.update_label_vg(str(None))
        context.scene.assign_index = index
        return {"FINISHED"}


class Stop(Operator):
    bl_idname = "mainpanel.stop"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        index = 0
        Kit.update_label_vg(str(None))
        context.scene.assign_index = index
        print("stop quick assign")
        return {"FINISHED"}


class Done(Operator):
    bl_idname = "mainpanel.done"
    bl_label = LANG[bl_idname]
    bl_description = LANG[bl_idname + ".tip"]

    def execute(self, context):
        print("starting...")
        if bpy.context.object.mode != "WEIGHT_PAINT":
            Kit.report(LANG["report.not_weight_mode"])
            return {"FINISHED"}
        mesh = bpy.data.objects[context.scene.mesh_pointer.name]
        my_list = context.scene.my_list
        vg_list = Kit.get_all_vg(mesh)
        vertex_groups = mesh.vertex_groups
        for i in my_list:
            for vg in vg_list:
                if vg["name"] == i.bone:
                    old_name = vg["name"]
                    print(
                        f"Vertex Group: {old_name} and Bone: {i.bone} is the same, please change the vertex group name"
                    )
                    Kit.report(LANG["report.name_collision"])
                    return {"FINISHED"}
                    """new_suffix = ".old.001"
                    vertex_group = vertex_groups.get(old_name)
                    new_name = old_name + new_suffix
                    index = 1
                    while new_name in vertex_groups:
                        index += 1
                        new_name = f"{old_name}.old.{str(index).zfill(3)}"
                    if vertex_group is not None:
                        vertex_group.name = new_name
                        print(f"{[old_name]} -> {new_name} renamed")
                    else:
                        print(f'No vertex group found with name "{[old_name]}"')"""

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
                is_exist = False
                for vg in vg_list:
                    if my_list[i].vg == vg["name"]:
                        is_exist = True
                if not is_exist:
                    print(f'No vertex group found with name "{[my_list[i].vg]}"')
                    continue
                vertex_group_names.append(my_list[i].vg)
            vertex_group = mesh.vertex_groups.new(name=merged_group_name)

            vertex_weights = {}
            for vert in mesh.data.vertices:
                if len(vert.groups):
                    for item in vert.groups:
                        vg = mesh.vertex_groups[item.group]
                        if vg.name in vertex_group_names:
                            if vert.index in vertex_weights:
                                vertex_weights[vert.index] += vg.weight(vert.index)
                            else:
                                vertex_weights[vert.index] = vg.weight(vert.index)
                            if vertex_weights[vert.index] > 1.0:
                                vertex_weights[vert.index] = 1.0

            # add the values to the group
            for key, value in vertex_weights.items():
                vertex_group.add([key], value, "REPLACE")  # 'ADD','SUBTRACT'
            print(f"{[vertex_group_names]} -> {merged_group_name} renamed")
        # print(f"{vg_list}")
        for item in my_list:
            is_dup = False
            for dup in duplicates:
                if item.bone == dup[0]:
                    is_dup = True
            if is_dup:
                continue
            old_name = item.vg
            new_name = item.bone
            is_exist = False
            for vg in vg_list:
                if old_name == vg["name"]:
                    is_exist = True
            if not is_exist:
                print(f'No vertex group found with name "{[old_name]}"')
                continue
            Kit.select_vg(old_name)
            bpy.ops.object.vertex_group_copy()
            vertex_groups[-1].name = new_name
            print(f"{[old_name]} -> {new_name} renamed")
        Kit.report(LANG["report.done"])
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
    RemoveUnused,
    RemoveEmpty,
    MergeTextureMaterial,
    SelectSeams,
    MiscPanel,
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
        name="vertex_group_string",
        default=LANG["mainpanel.vertex_group_string"] + str(None),
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
