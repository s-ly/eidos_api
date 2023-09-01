# Изменяет вес вормы всех выделенных объектов, если имя совподает с именем в поле.

import bpy


class PropChange_Panel(bpy.types.Panel):
    """ Класс панели. """
    bl_idname = 'eidos_prop_change'  # может быть одновременно несколько панелей
    bl_space_type = 'VIEW_3D'  # месторасположение панели
    bl_region_type = 'UI'     # уточняет регион, где именно
    bl_category = 'EIDOS'      # Группа для панели
    bl_label = 'Prop change'   # заголовок панели

    def draw(self, context):
        """ Рисует панель. """

        # obj = bpy.context.object
        layout = self.layout

        # Достут к свойству (сцена)
        scene = context.scene
        my_prop = scene.my_tool_prop_change

        # Достут к свойству (объект)
        # scene2 = context.object
        # my_prop = scene2.my_tool_prop_change

        layout.prop(my_prop, "my_string_name_def")
        layout.prop(my_prop, "my_float")
        # obj.data.shape_keys.key_blocks[1].value = 0.75

        # layout.operator("object.modal_operator", text='В')
        # bpy.ops.object.eidos_prop_change_op('EXEC_DEFAULT')


class ModalOperator(bpy.types.Operator):
    """
    Изменяет вес вормы всех выделенных объектов, если имя совподает с именем в поле.
    """
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    def execute(self, context):
        """Действие"""

        print(bpy.context.scene.my_tool_prop_change.my_float)
        self.key_action(context)
        return {'FINISHED'}

    def key_action(self, context):
        obj_sel = bpy.context.selected_objects  # выделенные объекты
        for i in obj_sel:
            self.obj_action(context, i)

    def obj_action(self, context, obj):
        """ Принимает ссылку на объект и делает с ним действие. """
        print(obj.name)
        all_shape_keys = obj.data.shape_keys.key_blocks # список всех форм 
        for i in all_shape_keys:
            if i.name == bpy.context.scene.my_tool_prop_change.my_string_name_def:
                i.value = bpy.context.scene.my_tool_prop_change.my_float
        # obj.data.shape_keys.key_blocks[1].value = bpy.context.scene.my_tool_prop_change.my_float


class Prop_PropertyGroup(bpy.types.PropertyGroup):
    """ Свойства """
    my_string_name_def: bpy.props.StringProperty(name = "Имя ключа", default="")
    
    my_float: bpy.props.FloatProperty(
        default=0.5, max=1, min=0, subtype='FACTOR')


def msgbus_callback_1(*args):
    """
    Метод вызывается когда меняем свойство по подписке.
    В ём вызывается оператор.
    """
    # print("Something changed!", args)
    bpy.ops.object.modal_operator()


def register():
    bpy.utils.register_class(ModalOperator)
    bpy.utils.register_class(PropChange_Panel)
    bpy.utils.register_class(Prop_PropertyGroup)

    # подключение глобального свойства
    bpy.types.Scene.my_tool_prop_change = bpy.props.PointerProperty(
        type=Prop_PropertyGroup)  # Сцена
    # bpy.types.Object.my_tool_prop_change = bpy.props.PointerProperty(type= Prop_PropertyGroup) # Объект

    #####################################################################
    # Подписка прослушивания события
    subscribe_to = bpy.context.scene.my_tool_prop_change  # ссылка на отслеживаемое свойство
    owner = object()  # хуй знает
    notify = msgbus_callback_1  # эта функция вызовится при изменении
    args = (11, 2, 3, 779007)  # нахуй ненужные обязательные аргументы

    bpy.msgbus.subscribe_rna(
        key=subscribe_to, owner=owner, args=args, notify=notify)
    #####################################################################


def unregister():
    bpy.utils.unregister_class(ModalOperator)
    bpy.utils.unregister_class(PropChange_Panel)
    bpy.utils.unregister_class(Prop_PropertyGroup)

    # отключение глобального свойства
    del bpy.types.Object.my_tool_prop_change  # Объект

    # bpy.msgbus.clear_by_owner(owner) # должно отписываться от события, пока не понял


if __name__ == "__main__":
    register()
