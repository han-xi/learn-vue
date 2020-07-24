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

//路由守卫
router.beforeEach((to, from, next)=>{
  if(window.localStorage.user_name){//如果本地有用户名则表示已登录
    // console.log(to.path) //每次跳转的路径
    if(to.path === '/'){
      //登录状态下 访问login.vue页面 会跳到index.vue让其退出登录删除localStorage。user_name
      next({path: '/PersonalCenter'});
    }else{
      next();
    }
  }else{
   // 如果没有session ,访问任何页面。都会进入到 登录页
   if (to.path === '/') { // 如果是登录页面的话，直接next() -->解决注销后的循环执行bug
    next();
   } else { // 否则 跳转到登录页面
    next({ path: '/' ,query: {redirect: to.fullPath} });
   }
  }
})
export default router;