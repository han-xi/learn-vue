import axios from "axios"
import {getCookie} from '@/api/util/util'
import router from "@/router/index"

const ajax=axios.create({
  baseURL:"http://localhost:9004",
  timeout:5000,
  withCredentials :true,
})



// http request 拦截器
ajax.interceptors.request.use(
  config => {
    const token = getCookie('u_uuid'); //获取Cookie
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
//console.log(response.data.errCode)
console.log(response.data["errCode"])
if(response.data["errCode"] == 2) {
  console.log("123455")
      router.push({
        path: '/PersonalCenterLogin',
       // query: {redirect: router.currentRoute.fullPath} //从哪个页面跳转
      })
    }
    return response;
  },
  error => {
    if(error.response.status==301){//如果是before_request中检测到丢失用户名则重新登录
    if(error.response.data["errCode"] == 2) {
      alert("请登录")
          router.push({
            path: '/PersonalCenterLogin',
           // query: {redirect: router.currentRoute.fullPath} //从哪个页面跳转
          })
        }
      }
    //console.log(error.response.data.errCode)
    else
    {
      if(error.response.status ==311){//登录界面反馈错误信息的状态号311
        alert(error.response.data.error)
        return Promise.reject(error.response.data)
      }
      else{
        return Promise.reject(error.response.data)
      }
    }
    
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