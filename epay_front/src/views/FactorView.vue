<template>
  <div class="FactorView">
    <div class="container">
      <CopyInput v-if="$is_authenticated" />
      <UserForm />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import UserForm from '@/components/UserForm.vue'
import CopyInput from '@/components/CopyInput.vue'

export default {
  name: 'FactorView',
  components: {
    UserForm,
    CopyInput
  }
}
</script>
