import bpy
import os
from .. import utils

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_OT_APPEND(Operator):
    bl_description = "append an asset"
    bl_idname = "mcam.asset_list_append"
    bl_label = "append asset"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        utils.AddonReloadManagement.reloadAssetList()
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.template_list("ASSET_UL_List", "The_List", scene.mcAssetsManagerProps, "asset_list", scene.mcAssetsManagerProps, "asset_index")
        
    def execute(self, context):
        scene = context.scene
        item = scene.mcAssetsManagerProps.asset_list[scene.mcAssetsManagerProps.asset_index]
        if item.path == "":
            blendfile = os.path.join(utils.AddonPathManagement.getAddonPath(), "files", "own_assets", item.name + ".blend")

            with bpy.data.libraries.load(blendfile, link=False) as (data_from, data_to):
                data_to.objects = data_from.objects
                data_to.collections = data_from.collections

            if data_to.collections:
                main_collection = None
                sub_collections = []
                
                for coll in data_to.collections:
                    if main_collection is None:
                        main_collection = coll
                    else:
                        sub_collections.append(coll)
                    bpy.context.scene.collection.children.link(coll)
                
                collection = bpy.context.view_layer.layer_collection.collection
                if collection:
                    for coll in sub_collections:
                        collection.children.unlink(coll)

            else:
                for obj in data_to.objects:
                    if obj is not None:
                        bpy.context.scene.collection.objects.link(obj)

        else:
            blendfile = item.path
            pathHalf = os.path.join(blendfile, item.type)
            pathFull = os.path.join(pathHalf, item.name)
            bpy.ops.wm.append(filepath=pathFull, filename=item.name,directory=pathHalf,link=False)
            
        self.report({'INFO'}, "asset successully appended")
        return{'FINISHED'}
    

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(ASSET_OT_APPEND)

def unregister():
    bpy.utils.unregister_class(ASSET_OT_APPEND)