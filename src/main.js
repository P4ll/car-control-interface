import Vue from 'vue'
import App from './App.vue'
import './quasar'

import VueRouter from 'vue-router'

import MainScreen from './pages/MainScreen.vue'
import ConnectionSetting from './pages/ConnectionSetting.vue'

const router = new VueRouter({
  routes: [
    {path: '/', redirect: '/setting' },
    {path: '/control', component: MainScreen},
    {path: '/setting', component: ConnectionSetting},
  ]
})

Vue.config.productionTip = false
Vue.use(VueRouter)

new Vue({
  router: router,
  render: h => h(App),
}).$mount('#app')
