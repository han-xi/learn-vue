<template>
  <div> 
    <div class="register-wrapper"> 
      <div id="register" >
        <p class="title">退出登录</p>
        <el-form
          :model="Login"
          status-icon
          :rules="rules2"
          ref="Login"
          label-width="0"
          class="demo-ruleForm"
        >
          <el-form-item>
          <el-button type="primary" @click="quit()" style="width:100%;">退出登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script> 
import delsession from "@/api/delsession";//登录post
export default {
  name:"PersonalCenterQuit", 
  data() {
    return {  
    }
  }, 
  methods: {
    quit(){
      //验证表单格式正确与否
          localStorage.clear();
          delsession().then(response=>{
this.$router.push({
        path: "/PersonalCenterLogin"
      });
          })
    },
      },
      mounted(){
    
    }
};
</script>
<style scoped>
.loading-wrapper {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  background: #aedff8;
  display: flex;
  align-items: center;
  justify-content: center;
}
.register-wrapper img {
  position: absolute;
  z-index: 1;
}
.register-wrapper {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
}
#register {
  max-width: 340px;
  margin: 60px auto;
  background: #fff !important;
  padding: 20px 40px;
  border-radius: 10px;
  position: relative;
  z-index: 9;
}
.title {
  font-size: 26px;
  line-height: 50px;
  font-weight: bold;
  margin: 10px;
  text-align: center;
}
.el-form-item {
  text-align: center;
}
.login {
  
  font-size: 14px;
  line-height: 22px;
  color: #1ab2ff;
  cursor: pointer;/*
  text-align: left;
  text-indent: 8px;
  width: 160px;
  margin-top: 10px;*/
}
.login:hover {
  color: #2c2fd6;
}
.code >>> .el-form-item__content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.code button {
  margin-left: 20px;
  width: 140px;
  text-align: center;
}
.el-button--primary:focus {
  background: #409EFF;
  border-color: #409EFF;
  color: #fff;
}
    .code-style{
        font-size: 16px;
        color: red;
        cursor: pointer;
    }
.confirm-botton{
        display: inline-block;
        width: 50px;
        background-color: #04b4ba;
        font-size: 16px;
        line-height: 32px;
        cursor: pointer;
    }
</style>
