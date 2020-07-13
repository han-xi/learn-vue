import ajax from "./config.js"

export default (username,password)=>{
    return ajax.get(`/${username}/${password}`);
}