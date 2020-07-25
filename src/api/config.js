import axios from "axios"
import {getCookie} from '@/api/util/util'
import router from "@/router/index"

const ajax=axios.create({
  baseURL:"http://localhost:9004",
  timeout:50000,
  withCredentials :true,
})



// http request 拦截器
ajax.interceptors.request.use(
  config => {
    // const token = getCookie('u_uuid'); //获取Cookie
    config.data = JSON.stringify(config.data);
    config.headers = {
      'Content-Type':'application/x-www-form-urlencoded' ,//设置跨域头部
    };
    // if (token) {
    //   config.params = {'token': token} //后台接收的参数
    // }
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
//console.log(response.data["errCode"])
if(response.data&&response.data["errCode"] == 2) {
  //console.log("123455")
      router.push({
        path: '/',
        query: {redirect: to.fullPath} //从哪个页面跳转
      })
      return new Promise(() => {})
    }
    return response;
  },
  error => {
    if(error.response &&error.response.status==401){//表示用户没有权限（令牌、用户名、密码错误）。
    if(error.response.data["errCode"]&&error.response.data["errCode"] == 2) {//如果是before_request中检测到丢失sessionid则重新登录
      alert("请登录")
          router.push({
            path: '/PersonalCenterLogin',
           // query: {redirect: router.currentRoute.fullPath} //从哪个页面跳转
          })
          return new Promise(() => {})
        }
        else{//表示用户名或密码不对
          //alert("用户名或密码错误")
          //return new Promise(() => {})//终止
          return Promise.reject(error)
        }
      }
      else if(error.response&&error.response.status===500){//数据库访问失败
        alert("数据库连接失败")
        return new Promise(() => {})//终止
      }
    else if(error.response&&error.response.status===510){//邮件发送失败
        return Promise.reject(error)
    }
    else
    {
      alert(error.message)
      console.log('Error', error.message);
      return new Promise(() => {})//终止
      }
    });
export default ajax;
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
export function put(url, data = {}) {
  return new Promise((resolve, reject) => {
    axios.put(url, data)
      .then(response => {
        resolve(response.data);
      }, err => {
        reject(err);
      })
  })
}