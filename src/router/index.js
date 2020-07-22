import Vue from 'vue'
import Router from 'vue-router'
import {delCookie,getCookie} from '@/api/util/util'
import PersonalCenter from '@/components/PersonalCenter'
import PersonalCenterRegister from '@/components/PersonalCenterRegister'
import PersonalCenterLogin from '@/components/PersonalCenterLogin'
import PersonalCenterForget from '@/components/PersonalCenterForget'
import {post,fetch} from '@/api/config.js'

Vue.use(Router)

const router= new Router({
  routes: [
    {
      path: '/',
      name: 'PersonalCenterLogin',
      component: PersonalCenterLogin
    },
    {
      path: '/PersonalCenter',
      name: 'PersonalCenter',
      component: PersonalCenter,
      meta:{
        needLogin: true
       }
    },
    {
      path: '/PersonalCenterRegister',
      name: 'PersonalCenterRegister',
      component: PersonalCenterRegister
    },
    {
      path: '/PersonalCenterLogin',
      name: 'PersonalCenterLogin',
      component: PersonalCenterLogin
    },
    {
      path: '/PersonalCenterForget',
      name: 'PersonalCenterForget',
      component: PersonalCenterForget
    },
  ]
})
// router.beforeEach((to, from, next)=>{
//   //路由中设置的needLogin字段就在to当中 
//   if(window.sessionStorage.data){
//    console.log(window.sessionStorage);
//    // console.log(to.path) //每次跳转的路径
//    if(to.path === '/'){
//     //登录状态下 访问login.vue页面 会跳到index.vue
//     next({path: '/PersonalCenter'});
//    }else{
//     next();
//    }
//   }else{
//    // 如果没有session ,访问任何页面。都会进入到 登录页
//    if (to.path === '/') { // 如果是登录页面的话，直接next() -->解决注销后的循环执行bug
//     next();
//    } else { // 否则 跳转到登录页面
//     next({ path: '/' });
//    }
//   }
// })
//路由守卫
//这个是请求页面路由的时候会验证token存不存在，不存在的话会到登录页
// router.beforeEach((to, from, next) => {
//   if(to.meta.requireAuth) {
//    fetch('/islogin').then(res => {
//     if(res.errCode == 200) {
//      next();
//     } else {
//      if(getCookie('session')) {
//       delCookie('session');
//      }
//     //  if(getCookie('u_uuid')) {
//     //   delCookie('u_uuid');
//     //  }
//      next({
//       path: '/PersonalCenterLogin'
//      });
//     }
//    });
//   } else {
//    next();
//   }
//  });

export default router;