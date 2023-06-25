<template>
  <div class="AdminForm">
    <h5 class="text-center my-3">ساخت فاکتور جدید</h5>

    <div class="margin form">
      <div class="mb-3">
          <label for="nickname" class="form-label">نام مستعار</label>
          <input autocomplete="off" type="text" v-model="nickname" class="form-control" id="nickname">
      </div>
      <div class="mb-3">
          <label for="price" class="form-label">مبلغ فاکتور</label>
          <input autocomplete="off" type="number" v-model="price" inputmode="digits" class="form-control" id="price">
      </div>
      <div class="mb-3" dir="ltr">
          <h6 class="form-label">نوع فاکتور</h6>
          <hr>
          <label v-if="$online_mode" for="mode-online" class="form-label pointer">درگاه بانکی</label>
          <input v-if="$online_mode" class="mx-2" value="online" type="radio" v-model="mode" name="mode" id="mode-online">
          <br v-if="$online_mode">
          <label v-if="$offline_mode" for="mode-offline" class="form-label pointer">کارت به کارت</label>
          <input v-if="$offline_mode" class="mx-2" value="offline" type="radio" v-model="mode" name="mode" id="mode-offline">
      </div>
      <button class="btn btn-info" v-if="price !== '' && nickname !== '' && mode !== ''" @click="send_data">ثبت</button>
      <button class="btn btn-secondary" v-if="price === '' || nickname === '' || mode === ''">ثبت</button>
    </div>
    <div class="container position-relative text-center mt-3">
        <router-link to="/factors" class="btn btn-light button my-3 w-100">لیست فاکتور ها</router-link>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  name: 'AdminForm',
  data () {
    return {
      nickname: '',
      price: '',
      mode: ''
    }
  },
  methods: {
    send_data: function () {
      this.$axios
        .get(this.$BASE_URL_BACKEND + '/make-factor/?price=' + this.price + '&nickname=' + this.nickname + '&mode=' + this.mode)
        .then(response => {
          if (response.data.Code === 200) {
            this.$router.push('/factor/' + response.data.id)
          } else {
            Swal.fire({
              icon: 'error',
              title: 'حساب کاربری یافت نشد',
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
