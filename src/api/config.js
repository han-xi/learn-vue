import axios from "axios";

const ajax = axios.create({
  baseURL: "http://localhost:9004"
});

export default ajax;