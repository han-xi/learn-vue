import Vue from 'vue'
import Router from 'vue-router'

import PersonalCenter from '@/components/PersonalCenter'
import PersonalCenterRegister from '@/components/PersonalCenterRegister'
import PersonalCenterLogin from '@/components/PersonalCenterLogin'
import PersonalCenterForget from '@/components/PersonalCenterForget'


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
router.beforeEach((to, from, next)=>{
  //路由中设置的needLogin字段就在to当中 
  if(window.sessionStorage.data){
   console.log(window.sessionStorage);
   // console.log(to.path) //每次跳转的路径
   if(to.path === '/'){
    //登录状态下 访问login.vue页面 会跳到index.vue
    next({path: '/PersonalCenter'});
   }else{
    next();
   }
  }else{
   // 如果没有session ,访问任何页面。都会进入到 登录页
   if (to.path === '/') { // 如果是登录页面的话，直接next() -->解决注销后的循环执行bug
    next();
   } else { // 否则 跳转到登录页面
    next({ path: '/' });
   }
  }
})
export default router;