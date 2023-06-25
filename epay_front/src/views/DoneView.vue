<template>
  <div class="DoneView">
    <div class="container text-center" v-if="factor">
        <h2>پرداخت انجام شد </h2>
        <h6>شماره فاکتور : {{this.$route.params.id}}</h6>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  name: 'DoneView',
  data () {
    return {
      factor: null
    }
  },
  mounted: function () {
    this.$axios
      .get(this.$BASE_URL_BACKEND + '/factor/?pk=' + this.$route.params.id)
      .then(response => {
        if (response.data.Code === 200 && response.data.status === true) {
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
  }
}
</script>
