<template>
  <div class="FactorEditView">
    <h4 class="text-center">اصلاح فاکتور</h4>
    <div class="margin form" v-if="factor">
        <div class="mb-3">
            <label class="form-label">شماره فاکتور : {{factor.id}}</label>
        </div>
        <div class="mb-3">
            <label for="name" class="form-label">قیمت</label>
            <input type="text" v-model="factor.price"  class="form-control" id="name">
        </div>
        <div class="mb-3">
            <label for="nickname" class="form-label">نام مستعار</label>
            <input type="text" v-model="factor.nickname" class="form-control" id="nickname">
        </div>
        <div class="mb-3">
            <label for="name" class="form-label">نام و نام خانوادگی</label>
            <input type="text" v-model="factor.name"  class="form-control" id="name">
        </div>
        <div class="mb-3">
            <label for="phone" class="form-label">شماره تماس</label>
            <input type="text" v-model="factor.phone" inputmode="digits" class="form-control" id="phone">
        </div>
        <div class="mb-3">
            <label for="address" class="form-label">آدرس پستی</label>
            <textarea v-model="factor.address" class="form-control" id="address" placeholder="مثال : تهران ، ستارخان ، خیابان صحرایی ..."></textarea>
        </div>
        <div class="mb-3">
            <label for="description" class="form-label">توضیحات بیشتر</label>
            <textarea v-model="factor.description"  class="form-control" id="description" placeholder="لیست سفارش به همراه تعداد و طعم"></textarea>
        </div>
      <button class="btn btn-info" @click="send_data">ثبت</button>
    </div>
    <div class="container position-relative text-center mt-3">
        <router-link to="/factors" class="btn btn-light button my-3 w-100">لیست فاکتور ها</router-link>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  name: 'FactorEditView',
  data () {
    return {
      factor: null
    }
  },
  mounted: function () {
    this.$axios
      .get(this.$BASE_URL_BACKEND + '/factor-for-edit/?pk=' + this.$route.params.id)
      .then(response => {
        if (response.data.Code === 200) {
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
      bodyFormData.append('price', this.factor.price)
      bodyFormData.append('nickname', this.factor.nickname)
      bodyFormData.append('name', this.factor.name)
      bodyFormData.append('phone', this.factor.phone)
      bodyFormData.append('address', this.factor.address)
      bodyFormData.append('description', this.factor.description)

      this.$axios({
        method: 'post',
        url: this.$BASE_URL_BACKEND + '/edit-factor/?pk=' + this.$route.params.id,
        data: bodyFormData,
        headers: { 'Content-Type': 'multipart/form-data' }
      })
        .then(response => {
          if (response.data.Code === 200) {
            Swal.fire({
              icon: 'success',
              title: 'ثبت شد',
              showConfirmButton: false,
              timer: 1000
            })
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
