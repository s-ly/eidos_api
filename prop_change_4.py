# Изменение свойст нескольких объектов. Основная разработка!

import bpy


class PropChange_Panel(bpy.types.Panel):
    """ Класс панели. """
    bl_idname = 'eidos_prop_change'  # может быть одновременно несколько панелей
    bl_space_type = 'VIEW_3D'  # месторасположение панели
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

        # layout.operator("object.modal_operator", text='В')
        # bpy.ops.object.eidos_prop_change_op('EXEC_DEFAULT')


class ModalOperator(bpy.types.Operator):
    """
    Делает то-то.

    Модальный оператор. Вызывая его происходит не само действие а некий цикл,
    в котором происодят действия по событиям.
    """
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    def execute(self, context):
        "Действие"
        print("ok")
        print(bpy.context.scene.my_tool.my_float)

        return {'FINISHED'}


class Prop_PropertyGroup(bpy.types.PropertyGroup):
    """ Свойства """
    my_float: bpy.props.FloatProperty(
        default=0.5, max=1, min=0, subtype='FACTOR')


def msgbus_callback_1(*args):
    """
    Метод вызывается когда меняем свойство по подписке.
    В ём вызывается оператор.
    """
    print("Something changed!", args)
    bpy.ops.object.modal_operator()


def register():
    bpy.utils.register_class(ModalOperator)
    bpy.utils.register_class(PropChange_Panel)
    bpy.utils.register_class(Prop_PropertyGroup)

    # подключение глобального свойства
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(
        type=Prop_PropertyGroup)  # Сцена
    # bpy.types.Object.my_tool = bpy.props.PointerProperty(type= Prop_PropertyGroup) # Объект

    #####################################################################
    # Подписка прослушивания события
    subscribe_to = bpy.context.scene.my_tool  # ссылка на отслеживаемое свойство
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
    del bpy.types.Object.my_tool  # Объект

    # bpy.msgbus.clear_by_owner(owner) # должно отписываться от события, пока не понял


if __name__ == "__main__":
    register()
