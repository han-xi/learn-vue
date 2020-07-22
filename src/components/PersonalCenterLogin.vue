<template>
  <div> 
    <div class="register-wrapper"> 
      <div id="register" >
        <p class="title">登录</p>
        <el-form
          :model="ruleForm2"
          status-icon
          :rules="rules2"
          ref="ruleForm2"
          label-width="0"
          class="demo-ruleForm"
        >
          
           <el-form-item prop="mail">
            <el-input v-model="ruleForm2.mail" auto-complete="off" placeholder="请输入邮箱地址"></el-input>
          </el-form-item>
          <el-form-item prop="pass">
            <el-input type="password" v-model="ruleForm2.password" auto-complete="off" placeholder="输入密码"></el-input>
          </el-form-item>
          <el-form-item prop="info">
            <el-input  v-model="info" auto-complete="off" placeholder="请输入验证码"></el-input>
            <el-span class="code-style" @click="createCode">{{vercode}}</el-span>
    
          </el-form-item>


          <el-form-item>
            
          <!--  <el-button type="primary" @click="submitForm('ruleForm2')" style="width:100%;">登录</el-button>-->
                        <el-button type="primary" @click="confirmTheCode();login()" style="width:100%;">登录</el-button>

            <p class="login" @click="gotoLogin">没有账号？立即注册</p>
            <p class="login" @click="gotoForget">忘记密码</p>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script> 
import loaddata from "@/api/loaddata";
import {setCookie,getCookie,delCookie} from "@/api/util/util"
import md5 from 'js-md5';
export default {
  //name: "Register",
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
         callback(new Error(' '))
      }
      else {
        callback()
      }
    };
    return {  
        vercode:'',
info:'',
      ruleForm2: {
        password: "",
        mail:"",

      },
      rules2: {
        password: [{ validator: validatePass, trigger: 'change' }],
        mail: [{ validator: checkMa, trigger: 'change' }],

      },

    }
  }, 
  created() {},
  methods: {
    login(){
   const self = this;
   if(this.info===''){
     alert ('验证失败');
   }
   //密码md5加密
   var password1=md5(this.ruleForm2.password)
   var userdata={"username":this.ruleForm2.mail,"password":password1}
     loaddata(userdata).then(response=>{
  
      var res =response.data
      //ses= window.sessionStorage; 
      let expireDays = 7  ;//生存周期为一天
      console.log("----------1")
      alert(res.token)
      setCookie('session',res.token,expireDays); //设置Session
     console.log(getCookie('session'))
      setCookie('u_uuid',this.ruleForm2.mail,expireDays); //设置用户编号 
      //ses.setItem('data', res.token);
      console.log("----------2")
    // if(res.errCode!=2){

     
       if(this.$route.query.redirect) {
         this.$router.push(this.$route.query.redirect);
        } else {
         this.$router.push('/PersonalCenter'); //跳转用户中心页
        }
    // }
      //跳转到首页
      // this.$router.push({
      //   path: "/PersonalCenter"
      // });
     }).catch(error=>{
     if(error){//错误状态
       
     console.log(error.error);
     }
        this.createCode()
        
   })
  },
    // <!--提交登录-->
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          setTimeout(() => {
            alert('登录成功')
          }, 400);
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
     gotoForget() {
      this.$router.push({
        path: "/PersonalCenterForget"
      });
    },
    checkMail(str){
         let re = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (re.test(str)) {
        return true;
      } else {
        return false;
      }
    },
    checkPass(str){
      let re = /^(?=.*[(a-z)|(A-Z)])(?=.*\d)[^]{6,16}$/
      if (re.test(str)) {
        return true;
      } else {
        return false;
      }
    },
     createCode:function () {    //通过随机数生成验证码
            this.vercode = '';
            var code = '';
            var codeLength = 4;     //验证码长度
            var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R', 'S','T','U','V','W','X','Y','Z');
            for(var i = 0;i<codeLength;i++){
                var index = Math.floor(Math.random()*36);
                code += random[index];
            }
            this.vercode = code
        },
         confirmTheCode() {      //验证函数
            var customerCode = this.info.toUpperCase();   //把你输入的小写转化为大写
            if(customerCode == 0){
                this.createCode();
                this.info = ''
                alert('请输入验证码')
            }else if(customerCode != this.vercode){
                this.createCode();
                this.info = ''
                alert('验证码不正确，请重新输入');
            }else {
            
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
