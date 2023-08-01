# Выделение полигонов от материалов по шаблону. ver 1.0
# Работает в режиме редактирования


import bpy
import re


#Шаблон
#materialNameSelect = r'out_'
#materialNameSelect = r'in_'
#materialNameSelect = r'bModeRing'
materialNameSelect = r'bModeHole'
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