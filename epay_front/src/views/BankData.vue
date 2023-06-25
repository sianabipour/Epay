<template>
  <div class="DoneView">
    <div class="container text-center" v-if="x">
        <h5>مبلغ مشخص شده را به شماره کارت زیر واریز کنید</h5>
        <div class="card mt-4">
            <img class="card-bg" src="../assets/card.jpg" alt="">
            <p class="card-number">{{x.bank_card_number}}</p>
            <p class="card-name">{{x.card_name}}</p>
        </div>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  name: 'DoneView',
  data () {
    return {
      x: null
    }
  },
  mounted: function () {
    this.$axios
      .get(this.$BASE_URL_BACKEND + '/get-bank-data/')
      .then(response => {
        if (response.data.Code === 200) {
          this.x = response.data
        } else {
          Swal.fire({
            icon: 'error',
            title: 'خطا',
            showConfirmButton: false,
            timer: 1500
          })
        }
      })
  }
}
</script>
<style scoped>
.card{
    border: none;
}
.card-bg{
    border-radius: 25px;
}
.card-number{
    position: absolute;
    top: 172px;
    right: 0;
    left: 0;
    font-size: 29pt;
    color: white;
}
.card-name{
    position: absolute;
    top: 240px;
    right: 0;
    left: 0;
    font-size: 18pt;
    font-weight: bold;
    color: white;
}
</style>
