<template >
<div > 
<div v-if="name==='A'">
    <el-button type="primary"  class='bt' @click.native="gotologin()" style="width:10%;">登录</el-button>
    <el-button type="primary" class='bt' @click="gotoregister()" style="width:10%;margin-left:0px">注册</el-button>
    </div>
  <div v-else>
    <el-button type="primary" class='bt' style="width:15%;">{{name}}</el-button>
    <el-button type="primary" class='bt' @click="logout()" style="width:10%;margin-left:0px">注销</el-button>
    <el-button type="primary" class='bt' @click="setpassword()" style="width:10%;margin-left:0px">修改密码</el-button>

    </div>

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
          <el-button type="primary" @click="logout()" style="width:100%;">退出登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script> 
import user from "@/api/user";//登录post
import swal from 'sweetalert';
export default {
  name:"PersonalCenterQuit", 
  data() {
    
    return { 
    name: this.load()
    }
  }, 
  methods: {
    logout(){
      //验证表单格式正确与否
          localStorage.clear();
          user.logout().then(response=>{
            this.name="A"
            // window.location.reload()
          }).catch(error=>{

            if(error.response){
              swal(error.response.data.error)
            } 
          })

    },
    setpassword(){
      let username=window.localStorage.getItem('user_name')
this.$router.push({path:'/PersonalCenterSetPassword',query:{"username": username}})//传用户名到设置密码以区分注册和修改密码
    },
    load(){
if (window.localStorage.getItem('user_name') == null ){
return 'A'
}else{
  return window.localStorage.getItem('user_name')
}
    },
    gotologin(){
this.$router.push('/PersonalCenterLogin')
    },
gotoregister(){
this.$router.push('/PersonalCenterRegister')
    },
      },
      mounted(){
    
    }
};
</script>
<style scoped>
.loading-wrapper {
  /* position: fixed; */
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
  /* position: fixed; */
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  padding-top: 5%;
  padding-bottom: 100%;
}
#register {
  max-width: 340px;
  opacity: 0.8;
  margin: 0px auto;
  background: #fff !important;
  padding: 20px 40px;
  border-radius: 10px;
  position: relative;
  z-index: 9;
}
.bt:focus{
  background: #409EFF;
  border-color: #409EFF;
  color: #409EFF;
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
.el-button--primary:focus {
  background: #409EFF;
  border-color: #409EFF;
  color: #fff;
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
