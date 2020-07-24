import ajax from "./config.js"

export default (data)=>{
    return ajax.post(`/userLogin`,data);
}