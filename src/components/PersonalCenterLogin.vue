<template>
  <div> 
    <div class="register-wrapper"> 
      <div id="register" >
        <p class="title">登录</p>
        <el-form
          :model="Login"
          status-icon
          :rules="rules2"
          ref="Login"
          label-width="0"
          class="demo-ruleForm"
        >
          <!-- 用户名 -->
          <el-form-item prop="mail">
            <el-input v-model="Login.mail" auto-complete="off" placeholder="请输入邮箱地址"></el-input>
          </el-form-item>
          <!-- 密码 -->
          <el-form-item prop="pass">
            <el-input type="password" v-model="Login.password" auto-complete="off" placeholder="输入密码"></el-input>
          </el-form-item>
          <!-- 验证码 -->
          <el-form-item prop="info">
            <el-input  v-model="info" auto-complete="off" placeholder="请输入验证码"></el-input>
            <el-span class="code-style" @click="createCode">{{vercode}}</el-span>
          </el-form-item>
          <!-- 登录 -->
          <el-form-item>
          <el-button type="primary" @click="login('Login')" style="width:100%;">登录</el-button>
            <p class="login" @click="gotoLogin">没有账号？立即注册</p>
            <p class="login" @click="gotoForget">忘记密码</p>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script> 
import loaddata from "@/api/loaddata";//登录post
// import {setCookie,getCookie,delCookie} from "@/api/util/util"
import md5 from 'js-md5';//密码加密
export default {
  name:"PersonalCenterLogin", 
  data() {
    //<!--验证邮箱是否正确-->
    let checkMa =(rule,value,callback)=>{
      if (value === '') {
        callback(new Error('请输入邮箱地址'))
      } else if (!this.checkMail(value)) {
        callback(new Error('邮箱不合法'))
      } else {
        callback()
      }
    }
    // <!--验证密码-->
    let validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"))
      } else if(!this.checkPass(value)){
         callback(new Error(' '))//密码不提醒，防止别有用心者
      }
      else {
        callback()
      }
    };
    return {  
      vercode:'',//显示验证码
      info:'',//输入验证码
      Login: {
        password: "",
        mail:"",
      },
      rules2: {
        password: [{ validator: validatePass, trigger: 'change' }],
        mail: [{ validator: checkMa, trigger: 'change' }],
      },
    }
  }, 
  methods: {
    login(formName){
      //验证表单格式正确与否

      this.$refs[formName].validate(valid => {
        if (valid) {//如果表单格式不正确直接跳转登录失败，不发送信息给后台
          if(!this.confirmTheCode()){//如果验证码不正确显示验证失败信息
             //alert ('验证失败');
          }
          else{
              var password1=md5(this.Login.password)//密码md5加密
              var userdata={"username":this.Login.mail,"password":password1}
              //发送用户名和密码到后端
              loaddata(userdata).then(response=>{
                if(!window.localStorage){
                   alert("浏览器不支持localstorage");
                  }
                else{
                  var userStroge=window.localStorage;
                  let expireDays = 7  ;//生存周期为一天
                  //console.log("----------1")
                  userStroge.setItem('user_name',this.Login.mail)
                  if(this.$route.query.redirect) {//登录完成之后跳入之前的path
                    this.$router.push(this.$route.query.redirect);
                    } 
                  else{
                    this.$router.push('/PersonalCenter'); //跳转用户中心页
                    }
                }
              }).catch(error=>{
                if(error.response&&error.response.status){//错误状态用户密码或者用户
                  alert(error.response.data.error);
                  //console.log("ass")
                }
                this.createCode()//出现错误之后更新验证码
              })
          // setTimeout(() => {
          //   alert('登录成功')
          // }, 400);
          }
        } else {
          console.log("error login!!");
          return false;
        }
      })
    },
    // <!--进入注册页-->
    gotoLogin() {
      this.$router.push({
        path: "/PersonalCenterRegister"
      });
    },
    // <!--进入忘记密码页-->
    gotoForget() {
      this.$router.push({
        path: "/PersonalCenterForget"
      });
    },
    // <!--核对邮件名格式-->
    checkMail(str){
       let re = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
        if (re.test(str)) {
          return true;
        } else {
          return false;
        }
    },
    // <!--核对密码格式-->
    checkPass(str){
      let re = /^(?=.*[(a-z)|(A-Z)])(?=.*\d)[^]{6,16}$/
      if (re.test(str)) {
        return true;
      } else {
        return false;
      }
    },
    // <!--通过随机数产生验证码-->
    createCode() {    
        this.vercode = '';
        var code = '';
        var codeLength = 4;     //验证码长度
        var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R', 'S','T','U','V','W','X','Y','Z');
        for(var i = 0;i<codeLength;i++){
              var index = Math.floor(Math.random()*36);
              code += random[index];
        }
        this.vercode = code;
        },
    // <!--验证验证码-->
    confirmTheCode() {      
        var customerCode = this.info.toUpperCase();   //把你输入的小写转化为大写
        if(customerCode == 0){
            this.createCode();
            this.info = '';
            alert('请输入验证码')
            return false ;
        }else if(customerCode != this.vercode){
            this.createCode();
            this.info = '';
            alert('验证码不正确，请重新输入');
            return false;
        }else {
            return true;
        }
    }
      },
      mounted(){
      this.createCode()
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
