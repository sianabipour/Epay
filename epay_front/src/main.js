import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueCookies from 'vue3-cookies'
import VueFeather from 'vue-feather'
import axios from 'axios'

const app = createApp(App)

app.use(VueCookies, { secure: true })
app.use(router)

app.component(VueFeather.name, VueFeather)

app.mixin({
  methods: {
    change_address: function (n) {

    }
  }
})

if (process.env.NODE_ENV === 'production') {
  // app.config.globalProperties.$BASE_URL_BACKEND = 'https://epayback.upidea.ir'
  app.config.globalProperties.$BASE_URL_BACKEND = 'http://127.0.0.1:8000'
} else {
  app.config.globalProperties.$BASE_URL_BACKEND = 'http://127.0.0.1:8000'
}

app.config.globalProperties.$axios = axios

if (app.config.globalProperties.$cookies.get('sessionid') == null) {
  axios
    .get(app.config.globalProperties.$BASE_URL_BACKEND + '/get-public-key/')
    .then(res => {
      app.config.globalProperties.$cookies.set('sessionid', res.data.key)
      axios.defaults.headers.common.Authorization = app.config.globalProperties.$cookies.get('sessionid')
      app.config.globalProperties.$is_authenticated = false
      app.config.globalProperties.$User = null
      app.config.globalProperties.$online_mode = false
      app.config.globalProperties.$offline_mode = false
      app.mount('#app')
    })
} else {
  axios.defaults.headers.common.Authorization = app.config.globalProperties.$cookies.get('sessionid')
  axios
    .get(app.config.globalProperties.$BASE_URL_BACKEND + '/is-authenticated/')
    .then(response => {
      if (response.data.Code === 200) {
        app.config.globalProperties.$is_authenticated = true
        app.config.globalProperties.$User = response.data.User
        app.config.globalProperties.$online_mode = response.data.online
        app.config.globalProperties.$offline_mode = response.data.offline
      } else if (response.data.Code === 401) {
        app.config.globalProperties.$is_authenticated = false
        app.config.globalProperties.$User = null
        app.config.globalProperties.$online_mode = false
        app.config.globalProperties.$offline_mode = false
      } else if (response.data.Code === 400) {
        axios
          .get(app.config.globalProperties.$BASE_URL_BACKEND + '/get-public-key/')
          .then(res => {
            app.config.globalProperties.$cookies.set('sessionid', res.data.key)
            axios.defaults.headers.common.Authorization = app.config.globalProperties.$cookies.get('sessionid')
            app.config.globalProperties.$is_authenticated = false
            app.config.globalProperties.$User = null
            app.config.globalProperties.$online_mode = false
            app.config.globalProperties.$offline_mode = false
          })
      }
      app.mount('#app')
    })
}
