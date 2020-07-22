// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';

import Vue from 'vue'
import App from './App'
import router from './router'
Vue.use(Element)
import ajax from './api/config.js'

//import Mint from 'mint-ui';
//import 'mint-ui/lib/style.css';
//Vue.use(Mint);


import  './assets/icon/iconfont.css';
//axios.defaults.headers.post['Content-Type'] = 'application/json';


Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App>'
})
