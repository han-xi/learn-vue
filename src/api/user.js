import ajax from "./config.js"
import md5 from 'js-md5';
export default{
    login(username,password){
        let md5password=md5(password)
        return ajax.post(`/user/login`,{"username":username,"password":md5password});
    },
    register(username){
        return ajax.post(`/user/register`, {"username":username});
    },
    forget(username){
        return ajax.post(`/user/forget`, {"username":username});
    },
    setpassword(password){
        let md5password=md5(password)
        return ajax.post(`/user/setpassword`, {"password":md5password});
    },
    changepassword(password){
        let md5password=md5(password)
        return ajax.post(`/user/changepassword`, {"password":md5password});
    },
    logout(){
        return ajax.post(`/user/logout`);
    }      

}

