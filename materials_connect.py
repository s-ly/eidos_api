# Разделитель полигонов по материалам по шаблону - ver 1.0.
# Затем отсоеденяет полигоны в отдельные мешы,
# затем снова всё склеивает. 
# Таким образом, например, отделяются все капы от остального меша.
# Работает в режиме объекта

import bpy # базовый 
import re # для регулярных авражений

#Шаблон имён материалов
#materialNameSelect = r'm2_'
#materialNameSelect = r'out_'
materialNameSelect = r'in_'
#materialNameSelect = r'bModeRing'
#materialNameSelect = r'bModeHole'
#materialNameSelect = r'segmentWall_'

# ссылки на выбранный объект и его слот материалов
obj = bpy.context.object
mat_slot = obj.material_slots

bpy.ops.object.mode_set(mode='EDIT') # режим редактирования
bpy.ops.mesh.reveal() # показать всё
bpy.ops.mesh.select_all(action='DESELECT') # снять выделение 

matIndex = 0
for i in mat_slot:    
    obj.active_material_index = matIndex # выбраем материал по индексу
    nameMat = obj.active_material.name # узнаём имя материала    
    matIndex = matIndex + 1 # для перехода к следующему материалу в слоте
    
    # проверка совпадения имени материала
    if re.match(materialNameSelect, nameMat):
        bpy.ops.object.material_slot_select() # выбираем полигоны материала        
        
        # проверка на пустой материал
        try:
            bpy.ops.mesh.separate(type='SELECTED') # отделяет выбранные грани 
        except RuntimeError:
            print('Материал: ' + nameMat + ' пустой')
        
        bpy.ops.mesh.select_all(action='DESELECT') # снять выделение  
    
bpy.ops.object.mode_set(mode='OBJECT') # режим объекта
bpy.ops.object.join() # объеденить объекты