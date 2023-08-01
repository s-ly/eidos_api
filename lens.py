import bpy

class Lens_50_Operator(bpy.types.Operator):
        """ Угол обзора 50 мм"""
        bl_idname = "object.lens_50"  # уникальный идентификатор для кнопок и пунктов меню 
        bl_label = "Name_Lens_50_Op"       # Имя для отображения в пользовательском интерфейсе
        
        def execute(self, context):
            """ действие оператора. """
            self.view3d = bpy.context.space_data
            self.view3d.lens = 50
            return {'FINISHED'}
        
        
        
class Lens_35_Operator(bpy.types.Operator):
        """ Угол обзора 35 мм"""
        bl_idname = "object.lens_35"  # уникальный идентификатор для кнопок и пунктов меню 
        bl_label = "Name_Lens_35_Op"       # Имя для отображения в пользовательском интерфейсе
        
        def execute(self, context):
            """ действие оператора. """
            self.view3d = bpy.context.space_data
            self.view3d.lens = 35
            return {'FINISHED'}



class Lens_24_Operator(bpy.types.Operator):
        """ Угол обзора 24 мм"""
        bl_idname = "object.lens_24"  # уникальный идентификатор для кнопок и пунктов меню 
        bl_label = "Name_Lens_24_Op"       # Имя для отображения в пользовательском интерфейсе
        
        def execute(self, context):
            """ действие оператора. """
            self.view3d = bpy.context.space_data
            self.view3d.lens = 24
            return {'FINISHED'}
        


class Lens_16_Operator(bpy.types.Operator):
        """ Угол обзора 16 мм"""
        bl_idname = "object.lens_16"  # уникальный идентификатор для кнопок и пунктов меню 
        bl_label = "Name_Lens_16_Op"       # Имя для отображения в пользовательском интерфейсе
        
        def execute(self, context):
            """ действие оператора. """
            self.view3d = bpy.context.space_data
            self.view3d.lens = 16
            return {'FINISHED'}
        


class Lens_8_Operator(bpy.types.Operator):
        """ Угол обзора 8 мм"""
        bl_idname = "object.lens_8"  # уникальный идентификатор для кнопок и пунктов меню 
        bl_label = "Name_Lens_8_Op"       # Имя для отображения в пользовательском интерфейсе
        
        def execute(self, context):
            """ действие оператора. """
            self.view3d = bpy.context.space_data
            self.view3d.lens = 8
            return {'FINISHED'}
        


class Lens_Panel(bpy.types.Panel): 
    """ Класс панели. """   
    bl_idname = 'eidos_lens'  # может быть одновременно несколько панелей    
    bl_space_type = 'VIEW_3D' # месторасположение панели
    bl_region_type = 'UI'     # уточняет регион, где именно
    bl_category = 'EIDOS'      # Группа для панели    
    bl_label = 'Lens'   # заголовок панели  
    
    def draw(self, context): 
        """ Рисует панель. """
        layout = self.layout
        layout.operator("object.lens_50", text='Угол 50 мм') 
        layout.operator("object.lens_35", text='Угол 35 мм') 
        layout.operator("object.lens_24", text='Угол 24 мм') 
        layout.operator("object.lens_16", text='Угол 16 мм') 
        layout.operator("object.lens_8", text='Угол 8 мм') 

        

def register(): 
    bpy.utils.register_class(Lens_50_Operator) 
    bpy.utils.register_class(Lens_35_Operator) 
    bpy.utils.register_class(Lens_24_Operator) 
    bpy.utils.register_class(Lens_16_Operator) 
    bpy.utils.register_class(Lens_8_Operator) 
    bpy.utils.register_class(Lens_Panel) 

def unregister(): 
    bpy.utils.unregister_class(Lens_50_Operator)
    bpy.utils.unregister_class(Lens_35_Operator)
    bpy.utils.unregister_class(Lens_24_Operator)
    bpy.utils.unregister_class(Lens_16_Operator)
    bpy.utils.unregister_class(Lens_8_Operator)
    bpy.utils.unregister_class(Lens_Panel)

if __name__ == "__main__": 
    register() 