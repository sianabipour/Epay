<template>
  <div class="FactorsView">
    <div class="container position-relative text-center">
        <router-link to="/" class="btn btn-info button my-3">بازگشت به صفحه ساخت فاکتور</router-link>
    </div>
    <div class="container">
      <div class="card mb-4">
        <div class="card-header bg-info">
          فیلتر ها
        </div>
        <div class="card-body">
          <blockquote class="blockquote mb-0">
            <input type="text" v-model="query" class="form-control my-3" placeholder="جستجو میان فاکتور ها">
            <label class="form-label" for="mode">نوع فاکتور</label>
            <select class="form-select" v-model="mode" id="mode" aria-label="Default select example">
              <option value="online">درگاه پرداخت</option>
              <option value="offline">کارت به کارت</option>
            </select>
            <div class="mt-3">
              <div class="form-group">
                <label class="form-label" for="start_date">شروع بازه</label>
                <div class="row">
                  <div class="col-4">
                    <input id="start_date" v-model="start_date1" type="number" class="form-control mb-3" placeholder="روز">
                  </div>
                  <div class="col-4">
                    <input id="start_date" v-model="start_date2" type="number" class="form-control mb-3" placeholder="ماه">
                  </div>
                  <div class="col-4">
                    <input id="start_date" v-model="start_date3" type="number" class="form-control mb-3" placeholder="سال">
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label" for="end_date">پایان بازه</label>
                <div class="row">
                  <div class="col-4">
                    <input id="start_date" v-model="end_date1" type="number" class="form-control mb-3" placeholder="روز">
                  </div>
                  <div class="col-4">
                    <input id="start_date" v-model="end_date2" type="number" class="form-control mb-3" placeholder="ماه">
                  </div>
                  <div class="col-4">
                    <input id="start_date" v-model="end_date3" type="number" class="form-control mb-3" placeholder="سال">
                  </div>
                </div>
              </div>
              <div class="form-group col-6">
                <button @click="filter_date" class="btn btn-info mx-2">اعمال</button>
              </div>
            </div>
          </blockquote>
        </div>
      </div>
    </div>
    <div class="container" v-if="factors">
      <div class="card mb-4">
        <div class="card-header bg-info">
          نتایج
        </div>
        <div class="card-body">
          <blockquote class="blockquote mb-0">
            <h6 class="text-center my-3">تعداد فاکتور های در حال نمایش : {{factors_result.length.toLocaleString()}}</h6>
            <h6 class="text-center my-3">مجموع فاکتور های در حال نمایش : {{factors_result.map(factor => parseInt(factor.price)).reduce((acc, amount) => acc + amount).toLocaleString()}}</h6>
          </blockquote>
        </div>
      </div>
        <div :class="my_class(factor)" :key="factor" v-for="factor in factors_result">
            <table class="table table-sm">
                <tbody>
                    <tr>
                        <th scope="row">شماره فاکتور</th>
                        <td>{{parseInt(factor.id)}}</td>
                    </tr>
                    <tr>
                        <th scope="row">نام</th>
                        <td>{{factor.name}}</td>
                    </tr>
                    <tr>
                        <th scope="row">نام مستعار</th>
                        <td>{{factor.nickname}}</td>
                    </tr>
                    <tr>
                        <th scope="row">آدرس</th>
                        <td>{{factor.address}}</td>
                    </tr>
                    <tr>
                        <th scope="row">توضیحات</th>
                        <td>{{factor.description}}</td>
                    </tr>
                    <tr>
                        <th scope="row">شماره تماس</th>
                        <td>{{factor.phone}}</td>
                    </tr>
                    <tr>
                        <th scope="row">قیمت</th>
                        <td>{{parseInt(factor.price).toLocaleString()}}</td>
                    </tr>
                    <tr>
                        <th scope="row">تاریخ</th>
                        <td>{{factor.date}}</td>
                    </tr>
                    <tr>
                        <th scope="row">وضعیت</th>
                        <td>{{factor.status}}</td>
                    </tr>
                    <tr>
                        <th scope="row">نوع فاکتور</th>
                        <td v-if="factor.mode == 'online'">درگاه بانکی</td>
                        <td v-if="factor.mode == 'offline'">کارت به کارت</td>
                    </tr>
                    <tr>
                        <th scope="row">عملیات ها</th>
                        <td>
                          <button @click="delete_factor(factor.id)" class="btn btn-danger mx-2"><i class="fa fa-trash"></i></button>
                          <router-link :to="'/factor/edit/' + factor.id" class="btn btn-warning mx-2"><i class="fa-solid fa-pen"></i></router-link>
                          <button v-if="factor.status_bool" @click="print_factor(factor.id)" class="btn btn-info mx-2"><i class="fa-solid fa-print"></i></button>
                          <router-link v-if="!factor.status_bool" :to="'/factor/' + factor.id" class="btn btn-secondary mx-2"><i class="fas fa-link"></i></router-link>
                          <button v-if="!factor.status_bool && factor.mode === 'offline'" @click="pay_factor(factor.id)" class="btn btn-success mx-2"><i class="fa fa-credit-card"></i></button>
                          <button v-if="factor.phone && !factor.status_bool" @click="sms_factor(factor.id)" class="btn btn-dark mx-2"><i class="fas fa-sms"></i></button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  name: 'FactorsView',
  data () {
    return {
      factors: null,
      query: '',
      start_date1: null,
      start_date2: null,
      start_date3: null,
      end_date1: null,
      end_date2: null,
      end_date3: null,
      mode: ''
    }
  },
  methods: {
    sms_factor: function (id) {
      Swal.fire({
        title: 'از ارسال پیامک یادآوری مطمئن هستید؟',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'بله',
        cancelButtonText: 'انصراف'
      }).then((result) => {
        if (result.isConfirmed) {
          this.$axios
            .get(this.$BASE_URL_BACKEND + '/send-sms/?pk=' + id + '&link=' + window.location.origin + this.$route.fullPath)
            .then(response => {
              if (response.data.Code === 200) {
                Swal.fire({
                  icon: 'success',
                  title: 'ارسال',
                  showConfirmButton: false,
                  timer: 1000
                })
              } else {
                Swal.fire({
                  icon: 'error',
                  title: 'اشکال در سرور',
                  showConfirmButton: false,
                  timer: 1500
                })
              }
            })
        }
      })
    },
    pay_factor: function (id) {
      Swal.fire({
        title: 'مطمئن هستید این فاکتور پرداخت شده است؟',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'بله',
        cancelButtonText: 'انصراف'
      }).then((result) => {
        if (result.isConfirmed) {
          this.$axios
            .get(this.$BASE_URL_BACKEND + '/pay-factor/?pk=' + id)
            .then(response => {
              if (response.data.Code === 200) {
                Swal.fire({
                  icon: 'success',
                  title: 'ثبت شد',
                  showConfirmButton: false,
                  timer: 1000
                }).then((result) => {
                  location.reload()
                })
              } else {
                Swal.fire({
                  icon: 'error',
                  title: 'اشکال در سرور',
                  showConfirmButton: false,
                  timer: 1500
                })
              }
            })
        }
      })
    },
    delete_factor: function (id) {
      Swal.fire({
        title: 'از پاک شدن این فاکتور مطمئن هستید؟',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'حذف',
        cancelButtonText: 'انصراف'
      }).then((result) => {
        if (result.isConfirmed) {
          this.$axios
            .get(this.$BASE_URL_BACKEND + '/delete-factor/?pk=' + id)
            .then(response => {
              if (response.data.Code === 200) {
                Swal.fire({
                  icon: 'success',
                  title: 'ثبت شد',
                  showConfirmButton: false,
                  timer: 1000
                }).then((result) => {
                  location.reload()
                })
              } else {
                Swal.fire({
                  icon: 'error',
                  title: 'اشکال در سرور',
                  showConfirmButton: false,
                  timer: 1500
                })
              }
            })
        }
      })
    },
    print_factor: function (id) {
      Swal.fire({
        title: 'از پرینت دوباره این فاکتور مطمئن هستید؟',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'پرینت',
        cancelButtonText: 'انصراف'
      }).then((result) => {
        if (result.isConfirmed) {
          this.$axios
            .get(this.$BASE_URL_BACKEND + '/print-factor/?pk=' + id)
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
                  title: 'اشکال در سرور',
                  showConfirmButton: false,
                  timer: 1500
                })
              }
            })
        }
      })
    },
    my_class: function (factor) {
      if (factor.status_bool) {
        return ['factor-card', 'bg-done']
      } else {
        return ['factor-card', 'bg-error']
      }
    },
    filter_date: function () {
      var startdate = this.start_date3 + '-' + this.start_date2 + '-' + this.start_date1
      var enddate = this.end_date3 + '-' + this.end_date2 + '-' + this.end_date1
      this.$axios
        .get(this.$BASE_URL_BACKEND + '/get-factor-list/?date=' + startdate + ',' + enddate + '&mode=' + this.mode)
        .then(response => {
          if (response.data.Code === 200) {
            this.factors = response.data.list
            if (this.factors.length === 0) {
              Swal.fire({
                icon: 'warning',
                title: 'موردی در بازه موجود نیست',
                showConfirmButton: false,
                timer: 1500
              })
            } else {
              Swal.fire({
                icon: 'success',
                title: 'اعمال شد',
                showConfirmButton: false,
                timer: 1000
              })
            }
          } else {
            Swal.fire({
              icon: 'error',
              title: 'اشکال در سرور',
              showConfirmButton: false,
              timer: 1500
            })
          }
        })
    }
  },
  computed: {
    factors_result () {
      if (this.query !== '') {
        return this.factors.filter((item) => {
          return this.query.toLowerCase().split(' ').every(v => {
            return item.nickname.includes(v) || item.name.includes(v) || item.id.includes(v) || item.address.includes(v) || item.phone.includes(v) || item.description.includes(v) || item.price.includes(v) || item.date.includes(v) || item.status.includes(v)
          })
        })
      } else {
        return this.factors
      }
    }
  }
}
</script>

<style scoped>
.factor-card{
    border: solid 3px whitesmoke;
    border-radius: 20px;
    padding: 20px;
    margin: 10px 0px;
}
.bg-done{
    background: #69e5ae6e;
}
.bg-error{
    background: aliceblue;
}
.form-label{
  font-size: 12pt;
  font-weight: 600;
}
</style>
