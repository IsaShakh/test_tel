<template>
  <div>
    <el-input
      v-model="search"
      placeholder="Поиск по SN или примечанию"
      class="mb-4"
      clearable
      @input="load"
    />

    <el-table :data="items" stripe border style="width: 100%">
      <el-table-column prop="id" label="ID" width="70" />
      
      <el-table-column label="Тип оборудования">
        <template #default="scope">
          <div v-if="editId !== scope.row.id">{{ scope.row.type_id }}</div>
          <el-input
            v-else
            v-model="editItem.type_id"
            size="small"
            placeholder="ID типа"
          />
        </template>
      </el-table-column>

      <el-table-column label="Серийный номер">
        <template #default="scope">
          <div v-if="editId !== scope.row.id">{{ scope.row.serial_number }}</div>
          <el-input
            v-else
            v-model="editItem.serial_number"
            size="small"
          />
        </template>
      </el-table-column>

      <el-table-column label="Примечание">
        <template #default="scope">
          <div v-if="editId !== scope.row.id">{{ scope.row.comment }}</div>
          <el-input
            v-else
            v-model="editItem.comment"
            type="textarea"
            autosize
            size="small"
          />
        </template>
      </el-table-column>

      <el-table-column label="Действия" width="180">
        <template #default="scope">
          <el-button
            v-if="editId !== scope.row.id"
            size="small"
            type="primary"
            icon="el-icon-edit"
            @click="startEdit(scope.row)"
          >
            Редактировать
          </el-button>

          <el-button
            v-else
            size="small"
            type="success"
            icon="el-icon-check"
            @click="saveEdit(scope.row.id)"
          >
            Сохранить
          </el-button>

          <el-button
            size="small"
            type="danger"
            icon="el-icon-delete"
            @click="remove(scope.row.id)"
          >
            Удалить
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { ElMessageBox, ElMessage } from 'element-plus'

const items = ref([])
const search = ref('')

const editId = ref(null)
const editItem = ref({})

const load = async () => {
  const res = await api.get('equipment/', { params: { search: search.value } })
  items.value = res.data.items
}

const startEdit = (item) => {
  editId.value = item.id
  editItem.value = { ...item }
}

const saveEdit = async (id) => {
  try {
    const res = await api.put(`equipment/${id}/`, editItem.value)
    const index = items.value.findIndex(i => i.id === id)
    items.value[index] = res.data.data
    editId.value = null
    ElMessage.success('Сохранено')
  } catch (e) {
    ElMessage.error('Ошибка при сохранении')
  }
}

const remove = async (id) => {
  try {
    await ElMessageBox.confirm(
      'Вы уверены, что хотите удалить запись?',
      'Подтверждение',
      {
        confirmButtonText: 'Да',
        cancelButtonText: 'Отмена',
        type: 'warning',
      }
    )
    await api.delete(`equipment/${id}/`)
    items.value = items.value.filter(i => i.id !== id)
    ElMessage.success('Удалено')
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('Ошибка при удалении')
    }
  }
}

onMounted(load)

defineExpose({ load }) 
</script>

<style scoped>
.mb-4 {
  margin-bottom: 1rem;
}
</style>
