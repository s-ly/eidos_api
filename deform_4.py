# Автоматическая деформация нескольких связанных объектов.
import bpy 
import re



class PropertyControll(bpy.types.PropertyGroup):
    '''Хранит данные (свойства)'''
    my_string: bpy.props.StringProperty(name = 'name_1', default = 'Cube')
    my_string_2: bpy.props.StringProperty(name = 'name_2', default = 'Cube')
    


class NameOperator(bpy.types.Operator):
    """ Создаёт объект с введёном именем. """
    bl_idname = "object.name_op"  # уникальный идентификатор для кнопок и пунктов меню 
    bl_label = "NameOp"       # Имя для отображения в пользовательском интерфейсе
    user_name = 'default'
    
    def execute(self, context):
        """ действие оператора. """        
        # переброска данных
        my_props = context.scene.NameObj
        self.user_name = my_props.my_string
        # действие
        bpy.ops.mesh.primitive_uv_sphere_add()
        obj = bpy.context.object 
        obj.name = self.user_name 
        return {'FINISHED'}



class PrintNameOperator(bpy.types.Operator):
    """ Печатает имя выделенного объекта. """
    bl_idname = "object.print_name_op"  # уникальный идентификатор для кнопок и пунктов меню 
    bl_label = "PrintNameOp"       # Имя для отображения в пользовательском интерфейсе
    
    def execute(self, context):
        """ действие оператора. """
        # действие
        obj = bpy.context.object
        print(obj.name)
        return {'FINISHED'}   
    
    

class CreateСorrectiveDeformationOperator(bpy.types.Operator):
    """ 
    Создаёт корректирующие ключи деформации.
    Работает с одним объектом в режиме «Объект»
    """
    bl_idname = "object.create_correct_deform_op"  # уникальный идентификатор для кнопок и пунктов меню 
    bl_label = "CreateСorrectDeformOper"       # Имя для отображения в пользовательском интерфейсе
    frames_1 = [0, 11, 15, 19] # кадры
    frames_2 = [0, 5, 11, 15, 19] # кадры
    frames = frames_1
    frame_end = 25 # последний кадр
    
    def execute(self, context):
        """ действие оператора. """
        obj = bpy.context.object
        print(obj.name)
        self.create_shape_keys(context)
        self.create_animation_keys(context)
        self.changing_key_interpolation(context)
        return {'FINISHED'}
    
    def create_shape_keys(self, context):
        """ Создаёт ключи формы. """
        obj = bpy.context.object # доступ к объекту
        for i in self.frames:
            bpy.ops.object.shape_key_add(from_mix=False) # добавть ключ формы            
            new_key_mame = 'DEF ' + str(i) # формируем имя созданного ключа
            activ_key = obj.active_shape_key_index # индекс активного ключа             
            obj.data.shape_keys.key_blocks[activ_key].name = new_key_mame # переименовываем активный ключ
            
    def create_animation_keys(self, context):
        """ Создаёт ключи анимации. """
        obj = bpy.context.object # доступ к объекту
        all_shape_keys = obj.data.shape_keys.key_blocks # список всех форм
        
        # Бежим по каждому кадру (кроме последнего)
        for i in self.frames:
            bpy.context.scene.frame_current = i # ставим в кадр
            
            # Бежим по списку форм,
            # если имя формы равно текущему кадру + префикс "DEF ",
            # то ставим его значение в 1.0, иначе в 0.0.
            # в начале проверяем, если в названии формы строка 'DEF',
            # если нет, то вообще пропускаем этот ключ формы.
            for SKey in all_shape_keys:
                if not re.match('DEF', SKey.name):
                    continue
                if (SKey.name == 'DEF ' + str(i)):
                    SKey.value = 1.0 # ставим значение
                else:
                    SKey.value = 0.0 # ставим значение
                SKey.keyframe_insert("value", frame=i) # ставим ключ
                
        # Работа с последним кадром        
        bpy.context.scene.frame_current = self.frame_end # ставим в последний кадр
        
        # бежим по списку форм, если имя формы равно первому,
        # то ставим его значение в 1.0, иначе в 0.0.
        # в начале проверяем, если в названии формы строка 'DEF',
        # если нет, то вообще пропускаем этот ключ формы.
        for SKey in all_shape_keys:
            if not re.match('DEF', SKey.name):
                continue
            if (SKey.name == 'DEF ' + str(self.frames[0])):
                SKey.value = 1.0 # ставим значение
            else:
                SKey.value = 0.0 # ставим значение
            SKey.keyframe_insert("value", frame=self.frame_end) # ставим ключ
            
    def changing_key_interpolation(self, context):
        """ Изменение интерполяции ключей.
        Проверяет, есть ли у объекта action."""
        obj = bpy.context.object # доступ к объекту        
        for fcu in obj.data.shape_keys.animation_data.action.fcurves: # перебор кривых
            for keyframe in fcu.keyframe_points: # перебор ключей
                keyframe.interpolation = 'LINEAR'
        


class CreateGlobalDeformationOperator(bpy.types.Operator):
    """ Создаёт глобальные корректирующие ключи деформации. """
    bl_idname = "object.create_global_correct_deform_op"  # уникальный идентификатор для кнопок и пунктов меню 
    bl_label = "CreateGlobalСorrectDeformOper"       # Имя для отображения в пользовательском интерфейсе
    
    def execute(self, context):
        """ действие оператора. """
        self.create_shape_keys_glob(context)
        return {'FINISHED'}
    
    def create_shape_keys_glob(self, context):
        """ Создаёт ключи формы. """
        obj_s = bpy.context.selected_objects # доступ к объекту       
        for obj_i in obj_s:
            all_shape_keys = obj_i.data.shape_keys.key_blocks # список всех форм
            obj_i.shape_key_add(from_mix=False) # добавть ключ формы
            print(len(all_shape_keys))
            for i in all_shape_keys:
                if i.name == 'Key':
                    i.name = 'GLOBAL'
                    i.value = 1.0 # ставим значение#   
                    obj_i.active_shape_key_index = len(all_shape_keys) - 1 # выбираем последний ключ формы
                


class MyPanel(bpy.types.Panel): 
    """ Класс панели. """   
    bl_idname = 'auto_api'  # может быть одновременно несколько панелей    
    bl_space_type = 'VIEW_3D' # месторасположение панели
    bl_region_type = 'UI'     # уточняет регион, где именно
    bl_category = 'Auto API'      # Группа для панели    
    bl_label = 'Deformator'   # заголовок панели 
    
    def draw(self, context): 
        """ Рисует панель. """
        layout = self.layout        
        layout.label(text="Текстовая метка")
        layout.operator("object.name_op", text='Создать объект с именем') 
        # создание и печать свойства
        my_props = context.scene.NameObj
        layout.prop(my_props, 'my_string')
        
        # вывод второй кнопки
        layout.operator("object.print_name_op", text='Печатать имя')       
        
        text = "no select"
        obj = bpy.context.object
        layout.label(text="Select: " + obj.name)  

        layout.label(text="Локальные ключи:") 
        layout.label(text="self.frames") 
        
        # вывод третей кнопки
        layout.operator("object.create_correct_deform_op", text='Создать ключи DEF')

        layout.label(text="Глобальные ключи:") 
        
        # вывод четёртой кнопки
        layout.operator("object.create_global_correct_deform_op", text='Создать ключ CLOBAL')
        
                             

def register(): 
    bpy.utils.register_class(PropertyControll) 
    bpy.utils.register_class(CreateСorrectiveDeformationOperator) 
    bpy.utils.register_class(CreateGlobalDeformationOperator) 
    
    
    bpy.utils.register_class(PrintNameOperator) 
    bpy.utils.register_class(NameOperator) 
    bpy.utils.register_class(MyPanel) 
    # подключение глобального свойства
    bpy.types.Scene.NameObj = bpy.props.PointerProperty(type = PropertyControll)


def unregister(): 
    bpy.utils.unregister_class(PropertyControll) 
    bpy.utils.unregister_class(CreateСorrectiveDeformationOperator) 
    bpy.utils.unregister_class(CreateGlobalDeformationOperator) 
    
    
    bpy.utils.unregister_class(PrintNameOperator) 
    bpy.utils.unregister_class(NameOperator) 
    bpy.utils.unregister_class(MyPanel) 


if __name__ == "__main__": 
    register() 