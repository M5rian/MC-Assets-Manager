import os, shutil

class SETUP:

    def __init__(self):
        self.main_path = os.path.dirname(os.path.realpath(__file__))
        self.error_message = "McAM: setup_addon_update: ERROR >"

        self.setup()
        self.setup_addon_update()

    def setup(self):
        """
          - creating all directories needed for the addon\n
          - initalization every time the addon starts
        """
        files_path = os.path.join(self.main_path, "files")

        dlcs = os.path.join(files_path, "DLCs")

        o_assets= os.path.join(files_path, "own_assets")
        o_rigs = os.path.join(files_path, "own_rigs")
        o_presets = os.path.join(files_path, "own_presets")

        o_assets_icons = os.path.join(o_assets, "icons")
        o_rigs_icons = os.path.join(o_rigs, "icons")
        o_presets_icons = os.path.join(o_presets, "icons")

        paths = {dlcs, o_assets, o_rigs, o_presets, o_assets_icons, o_rigs_icons, o_presets_icons}

        for p in paths:
            if not os.path.exists(p):
                os.mkdir(p)

    def setup_addon_update(self):
        """
        - setup after addon has updated\n
        - hard coded for every file change
        """
        #   moved reloadAddon operator file
        try:
            old_reloadAddon_py = os.path.join(self.main_path, "utils", "addonReloader.py")
            if os.path.exists(old_reloadAddon_py):
                shutil.rmtree(old_reloadAddon_py)
        except:
            print(f'{self.error_message} old_reloadAddon_py')

        #   moved icon folder
        try:
            old_icon_folder = os.path.join(self.main_path, "icons")
            if os.path.exists(old_icon_folder):
                shutil.rmtree(old_icon_folder)
        except:
            print(f'{self.error_message} old_icon_folder')

        #   change of utils.py to utils_utils module
        try:
            old_utils_py = os.path.join(self.main_path, "utils", "utils.py")
            if os.path.exists(old_utils_py):
                os.remove(old_utils_py)
        except:
            print(f'{self.error_message} old_utils_py')

        #   change of remove_chache_files.py.py to prepare_for_upload
        try:
            old_remove_chache_files_py = os.path.join(self.main_path, "remove_chache_files.py")
            if os.path.exists(old_remove_chache_files_py):
                os.remove(old_remove_chache_files_py)
        except:
            print(f'{self.error_message} old_remove_chache_files_py')

SETUP()