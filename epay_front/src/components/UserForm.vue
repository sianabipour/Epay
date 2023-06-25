<template>
  <div class="UserForm">
    <div class="margin form" v-if="factor">
        <div class="mb-3">
            <label class="form-label">قیمت : {{factor.price}}</label>
        </div>
        <div class="mb-3">
            <label for="name" class="form-label">نام و نام خانوادگی</label>
            <input type="text" v-model="name"  class="form-control" id="name">
        </div>
        <div class="mb-3">
            <label for="phone" class="form-label">شماره تماس</label>
            <input type="text" v-model="phone" inputmode="digits" class="form-control" id="phone">
        </div>
        <div class="mb-3">
            <label for="address" class="form-label">آدرس پستی</label>
            <textarea v-model="address" class="form-control" id="address" placeholder="مثال : تهران ، ستارخان ، خیابان صحرایی ..."></textarea>
        </div>
        <div class="mb-3">
            <label for="address" class="form-label">نقشه</label>
            <UserMap @done="address = $event" />
        </div>
        <div class="mb-3">
            <label for="description" class="form-label">توضیحات بیشتر</label>
            <textarea v-model="description"  class="form-control" id="description" placeholder="لیست سفارش به همراه تعداد و طعم"></textarea>
        </div>
      <button class="btn btn-info" v-if="name != '' && phone != '' && address != ''" @click="send_data">ثبت</button>
      <button class="btn btn-secondary" v-if="name === '' || phone === '' || address === ''">ثبت</button>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'
import UserMap from '@/components/UserMap.vue'

export default {
  name: 'UserForm',
  components: {
    UserMap
  },
  data () {
    return {
      factor: null,
      name: '',
      phone: '',
      address: '',
      description: '',
      baseUrl: window.location.origin
    }
  },
  mounted: function () {
    this.$axios
      .get(this.$BASE_URL_BACKEND + '/factor/?pk=' + this.$route.params.id)
      .then(response => {
        if (response.data.Code === 200 && response.data.status === false) {
          this.factor = response.data
        } else {
          Swal.fire({
            icon: 'error',
            title: 'فاکتور یافت نشد',
            showConfirmButton: false,
            timer: 1500
          })
        }
      })
  },
  methods: {
    send_data: function () {
      var bodyFormData = new FormData()
      bodyFormData.append('name', this.name)
      bodyFormData.append('phone', this.phone)
      bodyFormData.append('address', this.address)
      bodyFormData.append('description', this.description)

      this.$axios({
        method: 'post',
        url: this.$BASE_URL_BACKEND + '/fill-factor/?pk=' + this.$route.params.id,
        data: bodyFormData,
        headers: { 'Content-Type': 'multipart/form-data' }
      })
        .then(response => {
          if (response.data.Code === 200) {
            if (response.data.mode) {
              location.href = this.$BASE_URL_BACKEND + '/request/' + this.factor.price + '/' + this.$route.params.id + '?callback=' + this.baseUrl + '/done/' + this.$route.params.id + '&sessionid=' + this.$cookies.get('sessionid')
            } else {
              Swal.fire({
                icon: 'success',
                title: 'ثبت شد',
                showConfirmButton: false,
                timer: 1000
              }).then((result) => {
                this.$router.push('/bank-data')
              })
            }
          } else {
            Swal.fire({
              icon: 'error',
              title: 'ثبت نشد',
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
