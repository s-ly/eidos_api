# EIDOS Animation Create v2.0 GUI
# Создаёт новые ключи формы по вторичному объекту и анимирует их.

import bpy

# Список ключевых кадров.
frames_Heart = [0, 11, 15, 19] # Heart
frames_MV = [0, 2, 5, 11, 15, 19, 22] # MV
frames_TV = [0, 5, 11, 15, 19, 22] # TV
frames_PV = [0, 3, 6, 9, 10, 11, 12, 15, 17, 19] # PV
frames_AV = [0, 3, 5, 6, 9, 11, 13, 15, 17, 19, 21, 23] # AV
frames_25_All_Frames = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] 
frames_125_All_Frames = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124] 
frames_MV_Stenosis = [0, 11, 12, 15, 19, 22] # MV_Stenosis
frames_Abd_Aort_IVC = [0, 11, 15, 19, 25, 36, 40, 44, 50, 61, 65, 69, 75, 86, 90, 94, 100, 111, 115, 119]

# Последний ключевой кадр. Abd_Aort, IVC (frame_end = 125)
# frame_end = 25



class EIDOS_AnimationCreate_PT_MainPanel(bpy.types.Panel): 
    """ Класс панели. """   
    bl_idname = 'eidos_animation_create'  # может быть одновременно несколько панелей    
    bl_space_type = 'VIEW_3D' # месторасположение панели
    bl_region_type = 'UI'     # уточняет регион, где именно
    bl_category = 'EIDOS'      # Группа для панели    
    bl_label = 'Animation Create'   # заголовок панели  
    
    def draw(self, context): 
        """ Рисует панель. """
        layout = self.layout    

        # Достут к свойству
        scene = context.scene
        my_prop = scene.my_group_prop

        layout.prop(my_prop, "obj_enum")
        layout.prop(my_prop, "frames_enum")
        layout.operator("object.eidos_animation_create_op", text='Перенести анимацию') 



class EIDOS_AnimationCreate_PG_OBJ(bpy.types.PropertyGroup):
    """Выбор объектов для переноса анимации"""    
    obj_enum : bpy.props.EnumProperty(
        name= "Орган",
        description= "Анимируемые объекты",
        items= [('OBJ_Heart', "Heart", str(frames_Heart)),
                ('OBJ_MV', "MV", str(frames_MV)),
                ('OBJ_TV', "TV", str(frames_TV)),
                ('OBJ_PV', "PV", str(frames_PV)),
                ('OBJ_AV', "AV", str(frames_AV)),
                ('OBJ_25_All_Frames', "25_All_Frames", str(frames_25_All_Frames)),
                ('OBJ_125_All_Frames', "125_All_Frames", str(frames_125_All_Frames)),
                ('OBJ_MV_Stenosis', "MV_Stenosis", str(frames_MV_Stenosis)),
                ('OBJ_Abd_Aort_IVC', 'Abd_Aort, IVC (frame_end = 125)', str(frames_Abd_Aort_IVC))
            ]
        )

    frames_enum : bpy.props.EnumProperty(
        name= "Кадр",
        description= "Количество кадров анимации",
        items= [('25', "25", ""),
                ('125', "125", "")
            ]
        )



class EIDOS_AnimationCreate_OT_AniCreate(bpy.types.Operator):
    """Создаёт новые ключи формы по вторичному объекту и анимирует их. Выбрать анимируемый объект из списка, с последним кадром. Далее выделяем объект с анимацией, потом объект на который нужно всё перенести"""

    bl_idname = "object.eidos_animation_create_op"  # уникальный идентификатор для кнопок и пунктов меню 
    bl_label = "AniCreate_op"       # Имя для отображения в пользовательском интерфейсе
    
    def execute(self, context):
        """ Действие оператора. """

        
        """ БЛОК: Получение данных. """
        frames = [] # init
        all_shape_keys = [] # init
        frame_end = 0 # init
        obj = bpy.context.object # ссылка на объект  
        
        # Достут к свойству
        scene = context.scene
        my_prop = scene.my_group_prop 

        # Регистрируем ключевые кадры по выбранному объекту
        if my_prop.obj_enum == 'OBJ_Heart': frames = frames_Heart
        if my_prop.obj_enum == 'OBJ_MV': frames = frames_MV
        if my_prop.obj_enum == 'OBJ_TV': frames = frames_TV
        if my_prop.obj_enum == 'OBJ_PV': frames = frames_PV
        if my_prop.obj_enum == 'OBJ_AV': frames = frames_AV
        if my_prop.obj_enum == 'OBJ_25_All_Frames': frames = frames_25_All_Frames
        if my_prop.obj_enum == 'OBJ_125_All_Frames': frames = frames_125_All_Frames
        if my_prop.obj_enum == 'OBJ_MV_Stenosis': frames = frames_MV_Stenosis
        if my_prop.obj_enum == 'OBJ_Abd_Aort_IVC': frames = frames_Abd_Aort_IVC

        # Регистрируем последний кадр по выбранному
        if my_prop.frames_enum == '25': frame_end = 25
        if my_prop.frames_enum == '125': frame_end = 125        
        
        
        """ БЛОК: Ставим в нужный кадр и применяем форму. """
        for i in frames:
            bpy.context.scene.frame_current = i
            bpy.ops.object.join_shapes()

        
        """ БЛОК: Переименовываем ключи по порядку сверху вниз. """
        index = 1
        for i in frames:    
            obj.data.shape_keys.key_blocks[index].name = str(i)
            index = index + 1
        all_shape_keys = obj.data.shape_keys.key_blocks # список всех форм 

        
        """ БЛОК: Ставим ключи анимации. """
        for i in frames: 
            # ставим в кадр 
            bpy.context.scene.frame_current = i    
            
            # бежим по списку форм, если имя формы равно текущему кадру,
            # то ставим его значение в 1.0, иначе в 0.0.
            for SKey in all_shape_keys:
                if (SKey.name == str(i)):
                    SKey.value = 1.0 # ставим значение
                else:
                    SKey.value = 0.0 # ставим значение
                SKey.keyframe_insert("value", frame=i) # ставим ключ

        
        """ БЛОК: Работа с последним кадром. В последнем кадре нужен первая форма. """
        # ставим в последний кадр
        bpy.context.scene.frame_current = frame_end 

        # бежим по списку форм, если имя формы равно первому,
        # то ставим его значение в 1.0, иначе в 0.0.
        for SKey in all_shape_keys:
            if (SKey.name == str(frames[0])):
                SKey.value = 1.0 # ставим значение
            else:
                SKey.value = 0.0 # ставим значение
            SKey.keyframe_insert("value", frame=frame_end) # ставим ключ


        """ БЛОК: Изменение интерполяции ключей """
        obj = bpy.context.object # доступ к объекту        
        for fcu in obj.data.shape_keys.animation_data.action.fcurves: # перебор кривых
            for keyframe in fcu.keyframe_points: # перебор ключей
                keyframe.interpolation = 'LINEAR'


        print(my_prop.obj_enum)
        print(my_prop.frames_enum)
        print(obj.name)
        print(frames)
        print(str(frame_end))
        return {'FINISHED'}



def register(): 
    bpy.utils.register_class(EIDOS_AnimationCreate_PT_MainPanel)
    bpy.utils.register_class(EIDOS_AnimationCreate_PG_OBJ)
    bpy.utils.register_class(EIDOS_AnimationCreate_OT_AniCreate)

    # подключение глобального свойства
    bpy.types.Scene.my_group_prop = bpy.props.PointerProperty(type= EIDOS_AnimationCreate_PG_OBJ)

def unregister(): 
    bpy.utils.unregister_class(EIDOS_AnimationCreate_PT_MainPanel)
    bpy.utils.unregister_class(EIDOS_AnimationCreate_PG_OBJ)
    bpy.utils.unregister_class(EIDOS_AnimationCreate_OT_AniCreate)

    # отключение глобального свойства
    del bpy.types.Scene.my_group_prop

if __name__ == "__main__": 
    register() 