import ajax from "./config.js"

export default ()=>{
    return ajax.get(`/mail`);
}