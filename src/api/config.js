import axios from "axios"
import {getCookie} from '@/util/util'

const ajax=axios.create({
  baseURL:"http://localhost:9004",
  timeout:5000
})



// http request 拦截器
ajax.interceptors.request.use(
  config => {
    const token = getCookie('session'); //获取Cookie
    config.data = JSON.stringify(config.data);
    
    config.headers = {
      'Content-Type':'application/x-www-form-urlencoded' ,//设置跨域头部
    };
    if (token) {
      config.params = {'token': token} //后台接收的参数
    }
    return config;
  },
  err => {
    return Promise.reject(err);
  }
);
// http response 拦截器
ajax.interceptors.response.use(
  response => {
//response.data.errCode是接口返回的值，如果值为2，说明Cookie丢失，然后跳转到登录页，这里根据大家自己的情况来设定
    if(response.data.errCode == 2) {
      router.push({
        path: '/PersonalCenterLogin',
        query: {redirect: router.currentRoute.fullPath} //从哪个页面跳转
      })
    }
    return response;
  },
  error => {
    return Promise.reject(error.response.data)
  });
export default ajax;
export function fetch(url, params = {}) {
 
  return new Promise((resolve, reject) => {
    axios.get(url, {
      params: params
    })
    .then(response => {
      resolve(response.data);
    })
    .catch(err => {
      reject(err)
    })
  })
}

export function post(url, data = {}) {
 return new Promise((resolve, reject) => {
   axios.post(url, data)
     .then(response => {
       resolve(response.data);
     }, err => {
       reject(err);
     })
 })
}