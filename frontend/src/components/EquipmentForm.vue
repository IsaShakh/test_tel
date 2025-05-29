<template>
  <el-form @submit.prevent="handleSubmit" label-position="top" label-width="100%">
    <el-form-item label="Тип оборудования">
      <el-select v-model="form.type_id" placeholder="Выберите тип" clearable>
        <el-option
          v-for="type in types"
          :key="type.id"
          :label="type.name"
          :value="type.id"
        />
      </el-select>
    </el-form-item>

    <el-form-item label="Серийные номера">
      <el-input
        type="textarea"
        v-model="form.serial_numbers"
        rows="4"
      />
    </el-form-item>

    <el-form-item label="Примечание">
      <el-input type="textarea" v-model="form.comment" rows="2" />
    </el-form-item>

    <el-button type="primary" native-type="submit">Добавить</el-button>

    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      class="mt-3"
    />

    <el-alert
      v-if="Object.keys(snErrors).length"
      title="Ошибки по серийным номерам:"
      type="warning"
      show-icon
      class="mt-4"
    >
      <template #default>
        <ul>
          <li v-for="(message, sn) in snErrors" :key="sn">
            <b>{{ sn }}</b>: {{ message }}
          </li>
        </ul>
      </template>
    </el-alert>
  </el-form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const emit = defineEmits(['created'])

const form = ref({
  type_id: '',
  serial_numbers: '',
  comment: ''
})

const types = ref([])
const error = ref('')
const snErrors = ref({})

onMounted(async () => {
  const res = await api.get('equipment-type/')
  types.value = res.data.items
})

const handleSubmit = async () => {
  snErrors.value = {}
  error.value = ''

  const serials = form.value.serial_numbers
    .split('\n')
    .map(s => s.trim())
    .filter(Boolean)

  const payload = serials.map(sn => ({
    type_id: form.value.type_id,
    serial_number: sn,
    comment: form.value.comment
  }))

  try {
    const res = await api.post('equipment/', payload)

    if (res.data.errors?.length > 0) {
      res.data.errors.forEach(err => {
        const sn = Object.keys(err)[0]
        const msg = err[sn]
        snErrors.value[sn] = msg
      })
    }

    if (res.data.created?.length > 0) {
      ElMessage.success(`Добавлено: ${res.data.created.length}`)
      form.value.serial_numbers = ''
      form.value.comment = ''
      emit('created') 
    }

  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка при отправке'
  }
}
</script>
