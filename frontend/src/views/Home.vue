<template>
  <div>
    <EquipmentForm @created="reloadList" />
    <EquipmentList ref="listRef" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import EquipmentForm from '../components/EquipmentForm.vue'
import EquipmentList from '../components/EquipmentList.vue'

const listRef = ref()

const reloadList = () => {
  listRef.value?.load()
}
</script>
