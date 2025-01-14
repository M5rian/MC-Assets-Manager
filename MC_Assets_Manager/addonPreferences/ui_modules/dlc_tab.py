import os, importlib

from ...utils import utils
from ...load_modules import PACKAGE_NAME

def dlc_tab(self, context, layout, scene):
    smallHeader = layout.row()
    smallHeader.scale_y = 0.5
    row = smallHeader.box().row()
    row.label(text="Name")
    row.label(text="Type")
    row.label(text="Creator")
    row.label(text="", icon ="BLANK1")
    smallHeader.label(text="", icon="BLANK1")

    row = layout.row()
    row.template_list("DLC_UL_List", "The_List", scene.mcAssetsManagerProps, "dlc_list", scene.mcAssetsManagerProps, "dlc_index")

    colMain = row.column()
    colFir = colMain.column()
    colFir.operator("mcam.dlc_list_reload", text = "", icon = "FILE_REFRESH")
    colSec = colMain.column(align = True)
    colSec.operator("mcam.dlc_list_add", text = "", icon = "ADD")
    colSec.operator("mcam.dlc_list_remove", text = "", icon = "REMOVE")

    colThi = colMain.column(align = True)
    if context.scene.mcAssetsManagerProps.item_unlock == False: lock = "LOCKED"
    else: lock = "UNLOCKED"
    colThi.prop(context.scene.mcAssetsManagerProps, "item_unlock", text="", icon=lock)

def showDlcPreferences(self, context):
    dlc_list = context.scene.mcAssetsManagerProps.dlc_list
    if dlc_list:
        #   get paths and more
        addon_path = utils.AddonPathManagement.getAddonPath()
        dlc_paths = os.path.join(addon_path, "files", "DLCs")
        dlc_list = os.listdir(dlc_paths)

        for dlc in dlc_list:
            index = context.scene.mcAssetsManagerProps.dlc_index
            active = context.scene.mcAssetsManagerProps.dlc_list[index].active              #   read active status of dlc
            init_exists = utils.AddonPathManagement.getInitPath(dlc)[1]                     #   check init path and existence

            if self.data and active and init_exists:                                        #   if dlc exists & active & init file (script based)
                if dlc in locals():                                                         #   if already loaded
                    importlib.reload(eval(dlc))                                             #   reload module
                else:
                    module_name = ".files.DLCs."+dlc                                        #   get module name for importing
                    locals()[dlc] = importlib.import_module(name = module_name, package = PACKAGE_NAME) 
                
                selected_dlc = str(dlc_list[index])                                         #   get selected dlc from ui list
                dlc_name = os.path.splitext(locals()[dlc].__name__)[-1][1:]                 #   get dlc name from selection

                if selected_dlc == dlc_name and active:                                     #   if selection is dlc from iteration
                    locals()[dlc].CustomAddonPreferences.display(self)                      #   draw addon preferences from dlc