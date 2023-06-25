<template>
  <div class="LoginForm">
    <div class="margin form" v-if="!wait_code">
        <div class="mb-3">
            <label for="username" class="form-label">نام کاربری</label>
            <input autocomplete="off" type="text" v-model="username" class="form-control" id="username">
        </div>
        <button class="btn btn-info button" @click="login_api">ثبت</button>
    </div>
    <div class="margin form" v-if="wait_code">
        <div class="mb-3">
            <label for="code" class="form-label">کد یک بارمصرف</label>
            <input autocomplete="off" type="text" v-model="code" class="form-control" id="code">
        </div>
        <button class="btn btn-info" @click="check_login_api">ثبت</button>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  name: 'LoginForm',
  data () {
    return {
      username: '',
      wait_code: false,
      code: ''
    }
  },
  methods: {
    login_api: function () {
      this.$axios
        .get(this.$BASE_URL_BACKEND + '/gen-code/?phone=' + this.username)
        .then(response => {
          if (response.data.Code === 200) {
            this.wait_code = true
          } else {
            Swal.fire({
              icon: 'error',
              title: 'حساب کاربری یافت نشد',
              showConfirmButton: false,
              timer: 1500
            })
          }
        })
    },
    check_login_api: function () {
      this.$axios
        .get(this.$BASE_URL_BACKEND + '/check-code/?code=' + this.code)
        .then(response => {
          if (response.data.Code === 200) {
            document.location.reload()
          } else {
            Swal.fire({
              icon: 'error',
              title: 'کد وارد شده اشتباه است',
              showConfirmButton: false,
              timer: 1500
            })
          }
        })
    }
  }
}
</script>

<style scoped>

</style>
