# Выделение полигонов от материалов по шаблону. ver 1.0
# Работает в режиме редактирования
# GUI
# Разработка...



import bpy
import re # для распознания текста



class MaterialsSelect_Panel(bpy.types.Panel): 
    """ Класс панели. """   
    bl_idname = 'eidos_materials_select'  # может быть одновременно несколько панелей    
    bl_space_type = 'VIEW_3D' # месторасположение панели
    bl_region_type = 'UI'     # уточняет регион, где именно
    bl_category = 'EIDOS'      # Группа для панели    
    bl_label = 'Materials select'   # заголовок панели  
    
    def draw(self, context): 
        """ Рисует панель. """
        layout = self.layout        
        # layout.label(text="Auto rotate")

        # Достут к свойству
        scene = context.scene
        my_prop = scene.my_tool

        layout.prop(my_prop, "my_enum")
        layout.operator("object.materials_select_op", text='Выделить') 
        
        

class MaterialName_PropertyGroup(bpy.types.PropertyGroup):
    """ Свойства """    
    my_enum : bpy.props.EnumProperty(
        name= "Шаблоны",
        description= "Шаблоны материалов",
        items= [('OP1', "out_", ""),
                ('OP2', "in_", ""),
                ('OP3', "bModeRing", ""),
                ('OP4', "bModeHole", ""),
                ('OP5', "segmentWall_", "")
        ]
    )
        
        
        
class MaterialsSelect_Operator(bpy.types.Operator):
    """Выделение полигонов от материалов по шаблону. Работает в режиме редактирования"""
    bl_idname = "object.materials_select_op"  # уникальный идентификатор для кнопок и пунктов меню 
    bl_label = "NameOp_MS"       # Имя для отображения в пользовательском интерфейсе
    # user_name = 'default'
    
    def execute(self, context):
        """ действие оператора. """

        # Достут к свойству
        scene = context.scene
        my_prop = scene.my_tool

        materialNameSelect = r''
        
        if my_prop.my_enum == 'OP1': materialNameSelect = r'out_'
        if my_prop.my_enum == 'OP2': materialNameSelect = r'in_'
        if my_prop.my_enum == 'OP3': materialNameSelect = r'bModeRing'
        if my_prop.my_enum == 'OP4': materialNameSelect = r'bModeHole'
        if my_prop.my_enum == 'OP5': materialNameSelect = r'segmentWall_'
        #Шаблон
        # materialNameSelect = r'out_'
        #materialNameSelect = r'in_'
        #materialNameSelect = r'bModeRing'
        # materialNameSelect = r'bModeHole'
        #materialNameSelect = r'segmentWall_'

        obj = bpy.context.object
        mat_slot = obj.material_slots

        matIndex = 0
        for i in mat_slot:  
            bpy.context.object.active_material_index = matIndex    
            nameMat = bpy.context.object.active_material.name
            
            if re.match(materialNameSelect, nameMat):
                bpy.ops.object.material_slot_select()   
            
            matIndex = matIndex + 1
        
        return {'FINISHED'}



def register(): 
    bpy.utils.register_class(MaterialsSelect_Panel) 
    bpy.utils.register_class(MaterialsSelect_Operator) 
    bpy.utils.register_class(MaterialName_PropertyGroup) 
    
    # подключение глобального свойства
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= MaterialName_PropertyGroup)

def unregister(): 
    bpy.utils.unregister_class(MaterialsSelect_Panel)
    bpy.utils.unregister_class(MaterialsSelect_Operator) 
    bpy.utils.unregister_class(MaterialName_PropertyGroup) 
    del bpy.types.Scene.my_tool

if __name__ == "__main__": 
    register() 