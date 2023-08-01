import bpy 

class MyPanel(bpy.types.Panel): 
    """ Класс панели. """   
    bl_idname = 'test_api'  # может быть одновременно несколько панелей    
    bl_space_type = 'VIEW_3D' # месторасположение панели
    bl_region_type = 'UI'     # уточняет регион, где именно
    bl_category = 'Test API'      # Группа для панели    
    bl_label = 'T_e_s_t'   # заголовок панели 
    
    
    def draw(self, context): 
        """ Рисует панель. """
        layout = self.layout        
        layout.label(text="Текстовая метка")
        
        
def register(): 
    bpy.utils.register_class(MyPanel) 


def unregister(): 
    bpy.utils.unregister_class(MyPanel) 


if __name__ == "__main__": 
    register() 