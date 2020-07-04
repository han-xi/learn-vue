import ajax from "./config.js"

export default {
  table(data, page, size) {
    return ajax.post(`/search/table/${page}/${size}`, data);
  }
  
}