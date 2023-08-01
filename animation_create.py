# Создаёт новые ключи формы по вторичному объекту и анимирует их.
# В строке frame вставить список ключевых кадров, с последним кадром.
# Далее выделяем объект с анимацией, потом объект на который нужно всё перенести.
# ВНИМАНИЕ!!! После завершения, вручную изменить интерполяцию кадров на линейную.

# Сюда вставить список ключевых кадров.
#frames = [0, 11, 15, 19] # Heart

# Abd_Aort, IVC (frame_end = 125)
frames = [0, 11, 15, 19, 25, 36, 40, 44, 50, 61, 65, 69, 75, 86, 90, 94, 100, 111, 115, 119] 

frame_end = 125

#MV "0, 2, 5, 11, 15, 19, 22, "
#TV "0, 5, 11, 15, 19, 22, " 
#PV "0, 3, 6, 9, 10, 11, 12, 15, 17, 19, " 
#AV "0, 3, 5, 6, 9, 11, 13, 15, 17, 19, 21, 23, " 
################################################################################
import bpy


obj = bpy.context.object # ссылка на объект


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