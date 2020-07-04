import axios from "axios";

const ajax = axios.create({
  baseURL: "http://localhost:8080"
});

export default ajax;