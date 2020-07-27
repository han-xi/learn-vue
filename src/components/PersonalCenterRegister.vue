<template>
  <div> 
    <div class="register-wrapper"> 
      <div id="register">
        <p class="title">注册</p>
        <el-form
          :model="ruleForm2"
          status-icon
          :rules="rules2"
          ref="ruleForm2"
          label-width="0"
          class="demo-ruleForm"
        >
          <!-- 用户名 -->
          <el-form-item prop="mail">
            <el-input v-model="ruleForm2.mail" auto-complete="off" placeholder="请输入邮箱地址"></el-input>
          </el-form-item>
          <!-- 邮件验证码 -->
          <el-form-item prop="smscode" class="code">
            <el-input v-model="ruleForm2.smscode" placeholder="验证码"></el-input>
            <el-button type="primary" :disabled='isDisabled' @click="sendCode">{{buttonText}}</el-button>
          </el-form-item>
          <!-- 密码 -->
          <el-form-item prop="pass">
            <el-input type="password" v-model="ruleForm2.pass" auto-complete="off" placeholder="输入密码"></el-input>
          </el-form-item>
          <!-- 确认密码 -->
          <el-form-item prop="checkPass">
            <el-input type="password" v-model="ruleForm2.checkPass" auto-complete="off" placeholder="确认密码"></el-input>
          </el-form-item>
          <!-- 提交注册 -->
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm2')" style="width:100%;">注册</el-button>
            <p class="login" @click="gotoLogin">已有账号？立即登录</p>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script> 
 import updata from "@/api/updata";
import sendmail from "@/api/sendmail";
import md5 from 'js-md5';
export default {
  name:"PersonalCenterRegister", 
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
    //  <!--验证码是否为空-->
    let checkSmscode = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入验证码'))
      } else {
        callback()
      }
    }
    // <!--验证密码-->
    let validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"))
      } else if(!this.checkPass(value)){
         callback(new Error('密码格式不正确，密码长度大于6位且数字字母混合'))
      }
      else {
        if (this.ruleForm2.checkPass !== "") {
          this.$refs.ruleForm2.validateField("checkPass");
        }
        callback()
      }
    }
    // <!--二次验证密码-->
    let validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.ruleForm2.pass) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return { 
      code:null, 
      ruleForm2: {
        pass: "",
        checkPass: "",
        smscode: "",
        mail:""
      },
      rules2: {
        pass: [{ validator: validatePass, trigger: 'change' }],
        checkPass: [{ validator: validatePass2, trigger: 'change' }],
        smscode: [{ validator: checkSmscode, trigger: 'change' }],
        mail: [{ validator: checkMa, trigger: 'change' }],
      },
      buttonText: '发送验证码',
      isDisabled: false, // 是否禁止点击发送验证码按钮
      flag: true
    }
  }, 
  methods: {
   
    // <!--发送验证码-->
    sendCode () { 
      if (this.checkMail(this.ruleForm2.mail)) {
        let time = 60;
        this.buttonText = '正在发送';
        var newdata={}
        newdata={"tomail":this.ruleForm2.mail}
        sendmail(newdata).then(res=>{
          //发送成功
          this.buttonText = '已发送'
          this.isDisabled = true
          if (this.flag) {
            this.flag = false;
            let timer = setInterval(() => {
              time--;
              this.buttonText = time + ' 秒'
              if ((time === 0) || (this.flag===true) ) {
                clearInterval(timer);
                this.buttonText = '重新获取'
                this.isDisabled = false
                this.flag = true;
              }
            }, 1000)
          }        
        }).catch(error=>{
            if(error.response){
              alert(error.response.data.error)
              this.buttonText = '发送失败请重新尝试'
              this.isDisabled = false
            }else{
              
            }
})

      }
    },
 
 
    // <!--提交注册-->
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
            var newdata={}
            var md5password=md5(this.ruleForm2.pass)
            //var token=md5(this.ruleForm2.mail+this.ruleForm2.password)
            newdata={"username":this.ruleForm2.mail,"password":md5password,"smscode":this.ruleForm2.smscode}   
            updata(newdata).then(res=>{
            //注册成功
              alert("注册成功,跳转登录")
              this.$router.push({
                path: "/PersonalCenterLogin"
              }); 
            }).catch(error=>{
            //用户已经存在
            if(error.response){
              alert(error.response.data.error)
                  this.buttonText = '重新获取'
                  this.isDisabled = false
                  this.flag = true
            }   
            })
          
        } else {
          console.log("error submit!!");
          return false;
        }
      })
    },
    // <!--进入登录页-->
    gotoLogin() {
      this.$router.push({
        path: "/PersonalCenterLogin"
      });
    },
    // <!--验证用户名格式-->
    checkMail(str){
         let re = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (re.test(str)) {
        return true;
      } else {
        return false;
      }
    },
    // <!--验证密码格式-->
    checkPass(str){
      let re =/^(?=.*[(a-z)|(A-Z)])(?=.*\d)[^]{6,16}$/
      if (re.test(str)) {
        return true;
      } else {
        return false;
      }
    }
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
  background: #fff;
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
  margin-top: 10px;
  font-size: 14px;
  line-height: 22px;
  color: #1ab2ff;
  cursor: pointer;
  text-align: left;
  text-indent: 8px;
  width: 160px;
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
</style>
