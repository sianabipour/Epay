<template>
  <div class="CopyInput">
    <div class="container position-relative text-center">
        <input type="text" id="page-link" :value="baseUrl + $route.fullPath" class="form-control mt-3" >
        <button class="btn btn-info button share-button my-3" @click="copy">کپی</button>
        <router-link to="/" class="btn btn-info button my-3">بازگشت به صفحه ساخت فاکتور</router-link>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  name: 'CopyInput',
  data () {
    return {
      baseUrl: window.location.origin
    }
  },
  methods: {
    copy: function () {
      var copyText = document.getElementById('page-link')
      copyText.select()
      navigator.clipboard.writeText(copyText.value)
      Swal.fire({
        position: 'center',
        icon: 'success',
        title: 'کپی شد',
        showConfirmButton: false,
        timer: 1500
      })
    }
  }
}
</script>

<style scoped>
.share-button{
  position: absolute;
  top: -16px;
  right: 12px;
}
</style>
