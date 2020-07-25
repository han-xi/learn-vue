import ajax from "./config.js"

export default (data)=>{
    return ajax.put(`/userUpdate`, data);
}   