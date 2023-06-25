<template>
  <div class="HomeView">
    <AdminForm v-if="$is_authenticated" />
    <LoginForm v-if="!$is_authenticated" />
  </div>
</template>

<script>
// @ is an alias to /src
import AdminForm from '@/components/AdminForm.vue'
import LoginForm from '@/components/LoginForm.vue'

export default {
  name: 'HomeView',
  components: {
    AdminForm,
    LoginForm
  }
}
</script>
