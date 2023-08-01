import bpy
import math


class AutoRotate_Operator(bpy.types.Operator):
        """ Поворачивает выделенные объекты на 180 по X и 90 по Y """
        bl_idname = "object.auto_rotate_op"  # уникальный идентификатор для кнопок и пунктов меню 
        bl_label = "NameOp"       # Имя для отображения в пользовательском интерфейсе
        # user_name = 'default'
        
        def execute(self, context):
            """ действие оператора. """
            rot_x = math.radians(180)
            rot_y = math.radians(90)
            for i in bpy.context.selected_objects:
                i.rotation_euler[0] = rot_x
                i.rotation_euler[1] = rot_y
            return {'FINISHED'}
        


class AutoRotate_Panel(bpy.types.Panel): 
    """ Класс панели. """   
    bl_idname = 'eidos_auto_rotate'  # может быть одновременно несколько панелей    
    bl_space_type = 'VIEW_3D' # месторасположение панели
    bl_region_type = 'UI'     # уточняет регион, где именно
    bl_category = 'EIDOS'      # Группа для панели    
    bl_label = 'Auto rotate'   # заголовок панели  
    
    def draw(self, context): 
        """ Рисует панель. """
        layout = self.layout        
        # layout.label(text="Auto rotate")
        layout.operator("object.auto_rotate_op", text='Повернуть на 180 и 90') 

        

def register(): 
    bpy.utils.register_class(AutoRotate_Operator) 
    bpy.utils.register_class(AutoRotate_Panel) 

def unregister(): 
    bpy.utils.unregister_class(AutoRotate_Operator)
    bpy.utils.unregister_class(AutoRotate_Panel)

if __name__ == "__main__": 
    register() 