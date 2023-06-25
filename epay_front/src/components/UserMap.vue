<template>
  <div class="UserMap">
        <div class="open-map" @click="open_map()">
            <p>برای انتخاب مکان از روی نقشه اینجا کلیک کنید</p>
        </div>
        <div v-if="open" id="map"></div>
        <span v-if="open" @click="close_map()" class="close">X</span>
        <textarea v-if="open" class="form-control textarea" v-model="address"></textarea>
        <button v-if="open" @click="done()" class="btn btn-info">ثبت</button>
  </div>
</template>
<script>
/* eslint-disable */

export default {
  name: 'UserMap',
  data () {
    return {
      open: false,
      address: '',
    }
  },
  mounted: function () {},
  methods: {
    done: function () {
        this.$emit('done',this.address)
        this.close_map()
    },
    close_map: function () {
      this.open = false
      this.address = ''
    },
    open_map: function () {
      this.open = true
      const Mapp = window.Mapp
      const $ = window.jQuery
      var self = this
      $(document).ready(function () {
        var app = new Mapp({
          element: '#map',
          presets: {
            latlng: {
              lat: 32,
              lng: 52
            },
            zoom: 6
          },
          apiKey: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjFiODZjZDk2YTc0YjBmOGZlOGVmOWQwOTYxOTZjNzBmNzk0ZDhhYjg2MDkzYTk4NjcyYmYwOTc3MjgwYzU0Yzc0NmY0NmJmNGE2MDMzYjQ3In0.eyJhdWQiOiIxODE0NCIsImp0aSI6IjFiODZjZDk2YTc0YjBmOGZlOGVmOWQwOTYxOTZjNzBmNzk0ZDhhYjg2MDkzYTk4NjcyYmYwOTc3MjgwYzU0Yzc0NmY0NmJmNGE2MDMzYjQ3IiwiaWF0IjoxNjUzOTU2Mzg5LCJuYmYiOjE2NTM5NTYzODksImV4cCI6MTY1NjYzNDc4OSwic3ViIjoiIiwic2NvcGVzIjpbImJhc2ljIl19.d2E704GozA4eXZUIj-Ck_LiDwY4pmyVoG6xy6iQ6G45dz2lhr93ndwIAIc1fjiqvmfyGXs6FL41fU_5_GPUw5WdQRlH0DAxA_RPVo_0-dmQ1r31bocB28r1cA71YFvc38V8M5Y6NnxeA1EFqKJu3lOQjhiMMQaPOUqgfHelaVbMcjQXyJlCBpUkdcDHdcey2Kp--bMsJ5JVc62RIL59EQt5gS7DQo_ZDIeLEiednr65XJpWjZXTAZ0wkqTHv9jGvzArPR3LkC_-SyGJDhQ2-7UorvNS3jGjo_bpjWXV4e0SV9Ei05__JA8mU28rw45Gi-upIKTZENl9_fNdSuc8KGQ'
        })
        app.addLayers()
        app.addLocale()
        app.map.on('click', function (e) {
          app.findReverseGeocode({
            state: {
              latlng: {
                lat: e.latlng.lat,
                lng: e.latlng.lng
              },
              zoom: 12
            },
            after: function (data) {
              self.address = data.address
              app.addMarker({
                name: 'marker',
                latlng: {
                  lat: e.latlng.lat,
                  lng: e.latlng.lng
                }, 
                icon: app.icons.red,
                popup: false,
                pan: true
              })
            }
          })
        })
      })
    }
  }
}
</script>

<style scoped>
p{
  font-size: 11pt;
  font-weight: bold;
  margin: auto;
  color: gray;
}
.open-map{
  cursor: pointer;
  display: flex;
  height: 100%;
  width: 100%;
  background: white;
  min-height: 100px;
  border: solid 1px gray;
  border-radius: 15px;
}
#map{
  height: 100%;
  width: 100%;
  position: fixed !important;
  top: 0;
  left: 0;
}
.close{
  cursor: pointer;
  position: fixed;
  top: 0;
  right: 0;
  padding: 16px;
  font-size: 15pt;
  font-weight: bold;
}
.textarea{
  position: fixed;
  bottom:82px;
  right: 0;
  margin: auto;
  left: 0;
  height: 20px;
  width: 90%;
  padding: 16px;
  z-index: 100;
}
button{
  position: fixed;
  bottom:20px;
  right: 0;
  margin: auto;
  left: 0;
  width: 90%;
  padding: 16px;
  z-index: 100;
}
</style>
