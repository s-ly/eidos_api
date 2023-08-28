# Изменение свойст нескольких объектов.

import bpy

class PropChange_Panel(bpy.types.Panel): 
    """ Класс панели. """   
    bl_idname = 'eidos_prop_change'  # может быть одновременно несколько панелей    
    bl_space_type = 'VIEW_3D' # месторасположение панели
    bl_region_type = 'UI'     # уточняет регион, где именно
    bl_category = 'EIDOS_DEV'      # Группа для панели    
    bl_label = 'Prop change'   # заголовок панели  
    
    def draw(self, context): 
        """ Рисует панель. """

        # obj = bpy.context.object
        layout = self.layout

        # Достут к свойству (сцена)
        scene = context.scene
        my_prop = scene.my_tool
        
        # Достут к свойству (объект)
        # scene2 = context.object
        # my_prop = scene2.my_tool

        layout.prop(my_prop, "my_float")
        # obj.data.shape_keys.key_blocks[1].value = 0.75

        layout.operator("object.modal_operator", text='В') 
        # bpy.ops.object.eidos_prop_change_op('EXEC_DEFAULT')






class ModalOperator(bpy.types.Operator):
    """
    Делает то-то.

    Модальный оператор. Вызывая его происходит не само действие а некий цикл,
    в котором происодят действия по событиям.
    """
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"



    def __init__(self):
        """ Начало цикла """
        print("Start")
        self.report({'INFO'}, "Start")

    def __del__(self):
        """ Конец цикла """
        print("End")
        self.report({'INFO'}, "End")

    def execute(self, context):
        "Действие"
        # Достут к свойству
        scene = context.scene
        my_prop = scene.my_tool

        obj = bpy.context.object
        obj.data.shape_keys.key_blocks[1].value = my_prop.my_float
        self.report({'INFO'}, str(my_prop.my_float))

        return {'FINISHED'}

    def modal(self, context, event):
        """
        Будет выполняться для обработки событий до тех пор,
        пока не вернет {'FINISHED'} или {'CANCELLED'}.
        В ней мы вызываем повторяемое действие.
        """
        # if event.type == 'MOUSEMOVE':  # Apply
        if event.type == 'LEFTMOUSE':  # Apply
            # self.value = event.mouse_x
            self.execute(context)
        
        # elif event.type == 'LEFTMOUSE':  # Confirm
        #     return {'FINISHED'}
        
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            # Отменить все сделанные изменения
            # context.object.location.x = self.init_loc_x
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        """
        Переводит оператор в режим выполнения. Тут можно инициировать поля.
        """
        # self.init_loc_x = context.object.location.x
        # self.value = event.mouse_x
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}





class Prop_PropertyGroup(bpy.types.PropertyGroup):
    """ Свойства """
    my_float: bpy.props.FloatProperty(default=0.5, max=1, min=0, subtype='FACTOR')



def register(): 
    bpy.utils.register_class(ModalOperator)
    bpy.utils.register_class(PropChange_Panel)
    bpy.utils.register_class(Prop_PropertyGroup) 

    # подключение глобального свойства
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= Prop_PropertyGroup) # Сцена
    # bpy.types.Object.my_tool = bpy.props.PointerProperty(type= Prop_PropertyGroup) # Объект

def unregister(): 
    bpy.utils.unregister_class(ModalOperator)
    bpy.utils.unregister_class(PropChange_Panel)
    bpy.utils.unregister_class(Prop_PropertyGroup)

    # отключение глобального свойства
    del bpy.types.Object.my_tool # Объект


# # obj = bpy.context.object
# # obj.data.shape_keys.key_blocks[1].value = 0.75

# # bpy.ops.object.eidos_prop_change_op('INVOKE_DEFAULT')



if __name__ == "__main__": 
    register() 
