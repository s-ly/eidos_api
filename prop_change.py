import bpy
print('------------------------------------------')

class PropChange_Panel(bpy.types.Panel): 
    """ Класс панели. """   
    bl_idname = 'eidos_prop_change'  # может быть одновременно несколько панелей    
    bl_space_type = 'VIEW_3D' # месторасположение панели
    bl_region_type = 'UI'     # уточняет регион, где именно
    bl_category = 'EIDOS'      # Группа для панели    
    bl_label = 'Prop change'   # заголовок панели  
    
    def draw(self, context): 
        """ Рисует панель. """

        # obj = bpy.context.object
        layout = self.layout

        # Достут к свойству (сцена)
        # scene = context.scene
        # my_prop = scene.my_tool
        
        # Достут к свойству (объект)
        scene2 = context.object
        my_prop = scene2.my_tool

        layout.prop(my_prop, "my_float")
        # obj.data.shape_keys.key_blocks[1].value = 0.75

        # layout.operator("object.eidos_prop_change_op", text='В') 
        # bpy.ops.object.eidos_prop_change_op('EXEC_DEFAULT')









class ModalOperator(bpy.types.Operator):
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):
        context.object.location.x = self.value / 100.0
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            self.value = event.mouse_x
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            # Revert all changes that have been made
            context.object.location.x = self.init_loc_x
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.init_loc_x = context.object.location.x
        self.value = event.mouse_x
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


# Only needed if you want to add into a dynamic menu.
def menu_func(self, context):
    self.layout.operator(ModalOperator.bl_idname, text="Modal Operator")


# Register and add to the object menu (required to also use F3 search "Modal Operator" for quick access).
bpy.utils.register_class(ModalOperator)
bpy.types.VIEW3D_MT_object.append(menu_func)

# test call
bpy.ops.object.modal_operator('INVOKE_DEFAULT')













# class Prop_PropertyGroup(bpy.types.PropertyGroup):
#     """ Свойства """
#     my_float: bpy.props.FloatProperty(default=0.5, max=1, min=0,subtype='FACTOR')



# def register(): 
#     bpy.utils.register_class(PropChange_Panel) 
#     bpy.utils.register_class(PropChange_Operator) 
#     bpy.utils.register_class(Prop_PropertyGroup) 

#     # подключение глобального свойства
#     # bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= Prop_PropertyGroup) # Сцена
#     bpy.types.Object.my_tool = bpy.props.PointerProperty(type= Prop_PropertyGroup) # Объект

# def unregister(): 
#     bpy.utils.unregister_class(PropChange_Panel)
#     bpy.utils.unregister_class(PropChange_Operator)
#     bpy.utils.unregister_class(Prop_PropertyGroup)

#     # отключение глобального свойства
#     # del bpy.types.Scene.my_tool # Сцена
#     del bpy.types.Object.my_tool # Объект


# # obj = bpy.context.object
# # obj.data.shape_keys.key_blocks[1].value = 0.75

# # bpy.ops.object.eidos_prop_change_op('INVOKE_DEFAULT')



# if __name__ == "__main__": 
#     register() 
